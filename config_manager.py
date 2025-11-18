"""
Configuration Manager Module
Handles loading and saving application configuration
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration"""

    DEFAULT_CONFIG = {
        'tiktok_username': '',
        'window_geometry': {
            'width': 900,
            'height': 700,
            'x': 100,
            'y': 100
        },
        'mappings': [
            {
                'event_type': 'comment',
                'trigger': 'jump',
                'action': 'keyboard',
                'key': 'space',
                'duration': 0.1,
                'cooldown': 0.5,
                'enabled': True,
                'description': 'Jump command'
            },
            {
                'event_type': 'comment',
                'trigger': 'left',
                'action': 'keyboard',
                'key': 'left',
                'duration': 0.2,
                'cooldown': 0.3,
                'enabled': True,
                'description': 'Move left'
            },
            {
                'event_type': 'comment',
                'trigger': 'right',
                'action': 'keyboard',
                'key': 'right',
                'duration': 0.2,
                'cooldown': 0.3,
                'enabled': True,
                'description': 'Move right'
            },
            {
                'event_type': 'comment',
                'trigger': 'up',
                'action': 'keyboard',
                'key': 'up',
                'duration': 0.2,
                'cooldown': 0.3,
                'enabled': True,
                'description': 'Move up'
            },
            {
                'event_type': 'comment',
                'trigger': 'down',
                'action': 'keyboard',
                'key': 'down',
                'duration': 0.2,
                'cooldown': 0.3,
                'enabled': True,
                'description': 'Move down'
            }
        ],
        'settings': {
            'auto_reconnect': True,
            'log_events': True,
            'sound_enabled': False,
            'global_cooldown': 0.1
        }
    }

    def __init__(self, config_file: str = 'config.json'):
        """
        Initialize configuration manager

        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> bool:
        """
        Load configuration from file

        Returns:
            True if loaded successfully, False otherwise
        """
        if not os.path.exists(self.config_file):
            logger.info(f"Config file not found, using defaults")
            self.save()  # Create default config file
            return False

        try:
            with open(self.config_file, 'r') as f:
                loaded_config = json.load(f)

            # Merge with defaults (in case new fields were added)
            self.config = self._merge_configs(self.DEFAULT_CONFIG, loaded_config)

            logger.info(f"Loaded configuration from {self.config_file}")
            return True

        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return False

    def save(self) -> bool:
        """
        Save configuration to file

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)

            logger.info(f"Saved configuration to {self.config_file}")
            return True

        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False

    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """
        Merge loaded config with defaults

        Args:
            default: Default configuration
            loaded: Loaded configuration

        Returns:
            Merged configuration
        """
        merged = default.copy()

        for key, value in loaded.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value

        return merged

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key (supports dot notation, e.g., 'settings.auto_reconnect')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        Set configuration value

        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def get_tiktok_username(self) -> str:
        """Get TikTok username"""
        return self.config.get('tiktok_username', '')

    def set_tiktok_username(self, username: str):
        """Set TikTok username"""
        self.config['tiktok_username'] = username

    def get_mappings(self) -> List[Dict[str, Any]]:
        """Get event mappings"""
        return self.config.get('mappings', [])

    def set_mappings(self, mappings: List[Dict[str, Any]]):
        """Set event mappings"""
        self.config['mappings'] = mappings

    def get_window_geometry(self) -> Dict[str, int]:
        """Get window geometry"""
        return self.config.get('window_geometry', self.DEFAULT_CONFIG['window_geometry'])

    def set_window_geometry(self, width: int, height: int, x: int, y: int):
        """Set window geometry"""
        self.config['window_geometry'] = {
            'width': width,
            'height': height,
            'x': x,
            'y': y
        }

    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.config.get('settings', {}).get(key, default)

    def set_setting(self, key: str, value: Any):
        """Set a setting value"""
        if 'settings' not in self.config:
            self.config['settings'] = {}
        self.config['settings'][key] = value

    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        logger.info("Reset configuration to defaults")
