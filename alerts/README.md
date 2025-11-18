# TikForever Alerts Folder

This folder contains your alert media files (images, GIFs, videos) that will be displayed in your stream via Browser Source.

## Supported File Types

### Images
- **PNG** - Recommended for static images with transparency
- **GIF** - Animated images
- **JPG/JPEG** - Static images (no transparency)
- **WEBP** - Modern image format

### Videos
- **MP4** - Most compatible video format
- **WEBM** - Web-optimized video format
- **OGG** - Open video format

## File Organization

Organize your alerts by event type for easy reference:

```
alerts/
├── follow_alert.png
├── follow_alert.gif
├── rose_gift.gif
├── tiktok_gift.mp4
├── share_alert.png
├── like_effect.gif
└── README.md
```

## Recommended Specifications

### Images
- **Resolution**: 500x300 pixels (or similar aspect ratio)
- **File size**: Under 1 MB for best performance
- **Format**: PNG with transparency for best results

### Videos
- **Resolution**: 1920x1080 or 1280x720
- **Duration**: 2-5 seconds
- **File size**: Under 5 MB
- **Format**: MP4 (H.264 codec)

## Example Alert Configuration

In TikForever, configure your mappings like this:

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

## Where to Get Alert Assets

### Free Resources
- **Streamlabs**: https://streamlabs.com/library
- **Nerd or Die**: https://nerdordie.com/product-category/free-overlays/
- **OWN3D**: https://www.own3d.tv/en/products/category/free-overlays/
- **Placeit**: https://placeit.net/c/logos-graphics/stages/alerts
- **Giphy**: https://giphy.com/ (for animated GIFs)

### Create Your Own
- **Canva**: https://canva.com (free design tool)
- **Adobe Express**: https://www.adobe.com/express/
- **GIMP**: Free Photoshop alternative
- **DaVinci Resolve**: Free video editor

## Tips for Great Alerts

1. **Keep it short**: 2-5 seconds is ideal
2. **Use transparency**: PNG with transparent background looks professional
3. **Match your brand**: Use your stream colors and style
4. **Test first**: Always test alerts before going live
5. **Optimize size**: Smaller files load faster
6. **Don't overdo it**: Too many alerts can be distracting

## Testing Your Alerts

1. Start TikForever
2. Open browser to http://localhost:8000
3. Trigger test alerts from the GUI
4. Adjust timing and positioning as needed

## Browser Source Setup in TikTok Live Studio

1. Open TikTok Live Studio
2. Add Source → **Browser**
3. URL: `http://localhost:8000`
4. Width: `1920`, Height: `1080`
5. Check "Shutdown source when not visible" (optional)
6. Click **OK**

Your alerts will now appear in your stream!

## Troubleshooting

**Alert doesn't show?**
- Check the file exists in the alerts folder
- Check the filename matches exactly (case-sensitive)
- Check the browser source is added to TikTok Live Studio
- Check TikForever alert server is running (check Event Log)

**Alert too big/small?**
- Edit the CSS in the alert server settings
- Or resize your source images

**Alert lags?**
- Reduce file sizes (compress images/videos)
- Use lower resolution videos
- Close unnecessary browser tabs

**Alert doesn't auto-hide?**
- Check the duration setting in your mapping
- Increase the duration if needed

## Need Help?

Check the main TikForever documentation or open an issue on GitHub!
