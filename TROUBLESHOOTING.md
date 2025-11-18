# TikForever Troubleshooting Guide

## Events Not Triggering / Statistics Not Updating

If you're connected but not seeing events or statistics updating, try these steps:

### 1. Verify You're Actually Live

**IMPORTANT**: You must be **actively streaming live** on TikTok for events to work.

- The app connects to your live stream to receive events
- Simply opening the TikTok app is not enough
- You need to start an actual live broadcast

To test:
1. Open TikTok on your phone
2. Start a live stream
3. Keep the stream running
4. Then connect the TikForever app
5. Have someone (or use another device) send comments to your live stream

### 2. Check Connection Status

In the TikForever app:
- Status should say "Connected ✓" in green
- If it says "Disconnected" or "Connecting..." there's an issue

### 3. Verify Username is Correct

- Use your TikTok username WITHOUT the @ symbol
- Example: If your profile is @johndoe, enter just: `johndoe`
- Make sure there are no typos

### 4. Check Event Mappings

Go to the "Event Mappings" tab:
- Make sure you have mappings configured
- Check that mappings are "Enabled" (should say "Yes")
- Try simple commands like "jump" → "space"

### 5. Check Logs

Go to the "Event Log" tab:
- You should see a "Connected to..." message when connected
- When viewers send comments, you should see them appear here
- If you see comments but no actions, check your mappings

### 6. Enable Debug Logging

To see detailed logs in the console:

1. Run the app from command line:
   ```bash
   python main.py
   ```

2. Watch the terminal/console output for:
   - "Connected to @username's live stream!"
   - "Comment: username: text"
   - "Event matched mapping: trigger"
   - "Executed mapping for..."

If you see comments but no "Event matched mapping", your triggers don't match.

### 7. Common Mapping Issues

#### Comments Not Matching

The trigger text must match **exactly** (case-insensitive):

**Works:**
- Mapping trigger: "jump"
- Comment: "jump" ✓
- Comment: "JUMP" ✓
- Comment: "Jump" ✓
- Comment: "let's jump" ✓ (contains "jump")

**Doesn't Work:**
- Comment: "jmp" ✗
- Comment: "jumping" ✗
- Comment: "jumpp" ✗

**Solution**: Create multiple mappings for variations:
- "jump" → space
- "jumping" → space
- "jmp" → space

#### Keys Not Pressing

If you see "Executed mapping" but nothing happens in your game:

1. **Focus the game window**: Click on your game to make sure it's active
2. **Run as Administrator**: Right-click Python and "Run as Administrator"
3. **Check anti-cheat**: Some games block simulated inputs
4. **Test with Notepad**: Open Notepad and test if keys work there first

### 8. Test Input Simulation

Before going live, test if input simulation works:

**Test Keyboard:**
1. Open Notepad
2. Make sure Notepad window is focused (clicked)
3. Connect to your live
4. Post a comment that should trigger a key
5. You should see the key being typed in Notepad

**Test Controller:**
1. Open Windows Game Controller settings
2. You should see a "Virtual Xbox 360 Controller"
3. If not, install ViGEmBus (see SETUP_GUIDE.md)

### 9. Check Cooldowns

If actions work sometimes but not always:

- Check the "Cooldown" column in your mappings
- Cooldown prevents spam (e.g., 0.5 second cooldown = action can only trigger every 0.5s)
- If cooldown is too high, reduce it:
  - For movement: 0.1-0.3 seconds
  - For actions: 0.5-1.0 seconds
  - For special moves: 2-5 seconds

### 10. Connection Issues

**"Failed to connect" error:**
- Check your internet connection
- Make sure you're actually live on TikTok
- Try a different username format (with/without @)
- Your account might need to be public

**Disconnects randomly:**
- TikTok may have rate limits
- Try reconnecting
- Check your internet stability

### 11. Permissions Issues

**Windows 10/11:**
- Some games require Administrator privileges
- Right-click Python.exe → Run as Administrator
- Or run the command prompt as Admin first

**Antivirus:**
- Some antivirus software blocks input simulation
- Add TikForever folder to whitelist
- Temporarily disable to test

### 12. Still Not Working?

Enable maximum logging:

Edit your Python logging level in `main.py` line 24:
```python
logging.basicConfig(
    level=logging.DEBUG,  # Change INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

Then run from command line and watch for detailed logs.

## Common Scenarios

### Scenario 1: Connected but no events show up

**Cause**: You're not actually live on TikTok, or no one is interacting.

**Solution**:
1. Verify you started a live stream on TikTok
2. Send a test comment from another device/account
3. Check if the comment appears in the Event Log tab

### Scenario 2: Events show up but no game input

**Cause**:
- Game window not focused
- Mapping not configured correctly
- Keys not matching triggers

**Solution**:
1. Click on your game window to focus it
2. Check "Event Mappings" tab - verify triggers match
3. Test with Notepad first to verify keys work

### Scenario 3: Works for first few seconds then stops

**Cause**: Cooldowns are too high or global cooldown blocking all events.

**Solution**:
1. Reduce cooldown values in your mappings
2. Check `config.json` → `settings` → `global_cooldown` (should be 0.1 or less)

### Scenario 4: Some comments work, others don't

**Cause**: Trigger text doesn't match exactly.

**Solution**:
1. Go to Event Log and see the exact comment text
2. Make sure your mapping trigger matches exactly
3. Remember: triggers are case-insensitive but spelling must match

## Getting More Help

If you're still having issues:

1. Check the Event Log tab for any error messages
2. Run from command line to see console output
3. Try the CLI version: `python cli.py your_username`
4. Check GitHub issues page for similar problems
5. Post a new issue with:
   - Your console output
   - Event Log contents
   - Your configuration (config.json)
   - Description of what's not working

## Quick Checklist

Before reporting an issue, verify:

- [ ] I am actively live streaming on TikTok
- [ ] The app shows "Connected ✓" in green
- [ ] I have event mappings configured
- [ ] I've tested by sending a comment to my stream
- [ ] The comment appears in the Event Log
- [ ] My game window is focused (clicked on)
- [ ] I've tried running as Administrator
- [ ] My trigger text matches the comment exactly
- [ ] Cooldown is not too high
- [ ] I've tested with Notepad to verify keys work

If all of these are true and it still doesn't work, then there may be a bug. Please report it with details!
