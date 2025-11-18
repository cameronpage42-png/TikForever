# TikForever - TikTok Live Game Controller

A Windows application that connects to TikTok Live streams and allows viewers to interact with games through keyboard and controller inputs.

## Features

- 🎮 **Game Control**: Simulate keyboard presses and controller inputs
- 🔴 **TikTok Live Integration**: Connect to any TikTok Live stream
- 💬 **Event Mapping**: Map TikTok events (comments, gifts, likes, shares, follows) to game inputs
- 📺 **Browser Source Alerts**: Professional animated alerts for TikTok Live Studio (RECOMMENDED!)
- 🎯 **OBS Integration**: Control OBS Studio via WebSocket or hotkeys
- ⚙️ **Customizable**: Configure key bindings and event triggers via GUI
- 🖥️ **Windows Native**: Optimized for Windows with optional controller support

## Requirements

- Windows 10/11
- Python 3.8 or higher
- TikTok account (for live streaming)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd TikForever
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

1. Start the application:
```bash
python main.py
```

2. Enter your TikTok username (the one going live)
3. Configure event mappings (what commands trigger what inputs)
4. Click "Connect" to start receiving TikTok Live events
5. Start your game and watch as viewers interact!

### Event Types

The app supports the following TikTok Live events:

- **Comments**: Trigger actions based on specific comment text (e.g., "jump", "left", "right")
- **Gifts**: Different gifts can trigger different actions
- **Likes**: Trigger actions when viewers send likes
- **Shares**: Trigger actions when stream is shared
- **Follows**: Trigger actions when someone follows

### Input Types

#### Keyboard Inputs
- Single key press (e.g., "w", "space", "enter")
- Key combinations (e.g., "ctrl+c", "shift+w")
- Key hold duration

#### Controller Inputs (Xbox-style)
- Button presses (A, B, X, Y, LB, RB, etc.)
- Joystick movements
- Trigger presses

#### Browser Source Alerts (RECOMMENDED for TikTok Live Studio!)
- **Professional animated alerts** with images, GIFs, and videos
- **Works perfectly** with TikTok Live Studio AND OBS Studio
- **Easy setup**: Just add `http://localhost:8000` as a Browser Source
- **Auto-hiding** alerts with configurable duration
- **Multiple simultaneous alerts** supported

**Browser Source Setup**: See [BROWSER_SOURCE_SETUP.md](BROWSER_SOURCE_SETUP.md) for complete setup guide.

#### OBS WebSocket Actions (OBS Studio Only)
- **Show Source**: Make a source visible
- **Hide Source**: Hide a source
- **Toggle Source**: Toggle source visibility
- **Show Temporarily**: Show for X seconds then auto-hide

**OBS WebSocket Setup**: See [OBS_SETUP.md](OBS_SETUP.md) for instructions.

#### OBS Hotkey Actions (Works with TikTok Live Studio!)
- **Trigger hotkeys** in OBS or TikTok Live Studio
- **No WebSocket needed** - simpler setup
- **Flexible** - can trigger any action assigned to a hotkey

**Example Use Cases**:
- Show a "Follow Alert" graphic when someone follows
- Trigger gift animations when viewers send gifts
- Display thank you messages on screen
- Toggle special effects based on engagement

## Configuration

The application stores configuration in `config.json`. You can manually edit this file or use the GUI.

Example configuration:
```json
{
  "tiktok_username": "your_username",
  "obs": {
    "enabled": true,
    "host": "localhost",
    "port": 4455,
    "password": ""
  },
  "mappings": [
    {
      "event_type": "comment",
      "trigger": "jump",
      "action": "keyboard",
      "key": "space"
    },
    {
      "event_type": "gift",
      "trigger": "Rose",
      "action": "controller",
      "button": "A"
    },
    {
      "event_type": "follow",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Main Scene",
      "obs_source": "Follow Alert",
      "duration": 3.0
    }
  ]
}
```

## How It Works

1. **Connection**: The app connects to TikTok Live using the TikTokLive library
2. **Event Listening**: Listens for events (comments, gifts, etc.) from the live stream
3. **Event Processing**: Matches events against your configured mappings
4. **Input Simulation**: Simulates the corresponding keyboard or controller input
5. **Cooldowns**: Prevents spam with configurable cooldown periods

## Tips for Streamers

- Start with simple commands (e.g., "left", "right", "jump")
- Use cooldowns to prevent spam
- Test your configuration before going live
- Consider using rare gifts for powerful actions
- Have fun and engage with your audience!

## Troubleshooting

### Quick Fixes

**Events/Statistics Not Updating**:
- **MUST be actively live streaming on TikTok** (not just opening the app)
- Send a test comment from another device to verify
- Check the Event Log tab to see if events are being received

**Connection Issues**:
- Make sure your TikTok account is set to public
- Verify you're using the correct username (without @)
- Ensure you're actually live streaming when connecting
- Check your internet connection

**Input Not Working**:
- Run the application as Administrator (required for some games)
- Make sure the game window is focused (clicked on)
- Check that your mappings are configured correctly
- Test with Notepad first to verify keys work

**Controller Not Detected**:
- Install vgamepad properly (requires ViGEmBus driver)
- Check Windows device manager for virtual controller

**For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

## Safety & Privacy

- The app only reads public TikTok Live data
- No passwords or sensitive information required
- All configuration stored locally
- Open source - inspect the code yourself!

## Credits

Built with:
- [TikTokLive](https://github.com/isaackogan/TikTokLive) - TikTok Live connection
- [pynput](https://github.com/moses-palmer/pynput) - Keyboard/mouse control
- [vgamepad](https://github.com/yannbouteiller/vgamepad) - Virtual controller
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [Flask](https://flask.palletsprojects.com/) - Browser source alert server
- [obs-websocket-py](https://github.com/Elektordi/obs-websocket-py) - OBS WebSocket control

## License

MIT License - See LICENSE file for details
