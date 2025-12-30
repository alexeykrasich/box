# ❓ Frequently Asked Questions (FAQ)

## General Questions

### What is this project?
An automation control system that lets you manage various automation tasks from your Android phone. It consists of a Python Flask server that runs automations and a Kotlin Android app for control.

### What can I automate?
Anything you can code in Python! Examples include:
- Monitoring ticket availability
- Tracking news websites
- Monitoring prices
- Checking website uptime
- Social media monitoring
- File backups
- And much more!

### Do I need programming experience?
- **To use existing automations**: No
- **To create new automations**: Basic Python knowledge helpful
- **To modify the app**: Kotlin/Android knowledge needed

### Is this production-ready?
No, this is designed for personal use and testing. It lacks authentication, uses HTTP (not HTTPS), and has no persistence. See [ARCHITECTURE.md](ARCHITECTURE.md#security-considerations) for production recommendations.

## Setup Questions

### What do I need to get started?
- Python 3.7+ installed
- Android Studio (for building the app)
- Android device or emulator (API 24+)
- Same WiFi network (for real device)

### How long does setup take?
- Quick setup: 5 minutes (if experienced)
- Full setup: 20 minutes (first time)
- See [QUICKSTART.md](QUICKSTART.md) or [GETTING_STARTED.md](GETTING_STARTED.md)

### Can I use this on iOS?
Not currently. The client is Android-only. However, you could:
- Build a web interface
- Create an iOS app using the same REST API
- Use the API directly from any HTTP client

### Do I need to keep my computer running?
Yes, the Flask server must run on your computer. The automations execute on the server, not on your phone.

## Connection Questions

### What URL should I use in the Android app?

**For Android Emulator:**
```
http://10.0.2.2:5000/
```

**For Real Android Device:**
```
http://YOUR_COMPUTER_IP:5000/
```

Find your computer's IP:
- Windows: `ipconfig` → IPv4 Address
- Mac: `ifconfig | grep inet`
- Linux: `ip addr`

### Why can't the app connect to the server?

Common causes:
1. **Server not running** - Check terminal
2. **Wrong URL** - Verify IP address and port
3. **Different networks** - Phone and computer must be on same WiFi
4. **Firewall blocking** - Allow port 5000
5. **Missing trailing slash** - URL should end with `/`

### How do I know if the server is running?

You should see:
```
Starting Automation Server...
 * Running on http://0.0.0.0:5000
```

If you see errors, check that dependencies are installed.

### Can I access the server from outside my network?

Not by default. You would need to:
1. Set up port forwarding on your router
2. Use a VPN
3. Deploy to a cloud server
4. Add authentication and HTTPS first!

## Usage Questions

### How many automations can I run at once?

The system can handle 10-20 concurrent automations comfortably. Each runs in its own thread. Performance depends on:
- What the automations do
- Your computer's resources
- Network bandwidth

### Do automations keep running if I close the app?

Yes! Automations run on the server, not the phone. The app is just a remote control. You can:
- Close the app
- Turn off your phone
- Automations keep running on the server

### How do I stop all automations quickly?

Currently, you need to stop each one individually in the app. Or:
- Restart the server (stops all)
- Add a "Stop All" feature (requires code modification)

### Can I schedule automations to start/stop at specific times?

Not built-in currently, but you can:
- Add scheduling logic to your automation's `run()` method
- Use Python's `schedule` library
- Implement a scheduling feature (see [EXAMPLES.md](EXAMPLES.md))

### What happens if the server crashes?

All running automations stop. When you restart:
- Automation instances are lost (no persistence)
- You need to recreate and restart them
- Consider adding database persistence for production

## Development Questions

### How do I add a new automation type?

1. Create file: `server/automations/my_automation.py`
2. Inherit from `BaseAutomation`
3. Implement 4 methods: `get_name()`, `get_description()`, `get_config_schema()`, `run()`
4. Register in `server/automations/__init__.py`
5. Restart server

See [README.md](README.md#adding-new-automations) or [EXAMPLES.md](EXAMPLES.md) for details.

### Can I use external Python libraries in my automation?

Yes! Just:
1. Add the library to `server/requirements.txt`
2. Run `pip install -r requirements.txt`
3. Import and use in your automation

### How do I debug my automation?

1. **Use print statements** - They appear in server terminal
2. **Check server logs** - All output goes to terminal
3. **Test incrementally** - Start simple, add complexity
4. **Use try-except** - Catch and log errors
5. **Run test script** - `python server/test_server.py`

### Can I modify the Android app UI?

Yes! The code is in `android/app/src/main/`:
- Layouts: `res/layout/`
- Activities: `java/com/automation/client/`
- Themes: `res/values/themes.xml`

### How do I add a new configuration field type?

1. **Server**: Add handling in `base.py` if needed
2. **Android**: Add UI component in `ConfigActivity.kt`
3. Currently supported: text, number, date, time

## Technical Questions

### What's the difference between REST API and WebSocket?

- **REST API**: Request/response for actions (start, stop, create)
- **WebSocket**: Real-time updates (status changes)
- Both are used together for best experience

### Why use threading instead of async/await?

Simplicity and compatibility. Each automation runs independently. For production, consider:
- Celery for task queue
- AsyncIO for better performance
- Redis for state management

### Can I run multiple servers?

Yes, but each needs:
- Different port (change in `app.py`)
- Different Android app instance (or settings)
- Consider load balancing for production

### How is data stored?

Currently:
- **Server**: In-memory only (lost on restart)
- **Android**: SharedPreferences (server URL only)

For persistence, add:
- SQLite or PostgreSQL database
- Save automation configs and state
- Restore on server restart

### Is the communication secure?

No. Currently uses:
- HTTP (not HTTPS)
- No authentication
- No encryption

For production, add:
- HTTPS/WSS
- JWT authentication
- Input validation
- Rate limiting

## Troubleshooting Questions

### "ModuleNotFoundError: No module named 'flask'"

Install dependencies:
```bash
cd server
pip install -r requirements.txt
```

### "Address already in use"

Port 5000 is taken. Either:
- Stop other application using port 5000
- Change port in `server/app.py` (last line)

### App shows "Failed to load automations"

1. Check server is running
2. Verify server URL in Settings
3. Check server terminal for errors
4. Try refreshing the app
5. Check firewall settings

### Automation status stuck on "RUNNING"

The automation might be:
- Actually running (check server logs)
- Crashed (check for errors in logs)
- Not checking `stop_flag` (fix the code)

Force stop by restarting the server.

### WebSocket not connecting

1. Ensure URL ends with `/`
2. Restart app after changing settings
3. Check server supports WebSocket
4. Look for connection errors in logs

### Gradle sync failed in Android Studio

1. File → Invalidate Caches / Restart
2. Check internet connection
3. Update Android Studio
4. Check `build.gradle` for errors

## Performance Questions

### How often should automations check?

Depends on use case:
- **News monitoring**: 5-10 minutes
- **Ticket availability**: 1-5 minutes
- **Price tracking**: 1 hour
- **Uptime monitoring**: 1-5 minutes

Balance between responsiveness and resource usage.

### Can I run this 24/7?

Yes, but consider:
- Keep computer running
- Stable internet connection
- Monitor resource usage
- Add error recovery
- Consider cloud deployment

### How much bandwidth does it use?

Minimal:
- REST API: Only when you interact
- WebSocket: Small status updates
- Automations: Depends on what they do

Most bandwidth is from automation tasks (web scraping, API calls, etc.).

## Future Features

### What features might be added?

Potential additions:
- Scheduling (start/stop at specific times)
- Notifications (push to phone)
- Persistence (database storage)
- Authentication (user accounts)
- Web interface (browser access)
- Automation marketplace (share automations)
- Logging and analytics
- Cloud deployment support

### Can I contribute features?

Yes! This is open source. Feel free to:
- Add new automations
- Improve the UI
- Add features
- Fix bugs
- Improve documentation

## Getting Help

### Where can I find more information?

- **Setup**: [GETTING_STARTED.md](GETTING_STARTED.md)
- **Quick start**: [QUICKSTART.md](QUICKSTART.md)
- **Examples**: [EXAMPLES.md](EXAMPLES.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **All docs**: [INDEX.md](INDEX.md)

### I found a bug, what should I do?

1. Check if it's a known issue (see troubleshooting)
2. Check server logs for errors
3. Try to reproduce it
4. Document the steps
5. Check the code for obvious issues

### How do I request a feature?

Consider:
1. Is it generally useful?
2. Can you implement it yourself?
3. Does it fit the architecture?
4. Document your idea clearly

---

**Still have questions?** Check the documentation in [INDEX.md](INDEX.md) or review the code!

