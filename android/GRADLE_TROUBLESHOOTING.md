# Gradle Sync Troubleshooting

If you encounter Gradle sync errors, try these solutions:

## Common Issues and Solutions

### 1. Java/Gradle Version Compatibility

**Problem**: "Your build is currently configured to use incompatible Java X and Gradle Y"

**Solution**: The project is configured for:
- **Gradle 8.5** (compatible with Java 8-21)
- **Android Gradle Plugin 8.2.2**
- **Kotlin 1.9.22**

**Recommended Java versions:**
- Java 17 (LTS) - Most stable
- Java 21 (LTS) - Latest, requires Gradle 8.5+

**If using Java 21**, make sure Gradle is 8.5 or higher (already configured).

### 2. "module() method not found" Error

**Solution**: The project has been updated to use modern Gradle syntax. Make sure you:
- Use Android Studio Hedgehog (2023.1.1) or newer
- Gradle 8.5 (specified in gradle-wrapper.properties)

### 3. Socket.IO Dependency Conflict

**Solution**: The Socket.IO dependency now excludes the conflicting `org.json` module:
```gradle
implementation('io.socket:socket.io-client:2.1.0') {
    exclude group: 'org.json', module: 'json'
}
```

### 4. Repository Issues

**Solution**: Changed `repositoriesMode` from `FAIL_ON_PROJECT_REPOS` to `PREFER_SETTINGS` in settings.gradle

### 5. General Gradle Sync Failures

Try these steps in order:

#### Step 1: Invalidate Caches
1. File → Invalidate Caches / Restart
2. Select "Invalidate and Restart"
3. Wait for Android Studio to restart and re-sync

#### Step 2: Clean and Rebuild
```bash
./gradlew clean
./gradlew build
```

Or in Android Studio:
- Build → Clean Project
- Build → Rebuild Project

#### Step 3: Delete Gradle Cache
```bash
# Close Android Studio first
rm -rf ~/.gradle/caches/
rm -rf .gradle/
```

Then reopen Android Studio and let it re-download dependencies.

#### Step 4: Update Gradle Wrapper
```bash
cd android
./gradlew wrapper --gradle-version=8.5
```

#### Step 5: Check Versions
Make sure you're using:
- **Android Studio**: Hedgehog (2023.1.1) or newer
- **JDK**: 17 (recommended) or 21
- **Gradle**: 8.5 (auto-downloaded from wrapper)
- **Android Gradle Plugin**: 8.2.2

Update if needed from: https://developer.android.com/studio

### 5. Specific Dependency Issues

If a specific dependency fails, you can try alternative versions:

**Socket.IO alternatives:**
```gradle
// Option 1: Latest stable (recommended)
implementation('io.socket:socket.io-client:2.1.0') {
    exclude group: 'org.json', module: 'json'
}

// Option 2: Newer version (if available)
implementation 'io.socket:socket.io-client:2.1.1'

// Option 3: Use OkHttp WebSocket instead
implementation 'com.squareup.okhttp3:okhttp:4.12.0'
```

### 6. Network/Proxy Issues

If dependencies won't download:

**Add to gradle.properties:**
```properties
systemProp.http.proxyHost=your.proxy.host
systemProp.http.proxyPort=8080
systemProp.https.proxyHost=your.proxy.host
systemProp.https.proxyPort=8080
```

Or use offline mode:
- File → Settings → Build, Execution, Deployment → Gradle
- Check "Offline work"

### 7. Minimum Requirements

Ensure you have:
- **Android Studio**: Hedgehog (2023.1.1) or newer
- **JDK**: 17 (recommended) or 21
- **Gradle**: 8.5 (auto-configured)
- **Android Gradle Plugin**: 8.2.2 (auto-configured)
- **Kotlin**: 1.9.22 (auto-configured)
- **Android SDK**: API 34 (compileSdk)
- **Minimum Android**: API 24 (Android 7.0)

### 8. Create local.properties

Create `android/local.properties` with your SDK path:

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

## Still Having Issues?

### Check Gradle Output
1. View → Tool Windows → Build
2. Look for specific error messages
3. Search for the error online

### Use Command Line
```bash
cd android
./gradlew build --stacktrace
```

This gives more detailed error information.

### Simplify Dependencies

If all else fails, you can temporarily remove Socket.IO and use polling instead:

1. Comment out Socket.IO dependency in `app/build.gradle`
2. Comment out WebSocket code in `MainActivity.kt`
3. Use manual refresh instead of real-time updates

### Version Compatibility Matrix

| Java Version | Gradle Version | AGP Version | Status |
|--------------|----------------|-------------|---------|
| Java 17 (LTS) | 8.5 | 8.2.2 | ✅ Recommended |
| Java 21 (LTS) | 8.5+ | 8.2.2+ | ✅ Supported |
| Java 11 | 7.5+ | 7.4.2 | ⚠️ Older |

**Current Project Configuration:**
- Gradle: 8.5
- Android Gradle Plugin: 8.2.2
- Kotlin: 1.9.22
- Works with: Java 17 or Java 21

## Success Checklist

- [ ] Android Studio Hedgehog (2023.1.1) or newer installed
- [ ] JDK 17 or 21 configured
- [ ] Gradle 8.5 (auto-configured via wrapper)
- [ ] Android Gradle Plugin 8.2.2 (auto-configured)
- [ ] Caches invalidated
- [ ] Project cleaned and rebuilt
- [ ] local.properties created with correct SDK path
- [ ] Internet connection working (for dependency download)
- [ ] No proxy issues

## Getting Help

If you're still stuck:
1. Check the exact error message in Build output
2. Search for the error on Stack Overflow
3. Check Android Studio's Event Log for hints
4. Try the alternative Socket.IO versions above

## Quick Fix Script

Run this to reset everything:

```bash
# Close Android Studio first!
cd android
rm -rf .gradle
rm -rf app/build
rm -rf build
./gradlew clean
./gradlew wrapper --gradle-version=8.5
```

Then reopen in Android Studio and sync.

## Java Version Check

To check your Java version:

```bash
java -version
```

**If you see Java 21**, make sure you're using Gradle 8.5+ (already configured).

**If you see Java 8-11**, consider upgrading to Java 17 (LTS) for better compatibility.

**To change Java version in Android Studio:**
1. File → Settings (or Preferences on Mac)
2. Build, Execution, Deployment → Build Tools → Gradle
3. Gradle JDK → Select Java 17 or 21
4. Click OK and re-sync

