# Gradle Sync Troubleshooting

If you encounter Gradle sync errors, try these solutions:

## Common Issues and Solutions

### 1. "module() method not found" Error

**Solution**: The project has been updated to use modern Gradle syntax. Make sure you:
- Use Android Studio Hedgehog (2023.1.1) or newer
- Gradle 8.0 or newer (specified in gradle-wrapper.properties)

### 2. Socket.IO Dependency Conflict

**Solution**: The Socket.IO dependency now excludes the conflicting `org.json` module:
```gradle
implementation('io.socket:socket.io-client:2.1.0') {
    exclude group: 'org.json', module: 'json'
}
```

### 3. Repository Issues

**Solution**: Changed `repositoriesMode` from `FAIL_ON_PROJECT_REPOS` to `PREFER_SETTINGS` in settings.gradle

### 4. General Gradle Sync Failures

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
./gradlew wrapper --gradle-version=8.0
```

#### Step 5: Check Android Studio Version
Make sure you're using:
- Android Studio Hedgehog (2023.1.1) or newer
- JDK 17 or newer

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
- Android Studio Hedgehog (2023.1.1) or newer
- JDK 17 or newer
- Gradle 8.0 or newer
- Android SDK 34 (compileSdk)
- Minimum SDK 24 (minSdk)

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

### Alternative: Use Older Gradle

If you must use an older Android Studio version:

**In android/build.gradle:**
```gradle
plugins {
    id 'com.android.application' version '7.4.2' apply false
    id 'com.android.library' version '7.4.2' apply false
    id 'org.jetbrains.kotlin.android' version '1.8.0' apply false
}
```

**In gradle-wrapper.properties:**
```properties
distributionUrl=https\://services.gradle.org/distributions/gradle-7.5-bin.zip
```

## Success Checklist

- [ ] Android Studio Hedgehog or newer installed
- [ ] JDK 17 or newer configured
- [ ] Gradle wrapper updated to 8.0+
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
./gradlew wrapper --gradle-version=8.0
```

Then reopen in Android Studio and sync.

