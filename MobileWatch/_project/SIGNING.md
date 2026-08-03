# MobileWatch — building a signed release APK

Written 2026-07-31 (rev 395). `app/build.gradle.kts` now reads its release signing
config from `keystore.properties` at the project root.

## Why signing is not optional

Android will not install an unsigned APK at all. The question is never *whether*
to sign, only *with what key*:

- **Debug builds are already signed** — with the throwaway debug keystore Android
  generates for you. That is what you have been installing. It works, but the key
  is not yours, it expires, and an app installed with it cannot later be upgraded
  by a release build.
- **Release builds are unsigned unless you configure a key.** For a sideloaded
  personal app, a self-signed release key is exactly right. You do not need Google
  Play, and you do not need an AAB — an APK is the correct output.

## One-time setup

1. Generate the key (from the project root). 10000 days is ~27 years:

   ```
   keytool -genkeypair -v \
     -keystore mobilewatch-release.jks \
     -alias mobilewatch \
     -keyalg RSA -keysize 4096 -validity 10000
   ```

   It asks for a keystore password, then name/organisation fields (all optional —
   press Enter through them), then a key password. Using the same password for
   both is fine for a personal app.

2. Copy `keystore.properties.example` to `keystore.properties` and fill in the
   two passwords. It is gitignored, as are `*.jks` and `*.keystore`.

3. **Back up the .jks file and both passwords somewhere you will still have them
   in five years.** This is the one irreversible part. If you lose the keystore,
   Android treats a rebuild as a different app: you cannot upgrade over the
   installed copy, you have to uninstall first, and uninstalling wipes the app's
   saved data.

## Every build after that

```
./gradlew clean assembleRelease
```

Output: `app/build/outputs/apk/release/app-release.apk`

Verify it really is signed before copying it to the phone:

```
$ANDROID_HOME/build-tools/34.0.0/apksigner verify --print-certs \
  app/build/outputs/apk/release/app-release.apk
```

## Bump the version before each release you keep

In `app/build.gradle.kts` → `defaultConfig`:

- `versionCode` — an integer that must **increase** every build you install over
  a previous one. Android refuses a downgrade.
- `versionName` — the string you see in the app list, e.g. `1.1.0`.

## Notes specific to this project

- `isMinifyEnabled = false` on release. Leave it that way for now: R8 buys little
  here and this app reads a 2.8 MB JSON asset through org.json plus a lot of
  Compose, so shrinking is a good way to introduce a silent runtime failure for
  no real gain. The APK is asset-dominated, not code-dominated.
- The release APK will be roughly the size of `app/src/main/assets` plus a few MB.
  That is expected — mobs.json, zoneinfo.json, the item DB and the image folders
  are the app.
- `minSdk = 26`, `targetSdk = 34`, `compileSdk = 34`, AGP 8.5.2, Gradle 8.9,
  Kotlin 2.0.21, JDK 17. Building on a newer JDK than 17 is the usual cause of a
  sudden "Unsupported class file major version" failure.
