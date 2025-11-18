"""
OBS Controller Module
Handles connection to OBS WebSocket and source control
"""

import logging
from typing import Optional, List, Dict, Any

try:
    from obswebsocket import obsws, requests as obs_requests
    OBS_AVAILABLE = True
except ImportError:
    OBS_AVAILABLE = False
    logging.warning("obs-websocket-py not available - OBS features disabled")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OBSController:
    """Controls OBS/TikTok Live Studio via WebSocket"""

    def __init__(self, host: str = "localhost", port: int = 4455, password: str = ""):
        """
        Initialize OBS Controller

        Args:
            host: OBS WebSocket host (default: localhost)
            port: OBS WebSocket port (default: 4455 for OBS 28+)
            password: OBS WebSocket password
        """
        self.host = host
        self.port = port
        self.password = password
        self.ws = None
        self.is_connected = False

        if not OBS_AVAILABLE:
            logger.error("OBS WebSocket library not installed")

    def connect(self) -> bool:
        """
        Connect to OBS WebSocket

        Returns:
            True if connected successfully
        """
        if not OBS_AVAILABLE:
            logger.error("Cannot connect - OBS library not available")
            return False

        try:
            logger.info(f"Connecting to OBS at {self.host}:{self.port}...")
            self.ws = obsws(self.host, self.port, self.password)
            self.ws.connect()
            self.is_connected = True
            logger.info("Connected to OBS successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to OBS: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """Disconnect from OBS WebSocket"""
        if self.ws and self.is_connected:
            try:
                self.ws.disconnect()
                self.is_connected = False
                logger.info("Disconnected from OBS")
            except Exception as e:
                logger.error(f"Error disconnecting from OBS: {e}")

    def set_source_visibility(self, scene_name: str, source_name: str, visible: bool) -> bool:
        """
        Show or hide a source in a scene

        Args:
            scene_name: Name of the scene
            source_name: Name of the source
            visible: True to show, False to hide

        Returns:
            True if successful
        """
        if not self.is_connected:
            logger.warning("Not connected to OBS")
            return False

        try:
            # Get scene item ID
            response = self.ws.call(obs_requests.GetSceneItemId(
                sceneName=scene_name,
                sourceName=source_name
            ))

            scene_item_id = response.datain.get('sceneItemId')

            # Set visibility
            self.ws.call(obs_requests.SetSceneItemEnabled(
                sceneName=scene_name,
                sceneItemId=scene_item_id,
                sceneItemEnabled=visible
            ))

            action = "shown" if visible else "hidden"
            logger.info(f"Source '{source_name}' {action} in scene '{scene_name}'")
            return True

        except Exception as e:
            logger.error(f"Error setting source visibility: {e}")
            return False

    def show_source(self, scene_name: str, source_name: str) -> bool:
        """Show a source"""
        return self.set_source_visibility(scene_name, source_name, True)

    def hide_source(self, scene_name: str, source_name: str) -> bool:
        """Hide a source"""
        return self.set_source_visibility(scene_name, source_name, False)

    def toggle_source(self, scene_name: str, source_name: str) -> bool:
        """
        Toggle source visibility

        Args:
            scene_name: Name of the scene
            source_name: Name of the source

        Returns:
            True if successful
        """
        if not self.is_connected:
            logger.warning("Not connected to OBS")
            return False

        try:
            # Get current state
            response = self.ws.call(obs_requests.GetSceneItemId(
                sceneName=scene_name,
                sourceName=source_name
            ))

            scene_item_id = response.datain.get('sceneItemId')

            # Get current enabled state
            state_response = self.ws.call(obs_requests.GetSceneItemEnabled(
                sceneName=scene_name,
                sceneItemId=scene_item_id
            ))

            current_state = state_response.datain.get('sceneItemEnabled', False)

            # Toggle
            return self.set_source_visibility(scene_name, source_name, not current_state)

        except Exception as e:
            logger.error(f"Error toggling source: {e}")
            return False

    def show_source_temporarily(self, scene_name: str, source_name: str, duration: float) -> bool:
        """
        Show a source temporarily, then hide it

        Args:
            scene_name: Name of the scene
            source_name: Name of the source
            duration: How long to show (seconds)

        Returns:
            True if successful
        """
        import time
        import threading

        if not self.show_source(scene_name, source_name):
            return False

        def hide_after_delay():
            time.sleep(duration)
            self.hide_source(scene_name, source_name)

        thread = threading.Thread(target=hide_after_delay, daemon=True)
        thread.start()

        return True

    def get_scenes(self) -> List[str]:
        """
        Get list of scene names

        Returns:
            List of scene names
        """
        if not self.is_connected:
            logger.warning("Not connected to OBS")
            return []

        try:
            response = self.ws.call(obs_requests.GetSceneList())
            scenes = response.datain.get('scenes', [])
            return [scene.get('sceneName', '') for scene in scenes]

        except Exception as e:
            logger.error(f"Error getting scenes: {e}")
            return []

    def get_sources_in_scene(self, scene_name: str) -> List[str]:
        """
        Get list of source names in a scene

        Args:
            scene_name: Name of the scene

        Returns:
            List of source names
        """
        if not self.is_connected:
            logger.warning("Not connected to OBS")
            return []

        try:
            response = self.ws.call(obs_requests.GetSceneItemList(
                sceneName=scene_name
            ))

            items = response.datain.get('sceneItems', [])
            return [item.get('sourceName', '') for item in items]

        except Exception as e:
            logger.error(f"Error getting sources: {e}")
            return []

    def set_filter_enabled(self, source_name: str, filter_name: str, enabled: bool) -> bool:
        """
        Enable or disable a filter on a source

        Args:
            source_name: Name of the source
            filter_name: Name of the filter
            enabled: True to enable, False to disable

        Returns:
            True if successful
        """
        if not self.is_connected:
            logger.warning("Not connected to OBS")
            return False

        try:
            self.ws.call(obs_requests.SetSourceFilterEnabled(
                sourceName=source_name,
                filterName=filter_name,
                filterEnabled=enabled
            ))

            action = "enabled" if enabled else "disabled"
            logger.info(f"Filter '{filter_name}' {action} on source '{source_name}'")
            return True

        except Exception as e:
            logger.error(f"Error setting filter state: {e}")
            return False

    def trigger_hotkey(self, hotkey_name: str) -> bool:
        """
        Trigger an OBS hotkey

        Args:
            hotkey_name: Name of the hotkey (e.g., "OBSBasic.StartStreaming")

        Returns:
            True if successful
        """
        if not self.is_connected:
            logger.warning("Not connected to OBS")
            return False

        try:
            self.ws.call(obs_requests.TriggerHotkeyByName(
                hotkeyName=hotkey_name
            ))

            logger.info(f"Triggered hotkey: {hotkey_name}")
            return True

        except Exception as e:
            logger.error(f"Error triggering hotkey: {e}")
            return False

    def get_version(self) -> Optional[Dict[str, Any]]:
        """
        Get OBS version information

        Returns:
            Dictionary with version info or None
        """
        if not self.is_connected:
            return None

        try:
            response = self.ws.call(obs_requests.GetVersion())
            return response.datain

        except Exception as e:
            logger.error(f"Error getting version: {e}")
            return None
