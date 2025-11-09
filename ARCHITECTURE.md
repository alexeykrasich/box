# System Architecture

## Overview

The Automation Control System consists of two main components:
1. **Flask Server** - Backend that manages and runs automations
2. **Android Client** - Mobile app for controlling automations

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Android Client                          │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ MainActivity│  │ConfigActivity│  │SettingsActivity│       │
│  └─────┬──────┘  └──────┬───────┘  └──────┬───────┘        │
│        │                 │                  │                 │
│        └─────────────────┴──────────────────┘                │
│                          │                                    │
│        ┌─────────────────┴─────────────────┐                │
│        │                                     │                │
│   ┌────▼─────┐                      ┌──────▼──────┐         │
│   │ApiClient │                      │Socket.IO    │         │
│   │(Retrofit)│                      │Client       │         │
│   └────┬─────┘                      └──────┬──────┘         │
└────────┼────────────────────────────────────┼────────────────┘
         │                                     │
         │ REST API                            │ WebSocket
         │ (HTTP)                              │ (Real-time)
         │                                     │
┌────────▼─────────────────────────────────────▼────────────────┐
│                      Flask Server                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │                    app.py                             │    │
│  │  ┌──────────────┐           ┌──────────────┐        │    │
│  │  │ REST API     │           │ WebSocket    │        │    │
│  │  │ Endpoints    │           │ Events       │        │    │
│  │  └──────┬───────┘           └──────┬───────┘        │    │
│  └─────────┼──────────────────────────┼────────────────┘    │
│            │                           │                      │
│  ┌─────────▼───────────────────────────▼────────────────┐   │
│  │          AutomationManager                            │   │
│  │  - Create/Delete automations                          │   │
│  │  - Start/Stop automations                             │   │
│  │  - Manage automation instances                        │   │
│  │  - Broadcast status updates                           │   │
│  └─────────┬─────────────────────────────────────────────┘   │
│            │                                                   │
│  ┌─────────▼─────────────────────────────────────────────┐   │
│  │         Automation Instances                           │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │   │
│  │  │TicketBuyer #1│  │NewsMonitor #1│  │ Custom #1  │  │   │
│  │  │  (Thread)    │  │  (Thread)    │  │ (Thread)   │  │   │
│  │  └──────────────┘  └──────────────┘  └────────────┘  │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                                │
│  ┌───────────────────────────────────────────────────────┐   │
│  │         Automation Plugin System                       │   │
│  │  ┌──────────────────────────────────────────────────┐ │   │
│  │  │ BaseAutomation (Abstract Class)                  │ │   │
│  │  │  - get_name()                                     │ │   │
│  │  │  - get_description()                              │ │   │
│  │  │  - get_config_schema()                            │ │   │
│  │  │  - run()                                          │ │   │
│  │  │  - start() / stop()                               │ │   │
│  │  └──────────────────────────────────────────────────┘ │   │
│  │                                                         │   │
│  │  Implementations:                                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │   │
│  │  │TicketBuyer   │  │NewsMonitor   │  │Your Custom │  │   │
│  │  │Automation    │  │Automation    │  │Automation  │  │   │
│  │  └──────────────┘  └──────────────┘  └────────────┘  │   │
│  └───────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

## Communication Flow

### 1. Creating an Automation

```
Android App                    Flask Server
    │                              │
    │  POST /api/automations       │
    │  { type: "TicketBuyer" }     │
    ├─────────────────────────────>│
    │                              │ Create instance
    │                              │ Assign ID
    │  { id: "abc123", ... }       │
    │<─────────────────────────────┤
    │                              │
```

### 2. Starting an Automation

```
Android App                    Flask Server
    │                              │
    │  POST /api/automations/      │
    │       abc123/start           │
    │  { config: {...} }           │
    ├─────────────────────────────>│
    │                              │ Validate config
    │                              │ Start thread
    │  { status: "running" }       │
    │<─────────────────────────────┤
    │                              │
    │  WebSocket: status_update    │
    │<─────────────────────────────┤
    │                              │
```

### 3. Real-time Status Updates

```
Android App                    Flask Server
    │                              │
    │  WebSocket connected         │
    │<────────────────────────────>│
    │                              │
    │                              │ Automation
    │                              │ status changes
    │                              │
    │  status_update event         │
    │  { id, status, ... }         │
    │<─────────────────────────────┤
    │                              │
    │  Update UI                   │
    │                              │
```

## Data Flow

### Configuration Schema

Each automation defines its configuration schema:

```python
{
    "key": "field_name",
    "label": "Display Label",
    "type": "text|number|date|time",
    "required": True/False,
    "default": "default_value"
}
```

This schema is:
1. Sent to Android app via REST API
2. Used to dynamically build configuration UI
3. Validated when starting automation
4. Passed to automation's `run()` method

### Automation Lifecycle

```
Created → Configured → Running → Stopped → Deleted
   │          │           │         │         │
   │          │           │         │         └─> Remove instance
   │          │           │         └─> Stop thread
   │          │           └─> Execute in thread
   │          └─> Validate config
   └─> Instantiate class
```

## Threading Model

- Each automation runs in its own daemon thread
- Main thread handles Flask requests
- WebSocket runs in separate thread
- Thread-safe communication via callbacks

```
Main Thread              Automation Threads
    │                         │
    │ Start automation        │
    ├────────────────────────>│ Thread 1: Ticket Buyer
    │                         │   - Check tickets
    │                         │   - Wait interval
    │                         │   - Repeat
    │                         │
    │ Start automation        │
    ├────────────────────────>│ Thread 2: News Monitor
    │                         │   - Fetch news
    │                         │   - Compare changes
    │                         │   - Wait interval
    │                         │
    │ Status callback         │
    │<────────────────────────┤ Status changed
    │                         │
    │ Broadcast via WebSocket │
    │                         │
```

## Plugin System

### Adding New Automation

1. **Create class** inheriting from `BaseAutomation`
2. **Implement methods**:
   - `get_name()` - Display name
   - `get_description()` - Description
   - `get_config_schema()` - Configuration fields
   - `run()` - Main logic
3. **Register** in `__init__.py`
4. **Restart** server

The Android app automatically discovers new automations!

## Security Considerations

**Current Implementation** (Testing):
- No authentication
- HTTP (cleartext)
- No input validation
- Debug mode enabled

**Production Recommendations**:
- Add JWT authentication
- Use HTTPS/WSS
- Validate all inputs
- Rate limiting
- User management
- Disable debug mode

## Technology Stack

### Backend
- **Flask**: Web framework
- **Flask-SocketIO**: WebSocket support
- **Flask-CORS**: Cross-origin requests
- **Threading**: Concurrent execution

### Android
- **Kotlin**: Modern Android development
- **Retrofit**: Type-safe HTTP client
- **Socket.IO**: WebSocket client
- **Coroutines**: Async operations
- **Material Design**: UI components

## Scalability

Current design is suitable for:
- Single user
- ~10-20 concurrent automations
- Local network deployment

For production scale:
- Add database (SQLite/PostgreSQL)
- Use Celery for task queue
- Add Redis for caching
- Implement user sessions
- Deploy with Gunicorn/uWSGI
- Use nginx reverse proxy

