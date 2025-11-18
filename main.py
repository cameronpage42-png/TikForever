"""
TikForever - Main Application
TikTok Live Game Controller for Windows
"""

import sys
import asyncio
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QTextEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QGroupBox, QComboBox,
    QSpinBox, QDoubleSpinBox, QCheckBox, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor
import logging
from datetime import datetime

from tiktok_client import TikTokLiveManager
from input_simulator import InputSimulator
from event_mapper import EventMapper
from config_manager import ConfigManager
from obs_controller import OBSController
from alert_server import AlertServer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TikTokThread(QThread):
    """Thread for running TikTok Live client"""

    connected = pyqtSignal()
    disconnected = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, tiktok_manager):
        super().__init__()
        self.tiktok_manager = tiktok_manager
        self.running = False
        self.loop = None

    def run(self):
        """Run the TikTok Live client"""
        self.running = True
        try:
            # Create new event loop for this thread
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

            # Start the client (connects and keeps running)
            logger.info("Starting TikTok client...")
            self.loop.run_until_complete(self._run_client())

        except Exception as e:
            logger.error(f"TikTok thread error: {e}")
            self.error.emit(str(e))
        finally:
            self.running = False
            if self.loop:
                self.loop.close()
            self.disconnected.emit()

    async def _run_client(self):
        """Run the TikTok client with proper event loop handling"""
        try:
            # Start the client's websocket connection
            # This creates background tasks for processing messages
            logger.info("Starting TikTok Live client...")

            # Create a task for the client to run in the background
            client_task = asyncio.create_task(self.tiktok_manager.client.start())

            # Give it a moment to establish connection
            await asyncio.sleep(2)

            # Mark as connected
            self.tiktok_manager.is_connected = True
            self.connected.emit()
            logger.info("TikTok client running - listening for events")

            # Keep the event loop running to process websocket messages
            # The client_task will continue processing messages in the background
            try:
                while self.running and self.tiktok_manager.is_connected:
                    await asyncio.sleep(0.5)
            finally:
                # Cancel the client task when stopping
                if not client_task.done():
                    client_task.cancel()
                    try:
                        await client_task
                    except asyncio.CancelledError:
                        pass

        except Exception as e:
            logger.error(f"Error running client: {e}")
            raise
        finally:
            # Disconnect on exit
            logger.info("Disconnecting from TikTok Live...")
            if self.tiktok_manager.is_connected:
                await self.tiktok_manager.disconnect()

    def stop(self):
        """Stop the thread"""
        logger.info("Stopping TikTok thread...")
        self.running = False


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()

        self.config = ConfigManager()

        # Load controller setting and initialize input simulator
        controller_enabled = self.config.get_controller_enabled()
        self.input_simulator = InputSimulator(enable_controller=controller_enabled)

        self.obs_controller = OBSController()
        self.alert_server = AlertServer(port=8000)
        self.event_mapper = EventMapper(self.input_simulator, self.obs_controller, self.alert_server)
        self.tiktok_manager = None
        self.tiktok_thread = None

        # Start alert server automatically
        self.alert_server.start()

        # Statistics tracking
        self.stats = {
            'total': 0,
            'comments': 0,
            'gifts': 0,
            'likes': 0,
            'shares': 0,
            'follows': 0
        }

        self.init_ui()
        self.load_config()

    def init_ui(self):
        """Initialize user interface"""

        self.setWindowTitle("TikForever - TikTok Live Game Controller")

        # Set window geometry from config
        geometry = self.config.get_window_geometry()
        self.setGeometry(geometry['x'], geometry['y'], geometry['width'], geometry['height'])

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create tabs
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Connection tab
        connection_tab = self.create_connection_tab()
        tabs.addTab(connection_tab, "Connection")

        # Mappings tab
        mappings_tab = self.create_mappings_tab()
        tabs.addTab(mappings_tab, "Event Mappings")

        # OBS tab
        obs_tab = self.create_obs_tab()
        tabs.addTab(obs_tab, "OBS/TikTok Live Studio")

        # Log tab
        log_tab = self.create_log_tab()
        tabs.addTab(log_tab, "Event Log")

        # Status bar
        self.statusBar().showMessage("Ready")

    def create_connection_tab(self) -> QWidget:
        """Create connection tab"""

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Connection group
        connection_group = QGroupBox("TikTok Live Connection")
        connection_layout = QVBoxLayout()
        connection_group.setLayout(connection_layout)

        # Username input
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("TikTok Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your TikTok username (without @)")
        username_layout.addWidget(self.username_input)
        connection_layout.addLayout(username_layout)

        # Connect button
        button_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Connect to Live")
        self.connect_btn.clicked.connect(self.toggle_connection)
        self.connect_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px; font-weight: bold; }")
        button_layout.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect)
        self.disconnect_btn.setEnabled(False)
        self.disconnect_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 10px; font-weight: bold; }")
        button_layout.addWidget(self.disconnect_btn)

        connection_layout.addLayout(button_layout)

        # Status
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet("QLabel { color: #f44336; font-weight: bold; padding: 10px; }")
        connection_layout.addWidget(self.status_label)

        layout.addWidget(connection_group)

        # Settings group
        settings_group = QGroupBox("Input Settings")
        settings_layout = QVBoxLayout()
        settings_group.setLayout(settings_layout)

        # Virtual controller checkbox
        self.controller_checkbox = QCheckBox("Enable Virtual Xbox 360 Controller")
        self.controller_checkbox.setChecked(self.config.get_controller_enabled())
        self.controller_checkbox.stateChanged.connect(self.on_controller_toggle)
        self.controller_checkbox.setToolTip(
            "Enable virtual Xbox 360 controller for gamepad button mappings.\n"
            "Disable if you only need keyboard input or experience controller conflicts.\n"
            "Requires application restart to take effect."
        )
        settings_layout.addWidget(self.controller_checkbox)

        # Controller status
        if self.input_simulator.gamepad:
            controller_status = "✓ Virtual controller active"
            status_color = "#4CAF50"
        else:
            controller_status = "✗ Virtual controller inactive"
            status_color = "#f44336"

        self.controller_status_label = QLabel(controller_status)
        self.controller_status_label.setStyleSheet(f"QLabel {{ color: {status_color}; font-style: italic; padding-left: 20px; }}")
        settings_layout.addWidget(self.controller_status_label)

        layout.addWidget(settings_group)

        # Stats group
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()
        stats_group.setLayout(stats_layout)

        self.stats_label = QLabel("Total Events: 0\nComments: 0\nGifts: 0\nLikes: 0\nShares: 0\nFollows: 0")
        stats_layout.addWidget(self.stats_label)

        layout.addWidget(stats_group)

        # Info
        info_group = QGroupBox("Quick Start")
        info_layout = QVBoxLayout()
        info_group.setLayout(info_layout)

        info_text = QLabel(
            "1. Enter your TikTok username (the account that will go live)\n"
            "2. Configure event mappings in the 'Event Mappings' tab\n"
            "3. Click 'Connect to Live' when you start streaming\n"
            "4. Start your game and let viewers control it!\n\n"
            "Note: Make sure to run this app as Administrator for best compatibility."
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)

        layout.addWidget(info_group)

        layout.addStretch()

        return widget

    def create_mappings_tab(self) -> QWidget:
        """Create event mappings tab"""

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Mappings table
        self.mappings_table = QTableWidget()
        self.mappings_table.setColumnCount(7)
        self.mappings_table.setHorizontalHeaderLabels([
            "Event Type", "Trigger", "Action", "Input", "Duration", "Cooldown", "Enabled"
        ])
        self.mappings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.mappings_table)

        # Add mapping controls
        add_group = QGroupBox("Add New Mapping")
        add_layout = QVBoxLayout()
        add_group.setLayout(add_layout)

        # Row 1: Event type and trigger
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Event:"))
        self.event_type_combo = QComboBox()
        self.event_type_combo.addItems(["comment", "gift", "like", "share", "follow"])
        row1.addWidget(self.event_type_combo)

        row1.addWidget(QLabel("Trigger:"))
        self.trigger_input = QLineEdit()
        self.trigger_input.setPlaceholderText("e.g., 'jump' or 'Rose'")
        row1.addWidget(self.trigger_input)
        add_layout.addLayout(row1)

        # Row 2: Action type and input
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Action:"))
        self.action_combo = QComboBox()
        self.action_combo.addItems(["keyboard", "controller", "obs", "obs_hotkey", "browser_source"])
        self.action_combo.currentTextChanged.connect(self.on_action_type_changed)
        row2.addWidget(self.action_combo)

        row2.addWidget(QLabel("Input:"))
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("e.g., 'space', 'A', 'left'")
        row2.addWidget(self.input_field)
        add_layout.addLayout(row2)

        # OBS-specific fields (hidden by default)
        self.obs_fields_widget = QWidget()
        obs_fields_layout = QVBoxLayout()
        self.obs_fields_widget.setLayout(obs_fields_layout)

        obs_action_layout = QHBoxLayout()
        obs_action_layout.addWidget(QLabel("OBS Action:"))
        self.obs_action_combo = QComboBox()
        self.obs_action_combo.addItems(["show", "hide", "toggle", "show_temp"])
        obs_action_layout.addWidget(self.obs_action_combo)
        obs_fields_layout.addLayout(obs_action_layout)

        obs_scene_layout = QHBoxLayout()
        obs_scene_layout.addWidget(QLabel("Scene:"))
        self.obs_scene_input = QLineEdit()
        self.obs_scene_input.setPlaceholderText("e.g., 'Main Scene'")
        obs_scene_layout.addWidget(self.obs_scene_input)
        obs_fields_layout.addLayout(obs_scene_layout)

        obs_source_layout = QHBoxLayout()
        obs_source_layout.addWidget(QLabel("Source:"))
        self.obs_source_input = QLineEdit()
        self.obs_source_input.setPlaceholderText("e.g., 'Follow Alert'")
        obs_source_layout.addWidget(self.obs_source_input)
        obs_fields_layout.addLayout(obs_source_layout)

        self.obs_fields_widget.setVisible(False)  # Hidden by default
        add_layout.addWidget(self.obs_fields_widget)

        # OBS Hotkey fields (hidden by default)
        self.obs_hotkey_widget = QWidget()
        obs_hotkey_layout = QVBoxLayout()
        self.obs_hotkey_widget.setLayout(obs_hotkey_layout)

        hotkey_info_label = QLabel(
            "OBS Hotkey Mode - Works with TikTok Live Studio!\n"
            "Set up hotkeys in OBS/TikTok Live Studio (F13-F24 recommended),\n"
            "then enter the key here (e.g., 'f13', 'f14')"
        )
        hotkey_info_label.setStyleSheet("QLabel { color: #2196F3; font-style: italic; padding: 5px; }")
        obs_hotkey_layout.addWidget(hotkey_info_label)

        hotkey_input_layout = QHBoxLayout()
        hotkey_input_layout.addWidget(QLabel("Hotkey:"))
        self.obs_hotkey_input = QLineEdit()
        self.obs_hotkey_input.setPlaceholderText("e.g., 'f13', 'f14', 'f15'")
        hotkey_input_layout.addWidget(self.obs_hotkey_input)
        obs_hotkey_layout.addLayout(hotkey_input_layout)

        self.obs_hotkey_widget.setVisible(False)  # Hidden by default
        add_layout.addWidget(self.obs_hotkey_widget)

        # Browser Source fields (hidden by default)
        self.browser_source_widget = QWidget()
        browser_source_layout = QVBoxLayout()
        self.browser_source_widget.setLayout(browser_source_layout)

        browser_info_label = QLabel(
            "Browser Source Alerts - Professional stream alerts!\n"
            "Add Browser Source in TikTok Live Studio: http://localhost:8000\n"
            "Place your alert images/videos in the 'alerts' folder"
        )
        browser_info_label.setStyleSheet("QLabel { color: #4CAF50; font-style: italic; padding: 5px; }")
        browser_source_layout.addWidget(browser_info_label)

        alert_type_layout = QHBoxLayout()
        alert_type_layout.addWidget(QLabel("Alert Type:"))
        self.alert_type_combo = QComboBox()
        self.alert_type_combo.addItems(["follow", "gift", "share", "like", "comment"])
        alert_type_layout.addWidget(self.alert_type_combo)
        browser_source_layout.addLayout(alert_type_layout)

        alert_message_layout = QHBoxLayout()
        alert_message_layout.addWidget(QLabel("Message:"))
        self.alert_message_input = QLineEdit()
        self.alert_message_input.setPlaceholderText("e.g., 'Thanks for following!' (leave empty for default)")
        alert_message_layout.addWidget(self.alert_message_input)
        browser_source_layout.addLayout(alert_message_layout)

        media_file_layout = QHBoxLayout()
        media_file_layout.addWidget(QLabel("Media File:"))
        self.media_file_input = QLineEdit()
        self.media_file_input.setPlaceholderText("e.g., 'follow_alert.gif' (optional)")
        media_file_layout.addWidget(self.media_file_input)
        browser_source_layout.addLayout(media_file_layout)

        self.browser_source_widget.setVisible(False)  # Hidden by default
        add_layout.addWidget(self.browser_source_widget)

        # Row 3: Duration and cooldown
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Duration (s):"))
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setMinimum(0.01)
        self.duration_spin.setMaximum(5.0)
        self.duration_spin.setValue(0.1)
        self.duration_spin.setSingleStep(0.05)
        row3.addWidget(self.duration_spin)

        row3.addWidget(QLabel("Cooldown (s):"))
        self.cooldown_spin = QDoubleSpinBox()
        self.cooldown_spin.setMinimum(0.0)
        self.cooldown_spin.setMaximum(60.0)
        self.cooldown_spin.setValue(0.5)
        self.cooldown_spin.setSingleStep(0.1)
        row3.addWidget(self.cooldown_spin)
        add_layout.addLayout(row3)

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Add Mapping")
        add_btn.clicked.connect(self.add_mapping)
        button_layout.addWidget(add_btn)

        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self.remove_mapping)
        button_layout.addWidget(remove_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_mappings)
        button_layout.addWidget(clear_btn)

        save_btn = QPushButton("Save Mappings")
        save_btn.clicked.connect(self.save_config)
        save_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; }")
        button_layout.addWidget(save_btn)

        add_layout.addLayout(button_layout)

        layout.addWidget(add_group)

        return widget

    def create_log_tab(self) -> QWidget:
        """Create event log tab"""

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Courier", 9))
        layout.addWidget(self.log_text)

        # Clear button
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self.log_text.clear)
        layout.addWidget(clear_btn)

        return widget

    def create_obs_tab(self) -> QWidget:
        """Create OBS/TikTok Live Studio configuration tab"""

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # Connection group
        connection_group = QGroupBox("OBS WebSocket Connection")
        connection_layout = QVBoxLayout()
        connection_group.setLayout(connection_layout)

        # Host input
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Host:"))
        self.obs_host_input = QLineEdit()
        self.obs_host_input.setText("localhost")
        self.obs_host_input.setPlaceholderText("localhost")
        host_layout.addWidget(self.obs_host_input)
        connection_layout.addLayout(host_layout)

        # Port input
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.obs_port_input = QLineEdit()
        self.obs_port_input.setText("4455")
        self.obs_port_input.setPlaceholderText("4455")
        port_layout.addWidget(self.obs_port_input)
        connection_layout.addLayout(port_layout)

        # Password input
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password:"))
        self.obs_password_input = QLineEdit()
        self.obs_password_input.setPlaceholderText("Leave empty if no password")
        self.obs_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.obs_password_input)
        connection_layout.addLayout(password_layout)

        # Connect/Disconnect buttons
        obs_button_layout = QHBoxLayout()
        self.obs_connect_btn = QPushButton("Connect to OBS")
        self.obs_connect_btn.clicked.connect(self.connect_obs)
        self.obs_connect_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 10px; font-weight: bold; }")
        obs_button_layout.addWidget(self.obs_connect_btn)

        self.obs_disconnect_btn = QPushButton("Disconnect")
        self.obs_disconnect_btn.clicked.connect(self.disconnect_obs)
        self.obs_disconnect_btn.setEnabled(False)
        self.obs_disconnect_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 10px; font-weight: bold; }")
        obs_button_layout.addWidget(self.obs_disconnect_btn)

        connection_layout.addLayout(obs_button_layout)

        # Status
        self.obs_status_label = QLabel("Status: Not Connected")
        self.obs_status_label.setStyleSheet("QLabel { color: #f44336; font-weight: bold; padding: 10px; }")
        connection_layout.addWidget(self.obs_status_label)

        layout.addWidget(connection_group)

        # Scene/Source Browser
        browser_group = QGroupBox("Scene & Source Browser")
        browser_layout = QVBoxLayout()
        browser_group.setLayout(browser_layout)

        browser_info = QLabel("Connect to OBS first to browse scenes and sources")
        browser_info.setStyleSheet("QLabel { color: #888; font-style: italic; }")
        browser_layout.addWidget(browser_info)

        # Refresh button
        refresh_btn = QPushButton("Refresh Scenes & Sources")
        refresh_btn.clicked.connect(self.refresh_obs_scenes)
        browser_layout.addWidget(refresh_btn)

        # Scenes list
        scenes_layout = QHBoxLayout()
        scenes_layout.addWidget(QLabel("Scenes:"))
        self.obs_scenes_list = QTextEdit()
        self.obs_scenes_list.setReadOnly(True)
        self.obs_scenes_list.setMaximumHeight(100)
        scenes_layout.addWidget(self.obs_scenes_list)
        browser_layout.addLayout(scenes_layout)

        # Sources list
        sources_layout = QVBoxLayout()
        sources_layout.addWidget(QLabel("Sources in selected scene:"))

        scene_select_layout = QHBoxLayout()
        scene_select_layout.addWidget(QLabel("Scene:"))
        self.obs_scene_combo = QComboBox()
        self.obs_scene_combo.currentTextChanged.connect(self.load_scene_sources)
        scene_select_layout.addWidget(self.obs_scene_combo)
        sources_layout.addLayout(scene_select_layout)

        self.obs_sources_list = QTextEdit()
        self.obs_sources_list.setReadOnly(True)
        self.obs_sources_list.setMaximumHeight(150)
        sources_layout.addWidget(self.obs_sources_list)
        browser_layout.addLayout(sources_layout)

        layout.addWidget(browser_group)

        # Info
        info_group = QGroupBox("Quick Guide")
        info_layout = QVBoxLayout()
        info_group.setLayout(info_layout)

        info_text = QLabel(
            "1. Enable OBS WebSocket in OBS Studio or TikTok Live Studio\n"
            "   (Tools → WebSocket Server Settings)\n"
            "2. Enter connection details and click 'Connect to OBS'\n"
            "3. Browse scenes and sources to find names for mappings\n"
            "4. Go to 'Event Mappings' tab to add OBS actions\n\n"
            "For detailed setup: See OBS_SETUP.md"
        )
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)

        layout.addWidget(info_group)

        layout.addStretch()

        return widget

    def connect_obs(self):
        """Connect to OBS WebSocket"""
        host = self.obs_host_input.text().strip() or "localhost"
        port = int(self.obs_port_input.text().strip() or "4455")
        password = self.obs_password_input.text().strip()

        self.obs_controller.host = host
        self.obs_controller.port = port
        self.obs_controller.password = password

        if self.obs_controller.connect():
            self.obs_status_label.setText("Status: Connected ✓")
            self.obs_status_label.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; padding: 10px; }")
            self.obs_connect_btn.setEnabled(False)
            self.obs_disconnect_btn.setEnabled(True)
            self.refresh_obs_scenes()
            QMessageBox.information(self, "Success", "Connected to OBS successfully!")
        else:
            self.obs_status_label.setText("Status: Connection Failed")
            self.obs_status_label.setStyleSheet("QLabel { color: #f44336; font-weight: bold; padding: 10px; }")
            QMessageBox.critical(self, "Error", "Failed to connect to OBS. Make sure OBS WebSocket is enabled.")

    def disconnect_obs(self):
        """Disconnect from OBS WebSocket"""
        self.obs_controller.disconnect()
        self.obs_status_label.setText("Status: Not Connected")
        self.obs_status_label.setStyleSheet("QLabel { color: #f44336; font-weight: bold; padding: 10px; }")
        self.obs_connect_btn.setEnabled(True)
        self.obs_disconnect_btn.setEnabled(False)
        self.obs_scenes_list.clear()
        self.obs_sources_list.clear()
        self.obs_scene_combo.clear()

    def refresh_obs_scenes(self):
        """Refresh OBS scenes and sources"""
        if not self.obs_controller.is_connected:
            QMessageBox.warning(self, "Not Connected", "Please connect to OBS first")
            return

        scenes = self.obs_controller.get_scenes()
        if scenes:
            self.obs_scenes_list.setText("\n".join(scenes))
            self.obs_scene_combo.clear()
            self.obs_scene_combo.addItems(scenes)
        else:
            self.obs_scenes_list.setText("No scenes found")

    def load_scene_sources(self, scene_name: str):
        """Load sources for selected scene"""
        if not self.obs_controller.is_connected or not scene_name:
            return

        sources = self.obs_controller.get_sources_in_scene(scene_name)
        if sources:
            self.obs_sources_list.setText("\n".join(sources))
        else:
            self.obs_sources_list.setText("No sources found in this scene")

    def load_config(self):
        """Load configuration and populate UI"""

        # Load username
        username = self.config.get_tiktok_username()
        self.username_input.setText(username)

        # Load mappings
        mappings = self.config.get_mappings()
        self.event_mapper.load_mappings(mappings)
        self.refresh_mappings_table()

    def save_config(self):
        """Save configuration"""

        self.config.set_tiktok_username(self.username_input.text())
        self.config.set_mappings(self.event_mapper.get_mappings())

        # Save window geometry
        geo = self.geometry()
        self.config.set_window_geometry(geo.width(), geo.height(), geo.x(), geo.y())

        self.config.save()

        QMessageBox.information(self, "Success", "Configuration saved successfully!")

    def on_action_type_changed(self, action_type: str):
        """Handle action type change"""
        if action_type == 'obs':
            self.obs_fields_widget.setVisible(True)
            self.obs_hotkey_widget.setVisible(False)
            self.browser_source_widget.setVisible(False)
            self.input_field.setVisible(False)
        elif action_type == 'obs_hotkey':
            self.obs_fields_widget.setVisible(False)
            self.obs_hotkey_widget.setVisible(True)
            self.browser_source_widget.setVisible(False)
            self.input_field.setVisible(False)
        elif action_type == 'browser_source':
            self.obs_fields_widget.setVisible(False)
            self.obs_hotkey_widget.setVisible(False)
            self.browser_source_widget.setVisible(True)
            self.input_field.setVisible(False)
        else:
            self.obs_fields_widget.setVisible(False)
            self.obs_hotkey_widget.setVisible(False)
            self.browser_source_widget.setVisible(False)
            self.input_field.setVisible(True)

    def refresh_mappings_table(self):
        """Refresh the mappings table"""

        mappings = self.event_mapper.get_mappings()
        self.mappings_table.setRowCount(len(mappings))

        for i, mapping in enumerate(mappings):
            self.mappings_table.setItem(i, 0, QTableWidgetItem(mapping.get('event_type', '')))
            self.mappings_table.setItem(i, 1, QTableWidgetItem(mapping.get('trigger', '')))
            self.mappings_table.setItem(i, 2, QTableWidgetItem(mapping.get('action', '')))

            # Determine input field - for OBS show scene/source, for obs_hotkey show hotkey, for browser_source show alert details, otherwise show key/button
            if mapping.get('action') == 'obs':
                obs_info = f"{mapping.get('obs_action', '')} {mapping.get('obs_scene', '')}/{mapping.get('obs_source', '')}"
                input_val = obs_info.strip()
            elif mapping.get('action') == 'obs_hotkey':
                input_val = f"Hotkey: {mapping.get('obs_hotkey', '')}"
            elif mapping.get('action') == 'browser_source':
                alert_type = mapping.get('alert_type', '')
                media_file = mapping.get('media_file', '')
                input_val = f"Alert: {alert_type}" + (f" ({media_file})" if media_file else "")
            else:
                input_val = mapping.get('key') or mapping.get('button') or mapping.get('joystick') or mapping.get('trigger_name') or ''
            self.mappings_table.setItem(i, 3, QTableWidgetItem(str(input_val)))

            self.mappings_table.setItem(i, 4, QTableWidgetItem(str(mapping.get('duration', 0.1))))
            self.mappings_table.setItem(i, 5, QTableWidgetItem(str(mapping.get('cooldown', 0.5))))
            self.mappings_table.setItem(i, 6, QTableWidgetItem("Yes" if mapping.get('enabled', True) else "No"))

    def add_mapping(self):
        """Add a new mapping"""

        event_type = self.event_type_combo.currentText()
        trigger = self.trigger_input.text().strip()
        action = self.action_combo.currentText()
        duration = self.duration_spin.value()
        cooldown = self.cooldown_spin.value()

        if not trigger and event_type == 'comment':
            QMessageBox.warning(self, "Error", "Please enter a trigger text for comment events")
            return

        mapping_data = {
            'event_type': event_type,
            'trigger': trigger,
            'action': action,
            'duration': duration,
            'cooldown': cooldown,
            'enabled': True
        }

        # Determine input type based on action
        if action == 'obs':
            # OBS action via WebSocket
            obs_action = self.obs_action_combo.currentText()
            obs_scene = self.obs_scene_input.text().strip()
            obs_source = self.obs_source_input.text().strip()

            if not obs_scene or not obs_source:
                QMessageBox.warning(self, "Error", "Please enter both scene and source names for OBS actions")
                return

            mapping_data['obs_action'] = obs_action
            mapping_data['obs_scene'] = obs_scene
            mapping_data['obs_source'] = obs_source

        elif action == 'obs_hotkey':
            # OBS action via hotkey (works with TikTok Live Studio)
            obs_hotkey = self.obs_hotkey_input.text().strip().lower()

            if not obs_hotkey:
                QMessageBox.warning(self, "Error", "Please enter a hotkey (e.g., f13, f14)")
                return

            mapping_data['obs_hotkey'] = obs_hotkey

        elif action == 'browser_source':
            # Browser source alert (works with TikTok Live Studio)
            alert_type = self.alert_type_combo.currentText()
            alert_message = self.alert_message_input.text().strip()
            media_file = self.media_file_input.text().strip()

            mapping_data['alert_type'] = alert_type
            mapping_data['alert_message'] = alert_message
            mapping_data['media_file'] = media_file if media_file else None

        else:
            # Keyboard or controller action
            input_val = self.input_field.text().strip()

            if not input_val:
                QMessageBox.warning(self, "Error", "Please enter an input (key or button)")
                return

            if action == 'keyboard':
                mapping_data['key'] = input_val
            else:
                mapping_data['button'] = input_val

        self.event_mapper.add_mapping(mapping_data)
        self.refresh_mappings_table()

        # Clear inputs
        self.trigger_input.clear()
        self.input_field.clear()
        self.obs_scene_input.clear()
        self.obs_source_input.clear()
        self.obs_hotkey_input.clear()
        self.alert_message_input.clear()
        self.media_file_input.clear()

    def remove_mapping(self):
        """Remove selected mapping"""

        current_row = self.mappings_table.currentRow()
        if current_row >= 0:
            self.event_mapper.remove_mapping(current_row)
            self.refresh_mappings_table()

    def clear_mappings(self):
        """Clear all mappings"""

        reply = QMessageBox.question(
            self, "Confirm",
            "Are you sure you want to clear all mappings?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.event_mapper.clear_mappings()
            self.refresh_mappings_table()

    def on_controller_toggle(self, state):
        """Handle virtual controller checkbox toggle"""
        enabled = state == 2  # Qt.CheckState.Checked == 2
        self.config.set_controller_enabled(enabled)
        self.config.save()

        # Show restart reminder
        QMessageBox.information(
            self,
            "Restart Required",
            "Please restart TikForever for the controller setting to take effect.\n\n"
            f"Virtual controller will be {'enabled' if enabled else 'disabled'} on next start."
        )

    def toggle_connection(self):
        """Toggle TikTok Live connection"""

        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Error", "Please enter a TikTok username")
            return

        self.connect()

    def connect(self):
        """Connect to TikTok Live"""

        username = self.username_input.text().strip()

        # Remove @ if present
        if username.startswith('@'):
            username = username[1:]

        logger.info(f"Attempting to connect to @{username}")

        try:
            # Create TikTok manager
            self.tiktok_manager = TikTokLiveManager(username)

            # Register event handlers
            self.tiktok_manager.on_event('comment', lambda data: self.handle_event('comment', data))
            self.tiktok_manager.on_event('gift', lambda data: self.handle_event('gift', data))
            self.tiktok_manager.on_event('like', lambda data: self.handle_event('like', data))
            self.tiktok_manager.on_event('share', lambda data: self.handle_event('share', data))
            self.tiktok_manager.on_event('follow', lambda data: self.handle_event('follow', data))
            self.tiktok_manager.on_event('connect', lambda data: self.on_connected())

            # Start TikTok thread
            self.tiktok_thread = TikTokThread(self.tiktok_manager)
            self.tiktok_thread.connected.connect(self.on_connected)
            self.tiktok_thread.disconnected.connect(self.on_disconnected)
            self.tiktok_thread.error.connect(self.on_error)
            self.tiktok_thread.start()

            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self.username_input.setEnabled(False)
            self.status_label.setText("Status: Connecting...")
            self.status_label.setStyleSheet("QLabel { color: #FF9800; font-weight: bold; padding: 10px; }")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to connect: {str(e)}")

    def disconnect(self):
        """Disconnect from TikTok Live"""

        if self.tiktok_thread:
            self.tiktok_thread.stop()
            self.tiktok_thread.wait()

        if self.tiktok_manager:
            asyncio.run(self.tiktok_manager.disconnect())

        self.on_disconnected()

    def on_connected(self):
        """Handle successful connection"""

        # Reset statistics
        self.stats = {
            'total': 0,
            'comments': 0,
            'gifts': 0,
            'likes': 0,
            'shares': 0,
            'follows': 0
        }
        self.update_stats()

        self.status_label.setText("Status: Connected ✓")
        self.status_label.setStyleSheet("QLabel { color: #4CAF50; font-weight: bold; padding: 10px; }")
        self.statusBar().showMessage("Connected to TikTok Live")
        self.log_event("SYSTEM", f"Connected to @{self.username_input.text()}'s live stream")

    def on_disconnected(self):
        """Handle disconnection"""

        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.username_input.setEnabled(True)
        self.status_label.setText("Status: Disconnected")
        self.status_label.setStyleSheet("QLabel { color: #f44336; font-weight: bold; padding: 10px; }")
        self.statusBar().showMessage("Disconnected")
        self.log_event("SYSTEM", "Disconnected from live stream")

    def on_error(self, error_msg: str):
        """Handle connection error"""

        QMessageBox.critical(self, "Connection Error", f"Error: {error_msg}")
        self.on_disconnected()

    def handle_event(self, event_type: str, event_data: dict):
        """Handle TikTok Live event"""

        # Update statistics
        self.stats['total'] += 1
        if event_type == 'comment':
            self.stats['comments'] += 1
        elif event_type == 'gift':
            self.stats['gifts'] += 1
        elif event_type == 'like':
            self.stats['likes'] += 1
        elif event_type == 'share':
            self.stats['shares'] += 1
        elif event_type == 'follow':
            self.stats['follows'] += 1

        # Update stats display
        self.update_stats()

        # Log event
        user = event_data.get('user', 'Unknown')

        if event_type == 'comment':
            self.log_event("COMMENT", f"{user}: {event_data.get('comment')}")
        elif event_type == 'gift':
            self.log_event("GIFT", f"{user} sent {event_data.get('gift_name')}")
        elif event_type == 'like':
            self.log_event("LIKE", f"{user} sent {event_data.get('count')} likes")
        elif event_type == 'share':
            self.log_event("SHARE", f"{user} shared the stream")
        elif event_type == 'follow':
            self.log_event("FOLLOW", f"{user} followed!")

        # Process event through mapper
        self.event_mapper.process_event(event_type, event_data)

    def update_stats(self):
        """Update statistics display"""
        stats_text = (
            f"Total Events: {self.stats['total']}\n"
            f"Comments: {self.stats['comments']}\n"
            f"Gifts: {self.stats['gifts']}\n"
            f"Likes: {self.stats['likes']}\n"
            f"Shares: {self.stats['shares']}\n"
            f"Follows: {self.stats['follows']}"
        )
        self.stats_label.setText(stats_text)

    def log_event(self, event_type: str, message: str):
        """Log an event to the log display"""

        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] [{event_type}] {message}"
        self.log_text.append(log_line)

        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def closeEvent(self, event):
        """Handle window close event"""

        # Save configuration
        self.save_config()

        # Disconnect if connected
        if self.tiktok_manager and self.tiktok_manager.is_connected:
            self.disconnect()

        event.accept()


def main():
    """Main entry point"""

    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
