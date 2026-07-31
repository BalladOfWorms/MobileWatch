package com.balladofworms.mobilewatch

import java.time.Duration
import java.time.ZoneId
import java.time.ZonedDateTime

/**
 * Limited-Time Records of Eminence rotation — a fixed real-world clock schedule
 * (Pacific time), 6 four-hour slots per day. Ported from OmniWatch. No network.
 */
object RoeSchedule {
    // [dayOfWeek Sun=0..Sat=6][slot 0..5]
    private val ROTATION = arrayOf(
        arrayOf("Vanquish Arcana", "Gain Experience", "Vanquish Birds", "Vanquish Lizards", "Vanquish Undead", "Spoils (Seals)"),        // Sun
        arrayOf("Crack Treasure Caskets", "Vanquish Aquans", "Vanquish Amorphs", "Vanquish Vermin", "Vanquish Arcana", "Gain Experience"), // Mon
        arrayOf("Physical Damage Kills", "Vanquish Beasts", "Vanquish Undead", "Spoils (Seals)", "Crack Treasure Chests", "Vanquish Aquans"), // Tue
        arrayOf("Magic Damage Kills", "Vanquish Plantoids", "Vanquish Arcana", "Gain Experience", "Physical Damage Kills", "Vanquish Beasts"), // Wed
        arrayOf("Vanquish Birds", "Vanquish Lizards", "Crack Treasure Caskets", "Vanquish Aquans", "Magic Damage Kills", "Vanquish Plantoids"), // Thu
        arrayOf("Vanquish Amorphs", "Vanquish Vermin", "Physical Damage Kills", "Vanquish Beasts", "Vanquish Birds", "Vanquish Lizards"),   // Fri
        arrayOf("Vanquish Undead", "Spoils (Seals)", "Magic Damage Kills", "Vanquish Plantoids", "Vanquish Amorphs", "Vanquish Vermin"),    // Sat
    )

    data class RoeState(val current: String, val next: String, val secondsLeft: Long)

    fun current(): RoeState {
        val zone = runCatching { ZoneId.of("America/Los_Angeles") }.getOrElse { ZoneId.of("America/Los_Angeles") }
        // Shift +1h so slot boundaries land cleanly on 00/04/08/12/16/20.
        val shifted = ZonedDateTime.now(zone).plusHours(1)
        val slot = (shifted.hour / 4) % 6
        val daySun = shifted.dayOfWeek.value % 7            // DayOfWeek Mon=1..Sun=7 -> Sun=0..Sat=6
        val current = ROTATION[daySun][slot]

        val nextSlot = (slot + 1) % 6
        val nextDay = if (nextSlot != 0) daySun else (daySun + 1) % 7
        val next = ROTATION[nextDay][nextSlot]

        val nextSlotHour = ((shifted.hour / 4) + 1) * 4
        val nextBoundary = if (nextSlotHour >= 24)
            shifted.plusDays(1).withHour(nextSlotHour - 24).withMinute(0).withSecond(0).withNano(0)
        else
            shifted.withHour(nextSlotHour).withMinute(0).withSecond(0).withNano(0)
        val secondsLeft = Duration.between(shifted, nextBoundary).seconds.coerceAtLeast(0)
        return RoeState(current, next, secondsLeft)
    }

    fun formatCountdown(seconds: Long): String {
        val h = seconds / 3600
        val m = (seconds % 3600) / 60
        return if (h > 0) "%dh %02dm".format(h, m) else "%dm".format(m)
    }
}
