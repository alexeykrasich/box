# 🤖 Automation Control System

A flexible automation management system with a Flask server and Kotlin Android client. Easily start, stop, configure, and monitor various automation tasks from your Android phone.

> **📚 New here?** Check out **[INDEX.md](INDEX.md)** for a complete documentation guide!
>
> **🚀 Want to get started quickly?** See **[QUICKSTART.md](QUICKSTART.md)** or **[GETTING_STARTED.md](GETTING_STARTED.md)**

## Features

- **Plugin-based Architecture**: Easily add new automation types
- **REST API + WebSocket**: Real-time status updates
- **Dynamic Configuration**: Each automation has its own configuration schema
- **Android Client**: Native Kotlin app with modern Material Design UI
- **Example Automations**:
  - **Ticket Buyer**: Monitor and buy train tickets automatically
  - **News Monitor**: Track website changes and send notifications

## Project Structure

```
.
├── server/                      # Flask backend
│   ├── app.py                  # Main Flask application
│   ├── automation_manager.py  # Automation management logic
│   ├── requirements.txt        # Python dependencies
│   └── automations/            # Automation plugins
│       ├── base.py            # Base automation class
│       ├── ticket_buyer.py    # Ticket buying automation
│       └── news_monitor.py    # News monitoring automation
│
└── android/                    # Android client
    └── app/
        └── src/main/
            ├── java/com/automation/client/
            │   ├── MainActivity.kt
            │   ├── ConfigActivity.kt
            │   ├── SettingsActivity.kt
            │   ├── AutomationAdapter.kt
            │   ├── api/
            │   │   ├── ApiClient.kt
            │   │   └── ApiService.kt
            │   └── models/
            │       └── Models.kt
            └── res/
                └── layout/
```

## Setup Instructions

### Server Setup

1. **Install Python dependencies**:
   ```bash
   cd server
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python app.py
   ```
   
   The server will start on `http://0.0.0.0:5000`

### Android App Setup

1. **Open the project in Android Studio**:
   - Open Android Studio
   - Select "Open an Existing Project"
   - Navigate to the `android` folder

2. **Build and run**:
   - Connect your Android device or start an emulator
   - Click "Run" in Android Studio

3. **Configure server URL**:
   - Open the app
   - Go to Settings (menu → Settings)
   - Enter your server URL:
     - For emulator: `http://10.0.2.2:5000/`
     - For real device: `http://YOUR_COMPUTER_IP:5000/`
   - Save settings

## Usage

### Using the Android App

1. **Add an Automation**:
   - Tap the "+" button
   - Select automation type (Ticket Buyer, News Monitor, etc.)

2. **Configure and Start**:
   - Tap "Config" on an automation
   - Fill in the required fields
   - Tap "Start Automation"

3. **Monitor Status**:
   - View real-time status updates
   - See last run time and error messages
   - Stop running automations anytime

4. **Delete Automation**:
   - Tap "Delete" to remove an automation instance

### Adding New Automations

1. **Create a new automation class** in `server/automations/`:

```python
from .base import BaseAutomation
from typing import Dict, Any, List

class MyAutomation(BaseAutomation):
    def get_name(self) -> str:
        return "My Automation"
    
    def get_description(self) -> str:
        return "Description of what this does"
    
    def get_config_schema(self) -> List[Dict[str, Any]]:
        return [
            {
                "key": "my_field",
                "label": "My Field",
                "type": "text",  # text, number, date, time
                "required": True,
                "default": ""
            }
        ]
    
    def run(self):
        # Your automation logic here
        # Check self.stop_flag periodically to allow stopping
        while not self.stop_flag.is_set():
            # Do work
            config_value = self.config.get('my_field')
            # ...
            self.stop_flag.wait(60)  # Wait 60 seconds
```

2. **Register the automation** in `server/automations/__init__.py`:

```python
from .my_automation import MyAutomation

AVAILABLE_AUTOMATIONS = [
    TicketBuyerAutomation,
    NewsMonitorAutomation,
    MyAutomation,  # Add your automation here
]
```

3. **Restart the server** - the new automation will appear in the Android app!

## API Endpoints

### REST API

- `GET /api/automations/types` - Get available automation types
- `GET /api/automations` - List all automation instances
- `POST /api/automations` - Create new automation instance
- `GET /api/automations/{id}` - Get automation status
- `POST /api/automations/{id}/start` - Start automation with config
- `POST /api/automations/{id}/stop` - Stop automation
- `DELETE /api/automations/{id}` - Delete automation

### WebSocket Events

- `connect` - Client connected
- `status_update` - Real-time status updates
- `request_status` - Request current status

## Configuration Field Types

When defining automation config schemas, use these field types:

- `text` - Text input
- `number` - Numeric input
- `date` - Date picker
- `time` - Time picker
- `select` - Dropdown (provide `options` array)

## Technologies Used

### Backend
- Flask - Web framework
- Flask-SocketIO - WebSocket support
- Flask-CORS - Cross-origin support
- Python threading - Concurrent automation execution

### Android
- Kotlin - Programming language
- Retrofit - REST API client
- Socket.IO - WebSocket client
- Material Design - UI components
- Coroutines - Asynchronous operations

## Notes

- No authentication is implemented (for testing only)
- Server runs in debug mode by default
- Android app uses cleartext traffic (HTTP) - configure for production use
- WebSocket provides real-time updates without polling

## Troubleshooting

**Can't connect from Android app**:
- Make sure server is running
- Check firewall settings
- For emulator, use `10.0.2.2` instead of `localhost`
- For real device, use your computer's local IP address

**Automation not stopping**:
- Make sure your automation checks `self.stop_flag` regularly
- Use `self.stop_flag.wait(seconds)` instead of `time.sleep()`

**WebSocket not connecting**:
- Check server URL in settings
- Ensure URL format is correct (e.g., `http://10.0.2.2:5000/`)

## License

This project is open source and available for modification and extension.

