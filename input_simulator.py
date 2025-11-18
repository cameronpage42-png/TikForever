"""
Input Simulator Module
Handles keyboard and controller input simulation
"""

from pynput.keyboard import Controller as KeyboardController, Key
import time
import logging
from typing import Optional, List
import platform

# Only import vgamepad on Windows
if platform.system() == 'Windows':
    try:
        import vgamepad as vg
        VGAMEPAD_AVAILABLE = True
    except ImportError:
        VGAMEPAD_AVAILABLE = False
        logging.warning("vgamepad not available - controller support disabled")
else:
    VGAMEPAD_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InputSimulator:
    """Simulates keyboard and controller inputs"""

    def __init__(self):
        """Initialize input simulator"""
        self.keyboard = KeyboardController()
        self.gamepad = None

        if VGAMEPAD_AVAILABLE:
            try:
                self.gamepad = vg.VX360Gamepad()
                logger.info("Virtual Xbox 360 controller initialized")
            except Exception as e:
                logger.error(f"Failed to initialize virtual controller: {e}")
                self.gamepad = None

    def press_key(self, key_name: str, duration: float = 0.1):
        """
        Press a keyboard key

        Args:
            key_name: Name of the key (e.g., 'a', 'space', 'enter', 'ctrl')
            duration: How long to hold the key (seconds)
        """
        try:
            # Convert string to Key object if it's a special key
            key = self._get_key(key_name.lower())

            self.keyboard.press(key)
            time.sleep(duration)
            self.keyboard.release(key)

            logger.info(f"Pressed key: {key_name}")
        except Exception as e:
            logger.error(f"Error pressing key {key_name}: {e}")

    def press_key_combination(self, keys: List[str], duration: float = 0.1):
        """
        Press a combination of keys

        Args:
            keys: List of key names (e.g., ['ctrl', 'c'])
            duration: How long to hold the keys (seconds)
        """
        try:
            key_objects = [self._get_key(k.lower()) for k in keys]

            # Press all keys
            for key in key_objects:
                self.keyboard.press(key)

            time.sleep(duration)

            # Release in reverse order
            for key in reversed(key_objects):
                self.keyboard.release(key)

            logger.info(f"Pressed key combination: {'+'.join(keys)}")
        except Exception as e:
            logger.error(f"Error pressing key combination {keys}: {e}")

    def _get_key(self, key_name: str):
        """
        Convert key name string to Key object

        Args:
            key_name: Name of the key

        Returns:
            Key object or character
        """
        # Special keys mapping
        special_keys = {
            'space': Key.space,
            'enter': Key.enter,
            'return': Key.enter,
            'tab': Key.tab,
            'backspace': Key.backspace,
            'delete': Key.delete,
            'esc': Key.esc,
            'escape': Key.esc,
            'shift': Key.shift,
            'ctrl': Key.ctrl,
            'control': Key.ctrl,
            'alt': Key.alt,
            'cmd': Key.cmd,
            'up': Key.up,
            'down': Key.down,
            'left': Key.left,
            'right': Key.right,
            'home': Key.home,
            'end': Key.end,
            'pageup': Key.page_up,
            'pagedown': Key.page_down,
            'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3, 'f4': Key.f4,
            'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8,
            'f9': Key.f9, 'f10': Key.f10, 'f11': Key.f11, 'f12': Key.f12,
        }

        if key_name in special_keys:
            return special_keys[key_name]

        # Return single character for regular keys
        return key_name[0] if len(key_name) == 1 else key_name

    def press_button(self, button_name: str, duration: float = 0.1):
        """
        Press a controller button

        Args:
            button_name: Name of the button (e.g., 'A', 'B', 'X', 'Y', 'LB', 'RB')
            duration: How long to hold the button (seconds)
        """
        if not VGAMEPAD_AVAILABLE or not self.gamepad:
            logger.warning("Controller not available")
            return

        try:
            button_map = {
                'a': vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
                'b': vg.XUSB_BUTTON.XUSB_GAMEPAD_B,
                'x': vg.XUSB_BUTTON.XUSB_GAMEPAD_X,
                'y': vg.XUSB_BUTTON.XUSB_GAMEPAD_Y,
                'lb': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER,
                'rb': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER,
                'start': vg.XUSB_BUTTON.XUSB_GAMEPAD_START,
                'back': vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK,
                'ls': vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB,
                'rs': vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB,
                'dpad_up': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP,
                'dpad_down': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN,
                'dpad_left': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT,
                'dpad_right': vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT,
            }

            button = button_map.get(button_name.lower())
            if not button:
                logger.warning(f"Unknown button: {button_name}")
                return

            self.gamepad.press_button(button)
            self.gamepad.update()
            time.sleep(duration)
            self.gamepad.release_button(button)
            self.gamepad.update()

            logger.info(f"Pressed controller button: {button_name}")
        except Exception as e:
            logger.error(f"Error pressing button {button_name}: {e}")

    def move_joystick(self, stick: str, x: float, y: float, duration: float = 0.1):
        """
        Move a joystick

        Args:
            stick: 'left' or 'right'
            x: X-axis value (-1.0 to 1.0)
            y: Y-axis value (-1.0 to 1.0)
            duration: How long to hold the position (seconds)
        """
        if not VGAMEPAD_AVAILABLE or not self.gamepad:
            logger.warning("Controller not available")
            return

        try:
            # Convert -1 to 1 range to controller range
            x_value = int(x * 32767)
            y_value = int(y * 32767)

            if stick.lower() == 'left':
                self.gamepad.left_joystick(x_value, y_value)
            elif stick.lower() == 'right':
                self.gamepad.right_joystick(x_value, y_value)
            else:
                logger.warning(f"Unknown stick: {stick}")
                return

            self.gamepad.update()
            time.sleep(duration)

            # Reset to center
            if stick.lower() == 'left':
                self.gamepad.left_joystick(0, 0)
            else:
                self.gamepad.right_joystick(0, 0)

            self.gamepad.update()

            logger.info(f"Moved {stick} joystick: ({x}, {y})")
        except Exception as e:
            logger.error(f"Error moving joystick: {e}")

    def press_trigger(self, trigger: str, value: float = 1.0, duration: float = 0.1):
        """
        Press a trigger

        Args:
            trigger: 'left' or 'right'
            value: Trigger value (0.0 to 1.0)
            duration: How long to hold (seconds)
        """
        if not VGAMEPAD_AVAILABLE or not self.gamepad:
            logger.warning("Controller not available")
            return

        try:
            trigger_value = int(value * 255)

            if trigger.lower() == 'left':
                self.gamepad.left_trigger(trigger_value)
            elif trigger.lower() == 'right':
                self.gamepad.right_trigger(trigger_value)
            else:
                logger.warning(f"Unknown trigger: {trigger}")
                return

            self.gamepad.update()
            time.sleep(duration)

            # Reset trigger
            if trigger.lower() == 'left':
                self.gamepad.left_trigger(0)
            else:
                self.gamepad.right_trigger(0)

            self.gamepad.update()

            logger.info(f"Pressed {trigger} trigger: {value}")
        except Exception as e:
            logger.error(f"Error pressing trigger: {e}")
