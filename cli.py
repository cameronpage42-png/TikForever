"""
TikForever CLI Version
Simple command-line interface for testing without GUI
"""

import asyncio
import sys
from tiktok_client import TikTokLiveManager
from input_simulator import InputSimulator
from event_mapper import EventMapper
from config_manager import ConfigManager
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TikForeverCLI:
    """Command-line interface for TikForever"""

    def __init__(self, username: str):
        """
        Initialize CLI

        Args:
            username: TikTok username to connect to
        """
        self.username = username
        self.config = ConfigManager()
        self.input_simulator = InputSimulator()
        self.event_mapper = EventMapper(self.input_simulator)
        self.tiktok_manager = None

        # Load configuration
        self.load_config()

    def load_config(self):
        """Load configuration"""
        logger.info("Loading configuration...")

        # Override username if provided
        if self.username:
            self.config.set_tiktok_username(self.username)
        else:
            self.username = self.config.get_tiktok_username()
            if not self.username:
                logger.error("No username provided and none in config")
                sys.exit(1)

        # Load mappings
        mappings = self.config.get_mappings()
        self.event_mapper.load_mappings(mappings)

        logger.info(f"Loaded {len(mappings)} event mappings")
        logger.info(f"Username: @{self.username}")

    def handle_event(self, event_type: str, event_data: dict):
        """Handle TikTok Live event"""

        # Process through event mapper
        self.event_mapper.process_event(event_type, event_data)

    async def run(self):
        """Run the CLI application"""

        logger.info("="*50)
        logger.info("TikForever - TikTok Live Game Controller")
        logger.info("="*50)
        logger.info(f"Connecting to @{self.username}'s live stream...")
        logger.info("Press Ctrl+C to stop")
        logger.info("")

        try:
            # Create TikTok manager
            self.tiktok_manager = TikTokLiveManager(self.username)

            # Register event handlers
            self.tiktok_manager.on_event('comment', lambda data: self.handle_event('comment', data))
            self.tiktok_manager.on_event('gift', lambda data: self.handle_event('gift', data))
            self.tiktok_manager.on_event('like', lambda data: self.handle_event('like', data))
            self.tiktok_manager.on_event('share', lambda data: self.handle_event('share', data))
            self.tiktok_manager.on_event('follow', lambda data: self.handle_event('follow', data))

            # Connect
            await self.tiktok_manager.connect()

            logger.info("Connected! Listening for events...")
            logger.info("")

            # Keep running
            while self.tiktok_manager.is_connected:
                await asyncio.sleep(1)

        except KeyboardInterrupt:
            logger.info("\nStopping...")
        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            if self.tiktok_manager:
                await self.tiktok_manager.disconnect()
            logger.info("Disconnected. Goodbye!")


def main():
    """Main entry point"""

    username = None

    # Parse command line arguments
    if len(sys.argv) > 1:
        username = sys.argv[1]
        if username.startswith('@'):
            username = username[1:]

    # Run CLI
    cli = TikForeverCLI(username)
    asyncio.run(cli.run())


if __name__ == '__main__':
    main()
