package com.balladofworms.mobilewatch.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AccessTime
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.balladofworms.mobilewatch.ui.theme.*
import kotlinx.coroutines.delay
import java.time.ZoneId
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter
import java.util.Locale
import kotlin.math.abs
import kotlin.math.floor
import kotlin.math.roundToInt

// Vana'diel time on the phone. The game clock isn't sent anywhere -- it's a fixed function of
// real time (25x faster, counted from a known start), the same formula OmniWatch and every FFXI
// clock use. The phone's clock is set from the network, so it's right without any syncing.

object VanaTime {
    private const val OFFSET = 92514960L                 // seconds (Ashita's vanatime.lua)
    private const val SPEED = 25
    const val EARTH_SEC_PER_VDAY = 86400.0 / SPEED       // 57.6 minutes

    val DAYS = listOf("Firesday", "Earthsday", "Watersday", "Windsday",
        "Iceday", "Lightningday", "Lightsday", "Darksday")

    val DAY_COLORS = mapOf(
        "Firesday" to Color(0xFFFF5A3C), "Earthsday" to Color(0xFFD2C337),
        "Watersday" to Color(0xFF468CFF), "Windsday" to Color(0xFF46D246),
        "Iceday" to Color(0xFF96D2FF), "Lightningday" to Color(0xFFC864FF),
        "Lightsday" to Color(0xFFFFFFD2), "Darksday" to Color(0xFF9682AF))

    class Now(
        val hour: Int, val minute: Int,
        val year: Long, val month: Int, val day: Int,
        val weekday: String,
        val moonDay: Int, val moonPercent: Int, val moonName: String,
        val intoDayEarthSec: Double
    )

    fun now(unixMs: Long = System.currentTimeMillis()): Now {
        val vs = (unixMs / 1000.0 + OFFSET) * SPEED
        val days = floor(vs / 86400.0).toLong()
        val sec = vs - days * 86400.0
        val phase = ((days + 26) % 84).toInt()
        val pct = (abs(42 - phase) * 100.0 / 42.0).roundToInt()
        return Now(
            hour = (sec / 3600).toInt(), minute = ((sec % 3600) / 60).toInt(),
            year = days / 360, month = ((days % 360) / 30).toInt() + 1, day = (days % 30).toInt() + 1,
            weekday = DAYS[(days % 8).toInt()],
            moonDay = phase, moonPercent = pct, moonName = moonName(phase, pct),
            intoDayEarthSec = sec / SPEED)
    }

    /** The game's own naming, from the percentage, as OmniWatch's header uses it. */
    fun moonName(phaseDay: Int, pct: Int): String {
        val waning = phaseDay < 42
        return when {
            pct >= 93 -> "Full Moon"
            pct <= 5 -> "New Moon"
            pct in 43..57 -> if (waning) "Last Quarter" else "First Quarter"
            pct > 57 -> if (waning) "Waning Gibbous" else "Waxing Gibbous"
            else -> if (waning) "Waning Crescent" else "Waxing Crescent"
        }
    }

    private fun nameOnDay(phaseDay: Int): String {
        val pct = (abs(42 - phaseDay) * 100.0 / 42.0).roundToInt()
        return moonName(phaseDay, pct)
    }

    /** Each other day of the week and how long until it starts, soonest first. */
    fun nextDays(n: Now): List<Pair<String, Double>> {
        val idx = DAYS.indexOf(n.weekday)
        return (1..7).map { ahead ->
            DAYS[(idx + ahead) % 8] to (ahead * EARTH_SEC_PER_VDAY - n.intoDayEarthSec)
        }
    }

    /** Each other moon phase and how long until it begins, soonest first. */
    fun nextMoons(n: Now): List<Pair<String, Double>> {
        val out = ArrayList<Pair<String, Double>>()
        val seen = hashSetOf(n.moonName)
        for (ahead in 1..84) {
            val name = nameOnDay((n.moonDay + ahead) % 84)
            if (seen.add(name)) out.add(name to (ahead * EARTH_SEC_PER_VDAY - n.intoDayEarthSec))
        }
        return out.sortedBy { it.second }
    }

    fun until(secs: Double): String {
        val s = secs.toLong().coerceAtLeast(0)
        val h = s / 3600; val m = (s % 3600) / 60
        return if (h > 0) "%dh %02dm".format(h, m) else "%dm".format(m)
    }
}

/** The header button: a clock that opens the Vana'diel time panel. */
@Composable
internal fun VanaClockButton() {
    var open by remember { mutableStateOf(false) }
    IconButton(onClick = { open = true }) {
        Icon(Icons.Filled.AccessTime, "Vana'diel time", tint = TextPrimary)
    }
    if (open) VanaClockDialog(onDismiss = { open = false })
}

@Composable
private fun VanaClockDialog(onDismiss: () -> Unit) {
    var nowMs by remember { mutableLongStateOf(System.currentTimeMillis()) }
    LaunchedEffect(Unit) { while (true) { nowMs = System.currentTimeMillis(); delay(1000) } }
    val v = VanaTime.now(nowMs)
    val jst = ZonedDateTime.now(ZoneId.of("Asia/Tokyo"))
    val local = ZonedDateTime.now()
    val fmt = DateTimeFormatter.ofPattern("EEE d MMM  HH:mm", Locale.ENGLISH)
    val dayColor = VanaTime.DAY_COLORS[v.weekday] ?: TextPrimary

    AlertDialog(
        onDismissRequest = onDismiss,
        containerColor = CharcoalDark,
        confirmButton = { TextButton(onClick = onDismiss) { Text("Close", color = AccentGold) } },
        title = { Text("Vana'diel", color = AccentGold, fontWeight = FontWeight.Bold) },
        text = {
            Column(Modifier.verticalScroll(rememberScrollState())) {
                Row(verticalAlignment = Alignment.Bottom) {
                    Text("%02d:%02d".format(v.hour, v.minute), color = TextPrimary,
                        fontSize = 34.sp, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.width(12.dp))
                    Text("C.E. %d/%02d/%02d".format(v.year, v.month, v.day), color = TextMuted,
                        fontSize = 14.sp, modifier = Modifier.padding(bottom = 6.dp))
                }
                Text(v.weekday, color = dayColor, fontSize = 18.sp, fontWeight = FontWeight.SemiBold)
                Text("${v.moonName}  \u00b7  ${v.moonPercent}%", color = TextSoft, fontSize = 15.sp)
                Spacer(Modifier.height(10.dp))
                ClockLine("Japan", jst.format(fmt) + "  JST")
                ClockLine("Here", local.format(fmt))

                Spacer(Modifier.height(14.dp))
                Text("Days", color = AccentGold, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                VanaTime.nextDays(v).forEach { (name, secs) ->
                    Row(Modifier.fillMaxWidth().padding(vertical = 1.dp)) {
                        Text(name, color = VanaTime.DAY_COLORS[name] ?: TextPrimary, fontSize = 13.sp,
                            modifier = Modifier.weight(1f))
                        Text("in " + VanaTime.until(secs), color = TextMuted, fontSize = 13.sp)
                    }
                }
                Spacer(Modifier.height(12.dp))
                Text("Moon", color = AccentGold, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
                VanaTime.nextMoons(v).forEach { (name, secs) ->
                    Row(Modifier.fillMaxWidth().padding(vertical = 1.dp)) {
                        Text(name, color = TextPrimary, fontSize = 13.sp, modifier = Modifier.weight(1f))
                        Text("in " + VanaTime.until(secs), color = TextMuted, fontSize = 13.sp)
                    }
                }
            }
        }
    )
}

@Composable
private fun ClockLine(label: String, value: String) {
    Row(Modifier.padding(vertical = 2.dp)) {
        Text("$label:", color = TextMuted, fontSize = 13.sp, modifier = Modifier.widthIn(min = 60.dp))
        Text(value, color = TextPrimary, fontSize = 13.sp)
    }
}
