# Browser Source Alert Setup for TikTok Live Studio

## 🎉 The BEST Way to Add Alerts to TikTok Live Studio!

Browser Source alerts are the **recommended method** for adding professional-looking alerts to your TikTok Live streams. This is how major streamers and apps like StreamElements/Streamlabs work!

### Why Browser Source?

✅ **Works perfectly with TikTok Live Studio**
✅ **Professional animated alerts** with images, GIFs, and videos
✅ **Easy setup** - just add a browser source
✅ **No hotkey configuration needed**
✅ **Fully customizable** with HTML/CSS
✅ **Multiple alerts at once**
✅ **Smooth animations** and transitions

---

## How It Works

1. **TikForever runs a local web server** at `http://localhost:8000`
2. **You add a Browser Source** in TikTok Live Studio pointing to that URL
3. **When events happen** (follow, gift, share, etc.), TikForever sends the alert to the web page
4. **The alert appears** on your stream with beautiful animations!

---

## Quick Start Guide

### Step 1: Set Up Your Alerts Folder

1. Open the `alerts` folder in your TikForever directory
2. Add your alert images/videos:
   - `follow_alert.png` or `follow_alert.gif` - Follow notification
   - `rose_gift.gif` - Rose gift animation
   - `share_alert.png` - Share thank you
   - `like_effect.gif` - Like sparkles
   - etc.

**Tips:**
- Use **PNG** with transparency for best results
- **GIF** for animations
- **MP4** for video alerts
- Keep files under 1-5 MB for best performance

### Step 2: Configure TikForever

#### Using the GUI (Easiest):

1. Open **TikForever**
2. Go to **Event Mappings** tab
3. Select **Action**: `browser_source`
4. Configure your alert:
   - **Alert Type**: `follow`, `gift`, `share`, `like`, or `comment`
   - **Message**: Custom message (leave empty for default)
   - **Media File**: Filename from `alerts` folder (e.g., `follow_alert.gif`)
   - **Duration**: How long to show (e.g., 3.0 seconds)
   - **Cooldown**: Minimum time between alerts (e.g., 2.0 seconds)
5. Click **Add Mapping**
6. Click **Save Mappings**

#### Using config.json:

```json
{
  "event_type": "follow",
  "trigger": "",
  "action": "browser_source",
  "alert_type": "follow",
  "alert_message": "Thanks for following!",
  "media_file": "follow_alert.gif",
  "duration": 3.0,
  "cooldown": 2.0,
  "enabled": true
}
```

### Step 3: Add Browser Source to TikTok Live Studio

1. Open **TikTok Live Studio**
2. In the **Sources** panel, click the **+** button
3. Select **Browser**
4. Name it: `TikForever Alerts`
5. Enter URL: `http://localhost:8000`
6. Set dimensions:
   - **Width**: `1920`
   - **Height**: `1080`
7. *(Optional)* Check "Shutdown source when not visible" to save resources
8. Click **OK**

**Important**: Make sure TikForever is running BEFORE you go live!

### Step 4: Position and Test

1. **Position the source**: The alerts appear in the top-right corner by default
2. **Test it**:
   - Keep TikTok Live Studio open (don't go live yet)
   - Connect to your TikTok account in TikForever
   - Have a friend comment/follow to test
   - OR use a test account
3. **Adjust**: If needed, resize or reposition the browser source
4. **Go Live!** 🚀

---

## Example Configurations

### Basic Follow Alert

```json
{
  "event_type": "follow",
  "trigger": "",
  "action": "browser_source",
  "alert_type": "follow",
  "alert_message": "Thanks for following!",
  "media_file": "follow_alert.gif",
  "duration": 3.0,
  "cooldown": 2.0,
  "enabled": true,
  "description": "Show follow alert with GIF"
}
```

### Gift Alert (Rose)

```json
{
  "event_type": "gift",
  "trigger": "Rose",
  "action": "browser_source",
  "alert_type": "gift",
  "alert_message": "",
  "media_file": "rose_gift.gif",
  "duration": 4.0,
  "cooldown": 3.0,
  "enabled": true,
  "description": "Rose gift alert - auto message"
}
```

**Note**: Empty `alert_message` uses a default message like "Thanks for Rose!"

### Share Alert (No Media)

```json
{
  "event_type": "share",
  "trigger": "",
  "action": "browser_source",
  "alert_type": "share",
  "alert_message": "Thanks for sharing! 📤",
  "media_file": null,
  "duration": 3.0,
  "cooldown": 3.0,
  "enabled": true,
  "description": "Share alert - text only"
}
```

### Video Alert

```json
{
  "event_type": "gift",
  "trigger": "TikTok",
  "action": "browser_source",
  "alert_type": "gift",
  "alert_message": "WOW! Big gift!",
  "media_file": "big_gift_celebration.mp4",
  "duration": 5.0,
  "cooldown": 5.0,
  "enabled": true,
  "description": "Big gift video alert"
}
```

---

## Complete Setup Example

Let's set up a full alert system for your stream:

### 1. Prepare Alert Files

Place these in the `alerts` folder:
- `follow_alert.gif` - Animated follow notification
- `rose_gift.gif` - Small gift animation
- `tiktok_gift.mp4` - Big gift celebration video
- `share_alert.png` - Share thank you graphic

### 2. Configure in TikForever

Add these mappings in the GUI or config.json:

```json
{
  "mappings": [
    {
      "event_type": "comment",
      "trigger": "jump",
      "action": "keyboard",
      "key": "space",
      "duration": 0.1,
      "cooldown": 0.5,
      "enabled": true,
      "description": "Game control - jump"
    },
    {
      "event_type": "follow",
      "trigger": "",
      "action": "browser_source",
      "alert_type": "follow",
      "alert_message": "New Follower! Thanks!",
      "media_file": "follow_alert.gif",
      "duration": 3.0,
      "cooldown": 2.0,
      "enabled": true,
      "description": "Follow alert"
    },
    {
      "event_type": "gift",
      "trigger": "Rose",
      "action": "browser_source",
      "alert_type": "gift",
      "alert_message": "",
      "media_file": "rose_gift.gif",
      "duration": 3.0,
      "cooldown": 3.0,
      "enabled": true,
      "description": "Rose gift alert"
    },
    {
      "event_type": "gift",
      "trigger": "TikTok",
      "action": "browser_source",
      "alert_type": "gift",
      "alert_message": "🎉 EPIC GIFT! 🎉",
      "media_file": "tiktok_gift.mp4",
      "duration": 5.0,
      "cooldown": 5.0,
      "enabled": true,
      "description": "Big gift alert"
    },
    {
      "event_type": "share",
      "trigger": "",
      "action": "browser_source",
      "alert_type": "share",
      "alert_message": "Thanks for sharing! 📤",
      "media_file": "share_alert.png",
      "duration": 3.0,
      "cooldown": 3.0,
      "enabled": true,
      "description": "Share alert"
    }
  ]
}
```

### 3. Start Streaming

1. **Launch TikForever** - Alert server starts automatically at `http://localhost:8000`
2. **Open TikTok Live Studio**
3. **Add Browser Source** (see Step 3 above)
4. **Connect to TikTok** in TikForever
5. **Test alerts** with a friend before going live
6. **Go Live!**

---

## Advanced Customization

### Customizing Alert Appearance

The alerts are fully customizable via HTML/CSS. If you're comfortable with web development, you can edit `alert_server.py` to modify:

- **Alert position** (default: top-right)
- **Colors and gradients**
- **Animation style**
- **Font and text styling**
- **Alert size**

### Testing Alerts

To test alerts without going live:

1. Keep TikTok Live Studio open
2. Open a browser to `http://localhost:8000`
3. Open browser console (F12)
4. Run: `testAlert()` to trigger a test alert

### Multiple Simultaneous Alerts

The system supports multiple alerts showing at once. They will stack vertically in the top-right corner.

### Alert Duration Tips

- **Follow/Like**: 2-3 seconds
- **Small Gifts**: 3-4 seconds
- **Big Gifts**: 5-6 seconds
- **Shares**: 3 seconds

Longer durations can cause alerts to overlap if many events happen quickly.

---

## Troubleshooting

### Alert Doesn't Appear

✅ **Check TikForever is running** - Alert server must be running
✅ **Check browser source URL** - Must be exactly `http://localhost:8000`
✅ **Check browser source is visible** - Not hidden or behind other sources
✅ **Check mapping is enabled** - Look at Event Mappings tab
✅ **Check cooldown hasn't triggered** - Wait for cooldown period

### Alert Shows Wrong Image

✅ **Check filename matches exactly** - Case-sensitive! `Follow_Alert.gif` ≠ `follow_alert.gif`
✅ **Check file is in alerts folder** - Must be in the `alerts` directory
✅ **Check file format is supported** - PNG, GIF, JPG, MP4, WEBM

### Alert Lags or Stutters

✅ **Reduce file sizes** - Compress images/videos
✅ **Use lower resolution** - 500x300 instead of 1920x1080
✅ **Close unnecessary apps** - Free up system resources
✅ **Use GIF instead of video** - GIFs are lighter

### Browser Source Shows Black Screen

✅ **Make sure TikForever is running first**
✅ **Try refreshing the browser source** - Right-click → Refresh
✅ **Check Windows Firewall** - Allow localhost connections
✅ **Try opening http://localhost:8000 in your regular browser** - Should show the alert overlay

### Alert Stays On Screen

✅ **Check duration setting** - Should be 2-5 seconds, not 20-50
✅ **Refresh the browser source** - Right-click → Refresh
✅ **Restart TikForever**

---

## Where to Get Alert Assets

### Free Resources
- **StreamElements**: https://streamelements.com/dashboard/overlays/gallery
- **Nerd or Die**: https://nerdordie.com/product-category/free-overlays/
- **OWN3D**: https://www.own3d.tv/en/products/category/free-overlays/
- **Streamlabs**: https://streamlabs.com/library
- **Giphy**: https://giphy.com/ (animated GIFs)

### Create Your Own
- **Canva**: https://canva.com (free design tool)
- **Adobe Express**: https://www.adobe.com/express/
- **GIMP**: Free Photoshop alternative
- **Figma**: Free design tool

### Premium Resources
- **Placeit**: https://placeit.net/
- **Envato**: https://elements.envato.com/
- **Fiverr**: Hire designers to create custom alerts

---

## Comparison: Browser Source vs Hotkeys vs WebSocket

| Feature | Browser Source ⭐ | Hotkeys | WebSocket (OBS) |
|---------|------------------|---------|-----------------|
| Works with TikTok Live Studio | ✅ Yes | ✅ Yes | ❌ No (OBS only) |
| Professional animations | ✅ Yes | ❌ Limited | ✅ Yes |
| Easy setup | ✅ Very easy | ⚠️ Moderate | ⚠️ Moderate |
| Custom styling | ✅ Full control | ❌ No | ⚠️ Limited |
| Multiple alerts at once | ✅ Yes | ❌ No | ✅ Yes |
| Auto-hide alerts | ✅ Yes | ⚠️ Manual | ✅ Yes |
| Images/Videos | ✅ Yes | ❌ No | ⚠️ Limited |

**Recommendation**: Use **Browser Source** for TikTok Live Studio! It's the best option.

---

## Tips for Great Alerts

1. **Keep it short** - 2-4 seconds is perfect
2. **Use transparency** - PNG with transparent background looks professional
3. **Match your brand** - Use your stream colors and theme
4. **Don't overdo it** - Too many alerts become distracting
5. **Test before going live** - Always test with a friend first
6. **Optimize file sizes** - Smaller = faster = smoother
7. **Use sound sparingly** - (Future feature) Don't annoy viewers

---

## Next Steps

- ✅ Set up your alerts folder
- ✅ Configure your mappings
- ✅ Add browser source to TikTok Live Studio
- ✅ Test everything
- ✅ Customize alert appearance (optional)
- ✅ Go live and engage your audience!

For more help, check:
- [EXAMPLES.md](EXAMPLES.md) - More usage examples
- [OBS_SETUP.md](OBS_SETUP.md) - OBS WebSocket and hotkey methods
- [alerts/README.md](alerts/README.md) - Alert asset specifications

Happy Streaming! 🎮📺✨
