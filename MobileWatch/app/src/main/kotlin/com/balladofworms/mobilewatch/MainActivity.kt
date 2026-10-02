package com.balladofworms.mobilewatch

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import com.balladofworms.mobilewatch.music.MusicPlayer
import com.balladofworms.mobilewatch.music.MusicService
import com.balladofworms.mobilewatch.ui.MobileWatchApp
import com.balladofworms.mobilewatch.ui.theme.MobileWatchTheme

class MainActivity : ComponentActivity() {
    private val vm: MobileWatchViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        MusicPlayer.init(this)
        openMusicIfAsked(intent)
        setContent {
            MobileWatchTheme { MobileWatchApp() }
        }
    }

    // Tapping the music notification brings the app forward on the music screen.
    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        openMusicIfAsked(intent)
    }

    private fun openMusicIfAsked(i: Intent?) {
        if (i?.getBooleanExtra(MusicService.EXTRA_OPEN_MUSIC, false) == true) {
            vm.openMusic()
            i.removeExtra(MusicService.EXTRA_OPEN_MUSIC)
        }
    }

    // Leaving the app for good (back out of it, or swiped away) stops the music; just switching to
    // another app or turning the screen off doesn't.
    override fun onDestroy() {
        if (isFinishing) MusicPlayer.stop()
        super.onDestroy()
    }
}
