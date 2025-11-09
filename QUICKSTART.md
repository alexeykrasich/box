# Quick Start Guide

Get your automation system up and running in 5 minutes!

## Step 1: Start the Server (2 minutes)

### Option A: Using the launcher script
```bash
python main.py
```

### Option B: Manual start
```bash
cd server
pip install -r requirements.txt
python app.py
```

The server will start on `http://0.0.0.0:5000`

## Step 2: Build the Android App (2 minutes)

1. Open Android Studio
2. Click "Open an Existing Project"
3. Navigate to the `android` folder in this project
4. Wait for Gradle sync to complete
5. Click the "Run" button (green play icon)

## Step 3: Configure the App (1 minute)

1. Open the app on your device/emulator
2. Tap the menu icon (three dots) → Settings
3. Enter your server URL:
   - **For Android Emulator**: `http://10.0.2.2:5000/`
   - **For Real Device**: `http://YOUR_COMPUTER_IP:5000/`
     - Find your IP: 
       - Windows: `ipconfig` (look for IPv4 Address)
       - Mac/Linux: `ifconfig` or `ip addr` (look for inet)
4. Tap "Save Settings"

## Step 4: Create Your First Automation

1. Tap the **+** (plus) button
2. Select "Ticket Buyer" or "News Monitor"
3. Tap "Config" on the created automation
4. Fill in the configuration:
   
   **For Ticket Buyer**:
   - Travel Date: Select a date
   - Earliest/Latest Departure Time: Set time range
   - From/To Station: Enter station names
   - Check Interval: How often to check (in seconds)
   
   **For News Monitor**:
   - News Website URL: Enter a URL to monitor
   - Keywords: Optional keywords to watch for
   - Check Interval: How often to check (in seconds)

5. Tap "Start Automation"

## Step 5: Monitor Your Automation

- The automation card will show status: **RUNNING**
- Status updates in real-time via WebSocket
- Tap "Stop" to stop the automation
- Tap "Delete" to remove it

## Next Steps

### Add Your Own Automation

1. Copy `server/automations/example_template.py` to a new file
2. Modify the class and implement your logic
3. Add it to `server/automations/__init__.py`
4. Restart the server
5. Your new automation appears in the app!

### Customize Existing Automations

Edit the automation files in `server/automations/`:
- `ticket_buyer.py` - Add your actual ticket API integration
- `news_monitor.py` - Customize notification methods

## Troubleshooting

**App can't connect to server?**
- Make sure server is running
- Check the server URL in app settings
- For emulator, use `10.0.2.2` not `localhost`
- For real device, make sure phone and computer are on same network
- Check firewall settings

**Automation not working?**
- Check server console for error messages
- Make sure all required fields are filled
- Look at the error message in the app

**WebSocket not connecting?**
- Verify server URL format: `http://IP:5000/` (with trailing slash)
- Restart the app after changing settings

## Tips

- Use the refresh button to manually update automation list
- Automations keep running even if you close the app
- Stop automations before deleting them
- Check server console for detailed logs

## Example Use Cases

1. **Ticket Monitoring**: Set it up before tickets go on sale, let it monitor 24/7
2. **News Alerts**: Monitor news sites for breaking news or specific topics
3. **Price Tracking**: Create automation to monitor product prices
4. **Website Uptime**: Monitor if your website is accessible
5. **Social Media**: Track mentions or new posts

Happy Automating! 🚀

