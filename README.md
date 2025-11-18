# TikForever - TikTok Live Game Controller

A Windows application that connects to TikTok Live streams and allows viewers to interact with games through keyboard and controller inputs.

## Features

- 🎮 **Game Control**: Simulate keyboard presses and controller inputs
- 🔴 **TikTok Live Integration**: Connect to any TikTok Live stream
- 💬 **Event Mapping**: Map TikTok events (comments, gifts, likes) to game inputs
- ⚙️ **Customizable**: Configure key bindings and event triggers
- 🖥️ **Windows Native**: Optimized for Windows with full controller support

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

## Configuration

The application stores configuration in `config.json`. You can manually edit this file or use the GUI.

Example configuration:
```json
{
  "tiktok_username": "your_username",
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

**Connection Issues**:
- Make sure your TikTok account is set to public
- Verify you're using the correct username
- Check your internet connection

**Input Not Working**:
- Run the application as Administrator (required for some games)
- Make sure the game window is focused
- Check that your mappings are configured correctly

**Controller Not Detected**:
- Install vgamepad properly (requires ViGEmBus driver)
- Check Windows device manager for virtual controller

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

## License

MIT License - See LICENSE file for details
