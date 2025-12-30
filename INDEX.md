# 📚 Documentation Index

Welcome to the Automation Control System! This index will help you find the right documentation for your needs.

## 🚀 Getting Started (Choose Your Path)

### I'm New Here - Where Do I Start?
👉 **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete step-by-step setup guide (20 minutes)

### I Want to Get Running Quickly
👉 **[QUICKSTART.md](QUICKSTART.md)** - Fast setup for experienced developers (5 minutes)

### I Want to Understand the Project First
👉 **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - High-level overview of what's included

## 📖 Main Documentation

### Complete Reference
👉 **[README.md](README.md)** - Full project documentation
- Features overview
- Setup instructions
- Usage guide
- API reference
- Adding new automations

### System Architecture
👉 **[ARCHITECTURE.md](ARCHITECTURE.md)** - How the system works
- Architecture diagrams
- Communication flow
- Threading model
- Plugin system
- Technology stack

### Code Examples
👉 **[EXAMPLES.md](EXAMPLES.md)** - Real-world automation examples
- Price Tracker
- Uptime Monitor
- Social Media Monitor
- File Backup Monitor
- Complete code samples

### Visual Guide
👉 **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)** - Visual walkthrough
- User journey diagrams
- App screen mockups
- Communication flow
- Behind-the-scenes process

### FAQ
👉 **[FAQ.md](FAQ.md)** - Frequently Asked Questions
- Common questions answered
- Troubleshooting tips
- Development guidance

## 🎯 Quick Reference by Task

### Setting Up the System
1. **First Time Setup**: [GETTING_STARTED.md](GETTING_STARTED.md)
2. **Quick Setup**: [QUICKSTART.md](QUICKSTART.md)
3. **Server Setup**: [README.md](README.md#server-setup)
4. **Android Setup**: [README.md](README.md#android-app-setup)

### Using the System
1. **Creating Automations**: [README.md](README.md#usage)
2. **Configuring Automations**: [GETTING_STARTED.md](GETTING_STARTED.md#part-4-create-your-first-automation-3-minutes)
3. **Monitoring Status**: [README.md](README.md#using-the-android-app)

### Developing New Automations
1. **Quick Template**: `server/automations/example_template.py`
2. **Step-by-Step Guide**: [README.md](README.md#adding-new-automations)
3. **Real Examples**: [EXAMPLES.md](EXAMPLES.md)
4. **Architecture Details**: [ARCHITECTURE.md](ARCHITECTURE.md#plugin-system)

### Troubleshooting
1. **Common Issues**: [GETTING_STARTED.md](GETTING_STARTED.md#troubleshooting)
2. **Connection Problems**: [README.md](README.md#troubleshooting)
3. **Server Testing**: Run `python server/test_server.py`

## 📁 Code Reference

### Server Code
- **Main Application**: `server/app.py`
- **Automation Manager**: `server/automation_manager.py`
- **Base Class**: `server/automations/base.py`
- **Example Automations**: `server/automations/`

### Android Code
- **Main Activity**: `android/app/src/main/java/com/automation/client/MainActivity.kt`
- **Config Activity**: `android/app/src/main/java/com/automation/client/ConfigActivity.kt`
- **API Client**: `android/app/src/main/java/com/automation/client/api/ApiClient.kt`
- **Data Models**: `android/app/src/main/java/com/automation/client/models/Models.kt`

## 🎓 Learning Path

### Beginner Path
1. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Understand what you're building
2. Follow [GETTING_STARTED.md](GETTING_STARTED.md) - Set everything up
3. Try the example automations - Get familiar with the system
4. Read [README.md](README.md) - Learn all features

### Intermediate Path
1. Follow [QUICKSTART.md](QUICKSTART.md) - Get running fast
2. Study [EXAMPLES.md](EXAMPLES.md) - See real implementations
3. Modify existing automations - Customize for your needs
4. Read [ARCHITECTURE.md](ARCHITECTURE.md) - Understand the design

### Advanced Path
1. Review [ARCHITECTURE.md](ARCHITECTURE.md) - Understand the system
2. Study the code in `server/automations/` - See patterns
3. Create custom automations - Build your own
4. Extend the system - Add new features

## 🔍 Find Information By Topic

### API & Communication
- **REST API Endpoints**: [README.md](README.md#api-endpoints) or [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#-api-endpoints)
- **WebSocket Events**: [README.md](README.md#websocket-events) or [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#-websocket-events)
- **Communication Flow**: [ARCHITECTURE.md](ARCHITECTURE.md#communication-flow)

### Configuration
- **Server Configuration**: [README.md](README.md#server-setup)
- **Android Configuration**: [GETTING_STARTED.md](GETTING_STARTED.md#part-3-configure-the-app-2-minutes)
- **Field Types**: [README.md](README.md#configuration-field-types)

### Automation Development
- **Creating Automations**: [README.md](README.md#adding-new-automations)
- **Template File**: `server/automations/example_template.py`
- **Real Examples**: [EXAMPLES.md](EXAMPLES.md)
- **Base Class Reference**: `server/automations/base.py`

### System Design
- **Architecture Overview**: [ARCHITECTURE.md](ARCHITECTURE.md#overview)
- **Data Flow**: [ARCHITECTURE.md](ARCHITECTURE.md#data-flow)
- **Threading Model**: [ARCHITECTURE.md](ARCHITECTURE.md#threading-model)
- **Plugin System**: [ARCHITECTURE.md](ARCHITECTURE.md#plugin-system)

## 🛠️ Quick Commands

### Start Server
```bash
# Quick start
python main.py

# Or manually
cd server
pip install -r requirements.txt
python app.py
```

### Test Server
```bash
cd server
python test_server.py
```

### Run Android App
1. Open `android/` in Android Studio
2. Click Run (▶️)

## 📊 Project Statistics

- **Total Files Created**: 30+
- **Lines of Code**: 2000+
- **Documentation Pages**: 6
- **Example Automations**: 2 (+ 4 in examples)
- **Supported Field Types**: 4 (text, number, date, time)

## 🎯 Common Use Cases

| Use Case | Start Here | Then Read |
|----------|------------|-----------|
| First time user | [GETTING_STARTED.md](GETTING_STARTED.md) | [README.md](README.md) |
| Quick setup | [QUICKSTART.md](QUICKSTART.md) | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| Create automation | [EXAMPLES.md](EXAMPLES.md) | `example_template.py` |
| Understand system | [ARCHITECTURE.md](ARCHITECTURE.md) | [README.md](README.md) |
| Troubleshoot issue | [GETTING_STARTED.md](GETTING_STARTED.md#troubleshooting) | [README.md](README.md#troubleshooting) |
| Extend features | [ARCHITECTURE.md](ARCHITECTURE.md) | Source code |

## 📞 Need Help?

1. **Setup Issues**: Check [GETTING_STARTED.md](GETTING_STARTED.md#troubleshooting)
2. **Connection Problems**: See [README.md](README.md#troubleshooting)
3. **Code Questions**: Review [EXAMPLES.md](EXAMPLES.md) and `example_template.py`
4. **Architecture Questions**: Read [ARCHITECTURE.md](ARCHITECTURE.md)

## ✅ Quick Checklist

Before you start:
- [ ] Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) to understand the project
- [ ] Have Python 3.7+ installed
- [ ] Have Android Studio installed
- [ ] Have an Android device or emulator ready

To get running:
- [ ] Follow [GETTING_STARTED.md](GETTING_STARTED.md) or [QUICKSTART.md](QUICKSTART.md)
- [ ] Start the server
- [ ] Build and run the Android app
- [ ] Configure server URL in app
- [ ] Create and start your first automation

To develop:
- [ ] Read [EXAMPLES.md](EXAMPLES.md)
- [ ] Study `server/automations/example_template.py`
- [ ] Create your custom automation
- [ ] Test and iterate

---

**Ready to start?** Pick your path above and begin automating! 🚀

