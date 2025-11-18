"""
Event Mapper Module
Maps TikTok Live events to game inputs with cooldown management
"""

import time
import logging
from typing import Dict, List, Any, Optional
from input_simulator import InputSimulator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventMapping:
    """Represents a single event-to-input mapping"""

    def __init__(self, mapping_data: Dict[str, Any]):
        """
        Initialize event mapping

        Args:
            mapping_data: Dictionary containing mapping configuration
        """
        self.event_type = mapping_data.get('event_type')  # comment, gift, like, share, follow
        self.trigger = mapping_data.get('trigger')  # e.g., comment text, gift name
        self.action_type = mapping_data.get('action')  # keyboard, controller
        self.key = mapping_data.get('key')  # For keyboard
        self.button = mapping_data.get('button')  # For controller button
        self.joystick = mapping_data.get('joystick')  # For joystick movement
        self.trigger_name = mapping_data.get('trigger_name')  # For controller trigger
        self.duration = mapping_data.get('duration', 0.1)  # Action duration
        self.cooldown = mapping_data.get('cooldown', 0.5)  # Cooldown between triggers
        self.last_triggered = 0
        self.enabled = mapping_data.get('enabled', True)
        self.description = mapping_data.get('description', '')

    def can_trigger(self) -> bool:
        """Check if mapping can be triggered (cooldown check)"""
        if not self.enabled:
            return False

        current_time = time.time()
        return (current_time - self.last_triggered) >= self.cooldown

    def mark_triggered(self):
        """Mark this mapping as triggered (for cooldown)"""
        self.last_triggered = time.time()

    def matches_event(self, event_data: Dict[str, Any]) -> bool:
        """
        Check if this mapping matches the given event

        Args:
            event_data: Event data from TikTok Live

        Returns:
            True if the event matches this mapping
        """
        if self.event_type == 'comment':
            # Match comment text (case-insensitive, exact match or contains)
            comment = event_data.get('comment', '').lower().strip()
            trigger = self.trigger.lower().strip()
            return comment == trigger or trigger in comment

        elif self.event_type == 'gift':
            # Match gift name
            gift_name = event_data.get('gift_name', '')
            return gift_name.lower() == self.trigger.lower()

        elif self.event_type in ['like', 'share', 'follow']:
            # These events don't need specific triggers
            return True

        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert mapping to dictionary"""
        return {
            'event_type': self.event_type,
            'trigger': self.trigger,
            'action': self.action_type,
            'key': self.key,
            'button': self.button,
            'joystick': self.joystick,
            'trigger_name': self.trigger_name,
            'duration': self.duration,
            'cooldown': self.cooldown,
            'enabled': self.enabled,
            'description': self.description
        }


class EventMapper:
    """Manages event mappings and triggers inputs"""

    def __init__(self, input_simulator: InputSimulator):
        """
        Initialize event mapper

        Args:
            input_simulator: InputSimulator instance
        """
        self.input_simulator = input_simulator
        self.mappings: List[EventMapping] = []
        self.global_cooldown = 0.1  # Minimum time between any actions
        self.last_action_time = 0

    def add_mapping(self, mapping_data: Dict[str, Any]):
        """
        Add a new event mapping

        Args:
            mapping_data: Dictionary containing mapping configuration
        """
        mapping = EventMapping(mapping_data)
        self.mappings.append(mapping)
        logger.info(f"Added mapping: {mapping.event_type} '{mapping.trigger}' -> {mapping.action_type}")

    def remove_mapping(self, index: int):
        """
        Remove a mapping by index

        Args:
            index: Index of mapping to remove
        """
        if 0 <= index < len(self.mappings):
            removed = self.mappings.pop(index)
            logger.info(f"Removed mapping: {removed.event_type} '{removed.trigger}'")

    def clear_mappings(self):
        """Remove all mappings"""
        self.mappings.clear()
        logger.info("Cleared all mappings")

    def load_mappings(self, mappings_data: List[Dict[str, Any]]):
        """
        Load multiple mappings from list

        Args:
            mappings_data: List of mapping dictionaries
        """
        self.clear_mappings()
        for mapping_data in mappings_data:
            self.add_mapping(mapping_data)

    def get_mappings(self) -> List[Dict[str, Any]]:
        """Get all mappings as list of dictionaries"""
        return [m.to_dict() for m in self.mappings]

    def process_event(self, event_type: str, event_data: Dict[str, Any]):
        """
        Process a TikTok Live event and trigger matching inputs

        Args:
            event_type: Type of event (comment, gift, like, etc.)
            event_data: Event data dictionary
        """
        # Check global cooldown
        current_time = time.time()
        if (current_time - self.last_action_time) < self.global_cooldown:
            return

        # Find matching mappings
        for mapping in self.mappings:
            if mapping.event_type == event_type and mapping.matches_event(event_data):
                if mapping.can_trigger():
                    self._execute_mapping(mapping, event_data)
                    mapping.mark_triggered()
                    self.last_action_time = current_time
                    break  # Only execute first match

    def _execute_mapping(self, mapping: EventMapping, event_data: Dict[str, Any]):
        """
        Execute a mapping's action

        Args:
            mapping: EventMapping to execute
            event_data: Event data for logging
        """
        try:
            if mapping.action_type == 'keyboard':
                if mapping.key:
                    # Check if it's a key combination
                    if '+' in mapping.key:
                        keys = mapping.key.split('+')
                        self.input_simulator.press_key_combination(keys, mapping.duration)
                    else:
                        self.input_simulator.press_key(mapping.key, mapping.duration)

            elif mapping.action_type == 'controller':
                if mapping.button:
                    self.input_simulator.press_button(mapping.button, mapping.duration)
                elif mapping.joystick:
                    # Format: "left:0.5:1.0" or "right:-1.0:0.0"
                    parts = mapping.joystick.split(':')
                    if len(parts) == 3:
                        stick, x, y = parts[0], float(parts[1]), float(parts[2])
                        self.input_simulator.move_joystick(stick, x, y, mapping.duration)
                elif mapping.trigger_name:
                    # Format: "left:0.5" or "right:1.0"
                    parts = mapping.trigger_name.split(':')
                    if len(parts) == 2:
                        trigger, value = parts[0], float(parts[1])
                        self.input_simulator.press_trigger(trigger, value, mapping.duration)

            user = event_data.get('user', 'Unknown')
            logger.info(f"Executed mapping for {user}: {mapping.event_type} -> {mapping.action_type}")

        except Exception as e:
            logger.error(f"Error executing mapping: {e}")

    def get_mapping_stats(self) -> Dict[str, int]:
        """Get statistics about mappings"""
        stats = {
            'total': len(self.mappings),
            'enabled': sum(1 for m in self.mappings if m.enabled),
            'disabled': sum(1 for m in self.mappings if not m.enabled),
            'keyboard': sum(1 for m in self.mappings if m.action_type == 'keyboard'),
            'controller': sum(1 for m in self.mappings if m.action_type == 'controller')
        }
        return stats
