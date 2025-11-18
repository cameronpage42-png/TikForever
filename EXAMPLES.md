# TikForever + TikTok Live Studio - Example Scenarios

This guide provides step-by-step examples of common setups using TikForever with TikTok Live Studio (or OBS).

## Table of Contents
1. [Scenario 1: Basic Follow Alert](#scenario-1-basic-follow-alert)
2. [Scenario 2: Multi-Gift Alert System](#scenario-2-multi-gift-alert-system)
3. [Scenario 3: Interactive Game Stream](#scenario-3-interactive-game-stream)
4. [Scenario 4: Engagement Overlay System](#scenario-4-engagement-overlay-system)
5. [Scenario 5: Thank You Message Rotation](#scenario-5-thank-you-message-rotation)

---

## Scenario 1: Basic Follow Alert

**Goal**: Show a "Thank You for Following!" graphic for 3 seconds whenever someone follows.

### Step 1: Create Your Alert Graphic

1. Create a PNG image (1920x1080 or smaller):
   - Text: "Thanks for Following!"
   - Add your branding
   - **Use transparent background** for best results

2. Save as `follow_alert.png`

### Step 2: Set Up in TikTok Live Studio

1. **Open TikTok Live Studio**
2. In your scene, click **+ (Add Source)**
3. Select **Image**
4. Name it: `Follow Alert`
5. **Browse** and select your `follow_alert.png`
6. Position it where you want (top center is popular)
7. Resize if needed
8. **IMPORTANT**: Click the **eye icon** to hide it by default

### Step 3: Enable OBS WebSocket

1. In TikTok Live Studio, go to **Settings** → **Advanced**
2. Find **WebSocket Server** settings
3. Enable it
4. Note the **port** (usually 4455)
5. Note the **password** (if set)

### Step 4: Configure TikForever

Edit your `config.json`:

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
      "event_type": "follow",
      "trigger": "",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Scene",
      "obs_source": "Follow Alert",
      "duration": 3.0,
      "cooldown": 2.0,
      "enabled": true,
      "description": "Show follow alert for 3 seconds"
    }
  ]
}
```

**Important**: Replace `"Scene"` with your actual scene name from TikTok Live Studio.

### Step 5: Test It

1. Run TikForever: `python main.py`
2. Connect to your TikTok username
3. Have a friend follow you (or use a test account)
4. Watch your alert appear for 3 seconds!

### Troubleshooting

- **Alert doesn't show?** Check that:
  - Scene name matches exactly (case-sensitive)
  - Source name is `Follow Alert` exactly
  - Source is hidden by default
  - OBS WebSocket is enabled

---

## Scenario 2: Multi-Gift Alert System

**Goal**: Show different animations based on which gift is received.

### Setup Overview

Different gifts trigger different alerts:
- 🌹 **Rose** (1 coin) → Small thank you (2 seconds)
- 💝 **TikTok** (1 coin) → Medium celebration (3 seconds)
- 🎁 **Gift Box** (5 coins) → Big animation (5 seconds)
- 👑 **Drama Queen** (5000 coins) → Epic full-screen effect (10 seconds)

### Step 1: Create Alert Graphics

Create 4 different images/GIFs:
1. `rose_alert.png` - Simple "Thanks!"
2. `tiktok_alert.gif` - Animated TikTok logo
3. `giftbox_alert.gif` - Box opening animation
4. `bigspender_alert.mp4` - Full screen fireworks

### Step 2: Add to TikTok Live Studio

For each alert:
1. Add as **Image** (PNG/GIF) or **Media Source** (MP4)
2. Name them:
   - `Rose Alert`
   - `TikTok Alert`
   - `Gift Box Alert`
   - `Big Spender Alert`
3. Position them appropriately
4. **Hide all by default**

### Step 3: Configure TikForever

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
      "event_type": "gift",
      "trigger": "Rose",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Scene",
      "obs_source": "Rose Alert",
      "duration": 2.0,
      "cooldown": 1.0,
      "enabled": true,
      "description": "Rose gift - small thanks"
    },
    {
      "event_type": "gift",
      "trigger": "TikTok",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Scene",
      "obs_source": "TikTok Alert",
      "duration": 3.0,
      "cooldown": 2.0,
      "enabled": true,
      "description": "TikTok gift - medium celebration"
    },
    {
      "event_type": "gift",
      "trigger": "Gift Box",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Scene",
      "obs_source": "Gift Box Alert",
      "duration": 5.0,
      "cooldown": 3.0,
      "enabled": true,
      "description": "Gift Box - big animation"
    },
    {
      "event_type": "gift",
      "trigger": "Drama Queen",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Scene",
      "obs_source": "Big Spender Alert",
      "duration": 10.0,
      "cooldown": 5.0,
      "enabled": true,
      "description": "Epic gift - full screen effect"
    }
  ]
}
```

### Pro Tips

- **Layer Order**: Put bigger alerts on higher layers
- **Cooldowns**: Prevent spam with longer cooldowns for expensive gifts
- **Gift Names**: Check exact names in TikTok (case-sensitive!)
- **Test**: Send yourself gifts from a test account first

---

## Scenario 3: Interactive Game Stream

**Goal**: Viewers control the game with comments AND get visual feedback with OBS alerts.

### The Setup

- **Comments** → Control game (keyboard/controller)
- **Follows/Gifts** → Trigger on-screen effects
- **Special comments** → Trigger both game action AND visual effect

### Example: Platformer Game

#### Step 1: Create Visual Effects

Create these sources in TikTok Live Studio:
1. `Power Up Effect` - Glowing animation
2. `Jump Boost` - Stars animation
3. `Speed Boost` - Speed lines
4. `Follow Alert` - Thank you graphic

### Step 2: Configuration

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
      "trigger": "left",
      "action": "keyboard",
      "key": "left",
      "duration": 0.2,
      "cooldown": 0.3,
      "enabled": true,
      "description": "Move left"
    },
    {
      "event_type": "comment",
      "trigger": "right",
      "action": "keyboard",
      "key": "right",
      "duration": 0.2,
      "cooldown": 0.3,
      "enabled": true,
      "description": "Move right"
    },
    {
      "event_type": "comment",
      "trigger": "jump",
      "action": "keyboard",
      "key": "space",
      "duration": 0.1,
      "cooldown": 0.5,
      "enabled": true,
      "description": "Jump"
    },
    {
      "event_type": "gift",
      "trigger": "Rose",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Gaming Scene",
      "obs_source": "Power Up Effect",
      "duration": 3.0,
      "cooldown": 2.0,
      "enabled": true,
      "description": "Rose = Power Up visual"
    },
    {
      "event_type": "follow",
      "trigger": "",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Gaming Scene",
      "obs_source": "Follow Alert",
      "duration": 3.0,
      "cooldown": 2.0,
      "enabled": true,
      "description": "Follow alert"
    }
  ]
}
```

### Step 3: Stream Setup

1. **Scene Layout**:
   ```
   ┌─────────────────────────────────┐
   │     [Follow Alert - Hidden]     │
   ├─────────────────────────────────┤
   │                                 │
   │      [Game Capture]             │
   │                                 │
   ├─────────────────────────────────┤
   │  [Webcam]  [Power Up - Hidden]  │
   └─────────────────────────────────┘
   ```

2. **Start Stream**:
   - Start TikTok Live Studio streaming
   - Run TikForever and connect
   - Start your game
   - Tell viewers the commands!

### Chat Commands to Announce

```
🎮 CONTROL THE GAME! 🎮
Type: left, right, jump
🎁 Send gifts for effects!
❤️ Follow for a surprise!
```

---

## Scenario 4: Engagement Overlay System

**Goal**: Show running counters and effects based on total engagement.

### The Concept

Track engagement with visual feedback:
- Every **10 likes** → Show sparkle effect
- Every **follow** → Add to follower count display
- Every **100 total events** → Special celebration

### Step 1: Create Overlays

In TikTok Live Studio, create:
1. `Sparkle Effect` - Particle animation
2. `Milestone Alert` - "100 Events!" graphic
3. `Engagement Bar` - Progress bar image

### Step 2: Configuration

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
      "event_type": "like",
      "trigger": "",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Main Scene",
      "obs_source": "Sparkle Effect",
      "duration": 2.0,
      "cooldown": 10.0,
      "enabled": true,
      "description": "Sparkles on likes (max once per 10s)"
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
      "enabled": true,
      "description": "Follow alert"
    },
    {
      "event_type": "share",
      "trigger": "",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Main Scene",
      "obs_source": "Share Alert",
      "duration": 4.0,
      "cooldown": 3.0,
      "enabled": true,
      "description": "Thanks for sharing"
    }
  ]
}
```

### Pro Tips

- **Long Cooldowns**: Use 10+ second cooldowns for like events (they spam!)
- **Layer Effects**: Stack multiple effects on different layers
- **Counters**: TikForever tracks stats - use them to announce milestones

---

## Scenario 5: Thank You Message Rotation

**Goal**: Show different thank you messages randomly for gifts/follows.

### The Setup

Create multiple variations of thank you graphics:
1. `Thanks 1` - Rainbow theme
2. `Thanks 2` - Stars theme
3. `Thanks 3` - Hearts theme
4. `Thanks 4` - Fireworks theme

### Configuration Strategy

Use multiple mappings for the same event:

```json
{
  "mappings": [
    {
      "event_type": "follow",
      "trigger": "",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Scene",
      "obs_source": "Thanks 1",
      "duration": 3.0,
      "cooldown": 12.0,
      "enabled": true,
      "description": "Follow - Thanks variant 1"
    },
    {
      "event_type": "follow",
      "trigger": "",
      "action": "obs",
      "obs_action": "show_temp",
      "obs_scene": "Scene",
      "obs_source": "Thanks 2",
      "duration": 3.0,
      "cooldown": 12.0,
      "enabled": true,
      "description": "Follow - Thanks variant 2"
    }
  ]
}
```

**Note**: TikForever triggers the **first match** only, so you'll need to manually enable/disable variants or use different cooldown times.

**Better Approach**: Use one source and change the image file periodically.

---

## Common Configuration Patterns

### Pattern 1: Tiered Engagement

Small → Medium → Large reactions:

```json
{
  "mappings": [
    {
      "event_type": "like",
      "action": "obs",
      "obs_source": "Small Effect",
      "duration": 1.0,
      "cooldown": 30.0
    },
    {
      "event_type": "follow",
      "action": "obs",
      "obs_source": "Medium Effect",
      "duration": 3.0,
      "cooldown": 5.0
    },
    {
      "event_type": "gift",
      "trigger": "Drama Queen",
      "action": "obs",
      "obs_source": "Epic Effect",
      "duration": 10.0,
      "cooldown": 10.0
    }
  ]
}
```

### Pattern 2: Combined Actions

Game control + Visual feedback:

**Option A**: Separate mappings
```json
[
  {
    "event_type": "comment",
    "trigger": "power",
    "action": "keyboard",
    "key": "p"
  },
  {
    "event_type": "gift",
    "trigger": "Rose",
    "action": "obs",
    "obs_source": "Power Effect"
  }
]
```

**Option B**: Use gifts for special visual-only events

### Pattern 3: Scene-Specific Alerts

Different alerts for different scenes:

```json
[
  {
    "event_type": "follow",
    "action": "obs",
    "obs_scene": "Gaming Scene",
    "obs_source": "Gaming Follow Alert"
  },
  {
    "event_type": "follow",
    "action": "obs",
    "obs_scene": "Talking Scene",
    "obs_source": "Talking Follow Alert"
  }
]
```

---

## Testing Your Setup

### Before Going Live

1. **Connect TikForever** (not live yet)
2. **Test OBS connection**:
   ```python
   from obs_controller import OBSController
   obs = OBSController("localhost", 4455, "")
   obs.connect()
   obs.show_source_temporarily("Scene", "Follow Alert", 3.0)
   ```

3. **Test with dummy account**:
   - Go live on TikTok
   - Use another device/account
   - Send test comments/gifts
   - Verify alerts trigger

4. **Check timings**:
   - Alerts should appear/disappear smoothly
   - No lag or stuttering
   - Proper layer order

### During Stream

Monitor TikForever console for:
- `Comment: user: text` - Events being received ✅
- `Event matched mapping: X` - Mappings triggering ✅
- `Executed mapping for user` - Actions executed ✅
- `Source 'X' shown in scene 'Y'` - OBS commands sent ✅

---

## Quick Reference: Common Gift Names

Make sure you use the exact names (case-sensitive):

- `Rose` - 1 coin
- `TikTok` - 1 coin
- `Finger Heart` - 5 coins
- `Perfume` - 20 coins
- `Hand Heart` - 25 coins
- `Confetti` - 100 coins
- `Gift Box` - 100 coins
- `Drama Queen` - 5000 coins
- `Lion` - 29,999 coins

**Tip**: Check the exact spelling in TikTok Live by looking at the gift menu!

---

## Best Practices

### Do's ✅

- **Test before going live** - Always test your setup
- **Use reasonable cooldowns** - Prevent spam (2-10 seconds)
- **Hide sources by default** - Let TikForever control visibility
- **Keep alerts brief** - 2-5 seconds is ideal
- **Use transparent PNGs** - Looks more professional
- **Layer properly** - Alerts should be on top
- **Save configs** - Backup your config.json

### Don'ts ❌

- **Don't spam viewers** - Use cooldowns liberally
- **Don't block gameplay** - Position alerts carefully
- **Don't use huge files** - Keep images/videos optimized
- **Don't forget to test** - Murphy's law applies to streaming
- **Don't use too many alerts** - Keep it simple and clean

---

## Need Help?

- Check [OBS_SETUP.md](OBS_SETUP.md) for detailed OBS WebSocket setup
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Review the Event Log in TikForever to see what's happening

Happy Streaming! 🎮📺✨
