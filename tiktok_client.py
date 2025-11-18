"""
TikTok Live Client Module
Handles connection to TikTok Live streams and event processing
"""

from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent, LikeEvent, ShareEvent, FollowEvent
from typing import Callable, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TikTokLiveManager:
    """Manages TikTok Live connection and event handling"""

    def __init__(self, username: str):
        """
        Initialize TikTok Live Manager

        Args:
            username: TikTok username to connect to
        """
        # Clean username (remove @ if present)
        if username.startswith('@'):
            username = username[1:]

        self.username = username
        logger.info(f"Initializing TikTok client for @{username}")
        self.client = TikTokLiveClient(unique_id=f"@{username}")
        self.is_connected = False
        self.event_callbacks = {
            'comment': [],
            'gift': [],
            'like': [],
            'share': [],
            'follow': [],
            'connect': [],
            'disconnect': []
        }

        self._setup_event_handlers()

    def _setup_event_handlers(self):
        """Set up TikTok Live event handlers"""

        @self.client.on(ConnectEvent)
        async def on_connect(event: ConnectEvent):
            logger.info(f"Connected to @{self.username}'s live stream!")
            self.is_connected = True
            await self._trigger_callbacks('connect', {
                'unique_id': event.unique_id
            })

        @self.client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            logger.info(f"Comment: {event.user.nickname}: {event.comment}")
            await self._trigger_callbacks('comment', {
                'user': event.user.nickname,
                'comment': event.comment.lower().strip()
            })

        @self.client.on(GiftEvent)
        async def on_gift(event: GiftEvent):
            # Only process gifts that are not part of a streak
            if event.gift.streaking:
                return

            logger.info(f"Gift: {event.user.nickname} sent {event.gift.name} x{event.gift.count}")
            await self._trigger_callbacks('gift', {
                'user': event.user.nickname,
                'gift_name': event.gift.name,
                'gift_id': event.gift.id,
                'count': event.gift.count
            })

        @self.client.on(LikeEvent)
        async def on_like(event: LikeEvent):
            logger.info(f"Like: {event.user.nickname} sent {event.count} likes")
            await self._trigger_callbacks('like', {
                'user': event.user.nickname,
                'count': event.count,
                'total': event.total
            })

        @self.client.on(ShareEvent)
        async def on_share(event: ShareEvent):
            logger.info(f"Share: {event.user.nickname} shared the stream")
            await self._trigger_callbacks('share', {
                'user': event.user.nickname
            })

        @self.client.on(FollowEvent)
        async def on_follow(event: FollowEvent):
            logger.info(f"Follow: {event.user.nickname} followed!")
            await self._trigger_callbacks('follow', {
                'user': event.user.nickname
            })

    async def _trigger_callbacks(self, event_type: str, event_data: Dict[str, Any]):
        """
        Trigger all registered callbacks for an event type

        Args:
            event_type: Type of event (comment, gift, etc.)
            event_data: Event data dictionary
        """
        if event_type in self.event_callbacks:
            for callback in self.event_callbacks[event_type]:
                try:
                    if callback:
                        callback(event_data)
                except Exception as e:
                    logger.error(f"Error in callback: {e}")

    def on_event(self, event_type: str, callback: Callable):
        """
        Register a callback for an event type

        Args:
            event_type: Type of event (comment, gift, like, share, follow, connect, disconnect)
            callback: Function to call when event occurs
        """
        if event_type in self.event_callbacks:
            self.event_callbacks[event_type].append(callback)
        else:
            logger.warning(f"Unknown event type: {event_type}")

    async def connect(self):
        """Connect to TikTok Live stream"""
        try:
            logger.info(f"Connecting to @{self.username}'s live stream...")
            await self.client.connect()
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            self.is_connected = False
            raise

    async def disconnect(self):
        """Disconnect from TikTok Live stream"""
        try:
            if self.is_connected:
                await self.client.disconnect()
                self.is_connected = False
                logger.info("Disconnected from live stream")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")

    def run(self):
        """Run the TikTok Live client (blocking)"""
        try:
            self.client.run()
        except KeyboardInterrupt:
            logger.info("Stopped by user")
        except Exception as e:
            logger.error(f"Error running client: {e}")
            raise
