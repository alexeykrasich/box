# App Icon Guide

The app currently uses a simple placeholder icon. Here's how to add a custom icon.

## Current Icon

The app uses a simple blue circle with a robot symbol as a placeholder:
- Location: `app/src/main/res/drawable/ic_launcher_placeholder.xml`
- Type: Vector drawable (works on all Android versions)
- Color: Blue (#2196F3) matching the app theme

## Option 1: Use Android Studio's Image Asset Studio (Recommended)

This is the easiest way to create proper app icons.

### Steps:

1. **Right-click** on `app/src/main/res` in Android Studio
2. Select **New** → **Image Asset**
3. Choose **Launcher Icons (Adaptive and Legacy)**
4. Configure your icon:
   - **Foreground Layer**: Upload your icon image or use clipart
   - **Background Layer**: Choose a color or image
   - **Shape**: Circle, Square, Rounded Square, etc.
5. Click **Next** → **Finish**

This will automatically generate icons for all densities:
- `mipmap-mdpi/` (48x48)
- `mipmap-hdpi/` (72x72)
- `mipmap-xhdpi/` (96x96)
- `mipmap-xxhdpi/` (144x144)
- `mipmap-xxxhdpi/` (192x192)
- `mipmap-anydpi-v26/` (Adaptive icons for Android 8.0+)

### After Generation:

Update `AndroidManifest.xml`:
```xml
<application
    android:icon="@mipmap/ic_launcher"
    android:roundIcon="@mipmap/ic_launcher_round"
    ...>
```

## Option 2: Use Online Icon Generator

### Recommended Tools:

1. **Android Asset Studio** (Free)
   - URL: https://romannurik.github.io/AndroidAssetStudio/
   - Features: Launcher icons, notification icons, action bar icons
   - Generates all required sizes

2. **App Icon Generator** (Free)
   - URL: https://appicon.co/
   - Upload one image, get all sizes
   - Supports Android and iOS

3. **Icon Kitchen** (Free)
   - URL: https://icon.kitchen/
   - Modern adaptive icon support
   - Preview on different devices

### Steps:

1. Create or find your icon image (512x512 PNG recommended)
2. Upload to one of the tools above
3. Download the generated icon pack
4. Extract and copy to your project:
   ```
   android/app/src/main/res/
   ├── mipmap-mdpi/
   ├── mipmap-hdpi/
   ├── mipmap-xhdpi/
   ├── mipmap-xxhdpi/
   ├── mipmap-xxxhdpi/
   └── mipmap-anydpi-v26/
   ```
5. Update `AndroidManifest.xml` (see above)

## Option 3: Manual Creation

If you want to create icons manually:

### Required Sizes:

| Density | Size | Folder |
|---------|------|--------|
| mdpi | 48x48 | mipmap-mdpi |
| hdpi | 72x72 | mipmap-hdpi |
| xhdpi | 96x96 | mipmap-xhdpi |
| xxhdpi | 144x144 | mipmap-xxhdpi |
| xxxhdpi | 192x192 | mipmap-xxxhdpi |

### File Names:
- `ic_launcher.png` - Standard icon
- `ic_launcher_round.png` - Round icon (optional)

### For Adaptive Icons (Android 8.0+):

Create in `mipmap-anydpi-v26/`:

**ic_launcher.xml:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
```

**ic_launcher_round.xml:**
```xml
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_launcher_foreground"/>
</adaptive-icon>
```

## Icon Design Guidelines

### Best Practices:

1. **Size**: Start with 512x512 or 1024x1024
2. **Format**: PNG with transparency
3. **Safe Zone**: Keep important content in center 66% of icon
4. **Colors**: Use your app's brand colors
5. **Simplicity**: Simple, recognizable shapes work best
6. **Testing**: Test on different backgrounds (light/dark)

### Android Adaptive Icon Guidelines:

- **Foreground**: 108x108 dp canvas, safe zone 72x72 dp
- **Background**: Solid color or simple pattern
- **No text**: Icons should work without text
- **Scalable**: Should look good at any size

### Automation App Icon Ideas:

- 🤖 Robot symbol
- ⚙️ Gear/cog
- 🔄 Circular arrows (automation loop)
- ⚡ Lightning bolt (automation speed)
- 📱 Phone with automation symbol
- 🎯 Target with automation elements

## Quick Icon Resources

### Free Icon Sources:

1. **Material Icons** - https://fonts.google.com/icons
2. **Flaticon** - https://www.flaticon.com/
3. **Icons8** - https://icons8.com/
4. **Noun Project** - https://thenounproject.com/

### Design Tools:

1. **Figma** (Free) - https://www.figma.com/
2. **Canva** (Free) - https://www.canva.com/
3. **GIMP** (Free) - https://www.gimp.org/
4. **Inkscape** (Free) - https://inkscape.org/

## Current Placeholder Icon

The current icon is defined in:
```
app/src/main/res/drawable/ic_launcher_placeholder.xml
```

It's a simple vector drawable that:
- Works on all Android versions
- Scales perfectly (vector)
- Matches app theme colors
- Is good enough for development/testing

## When to Update the Icon

**Keep placeholder if:**
- You're still in development
- Testing functionality
- Don't have final branding yet

**Update icon when:**
- Ready for production
- Have final branding
- Publishing to Play Store
- Sharing with users

## Testing Your Icon

After adding a new icon:

1. **Uninstall old app** (to clear cache)
2. **Rebuild and install**
3. **Check on home screen**
4. **Test on different launchers** (if possible)
5. **Check in app drawer**
6. **Test on different Android versions**

## Troubleshooting

### Icon not updating?

1. Uninstall the app completely
2. Clean project: Build → Clean Project
3. Rebuild: Build → Rebuild Project
4. Reinstall

### Icon looks blurry?

- Make sure you have all density folders
- Check that images are correct sizes
- Use vector drawables when possible

### Icon has white background?

- Make sure PNG has transparency
- Check adaptive icon background color
- Test on different launcher backgrounds

## Example: Creating a Simple Icon

Here's a quick example using Material Icons:

1. Go to https://fonts.google.com/icons
2. Search for "settings_automation" or "robot"
3. Download the icon
4. Use Android Studio's Image Asset Studio
5. Import the downloaded icon
6. Generate all sizes
7. Done!

---

**For now, the placeholder icon works fine for development and testing!**

When you're ready for a custom icon, use Android Studio's Image Asset Studio - it's the easiest method.

