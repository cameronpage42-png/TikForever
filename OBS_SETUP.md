# OBS/TikTok Live Studio Integration Guide for TikForever

This guide shows you how to connect TikForever with OBS Studio and TikTok Live Studio to control sources and trigger visual effects.

## Two Integration Methods

TikForever supports **two methods** for controlling OBS/TikTok Live Studio:

### Method 1: WebSocket (OBS Studio Only) ✅
- **Works with**: OBS Studio 28+
- **Requires**: OBS WebSocket enabled
- **Features**: Direct control of sources (show, hide, toggle, show_temp)
- **Setup**: Moderate (see below)

### Method 2: Hotkeys (OBS Studio + TikTok Live Studio) ✅ RECOMMENDED FOR TIKTOK LIVE STUDIO
- **Works with**: OBS Studio AND TikTok Live Studio
- **Requires**: Only hotkey configuration in streaming software
- **Features**: Trigger any action you can assign to a hotkey
- **Setup**: Easy (just assign hotkeys and configure TikForever)
- **Note**: This is how similar apps work with TikTok Live Studio!

**💡 For TikTok Live Studio users**: Use Method 2 (Hotkeys) as TikTok Live Studio does not expose WebSocket settings.

---

## What Can You Do?

Both methods enable features like:
- 📺 Show/hide sources when viewers follow, gift, or comment
- 🎬 Trigger animations or overlays
- 🎮 Make your stream interactive

## Prerequisites

- **OBS Studio 28.0+** or **TikTok Live Studio**
- **TikForever** installed

## Step 1: Enable OBS WebSocket

### For OBS Studio 28+:

1. Open **OBS Studio**
2. Go to **Tools** → **WebSocket Server Settings**
3. Check **"Enable WebSocket server"**
4. Note the **Server Port** (default: 4455)
5. Set a **Server Password** (optional but recommended)
6. Click **OK**

### For TikTok Live Studio:

TikTok Live Studio has OBS WebSocket built-in:

1. Open **TikTok Live Studio**
2. Go to **Settings** (gear icon)
3. Look for **"Advanced"** or **"WebSocket"** settings
4. Enable **WebSocket Server**
5. Note the port (usually 4455) and password if set

**Note**: If you can't find WebSocket settings in TikTok Live Studio, it may be using default settings (port 4455, no password).

## Step 2: Configure TikForever

### Option A: Manual Configuration

Edit `config.json` and add OBS settings:

```json
{
  "tiktok_username": "your_username",
  "obs": {
    "enabled": true,
    "host": "localhost",
    "port": 4455,
    "password": "your_password_here"
  },
  "mappings": [
    {
      "event_type": "follow",
      "trigger": "",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Main Scene",
      "obs_source": "Follow Alert",
      "duration": 3.0,
      "cooldown": 2.0,
      "enabled": true,
      "description": "Show follow alert for 3 seconds"
    },
    {
      "event_type": "gift",
      "trigger": "Rose",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Main Scene",
      "obs_source": "Gift Animation",
      "duration": 5.0,
      "cooldown": 5.0,
      "enabled": true,
      "description": "Show gift animation when Rose received"
    }
  ]
}
```

### Option B: Using the GUI (Coming Soon)

Future versions will have GUI configuration for OBS settings.

## Step 3: Test the Connection

### Using Python:

```python
from obs_controller import OBSController

# Create controller
obs = OBSController(host="localhost", port=4455, password="your_password")

# Connect
if obs.connect():
    print("Connected!")

    # List scenes
    scenes = obs.get_scenes()
    print("Available scenes:", scenes)

    # List sources in first scene
    if scenes:
        sources = obs.get_sources_in_scene(scenes[0])
        print(f"Sources in {scenes[0]}:", sources)

    obs.disconnect()
else:
    print("Failed to connect")
```

---

## Method 2: Hotkey Integration (Works with TikTok Live Studio!)

This method works with **both OBS Studio and TikTok Live Studio** by triggering hotkeys you configure in your streaming software.

### Why Use Hotkeys?

✅ **Works with TikTok Live Studio** (which doesn't expose WebSocket)
✅ **Simpler setup** - no WebSocket configuration needed
✅ **More flexible** - can trigger ANY action you can assign to a hotkey
✅ **Reliable** - same method used by apps like TikFinity

### How It Works

1. You assign hotkeys in OBS/TikTok Live Studio (e.g., F13 = Show Follow Alert)
2. TikForever simulates pressing those keys when events happen
3. Your streaming software responds to the hotkey just like you pressed it

### Step 1: Set Up Hotkeys in TikTok Live Studio

#### For TikTok Live Studio:

1. Open **TikTok Live Studio**
2. Go to **Settings** → **Hotkeys**
3. Find "Show/Hide Source" or similar options
4. Assign function keys to sources:
   - **F13**: Show Follow Alert
   - **F14**: Show Gift Alert
   - **F15**: Show Share Alert
   - **F16**: Show Like Effect
   - etc.

**💡 Tip**: Use F13-F24 as they're rarely used by other applications.

#### For OBS Studio:

1. Open **OBS Studio**
2. Go to **Settings** → **Hotkeys**
3. Scroll to find your sources
4. Assign hotkeys to "Show" or "Toggle" for each source
5. Click **OK**

### Step 2: Configure TikForever

In the TikForever GUI:

1. Go to **Event Mappings** tab
2. Select **Action**: `obs_hotkey`
3. Enter the hotkey you configured (e.g., `f13`, `f14`)
4. Set your event, trigger, duration, and cooldown
5. Click **Add Mapping**

### Example: Follow Alert with Hotkey

**In TikTok Live Studio:**
- Assign F13 to show/hide your "Follow Alert" source

**In TikForever GUI:**
```
Event: follow
Trigger: (leave empty)
Action: obs_hotkey
Hotkey: f13
Duration: 0.1
Cooldown: 2.0
```

**Or in config.json:**
```json
{
  "event_type": "follow",
  "trigger": "",
  "action": "obs_hotkey",
  "obs_hotkey": "f13",
  "duration": 0.1,
  "cooldown": 2.0,
  "enabled": true,
  "description": "Show follow alert via F13 hotkey"
}
```

### Complete Hotkey Example

```json
{
  "tiktok_username": "your_username",
  "mappings": [
    {
      "event_type": "follow",
      "trigger": "",
      "action": "obs_hotkey",
      "obs_hotkey": "f13",
      "duration": 0.1,
      "cooldown": 2.0,
      "enabled": true,
      "description": "Follow alert"
    },
    {
      "event_type": "gift",
      "trigger": "Rose",
      "action": "obs_hotkey",
      "obs_hotkey": "f14",
      "duration": 0.1,
      "cooldown": 3.0,
      "enabled": true,
      "description": "Rose gift alert"
    },
    {
      "event_type": "share",
      "trigger": "",
      "action": "obs_hotkey",
      "obs_hotkey": "f15",
      "duration": 0.1,
      "cooldown": 3.0,
      "enabled": true,
      "description": "Share alert"
    }
  ]
}
```

### Hotkey Setup Tips

1. **Use F13-F24**: These function keys are rarely used and won't conflict
2. **Toggle vs Show**: Configure your hotkeys to toggle sources on/off
3. **Test First**: Test each hotkey manually before going live
4. **Keep a List**: Write down which F-key controls which source
5. **Duration**: Keep duration short (0.1s) - just long enough to trigger the hotkey

### Recommended Hotkey Mapping

| Event | Hotkey | Source in TikTok Live Studio |
|-------|--------|------------------------------|
| Follow | F13 | Follow Alert |
| Gift (Rose) | F14 | Small Gift Alert |
| Gift (TikTok) | F15 | Medium Gift Alert |
| Gift (Drama Queen) | F16 | Big Gift Alert |
| Share | F17 | Share Alert |
| Like | F18 | Like Effect |

---

## OBS Action Types (WebSocket Method Only)

**Note**: These action types only work with Method 1 (WebSocket/OBS Studio). For TikTok Live Studio, use Method 2 (Hotkeys).

TikForever supports several OBS actions via WebSocket:

### 1. `show` - Show a source
Shows a source permanently until hidden.

```json
{
  "action": "obs",
  "obs_action": "show",
  "obs_scene": "Main Scene",
  "obs_source": "Webcam"
}
```

### 2. `hide` - Hide a source
Hides a source.

```json
{
  "action": "obs",
  "obs_action": "hide",
  "obs_scene": "Main Scene",
  "obs_source": "Webcam"
}
```

### 3. `toggle` - Toggle source visibility
Toggles between shown and hidden.

```json
{
  "action": "obs",
  "obs_action": "toggle",
  "obs_scene": "Main Scene",
  "obs_source": "Background Music"
}
```

### 4. `show_temp` - Show temporarily
Shows a source for a duration, then hides it. **Perfect for alerts!**

```json
{
  "action": "obs",
  "obs_action": "show_temp",
  "obs_scene": "Main Scene",
  "obs_source": "Alert",
  "duration": 5.0
}
```

## Example Use Cases

### Example 1: Follow Alert

When someone follows, show an alert for 3 seconds:

```json
{
  "event_type": "follow",
  "trigger": "",
  "action": "obs",
  "obs_action": "show_temp",
  "obs_scene": "Main Scene",
  "obs_source": "Follow Alert",
  "duration": 3.0,
  "cooldown": 2.0,
  "enabled": true
}
```

### Example 2: Gift Animation

When someone sends a Rose gift, trigger an animation:

```json
{
  "event_type": "gift",
  "trigger": "Rose",
  "action": "obs",
  "obs_action": "show_temp",
  "obs_scene": "Main Scene",
  "obs_source": "Rose Animation",
  "duration": 5.0,
  "cooldown": 3.0,
  "enabled": true
}
```

### Example 3: Like Counter

When viewers send likes, toggle a special effect:

```json
{
  "event_type": "like",
  "trigger": "",
  "action": "obs",
  "obs_action": "toggle",
  "obs_scene": "Main Scene",
  "obs_source": "Sparkle Effect",
  "cooldown": 10.0,
  "enabled": true
}
```

## Setting Up Sources in OBS/TikTok Live Studio

### 1. Create Alert Images/Animations

Create your alert graphics:
- **Follow Alert**: PNG/GIF with transparent background
- **Gift Alerts**: Different animations for different gifts
- **Subscriber Alerts**: Special graphics

### 2. Add Sources to OBS

1. In your scene, click **+** (Add Source)
2. Choose **Image** or **Media Source**
3. Name it (e.g., "Follow Alert")
4. Select your image/video file
5. **Important**: Set visibility to **hidden** by default (click the eye icon)

### 3. Position and Style

- Resize and position the source
- Add filters (Color Correction, Chroma Key, etc.)
- Make sure the source name matches what's in your config

## Troubleshooting

### Connection Failed

**Problem**: Can't connect to OBS WebSocket

**Solutions**:
- ✅ Make sure OBS/TikTok Live Studio is running
- ✅ Check that WebSocket server is enabled in OBS settings
- ✅ Verify port number (default: 4455)
- ✅ Check password is correct
- ✅ Try without password first to test

### Source Not Found

**Problem**: "Source not found" error

**Solutions**:
- ✅ Check source name matches exactly (case-sensitive)
- ✅ Make sure source exists in the specified scene
- ✅ Use `obs.get_sources_in_scene()` to list available sources

### Source Doesn't Show

**Problem**: Action executes but source doesn't appear

**Solutions**:
- ✅ Check that source isn't already at 100% opacity
- ✅ Verify source is in the correct scene
- ✅ Make sure source layer order is correct (not behind other sources)
- ✅ Check source size isn't 0x0

### Actions Trigger Too Often

**Problem**: Alerts spam the screen

**Solutions**:
- ✅ Increase cooldown time
- ✅ Use `show_temp` instead of `show` for auto-hiding
- ✅ Add global cooldown in settings

## Advanced: Multiple Scenes

You can control sources across different scenes:

```json
{
  "event_type": "comment",
  "trigger": "scene1",
  "action": "obs",
  "obs_action": "show",
  "obs_scene": "Gaming Scene",
  "obs_source": "Camera",
  "enabled": true
}
```

## Tips for Best Results

1. **Use `show_temp` for alerts** - Auto-hides after duration
2. **Set reasonable cooldowns** - Prevent spam (2-10 seconds)
3. **Test before going live** - Make sure everything works
4. **Keep source names simple** - Easier to configure
5. **Use transparent PNGs** - Looks more professional
6. **Layer order matters** - Put alerts on top layers

## Need Help?

- Check the main [TROUBLESHOOTING.md](TROUBLESHOOTING.md) guide
- Verify OBS WebSocket is running: http://localhost:4455
- Check TikForever console for error messages
- Make sure OBS/TikTok Live Studio is running when connecting

## Example Complete Setup

Here's a complete config with keyboard + OBS actions:

```json
{
  "tiktok_username": "yourname",
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
      "key": "space",
      "duration": 0.1,
      "cooldown": 0.5,
      "enabled": true
    },
    {
      "event_type": "follow",
      "trigger": "",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Main Scene",
      "obs_source": "Follow Alert",
      "duration": 3.0,
      "cooldown": 2.0,
      "enabled": true
    },
    {
      "event_type": "gift",
      "trigger": "Rose",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Main Scene",
      "obs_source": "Gift Alert",
      "duration": 5.0,
      "cooldown": 5.0,
      "enabled": true
    }
  ]
}
```

---

## Which Method Should I Use?

### Use Method 2 (Hotkeys) if:
✅ You're using **TikTok Live Studio** (required)
✅ You want **easier setup**
✅ You want to trigger **any action** (scene switching, filters, etc.)
✅ You don't want to deal with WebSocket configuration

### Use Method 1 (WebSocket) if:
✅ You're using **OBS Studio** (not TikTok Live Studio)
✅ You want **fine-grained control** (show_temp with automatic hiding)
✅ You want to **query** scenes and sources programmatically
✅ You're comfortable with WebSocket setup

### Can I Use Both?
Yes! You can use both methods in the same configuration:
- Use `action: "obs"` for WebSocket control (OBS Studio)
- Use `action: "obs_hotkey"` for hotkey control (any software)

---

Now your stream is fully interactive with both game control and visual alerts! 🎮✨
