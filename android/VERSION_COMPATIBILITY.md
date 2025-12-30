# Version Compatibility Reference

This document explains the version requirements and compatibility for the Android app.

## Current Configuration

The project is configured with these versions:

| Component | Version | File |
|-----------|---------|------|
| Gradle | 8.5 | `gradle/wrapper/gradle-wrapper.properties` |
| Android Gradle Plugin | 8.2.2 | `build.gradle` |
| Kotlin | 1.9.22 | `build.gradle` |
| Compile SDK | 34 (Android 14) | `app/build.gradle` |
| Target SDK | 34 (Android 14) | `app/build.gradle` |
| Min SDK | 24 (Android 7.0) | `app/build.gradle` |

## Java Compatibility

### Recommended: Java 17 (LTS)
- ✅ Most stable
- ✅ Long-term support
- ✅ Compatible with Gradle 8.5
- ✅ Works with all dependencies

### Supported: Java 21 (LTS)
- ✅ Latest LTS version
- ✅ Requires Gradle 8.5 or higher (✓ configured)
- ✅ Better performance
- ⚠️ Some plugins may not be fully tested

### Not Recommended: Java 11 or older
- ⚠️ Older version
- ⚠️ May have compatibility issues
- ⚠️ Consider upgrading

## Version Compatibility Matrix

### Gradle vs Java

| Gradle Version | Java 8 | Java 11 | Java 17 | Java 21 |
|----------------|--------|---------|---------|---------|
| 7.5 | ✅ | ✅ | ✅ | ❌ |
| 8.0 | ✅ | ✅ | ✅ | ❌ |
| 8.5 | ✅ | ✅ | ✅ | ✅ |
| 8.6+ | ✅ | ✅ | ✅ | ✅ |

**Current Project**: Gradle 8.5 → Works with Java 8-21

### Android Gradle Plugin vs Gradle

| AGP Version | Min Gradle | Max Gradle | Recommended Gradle |
|-------------|------------|------------|-------------------|
| 7.4.x | 7.5 | 8.0 | 7.6 |
| 8.0.x | 8.0 | 8.2 | 8.0 |
| 8.1.x | 8.0 | 8.4 | 8.2 |
| 8.2.x | 8.2 | 8.5+ | 8.5 |

**Current Project**: AGP 8.2.2 + Gradle 8.5 ✅

### Kotlin vs Gradle

| Kotlin Version | Min Gradle | Recommended Gradle |
|----------------|------------|-------------------|
| 1.8.x | 7.3 | 7.6 |
| 1.9.x | 7.5 | 8.5 |
| 2.0.x | 8.1.1 | 8.5+ |

**Current Project**: Kotlin 1.9.22 + Gradle 8.5 ✅

## Android Studio Compatibility

| Android Studio Version | Release Date | Min AGP | Recommended AGP |
|------------------------|--------------|---------|-----------------|
| Flamingo (2022.2.1) | May 2023 | 7.2 | 8.0 |
| Giraffe (2022.3.1) | Jul 2023 | 7.4 | 8.1 |
| Hedgehog (2023.1.1) | Nov 2023 | 8.0 | 8.2 |
| Iguana (2023.2.1) | Mar 2024 | 8.1 | 8.3 |
| Jellyfish (2023.3.1) | May 2024 | 8.2 | 8.4 |

**Minimum Required**: Hedgehog (2023.1.1) or newer

**Recommended**: Latest stable version

## Dependency Versions

### Core Android Libraries

```gradle
androidx.core:core-ktx:1.12.0              // ✅ Stable
androidx.appcompat:appcompat:1.6.1         // ✅ Stable
material:1.11.0                            // ✅ Stable
constraintlayout:2.1.4                     // ✅ Stable
```

### Networking

```gradle
retrofit:2.9.0                             // ✅ Stable
okhttp:4.12.0                              // ✅ Latest
socket.io-client:2.1.0                     // ✅ Stable (with exclusion)
```

### Kotlin Coroutines

```gradle
kotlinx-coroutines-android:1.7.3          // ✅ Compatible with Kotlin 1.9.22
```

## Common Version Issues

### Issue 1: Java 21 with Gradle < 8.5

**Error**: "Your build is currently configured to use incompatible Java 21 and Gradle X"

**Solution**: 
- Upgrade to Gradle 8.5+ (already done in this project)
- Or downgrade to Java 17

### Issue 2: AGP version mismatch

**Error**: "This version of Android Gradle plugin requires Gradle X"

**Solution**: 
- Check compatibility matrix above
- Update gradle-wrapper.properties to compatible version

### Issue 3: Kotlin version incompatibility

**Error**: "The Kotlin Gradle plugin was loaded multiple times"

**Solution**:
- Ensure all modules use same Kotlin version
- Check build.gradle files for version conflicts

## How to Check Your Versions

### Check Java Version

```bash
java -version
```

Expected output:
```
openjdk version "17.0.x" or "21.0.x"
```

### Check Gradle Version

```bash
cd android
./gradlew --version
```

Expected output:
```
Gradle 8.5
```

### Check Android Studio Version

1. Help → About Android Studio
2. Look for version number (e.g., "Hedgehog | 2023.1.1")

### Check in Android Studio Settings

1. File → Settings (Preferences on Mac)
2. Build, Execution, Deployment → Build Tools → Gradle
3. Check "Gradle JDK" version

## Upgrading Versions

### Upgrade Gradle

Edit `gradle/wrapper/gradle-wrapper.properties`:
```properties
distributionUrl=https\://services.gradle.org/distributions/gradle-8.5-bin.zip
```

Or run:
```bash
./gradlew wrapper --gradle-version=8.5
```

### Upgrade Android Gradle Plugin

Edit `build.gradle`:
```gradle
plugins {
    id 'com.android.application' version '8.2.2' apply false
}
```

### Upgrade Kotlin

Edit `build.gradle`:
```gradle
plugins {
    id 'org.jetbrains.kotlin.android' version '1.9.22' apply false
}
```

## Recommended Setup

For best compatibility and stability:

1. **Java**: 17 (LTS) or 21 (LTS)
2. **Android Studio**: Latest stable (Hedgehog or newer)
3. **Gradle**: 8.5 (auto-configured)
4. **AGP**: 8.2.2 (auto-configured)
5. **Kotlin**: 1.9.22 (auto-configured)

## References

- [Gradle Compatibility Matrix](https://docs.gradle.org/current/userguide/compatibility.html)
- [AGP Release Notes](https://developer.android.com/studio/releases/gradle-plugin)
- [Kotlin Compatibility](https://kotlinlang.org/docs/gradle-configure-project.html)

## Quick Reference

**If you have Java 17**: ✅ Everything works out of the box

**If you have Java 21**: ✅ Works with Gradle 8.5 (configured)

**If you have Java 11 or older**: ⚠️ Consider upgrading to Java 17

**If sync fails**: See [GRADLE_TROUBLESHOOTING.md](GRADLE_TROUBLESHOOTING.md)

