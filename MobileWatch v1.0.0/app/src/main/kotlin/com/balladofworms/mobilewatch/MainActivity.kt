package com.balladofworms.mobilewatch

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import com.balladofworms.mobilewatch.ui.MobileWatchApp
import com.balladofworms.mobilewatch.ui.theme.MobileWatchTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MobileWatchTheme { MobileWatchApp() }
        }
    }
}
