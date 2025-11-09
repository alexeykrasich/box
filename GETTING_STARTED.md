# Getting Started with Automation Control System

This guide will walk you through setting up and using your automation system for the first time.

## Prerequisites

### For Server
- Python 3.7 or higher
- pip (Python package manager)

### For Android App
- Android Studio (latest version)
- Android device or emulator (API 24+)

## Step-by-Step Setup

### Part 1: Server Setup (5 minutes)

#### 1. Navigate to the project directory
```bash
cd /path/to/automation-control-system
```

#### 2. Install Python dependencies
```bash
cd server
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-3.0.0 Flask-CORS-4.0.0 Flask-SocketIO-5.3.5 ...
```

#### 3. Test the server components (optional but recommended)
```bash
python test_server.py
```

**Expected output:**
```
✅ All tests passed! Server is ready to run.
```

#### 4. Start the server
```bash
python app.py
```

**Expected output:**
```
Starting Automation Server...
 * Running on http://0.0.0.0:5000
```

**✅ Server is now running!** Keep this terminal open.

### Part 2: Android App Setup (10 minutes)

#### 1. Open Android Studio
- Launch Android Studio
- Click "Open an Existing Project"
- Navigate to the `android` folder in your project
- Click "OK"

#### 2. Wait for Gradle sync
- Android Studio will automatically sync Gradle
- This may take a few minutes on first run
- Wait for "Gradle sync finished" message

#### 3. Configure an Android device

**Option A: Use an Emulator**
- Click "Device Manager" in Android Studio
- Click "Create Device"
- Select a device (e.g., Pixel 5)
- Select a system image (API 24 or higher)
- Click "Finish"

**Option B: Use a Real Device**
- Enable Developer Options on your Android phone
- Enable USB Debugging
- Connect phone via USB
- Accept debugging prompt on phone

#### 4. Run the app
- Click the green "Run" button (▶️) in Android Studio
- Select your device/emulator
- Wait for app to build and install

**✅ App is now installed!**

### Part 3: Configure the App (2 minutes)

#### 1. Find your server IP address

**For Emulator:**
- Use: `http://10.0.2.2:5000/`
- This is a special address that points to your computer's localhost

**For Real Device:**
- Find your computer's IP address:
  - **Windows**: Open Command Prompt, type `ipconfig`, look for "IPv4 Address"
  - **Mac**: Open Terminal, type `ifconfig | grep inet`, look for your local IP
  - **Linux**: Open Terminal, type `ip addr`, look for your local IP
- Use: `http://YOUR_IP:5000/` (e.g., `http://192.168.1.100:5000/`)

#### 2. Configure the app
1. Open the app on your device
2. Tap the menu icon (⋮) in the top right
3. Tap "Settings"
4. Enter your server URL
5. Tap "Save Settings"

#### 3. Test the connection
1. Go back to the main screen
2. Tap the refresh icon
3. If connected, you should see an empty list (no errors)

**✅ App is now connected to the server!**

### Part 4: Create Your First Automation (3 minutes)

#### 1. Add a News Monitor automation
1. Tap the **+** (plus) button at the bottom right
2. Select "News Monitor" from the list
3. You'll see a new card appear with status "STOPPED"

#### 2. Configure the automation
1. Tap the "Config" button on the News Monitor card
2. Fill in the fields:
   - **News Website URL**: `https://news.ycombinator.com`
   - **Keywords**: `python, automation` (optional)
   - **Check Interval**: `60` (check every 60 seconds)
3. Tap "Start Automation"

#### 3. Monitor the automation
1. You'll be taken back to the main screen
2. The status should change to "RUNNING" (in green)
3. Check your server terminal - you should see log messages

**✅ Your first automation is running!**

### Part 5: Explore Features (5 minutes)

#### Try the Ticket Buyer automation
1. Tap **+** to add another automation
2. Select "Ticket Buyer"
3. Tap "Config" and fill in:
   - **Travel Date**: Select tomorrow's date
   - **Earliest Departure Time**: `08:00`
   - **Latest Departure Time**: `18:00`
   - **From Station**: `New York`
   - **To Station**: `Boston`
   - **Check Interval**: `300`
4. Tap "Start Automation"

#### Stop an automation
1. Tap the "Stop" button on any running automation
2. Status changes to "STOPPED"
3. Check server logs - you'll see "stopped" message

#### Delete an automation
1. Make sure automation is stopped
2. Tap the "Delete" button
3. Confirm deletion
4. Automation is removed from the list

## Troubleshooting

### Server Issues

**Problem: "ModuleNotFoundError: No module named 'flask'"**
- Solution: Install dependencies with `pip install -r requirements.txt`

**Problem: "Address already in use"**
- Solution: Port 5000 is already in use. Either:
  - Stop the other application using port 5000
  - Change the port in `server/app.py` (last line)

**Problem: Server starts but no output**
- Solution: This is normal. The server is waiting for connections.

### Android App Issues

**Problem: "Failed to load automations"**
- Check server is running
- Verify server URL in Settings
- Make sure phone and computer are on same WiFi network (for real device)
- Check firewall isn't blocking port 5000

**Problem: "Gradle sync failed"**
- Click "File" → "Invalidate Caches / Restart"
- Make sure you have internet connection
- Update Android Studio to latest version

**Problem: App crashes on startup**
- Check Android Studio's Logcat for error messages
- Make sure you're using API 24 or higher
- Try cleaning and rebuilding: "Build" → "Clean Project" → "Rebuild Project"

### Connection Issues

**Problem: WebSocket not connecting**
- Make sure server URL ends with `/` (e.g., `http://10.0.2.2:5000/`)
- Restart the app after changing settings
- Check server logs for connection attempts

**Problem: Can't connect from real device**
- Make sure phone and computer are on same WiFi network
- Disable firewall temporarily to test
- Try pinging your computer from phone (use a network tool app)

## Next Steps

### 1. Customize Existing Automations
- Edit `server/automations/ticket_buyer.py` to add real ticket API
- Edit `server/automations/news_monitor.py` to add email notifications

### 2. Create Your Own Automation
- Copy `server/automations/example_template.py`
- Rename and modify it
- Add to `server/automations/__init__.py`
- Restart server
- Your automation appears in the app!

### 3. Explore Examples
- Check `EXAMPLES.md` for more automation ideas:
  - Price Tracker
  - Uptime Monitor
  - Social Media Monitor
  - File Backup Monitor

### 4. Read the Documentation
- **README.md** - Complete documentation
- **ARCHITECTURE.md** - How the system works
- **PROJECT_SUMMARY.md** - Quick overview

## Tips for Success

1. **Start Simple**: Begin with the example automations before creating your own
2. **Check Logs**: Always monitor the server terminal for errors and status
3. **Test Incrementally**: Test each automation individually before running multiple
4. **Use Short Intervals**: For testing, use short check intervals (30-60 seconds)
5. **Stop Before Delete**: Always stop automations before deleting them

## Common Workflows

### Daily Use
1. Open app
2. Tap refresh to see current status
3. Start/stop automations as needed
4. Check server logs for detailed information

### Adding New Automation Type
1. Create Python file in `server/automations/`
2. Implement the 4 required methods
3. Register in `__init__.py`
4. Restart server
5. Refresh app - new type appears!

### Debugging Issues
1. Check server terminal for errors
2. Look at automation status in app
3. Check error messages in red text
4. Stop and restart the automation
5. Check configuration values

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review the server logs for error messages
3. Check Android Studio's Logcat for app errors
4. Verify all configuration values are correct
5. Try restarting both server and app

## Success Checklist

- [ ] Server starts without errors
- [ ] Android app builds and installs
- [ ] App connects to server (no connection errors)
- [ ] Can create an automation
- [ ] Can configure and start an automation
- [ ] Can see status updates in real-time
- [ ] Can stop an automation
- [ ] Can delete an automation

**If you've checked all these boxes, you're ready to start automating!** 🎉

---

**Happy Automating!** For more information, see README.md and other documentation files.

