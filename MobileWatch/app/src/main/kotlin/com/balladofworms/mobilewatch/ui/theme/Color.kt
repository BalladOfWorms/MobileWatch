package com.balladofworms.mobilewatch.ui.theme

import androidx.compose.ui.graphics.Color

val Charcoal      = Color(0xFF1E1E28)   // background
val CharcoalDark  = Color(0xFF181820)   // bars / strips
val Panel         = Color(0xFF14141C)   // list surfaces
val TextPrimary   = Color(0xFFDCDCE6)
val TextSoft      = Color(0xFFC8CEDE)
val TextMuted     = Color(0xFF8A90A2)
val AccentGreen   = Color(0xFF8FD39A)
val AccentGold    = Color(0xFFE6D29A)
val Selection     = Color(0xFF33415C)
val AccentRed     = Color(0xFFE39A9A)
val JobsBlue     = Color(0xFF9AB0D0)

// bolder-look accents
val HeaderAccent = Color(0xFF26374C)   // gradient midpoint in the top bar
val PopStripTint = Color(0xFF16241C)   // subtle green tint under the population strip

// Header tiers. Every TOP-LEVEL heading in every tab uses HeaderL1 so the tabs read as one app
// instead of eight; L2 and L3 keep the bestiary's nested tree legible underneath it.
val HeaderL1 = AccentGold              // top-level section titles, all tabs
val HeaderL2 = JobsBlue                // second level
val HeaderL3 = Color(0xFF7E8AA0)       // third level
