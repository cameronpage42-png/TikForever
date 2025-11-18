# TikForever Setup Guide

Complete step-by-step guide to setting up TikForever on Windows.

## Prerequisites

### 1. Install Python

1. Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
2. **IMPORTANT**: During installation, check "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

### 2. Install Virtual Controller Driver (Optional - for controller support)

If you want to use virtual controller inputs:

1. Download ViGEmBus from: https://github.com/ViGEm/ViGEmBus/releases
2. Install `ViGEmBus_Setup_x64.msi`
3. Restart your computer

## Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd TikForever
```

Or download and extract the ZIP file.

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

```bash
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- TikTokLive - for TikTok Live connection
- PyQt6 - for the GUI
- pynput - for keyboard simulation
- vgamepad - for controller simulation (Windows only)

## Configuration

### 1. Create Configuration File

Copy the example configuration:

```bash
copy config.example.json config.json
```

### 2. Edit Configuration

Open `config.json` in a text editor and set your TikTok username:

```json
{
  "tiktok_username": "your_username_here",
  ...
}
```

### 3. Customize Mappings

Edit the `mappings` section to configure what TikTok events trigger what inputs.

Example mapping:
```json
{
  "event_type": "comment",
  "trigger": "jump",
  "action": "keyboard",
  "key": "space",
  "duration": 0.1,
  "cooldown": 0.5,
  "enabled": true,
  "description": "Jump command"
}
```

## Running the Application

### GUI Version (Recommended)

```bash
python main.py
```

### CLI Version (For Testing)

```bash
python cli.py your_username
```

## Usage

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Enter your TikTok username** (the account that will go live)

3. **Configure event mappings** in the "Event Mappings" tab
   - Click "Add Mapping" to create new mappings
   - Common examples:
     - Comment "jump" → Keyboard "space"
     - Comment "left" → Keyboard "left arrow"
     - Gift "Rose" → Controller "A button"

4. **Start your TikTok Live stream** on your phone or computer

5. **Click "Connect to Live"** in the application

6. **Launch your game** and make sure the game window is focused

7. **Let viewers control the game!** Tell them to type commands in chat

## Common Event Mappings

### Keyboard Mappings

| Trigger | Key | Use Case |
|---------|-----|----------|
| jump | space | Jumping |
| left | left | Move left |
| right | right | Move right |
| up | up | Move up |
| down | down | Move down |
| attack | ctrl | Attack/Action |
| run | shift | Run/Sprint |

### Controller Mappings

| Trigger | Button | Use Case |
|---------|--------|----------|
| a | a | A button |
| b | b | B button |
| x | x | X button |
| y | y | Y button |
| start | start | Start/Pause |

### Gift Mappings

| Gift | Action | Use Case |
|------|--------|----------|
| Rose | Special move | Cheap gift = common action |
| TikTok | Ultimate ability | Expensive gift = powerful action |

## Troubleshooting

### "Module not found" error

Make sure you activated the virtual environment:
```bash
venv\Scripts\activate
```

Then reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Connection fails

- Verify your TikTok username is correct (without @)
- Make sure you are currently live on TikTok
- Check your internet connection
- Your account must be public

### Inputs not working in game

- **Run as Administrator**: Right-click `main.py` → Run as administrator
- Make sure the game window is focused (clicked on)
- Some games block simulated inputs (anti-cheat)
- Try testing with Notepad first to verify inputs work

### Controller not working

- Install ViGEmBus driver (see Prerequisites)
- Restart your computer after installing
- Check Device Manager for "Virtual Xbox 360 Controller"

### High latency / delayed inputs

- Reduce cooldown values in mappings
- Check your internet connection
- TikTok Live has inherent 2-5 second delay

## Advanced Configuration

### Cooldown Settings

- `duration`: How long to hold the key/button (seconds)
- `cooldown`: Minimum time before same command can trigger again (seconds)

Adjust based on your needs:
- Fast-paced games: Lower cooldown (0.1-0.5s)
- Prevent spam: Higher cooldown (1-5s)
- Special moves: Very high cooldown (10-30s)

### Multiple Triggers

You can have multiple mappings for the same input:

```json
[
  {"trigger": "jump", "key": "space"},
  {"trigger": "hop", "key": "space"},
  {"trigger": "leap", "key": "space"}
]
```

### Key Combinations

Use `+` to combine keys:

```json
{
  "key": "ctrl+c",
  "description": "Copy"
}
```

## Tips for Streamers

1. **Start Simple**: Begin with 4-5 basic commands
2. **Test First**: Test all mappings before going live
3. **Set Cooldowns**: Prevent spam with appropriate cooldowns
4. **Engage Chat**: Tell viewers what commands are available
5. **Use Gifts Wisely**: Map rare gifts to powerful/funny actions
6. **Have a Failsafe**: Keep manual control in case you need it

## Security Notes

- The app only reads **public** TikTok Live data
- No login required
- No passwords stored
- All data stays on your computer
- Open source - you can inspect the code

## Getting Help

If you encounter issues:

1. Check this guide's Troubleshooting section
2. Read the main README.md
3. Check the GitHub Issues page
4. Make sure you're using the latest version

## Uninstallation

To remove TikForever:

1. Deactivate virtual environment:
   ```bash
   deactivate
   ```

2. Delete the TikForever folder

3. (Optional) Uninstall ViGEmBus from Windows Settings

That's it! Enjoy using TikForever! 🎮
