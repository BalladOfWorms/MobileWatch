import java.io.FileInputStream
import java.util.Properties

// Release signing. Credentials live in keystore.properties at the project root,
// which is gitignored and never committed. If that file is absent the project
// still configures and `assembleDebug` still works — only `assembleRelease`
// produces an unsigned APK, which Android will refuse to install.
val keystorePropsFile = rootProject.file("keystore.properties")
val keystoreProps = Properties().apply {
    if (keystorePropsFile.exists()) FileInputStream(keystorePropsFile).use { load(it) }
}

// The file EXISTING is not enough. An empty or half-filled keystore.properties used to reach
// signingConfigs with a null storeFile and fail the whole build on Gradle's unhelpful
// "path may not be null or empty string. path='null'", pointing at a line that was not the
// problem. Require all four keys, and if the file is there but incomplete, say exactly what
// is missing instead of letting it blow up later.
val signingKeys = listOf("storeFile", "storePassword", "keyAlias", "keyPassword")
val missingKeys = signingKeys.filter { keystoreProps.getProperty(it).isNullOrBlank() }
val hasSigning = keystorePropsFile.exists() && missingKeys.isEmpty()

if (keystorePropsFile.exists() && missingKeys.isNotEmpty()) {
    logger.warn(
        "keystore.properties exists but is missing: ${missingKeys.joinToString(", ")}. " +
        "Release builds will be UNSIGNED. Copy keystore.properties.example over it and fill " +
        "in the two passwords, or delete keystore.properties if you have not made a key yet."
    )
} else if (hasSigning && !rootProject.file(keystoreProps.getProperty("storeFile")).exists()) {
    logger.warn(
        "keystore.properties points at '${keystoreProps.getProperty("storeFile")}', which does " +
        "not exist. storeFile is resolved relative to the project root — the .jks must sit " +
        "beside keystore.properties."
    )
}

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
}

android {
    namespace = "com.balladofworms.mobilewatch"
    compileSdk = 34

    defaultConfig {
        // DELIBERATELY LEFT ON THE OLD ID. `namespace` above (the R/BuildConfig package) was
        // renamed to ...mobilewatch, but `applicationId` is the identity Android installs under.
        // Changing it makes the next build a SEPARATE app: it installs beside the current one
        // instead of over it, and everything in the "mobilewatch" SharedPreferences — your saved
        // mob notes and view preferences — stays behind in the old sandbox. Change this line only
        // if you are willing to lose that, and uninstall the old app afterwards.
        applicationId = "com.balladofworms.auctionwatch"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
    }

    signingConfigs {
        if (hasSigning) {
            create("release") {
                storeFile = rootProject.file(keystoreProps.getProperty("storeFile"))
                storePassword = keystoreProps.getProperty("storePassword")
                keyAlias = keystoreProps.getProperty("keyAlias")
                keyPassword = keystoreProps.getProperty("keyPassword")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            if (hasSigning) signingConfig = signingConfigs.getByName("release")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }
    buildFeatures { compose = true }

    sourceSets["main"].java.srcDirs("src/main/kotlin")
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")
    implementation("androidx.activity:activity-compose:1.9.2")
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.6")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.6")

    implementation(platform("androidx.compose:compose-bom:2024.10.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    debugImplementation("androidx.compose.ui:ui-tooling")
}
