package com.balladofworms.mobilewatch.ui.theme

import android.app.Activity
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val AuctionColors = darkColorScheme(
    primary = AccentGreen,
    onPrimary = CharcoalDark,
    secondary = AccentGold,
    onSecondary = CharcoalDark,
    background = Charcoal,
    onBackground = TextPrimary,
    surface = CharcoalDark,
    onSurface = TextPrimary,
    surfaceVariant = Panel,
    onSurfaceVariant = TextMuted,
    error = AccentRed,
    onError = CharcoalDark,
)

@Composable
fun MobileWatchTheme(content: @Composable () -> Unit) {
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            WindowCompat.setDecorFitsSystemWindows(window, true)
        }
    }
    MaterialTheme(
        colorScheme = AuctionColors,
        typography = AppTypography,
        content = content
    )
}
