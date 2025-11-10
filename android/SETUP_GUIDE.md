# Android App Setup Guide

Quick guide to get the Android app running.

## Prerequisites

- **Android Studio**: Hedgehog (2023.1.1) or newer
- **JDK**: Version 17 or newer
- **Android SDK**: API 34 (will be downloaded automatically)
- **Minimum Android Version**: API 24 (Android 7.0)

## Step-by-Step Setup

### 1. Install Android Studio

Download from: https://developer.android.com/studio

Make sure to install:
- Android SDK
- Android SDK Platform
- Android Virtual Device (for emulator)

### 2. Open the Project

1. Launch Android Studio
2. Click **"Open"** (not "New Project")
3. Navigate to the `android` folder in this project
4. Click **"OK"**

### 3. Wait for Gradle Sync

Android Studio will automatically:
- Download Gradle wrapper
- Download dependencies
- Index the project

This may take 5-10 minutes on first run.

**If Gradle sync fails**, see [GRADLE_TROUBLESHOOTING.md](GRADLE_TROUBLESHOOTING.md)

### 4. Configure SDK Path (if needed)

If you see "SDK not found" error:

1. Create `android/local.properties` file
2. Add your SDK path:

**Windows:**
```properties
sdk.dir=C\:\\Users\\YourUsername\\AppData\\Local\\Android\\Sdk
```

**Mac:**
```properties
sdk.dir=/Users/YourUsername/Library/Android/sdk
```

**Linux:**
```properties
sdk.dir=/home/YourUsername/Android/Sdk
```

### 5. Set Up a Device

#### Option A: Use an Emulator (Recommended for testing)

1. Click **"Device Manager"** in Android Studio
2. Click **"Create Device"**
3. Select **"Pixel 5"** (or any phone)
4. Click **"Next"**
5. Select **"Tiramisu"** (API 33) or **"UpsideDownCake"** (API 34)
6. Click **"Download"** if needed
7. Click **"Next"** → **"Finish"**

#### Option B: Use a Real Device

1. Enable **Developer Options** on your Android phone:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   
2. Enable **USB Debugging**:
   - Go to Settings → Developer Options
   - Enable "USB Debugging"
   
3. Connect phone via USB

4. Accept the debugging prompt on your phone

### 6. Run the App

1. Click the **Run** button (green play icon ▶️)
2. Select your device/emulator
3. Click **"OK"**

The app will build and install (may take 2-3 minutes first time).

### 7. Configure Server Connection

Once the app is running:

1. Tap the **menu icon** (⋮) in the top right
2. Tap **"Settings"**
3. Enter your server URL:
   - **For Emulator**: `http://10.0.2.2:5000/`
   - **For Real Device**: `http://YOUR_COMPUTER_IP:5000/`
4. Tap **"Save Settings"**

**Finding your computer's IP:**
- Windows: `ipconfig` → IPv4 Address
- Mac: System Preferences → Network
- Linux: `ip addr` or `ifconfig`

### 8. Test the Connection

1. Make sure the Flask server is running
2. Go back to the main screen
3. Tap the **refresh icon**
4. You should see an empty list (no errors)

**If you see connection errors:**
- Verify server is running
- Check the server URL
- Make sure phone and computer are on same WiFi
- Check firewall settings

## Common Issues

### Gradle Sync Failed

See [GRADLE_TROUBLESHOOTING.md](GRADLE_TROUBLESHOOTING.md) for detailed solutions.

**Quick fix:**
1. File → Invalidate Caches / Restart
2. Build → Clean Project
3. Build → Rebuild Project

### App Won't Install

**Error: "Installation failed with message INSTALL_FAILED_INSUFFICIENT_STORAGE"**
- Free up space on device/emulator
- Or use a different device

**Error: "Installation failed with message INSTALL_FAILED_UPDATE_INCOMPATIBLE"**
- Uninstall the old version first
- Or change the applicationId in build.gradle

### App Crashes on Startup

1. Check Android Studio's **Logcat** for errors
2. Make sure you're using API 24 or higher
3. Try cleaning and rebuilding

### Can't Connect to Server

**From Emulator:**
- Use `http://10.0.2.2:5000/` (NOT `localhost`)
- Make sure server is running on port 5000

**From Real Device:**
- Use your computer's actual IP address
- Make sure both are on same WiFi network
- Check firewall isn't blocking port 5000
- Try disabling firewall temporarily to test

## Build Variants

The app has two build variants:

- **debug** - For development (default)
- **release** - For production (requires signing)

To switch:
1. Build → Select Build Variant
2. Choose "debug" or "release"

## Project Structure

```
android/
├── app/
│   ├── src/main/
│   │   ├── java/com/automation/client/
│   │   │   ├── MainActivity.kt          # Main screen
│   │   │   ├── ConfigActivity.kt        # Configuration
│   │   │   ├── SettingsActivity.kt      # Settings
│   │   │   ├── AutomationAdapter.kt     # List adapter
│   │   │   ├── api/                     # API client
│   │   │   └── models/                  # Data models
│   │   ├── res/
│   │   │   ├── layout/                  # UI layouts
│   │   │   ├── values/                  # Strings, themes
│   │   │   └── menu/                    # Menu items
│   │   └── AndroidManifest.xml
│   └── build.gradle                     # App dependencies
├── build.gradle                         # Project config
├── settings.gradle                      # Gradle settings
└── gradle.properties                    # Gradle properties
```

## Customization

### Change App Name
Edit `app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">Your App Name</string>
```

### Change Colors
Edit `app/src/main/res/values/themes.xml`:
```xml
<item name="colorPrimary">#2196F3</item>
<item name="colorPrimaryDark">#1976D2</item>
<item name="colorAccent">#FF5722</item>
```

### Change Package Name
1. Right-click package in Android Studio
2. Refactor → Rename
3. Update in AndroidManifest.xml and build.gradle

## Building APK

To create an installable APK:

1. Build → Build Bundle(s) / APK(s) → Build APK(s)
2. Wait for build to complete
3. Click "locate" in the notification
4. APK is in `app/build/outputs/apk/debug/`

## Next Steps

Once the app is running:
1. Read the main [README.md](../README.md)
2. Follow [GETTING_STARTED.md](../GETTING_STARTED.md)
3. Create your first automation!

## Getting Help

- **Gradle issues**: See [GRADLE_TROUBLESHOOTING.md](GRADLE_TROUBLESHOOTING.md)
- **General setup**: See [GETTING_STARTED.md](../GETTING_STARTED.md)
- **FAQ**: See [FAQ.md](../FAQ.md)

## Success Checklist

- [ ] Android Studio installed and updated
- [ ] Project opened in Android Studio
- [ ] Gradle sync completed successfully
- [ ] Device/emulator configured
- [ ] App builds without errors
- [ ] App installs on device
- [ ] App opens without crashing
- [ ] Server URL configured
- [ ] Can connect to server

**All checked?** You're ready to start automating! 🎉

