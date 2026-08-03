package com.balladofworms.mobilewatch.ui

import android.content.Intent
import android.graphics.BitmapFactory
import android.net.Uri
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.ArrowDropDown
import androidx.compose.material.icons.filled.ArrowForward
import androidx.compose.material.icons.filled.ArrowDropUp
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Place
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.listSaver
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.saveable.SaveableStateHolder
import androidx.compose.runtime.saveable.rememberSaveableStateHolder
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.input.pointer.positionChanged
import androidx.compose.foundation.gestures.awaitEachGesture
import androidx.compose.foundation.gestures.awaitFirstDown
import androidx.compose.foundation.gestures.calculatePan
import androidx.compose.foundation.gestures.calculateZoom
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.gestures.detectHorizontalDragGestures
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.balladofworms.mobilewatch.*
import com.balladofworms.mobilewatch.R
import com.balladofworms.mobilewatch.ui.theme.*
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

private val DATE_FMT: DateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd  HH:mm")
private fun fmtDate(epoch: Long): String = try {
    Instant.ofEpochSecond(epoch).atZone(ZoneId.systemDefault()).format(DATE_FMT)
} catch (e: Exception) { epoch.toString() }

private fun onsaleText(v: Int?): String = when (v) {
    null -> "?"; -1 -> "n/a"; else -> v.toString()
}

// ── COLLAPSE ON LEAVE ────────────────────────────────────────────────────────
// Every CollapsibleSection with persist = true keys its saved state on the CURRENT
// PAGE VISIT rather than on the page alone. Scrolling never changes the visit id, so
// a panel you opened stays open while you scroll a long list; LEAVING the page and
// coming back mints a NEW visit id, so the page always opens fully collapsed.
//
// Deliberately NOT done by clearing the SaveableStateHolder: that would also throw
// away each page's scroll position, so backing out of a mob would jump the bestiary
// list back to the top.
private var pageVisitCounter = 0
private val LocalPageVisit = compositionLocalOf { 0 }

@Composable
private fun SaveableStateHolder.Page(key: String, epochKey: Any = key, content: @Composable () -> Unit) {
    val visit = remember(key, epochKey) { ++pageVisitCounter }
    CompositionLocalProvider(LocalPageVisit provides visit) {
        SaveableStateProvider(key, content)
    }
}

@Composable
fun MobileWatchApp(vm: MobileWatchViewModel = viewModel()) {
    val ui = vm.ui
    val holder = rememberSaveableStateHolder()
    when {
        ui.showSettings -> holder.Page("settings") { BackHandler { vm.closeSettings() }; SettingsScreen(vm) }
        ui.selectedSubtype != null && ui.selectedMob != null -> holder.Page("subtype:${ui.selectedSubtype?.name}") { BackHandler { vm.clearSubtype() }; SubtypeDetailScreen(vm) }
        ui.selectedMob != null -> holder.Page("mob:${ui.selectedMob?.key}") { BackHandler { vm.clearMob() }; MobDetailScreen(vm) }
        ui.mode == "maps" && ui.selectedZone != null && ui.showMap -> holder.Page("map:${ui.selectedZone?.id}") { BackHandler { vm.closeMap() }; MapViewerScreen(vm) }
        ui.mode == "maps" && ui.selectedZone != null -> holder.Page("zone:${ui.selectedZone?.id}") { BackHandler { vm.back() }; ZoneDetailScreen(vm) }
        ui.mode == "jobs" && ui.selectedJob != null && ui.selectedPet != null -> holder.Page("pet:${ui.selectedPet?.name}") { BackHandler { vm.clearPet() }; PetDetailScreen(vm) }
        ui.mode == "jobs" && ui.selectedJob != null && ui.selectedSpell != null -> holder.Page("spell:${ui.selectedSpell}") { BackHandler { vm.clearSpell() }; SpellDetailScreen(vm) }
        ui.mode == "jobs" && ui.selectedJob != null -> holder.Page("job:${ui.selectedJob?.id}") { BackHandler { vm.back() }; JobDetailScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby != null && ui.showHobbyInfo -> holder.Page("hobbyinfo:${ui.selectedHobby}") { BackHandler { vm.closeHobbyInfo() }; HobbyInfoScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "fishing" && ui.selectedFish != null -> holder.Page("fish:${ui.selectedFish?.name}") { BackHandler { vm.clearFish() }; FishDetailScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "fishing" -> holder.Page("hobby:fishing") { BackHandler { vm.clearHobby() }; FishingScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "gardening" && ui.selectedPlanting != null -> holder.Page("planting:${ui.selectedPlanting?.id}") { BackHandler { vm.clearPlanting() }; PlantingScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "gardening" -> holder.Page("hobby:gardening") { BackHandler { vm.clearHobby() }; GardeningScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "logging" && ui.selectedLogZone != null -> holder.Page("logzone:${ui.selectedLogZone?.name}") { BackHandler { vm.clearLogZone() }; LogZoneScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "logging" -> holder.Page("hobby:logging") { BackHandler { vm.clearHobby() }; LoggingScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "excavation" && ui.selectedExcZone != null -> holder.Page("exczone:${ui.selectedExcZone?.name}") { BackHandler { vm.clearExcZone() }; ExcZoneScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "excavation" -> holder.Page("hobby:excavation") { BackHandler { vm.clearHobby() }; ExcavationScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "mining" && ui.selectedMineZone != null -> holder.Page("minezone:${ui.selectedMineZone?.name}") { BackHandler { vm.clearMineZone() }; MineZoneScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "mining" -> holder.Page("hobby:mining") { BackHandler { vm.clearHobby() }; MiningScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "harvesting" && ui.selectedHarvestZone != null -> holder.Page("harvestzone:${ui.selectedHarvestZone?.name}") { BackHandler { vm.clearHarvestZone() }; HarvestZoneScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "harvesting" -> holder.Page("hobby:harvesting") { BackHandler { vm.clearHobby() }; HarvestingScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "raising" -> holder.Page("hobby:raising") { BackHandler { vm.clearHobby() }; HobbyInfoScreen(vm, onBack = { vm.clearHobby() }) }
        ui.mode == "hobbies" && ui.selectedHobby == "racing" -> holder.Page("hobby:racing") { BackHandler { vm.clearHobby() }; HobbyInfoScreen(vm, onBack = { vm.clearHobby() }) }
        ui.mode == "hobbies" && ui.selectedHobby == "clamming" -> holder.Page("hobby:clamming") { BackHandler { vm.clearHobby() }; HobbyInfoScreen(vm, onBack = { vm.clearHobby() }) }
        ui.mode == "hobbies" && ui.selectedHobby == "moggarden" -> holder.Page("hobby:moggarden") { BackHandler { vm.clearHobby() }; HobbyInfoScreen(vm, onBack = { vm.clearHobby() }) }
        ui.mode == "hobbies" && ui.selectedHobby == "monsterrearing" -> holder.Page("hobby:monsterrearing") { BackHandler { vm.clearHobby() }; HobbyInfoScreen(vm, onBack = { vm.clearHobby() }) }
        ui.mode == "hobbies" && ui.selectedHobby == "monstrosity" -> holder.Page("hobby:monstrosity") { BackHandler { vm.clearHobby() }; HobbyInfoScreen(vm, onBack = { vm.clearHobby() }) }
        ui.mode == "hobbies" && ui.selectedHobby == "digging" && ui.selectedDigZone != null -> holder.Page("digzone:${ui.selectedDigZone?.name}") { BackHandler { vm.clearDigZone() }; DigZoneScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby == "digging" -> holder.Page("hobby:digging") { BackHandler { vm.clearHobby() }; DiggingScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby in CraftKeys && ui.selectedRecipe != null -> holder.Page("recipe:${ui.selectedHobby}:${ui.selectedRecipe?.id}") { BackHandler { vm.clearRecipe() }; RecipeDetailScreen(vm) }
        ui.mode == "hobbies" && ui.selectedHobby in CraftKeys -> holder.Page("hobby:${ui.selectedHobby}") { BackHandler { vm.clearHobby() }; CraftScreen(vm, ui.selectedHobby!!) }
        ui.mode == "trusts" && ui.selectedTrust != null ->
            holder.Page("trust:${ui.selectedTrust}") { BackHandler { vm.clearTrust() }; TrustScreen(vm) }
        ui.mode == "chains" && ui.showWsList ->
            holder.Page("wslist") { BackHandler { vm.closeWsList() }; WeaponSkillListScreen(vm) }
        ui.mode == "content" && ui.selectedContent != null && ui.selectedContentZone != null ->
            holder.Page("contentzone:${ui.selectedContentZone}") { BackHandler { vm.clearContentZone() }; DynamisZoneScreen(vm) }
        ui.mode == "content" && ui.selectedContent != null ->
            holder.Page("content:${ui.selectedContent}") {
                BackHandler { vm.clearContent() }
                if (ui.selectedContent == "omen") OmenScreen(vm)
                else if (ui.selectedContent == "odyssey") OdysseyScreen(vm)
                else if (ui.selectedContent == "apexlocus") ApexLocusScreen(vm)
                else if (ui.selectedContent == "sortie") SortieScreen(vm)
                else if (ui.selectedContent == "unity") UnityScreen(vm)
                else if (ui.selectedContent == "vagary") VagaryScreen(vm)
                else if (ui.selectedContent == "abyssea") AbysseaScreen(vm)
                else if (ui.selectedContent == "mastertrials") MasterTrialsScreen(vm)
                else if (ui.selectedContent == "limbus") LimbusScreen(vm)
                else if (ui.selectedContent == "geasfete") GeasFeteScreen(vm)
                else if (ui.selectedContent == "ultimate") UltimateWeaponsScreen(vm)
                else ContentTypeScreen(vm)
            }
        ui.mode == "items" && ui.selected != null -> holder.Page("item:${ui.selected?.id}") { BackHandler { vm.back() }; DetailScreen(vm) }
        else -> holder.Page("search", ui.mode) { SearchScreen(vm) }   // one key, one scroll state per tab; ui.mode still mints a new visit
    }
}

@Composable
private fun GradientTopBar(title: String, titleColor: Color = AccentGold, onBack: (() -> Unit)? = null, trailing: String? = null, logoRes: Int? = null, onLogoClick: (() -> Unit)? = null, actions: (@Composable () -> Unit)? = null) {
    Box(
        Modifier.fillMaxWidth()
            .background(Brush.horizontalGradient(listOf(Charcoal, HeaderAccent, Charcoal)))
            .windowInsetsPadding(WindowInsets.statusBars)
            .height(56.dp).padding(end = 8.dp),
        contentAlignment = Alignment.CenterStart
    ) {
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            if (onBack != null) IconButton(onClick = onBack) { Icon(Icons.Filled.ArrowBack, "Back", tint = TextPrimary) }
            else Spacer(Modifier.width(16.dp))
            if (logoRes != null) {
                Image(painterResource(logoRes), title,
                    modifier = Modifier.height(40.dp)
                        .then(if (onLogoClick != null) Modifier.clickable { onLogoClick() } else Modifier))
                Spacer(Modifier.weight(1f))
            } else {
                Text(title, color = titleColor, fontWeight = FontWeight.Bold, fontSize = 20.sp,
                    maxLines = 1, overflow = TextOverflow.Ellipsis, modifier = Modifier.weight(1f))
            }
            if (trailing != null) Text(trailing, color = TextPrimary, fontSize = 14.sp,
                fontWeight = FontWeight.Medium, modifier = Modifier.padding(start = 8.dp, end = 4.dp))
            if (actions != null) actions()
        }
    }
}

// Bucket label for mobs with no zone data at all — pinned to the bottom of the Zone view so it
// doubles as the "what still needs an Adversaries table" list.
private const val NO_ZONE = "\u2014 No zone data"

// Rev 350, user: "lets hide the other>unknown entries. we can keep them in the json and i will
// continue searching for them but i dont want them seen in the app."
//
// A record with a blank `fam` used to surface as Other > Unknown in the Family view AND as an
// "Unknown" sub-group inside every Zone and Content group it touched. All four mob views derive
// from one list, so ONE filter at that point removes it from all of them.
//
// It is a BROWSE filter, not a data change: nothing is deleted, and the filter is skipped while
// a search query is active, so typing a name still reaches the record. That keeps the research
// loop working — the bucket is invisible while browsing and one query away when wanted.
// Flip this to false to bring the whole bucket back.
private const val HIDE_UNFAMILIED = true

// A content tag is `Group[: Section[: Role]]` — e.g. "Peculiar Foes", "Unity Mobs",
// "Sortie: Section A", "Sortie: Section A: Boss". Splitting here means a new sectioned
// content type needs NO Kotlin change: the tag string carries its own structure.
private fun contentParts(tag: String): Triple<String, String, String> {
    val p = tag.split(":").map { it.trim() }
    return Triple(p.getOrElse(0) { "" }, p.getOrElse(1) { "" }, p.getOrElse(2) { "" })
}

// Ordering inside a section: an Atonement tier (highest first) beats a declared Boss,
// which beats NMs, which beat regular mobs. Only those roles need spelling out in the
// tag — `nm` already separates the last two.
//   "Odyssey: Sheol Gaol: Atonement 4"  -> -4   (so 4, 3, 2, 1 lead the section)
//   "Dynamis: Dynamis-Bastok: Arch Mega"-> -2   (Arch Mega Boss — trade all five Fiendish Tomes)
//   "Dynamis: Dynamis-Bastok: Mega"     -> -1   (Mega Boss — the plain statue, drops one of the five)
//   "Dynamis D: ...: Disjoined"         -> -1   (Divergence's post-zone-boss fight)
//   "Sortie: Section A: Boss"           ->  0
//   "Omen: Bosses: Midboss"             ->  1   (below the boss, above the plain NMs)
//   "Dynamis: Dynamis-Windurst: TE"     ->  3   (Time Extension mobs head the regular block)
// BG's classic-Dynamis tables name both tiers ("Mega Boss" / "Arch Mega Boss") but the wording
// wobbles page to page — structure decides: the plain statue drops one of the five tomes, the
// Arch is spawned by trading all five. Arch Mega and Atonement both land on negative ranks but
// never share a section — Atonement is Odyssey's Sheol Gaol, the Mega tiers are Dynamis.
private fun contentRole(mob: Mob, group: String, section: String): String =
    mob.content
        .map { contentParts(it) }
        .firstOrNull { it.first == group && it.second == section }
        ?.third ?: ""

private fun contentRank(mob: Mob, group: String, section: String): Int {
    val role = contentRole(mob, group, section)
    val tier = if (role.startsWith("Atonement", ignoreCase = true))
        role.filter { it.isDigit() }.toIntOrNull() else null
    return when {
        tier != null -> -tier
        role.equals("Arch Mega", ignoreCase = true) -> -2
        role.equals("Mega", ignoreCase = true) -> -1
        role.equals("Disjoined", ignoreCase = true) -> -1
        role.equals("Boss", ignoreCase = true) -> 0
        role.equals("Midboss", ignoreCase = true) -> 1
        mob.nm -> 2
        role.equals("TE", ignoreCase = true) -> 3
        else -> 4
    }
}

// Section order within a group. Alphabetical unless a group needs its own running order —
// Odyssey leads with Sheol Gaol, then Sheol A-C.
private fun sectionPriority(group: String, section: String): Int = when {
    group == "Odyssey" && section.equals("Sheol Gaol", ignoreCase = true) -> 0
    else -> 1
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun GroupHeader(title: String, count: Int? = null, expanded: Boolean, onClick: () -> Unit) {
    Row(
        Modifier.fillMaxWidth().clickable { onClick() }.background(CharcoalDark)
            .padding(horizontal = 10.dp, vertical = 9.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(if (expanded) Icons.Filled.ArrowDropUp else Icons.Filled.ArrowDropDown, null, tint = TextMuted)
        Spacer(Modifier.width(4.dp))
        Text(title, color = HeaderL1, fontWeight = FontWeight.Bold, fontSize = 13.sp, modifier = Modifier.weight(1f))
        if (count != null) Text(count.toString(), color = TextMuted, fontSize = 12.sp)
    }
}

@Composable
private fun SubGroupHeader(title: String, count: Int, subCount: Int, expanded: Boolean, onClick: () -> Unit) {
    Row(
        Modifier.fillMaxWidth().clickable { onClick() }.background(Panel)
            .padding(start = 22.dp, end = 10.dp, top = 8.dp, bottom = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(if (expanded) Icons.Filled.ArrowDropUp else Icons.Filled.ArrowDropDown, null, tint = TextMuted)
        Spacer(Modifier.width(4.dp))
        Text(title, color = HeaderL2, fontWeight = FontWeight.Medium, fontSize = 13.sp)
        if (subCount > 1) Text("($subCount)", color = TextMuted, fontSize = 11.sp, modifier = Modifier.padding(start = 4.dp))
        Spacer(Modifier.weight(1f))
        Text(count.toString(), color = TextMuted, fontSize = 12.sp)
    }
}

@Composable
private fun SubSubHeader(title: String, count: Int, expanded: Boolean, onClick: () -> Unit) {
    Row(
        Modifier.fillMaxWidth().clickable { onClick() }.background(Charcoal)
            .padding(start = 40.dp, end = 10.dp, top = 7.dp, bottom = 7.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(if (expanded) Icons.Filled.ArrowDropUp else Icons.Filled.ArrowDropDown, null, tint = TextMuted)
        Spacer(Modifier.width(4.dp))
        Text(title, color = HeaderL3, fontSize = 12.sp, modifier = Modifier.weight(1f))
        Text(count.toString(), color = TextMuted, fontSize = 11.sp)
    }
}

@Composable
private fun PickerButton(label: String, current: String, options: List<Pair<String, String>>, onSelect: (String) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    val currentLabel = options.firstOrNull { it.first == current }?.second ?: options.first().second
    Box {
        OutlinedButton(
            onClick = { expanded = true }, shape = RoundedCornerShape(10.dp),
            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 2.dp),
            colors = ButtonDefaults.outlinedButtonColors(contentColor = TextSoft)
        ) {
            Text("$label: $currentLabel", fontSize = 13.sp, maxLines = 1)
            Icon(Icons.Filled.ArrowDropDown, null)
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            options.forEach { (value, lbl) ->
                DropdownMenuItem(text = { Text(lbl) }, onClick = { onSelect(value); expanded = false })
            }
        }
    }
}

@Composable
private fun MobRow(vm: MobileWatchViewModel, mob: Mob, inZone: String? = null, nameSuffix: String? = null) {
    Row(
        Modifier.fillMaxWidth().clickable { vm.selectMob(mob, inZone) }.padding(horizontal = 12.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        SubtypeImage(vm.iconForMob(mob), 40.dp)
        Spacer(Modifier.width(12.dp))
        Column {
            Text(
                mob.name + (nameSuffix?.let { " $it" } ?: ""),
                color = TextSoft, fontWeight = FontWeight.Medium, maxLines = 1, overflow = TextOverflow.Ellipsis
            )
            // Under a zone header the family is already the sub-header, so show that zone's own level
            // range instead (mobs.json stores a per-zone range); fall back to the mob's overall level.
            val sub = if (inZone != null) {
                val zl = mob.zones.firstOrNull { it.first == inZone }?.second?.let { "Lv $it" }
                    ?: mob.levelText.ifBlank { null }
                listOfNotNull(if (mob.nm) "NM" else null, zl).joinToString("  \u00b7  ")
            } else {
                listOfNotNull(mob.family.ifBlank { null }, mob.levelText.ifBlank { null }).joinToString("  \u00b7  ")
            }
            if (sub.isNotEmpty()) Text(sub, color = TextMuted, fontSize = 11.sp)
        }
    }
    HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun ZoneRow(vm: MobileWatchViewModel, zone: Zone) {
    Row(
        Modifier.fillMaxWidth().clickable { vm.selectZone(zone) }.padding(horizontal = 16.dp, vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(Icons.Filled.Place, null, tint = AccentGreen, modifier = Modifier.size(18.dp))
        Spacer(Modifier.width(10.dp))
        Column { Text(zone.name, color = TextSoft, fontWeight = FontWeight.Medium, maxLines = 1, overflow = TextOverflow.Ellipsis) }
    }
    HorizontalDivider(color = CharcoalDark)
}

// The top menu, in order. The pill row renders it and a horizontal swipe on the body steps
// through the same list, so the gesture and the menu can never disagree about what comes next.
private val MODES = listOf(
    "items" to "Items", "events" to "Events", "jobs" to "Jobs", "mobs" to "Bestiary",
    "maps" to "Zones", "content" to "Content", "hobbies" to "Hobbies", "trusts" to "Trusts",
    "chains" to "Chains"
)

@Composable
private fun SearchScreen(vm: MobileWatchViewModel) {
    val ui = vm.ui
    val mobs = ui.mode == "mobs"
    val items = ui.mode == "items"
    val groupExpanded = rememberSaveable(
        saver = listSaver(
            save = { map -> map.filterValues { it }.keys.toList() },
            restore = { keys -> mutableStateMapOf<String, Boolean>().apply { keys.forEach { put(it, true) } } }
        ),
        // rev 396: keyed on the page visit, exactly like CollapsibleSection, so
        // leaving the tab and coming back opens the list fully collapsed again.
        key = "browse_groups_${LocalPageVisit.current}"
    ) { mutableStateMapOf<String, Boolean>() }
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("MobileWatch", logoRes = R.drawable.mobilewatch_logo, onLogoClick = { vm.openSettings() }, actions = { WorldDropdown(ui.world, vm::setWorld) }) },
        bottomBar = { if (items) PopulationStrip(vm) }
    ) { pad ->
        val tabScroll = rememberScrollState()
        val modeIndex = MODES.indexOfFirst { it.first == ui.mode }
        // Eight pills do not fit on a phone, so pull the selected one into view whenever the mode
        // changes — otherwise a swipe can land you on a tab whose pill is off-screen.
        LaunchedEffect(ui.mode, tabScroll.maxValue) {
            if (modeIndex >= 0 && tabScroll.maxValue > 0)
                tabScroll.animateScrollTo(tabScroll.maxValue * modeIndex / (MODES.size - 1))
        }
        Column(
            Modifier.padding(pad).fillMaxSize()
                // Swipe left/right anywhere on the body to walk the top menu. The pill row above has
                // its own horizontal scroll and claims the gesture first, so dragging the pills still
                // just scrolls the pills. Clamped at both ends rather than wrapping.
                .pointerInput(ui.mode) {
                    var dx = 0f
                    val threshold = 72.dp.toPx()
                    detectHorizontalDragGestures(
                        onDragStart = { dx = 0f },
                        onDragEnd = {
                            if (modeIndex >= 0 && kotlin.math.abs(dx) > threshold)
                                MODES.getOrNull(if (dx < 0) modeIndex + 1 else modeIndex - 1)
                                    ?.let { vm.setMode(it.first) }
                        }
                    ) { _, amount -> dx += amount }
                }
        ) {
            Row(
                Modifier.fillMaxWidth().horizontalScroll(tabScroll)
                    .padding(horizontal = 12.dp, vertical = 6.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                MODES.forEach { (k, lbl) ->
                    val sel = ui.mode == k
                    Surface(
                        color = if (sel) Selection else Panel,
                        shape = RoundedCornerShape(8.dp),
                        modifier = Modifier.clickable { vm.setMode(k) }
                    ) {
                        Text(lbl, color = if (sel) TextPrimary else TextMuted, fontSize = 13.sp,
                            fontWeight = if (sel) FontWeight.Bold else FontWeight.Normal,
                            textAlign = TextAlign.Center, maxLines = 1,
                            modifier = Modifier.padding(horizontal = 18.dp, vertical = 9.dp))
                    }
                }
            }
            if (ui.mode != "chains" && ui.mode != "events" && ui.mode != "jobs" && ui.mode != "hobbies" && ui.mode != "content" && ui.mode != "trusts") {
                Row(
                    Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    OutlinedTextField(
                        value = ui.query, onValueChange = vm::onQueryChange,
                        modifier = Modifier.weight(1f), singleLine = true, shape = RoundedCornerShape(12.dp),
                        leadingIcon = { Icon(Icons.Filled.Search, null) },
                        trailingIcon = {
                            if (ui.query.isNotEmpty()) IconButton(onClick = { vm.onQueryChange("") }) {
                                Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                            }
                        },
                        placeholder = { Text(when (ui.mode) { "mobs" -> "Search mob or family"; "maps" -> "Search zone"; else -> "Search item" }, maxLines = 1, overflow = TextOverflow.Ellipsis) }
                    )
                }
                if (ui.mode == "mobs" || ui.mode == "maps") {
                    Row(
                        Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 2.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        if (ui.mode == "mobs") {
                            PickerButton("View", ui.mobView, listOf("all" to "All", "family" to "Family", "zone" to "Zone", "content" to "Content")) { vm.setMobView(it) }
                            PickerButton("Filter", ui.mobFilter, listOf("all" to "All", "nm" to "NM")) { vm.setMobFilter(it) }
                        } else {
                            PickerButton("View", ui.zoneView, listOf("all" to "All", "region" to "Region")) { vm.setZoneView(it) }
                            PickerButton("Filter", ui.zoneFilter, listOf("all" to "All", "City" to "City", "Field" to "Field", "Dungeon" to "Dungeon", "Battlefield" to "Battlefield")) { vm.setZoneFilter(it) }
                        }
                    }
                }
            }

            if (!ui.ready) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        CircularProgressIndicator(color = AccentGreen)
                        Spacer(Modifier.height(12.dp)); Text("Loading database\u2026", color = TextMuted)
                    }
                }
            } else if (mobs) {
                // HIDE_UNFAMILIED drops fam=="" records from BROWSING only (see the constant).
                // Search results are left whole so the bucket stays reachable by name.
                val mobList = ui.mobResults
                    .let { if (HIDE_UNFAMILIED && ui.query.isBlank()) it.filter { m -> m.family.isNotBlank() } else it }
                    .let { if (ui.mobFilter == "nm") it.filter { m -> m.nm } else it }
                // ecosystem -> (type -> mobs), memoized
                val nested = remember(mobList, ui.mobView) {
                    if (ui.mobView == "family")
                        mobList.groupBy { vm.ecosystemOf(it)?.ifBlank { null } ?: "Other" }.toSortedMap()
                            .mapValues { (_, ms) -> ms.groupBy { it.family.ifBlank { "Unknown" } }.toSortedMap() }
                    else null
                }
                // zone -> (family -> mobs). A mob is listed under EVERY zone it appears in; anything with
                // no zone data at all falls into NO_ZONE, which sorts last — that bucket is the to-do list.
                val zoneNested = remember(mobList, ui.mobView) {
                    if (ui.mobView != "zone") null else {
                        val acc = HashMap<String, MutableList<Mob>>()
                        mobList.forEach { mob ->
                            if (mob.zones.isEmpty()) acc.getOrPut(NO_ZONE) { mutableListOf() }.add(mob)
                            else mob.zones.map { it.first }.filter { it.isNotBlank() }.distinct()
                                .forEach { z -> acc.getOrPut(z) { mutableListOf() }.add(mob) }
                        }
                        // alphabetical, but NO_ZONE is pinned to the bottom so it never buries the real data
                        val ordered = LinkedHashMap<String, Map<String, List<Mob>>>()
                        acc.keys.filter { it != NO_ZONE }.sorted().forEach { z ->
                            ordered[z] = acc.getValue(z).groupBy { it.family.ifBlank { "Unknown" } }.toSortedMap()
                        }
                        acc[NO_ZONE]?.let { ordered[NO_ZONE] = it.groupBy { m -> m.family.ifBlank { "Unknown" } }.toSortedMap() }
                        ordered
                    }
                }
                // content -> (sub-group -> mobs). A mob is listed under EVERY content tag it carries.
                // UNTAGGED MOBS ARE EXCLUDED ENTIRELY (user, rev 187) — unlike the Zone view there is no
                // catch-all bucket, so the view is empty until tags exist.
                //
                // EACH CONTENT TYPE PICKS ITS OWN LAYOUT (user, rev 188: "The content entries will have
                // different layouts depending on what they are"):
                //   "Peculiar Foes"     -> Content > ZONE > mobs      (no family level)
                //   "Unity Mobs"        -> Content > mobs by LEVEL    (no sub-header at all)
                //   "Sortie: Section A" -> Content > SECTION > mobs   (boss, then NMs, then regular)
                //   "Odyssey: Sheol A"  -> Content > SECTION > mobs   (Gaol first; Atonement 4..1, then NMs)
                //   "Omen: Bosses"      -> Content > SECTION > mobs   (Ou carries ": Boss", mid-bosses are
                //                                                      nm, regular mobs sit in a 2nd section)
                //   "Dynamis: Dynamis-Bastok" / "Dynamis D: Dynamis-Bastok [D]" / "Abyssea: Abyssea-Altepa"
                //                       -> Content > ZONE section > mobs (bosses carry ": Boss", then NMs,
                //                          then regular; sections are the zones.json names, alphabetical).
                //                          These rosters are PROJECTED from each record's zone entries —
                //                          a content-exclusive zone needs no separate mob list.
                //   anything else       -> Content > FAMILY > mobs    (the default)
                // A tag carrying its own section wins over the per-name arms below, so any future
                // sectioned content works by tagging alone. A sub-group key of "" is the flat layout:
                // rows render straight under the content header.
                val contentNested = remember(mobList, ui.mobView) {
                    if (ui.mobView != "content") null else {
                        // group -> section -> mobs. Section "" = the tag declared none.
                        val acc = HashMap<String, HashMap<String, MutableList<Mob>>>()
                        mobList.forEach { mob ->
                            mob.content.filter { it.isNotBlank() }.distinct().forEach { tag ->
                                val (g, sec, _) = contentParts(tag)
                                if (g.isNotBlank()) acc.getOrPut(g) { HashMap() }
                                    .getOrPut(sec) { mutableListOf() }.add(mob)
                            }
                        }
                        val ordered = LinkedHashMap<String, Map<String, List<Mob>>>()
                        acc.keys.sorted().forEach { c ->
                            val bySection = acc.getValue(c)
                            val inTag = bySection.values.flatten().distinctBy { it.key }
                            ordered[c] = when {
                                // TAG-DECLARED SECTIONS (Sortie: Section A .. H) — the tag brings its own
                                // structure, so this arm needs no per-content-type code.
                                bySection.keys.any { it.isNotBlank() } -> {
                                    val out = LinkedHashMap<String, List<Mob>>()
                                    bySection.keys.filter { it.isNotBlank() }
                                        .sortedWith(compareBy({ sectionPriority(c, it) }, { it }))
                                        .forEach { sec ->
                                            out[sec] = bySection.getValue(sec).sortedWith(
                                                compareBy({ contentRank(it, c, sec) }, { it.levelLo }, { it.name })
                                            )
                                        }
                                    out
                                }
                                c == "Peculiar Foes" -> {
                                    val byZone = HashMap<String, MutableList<Mob>>()
                                    inTag.forEach { mob ->
                                        val zs = mob.zones.map { it.first }.filter { it.isNotBlank() }.distinct()
                                        if (zs.isEmpty()) byZone.getOrPut("Unknown") { mutableListOf() }.add(mob)
                                        else zs.forEach { z -> byZone.getOrPut(z) { mutableListOf() }.add(mob) }
                                    }
                                    byZone.toSortedMap().mapValues { (_, v) -> v.sortedBy { it.name } }
                                }
                                c == "Unity Mobs" -> mapOf(
                                    "" to inTag.sortedWith(compareBy({ it.levelLo }, { it.levelHi }, { it.name }))
                                )
                                else -> inTag.groupBy { it.family.ifBlank { "Unknown" } }.toSortedMap()
                            }
                        }
                        ordered
                    }
                }
                LazyColumn(Modifier.fillMaxSize()) {
                    if (contentNested != null) {
                        contentNested.forEach { (ctn, famMap) ->
                            val cKey = "content:$ctn"
                            val cOpen = groupExpanded[cKey] == true
                            val cCount = famMap.values.flatten().distinctBy { it.key }.size
                            item(key = cKey) {
                                GroupHeader(ctn, cCount, cOpen) {
                                    if (cOpen) groupExpanded[cKey] = false
                                    else { groupExpanded.keys.filter { it.startsWith("content:") }.forEach { groupExpanded[it] = false }; groupExpanded[cKey] = true }
                                }
                            }
                            if (cOpen) {
                                famMap.forEach { (sub, subMobs) ->
                                    if (sub.isBlank()) {
                                        // flat layout (Unity Mobs): no sub-header, rows are already ordered
                                        items(subMobs, key = { "$ctn||${it.key}" }) { mob -> MobRow(vm, mob) }
                                    } else {
                                        val fKey = "cfam:$ctn:$sub"
                                        val fOpen = groupExpanded[fKey] == true
                                        item(key = fKey) {
                                            SubGroupHeader(sub, subMobs.size, 1, fOpen) {
                                                if (fOpen) groupExpanded[fKey] = false
                                                else { groupExpanded.keys.filter { it.startsWith("cfam:$ctn:") }.forEach { groupExpanded[it] = false }; groupExpanded[fKey] = true }
                                            }
                                        }
                                        // under a ZONE sub-header show that zone's band (rule: MobRow's 3rd arg)
                                        val inZone = if (ctn == "Peculiar Foes") sub else null
                                        if (fOpen) items(subMobs, key = { "$ctn|$sub|${it.key}" }) { mob ->
                                            val role = contentRole(mob, ctn, sub)
                                            val suffix = when {
                                                role.equals("Arch Mega", ignoreCase = true) -> "(Arch Mega Boss)"
                                                role.equals("Mega", ignoreCase = true) -> "(Mega Boss)"
                                                role.equals("Disjoined", ignoreCase = true) -> "(Disjoined Boss)"
                                                role.equals("TE", ignoreCase = true) -> "(T.E.)"
                                                else -> null
                                            }
                                            MobRow(vm, mob, inZone, suffix)
                                        }
                                    }
                                }
                            }
                        }
                    } else if (zoneNested != null) {
                        zoneNested.forEach { (zone, famMap) ->
                            val zKey = "zone:$zone"
                            val zOpen = groupExpanded[zKey] == true
                            val zCount = famMap.values.sumOf { it.size }
                            item(key = zKey) {
                                GroupHeader(zone, zCount, zOpen) {
                                    if (zOpen) groupExpanded[zKey] = false
                                    else { groupExpanded.keys.filter { it.startsWith("zone:") }.forEach { groupExpanded[it] = false }; groupExpanded[zKey] = true }
                                }
                            }
                            if (zOpen) {
                                famMap.forEach { (fam, famMobs) ->
                                    val fKey = "zfam:$zone:$fam"
                                    val fOpen = groupExpanded[fKey] == true
                                    item(key = fKey) {
                                        SubGroupHeader(fam, famMobs.size, 1, fOpen) {
                                            if (fOpen) groupExpanded[fKey] = false
                                            else { groupExpanded.keys.filter { it.startsWith("zfam:$zone:") }.forEach { groupExpanded[it] = false }; groupExpanded[fKey] = true }
                                        }
                                    }
                                    if (fOpen) items(famMobs, key = { "$zone|${it.key}" }) { mob -> MobRow(vm, mob, zone) }
                                }
                            }
                        }
                    } else if (nested != null) {
                        nested.forEach { (eco, typeMap) ->
                            val ecoKey = "eco:$eco"
                            val ecoOpen = groupExpanded[ecoKey] == true
                            item(key = ecoKey) {
                                GroupHeader(eco, typeMap.size, ecoOpen) {
                                    if (ecoOpen) groupExpanded[ecoKey] = false
                                    else { groupExpanded.keys.filter { it.startsWith("eco:") }.forEach { groupExpanded[it] = false }; groupExpanded[ecoKey] = true }
                                }
                            }
                            if (ecoOpen) {
                                typeMap.forEach { (type, typeMobs) ->
                                    val typeKey = "type:$eco:$type"
                                    val typeOpen = groupExpanded[typeKey] == true
                                    val subGroups = typeMobs.groupBy { it.sub ?: type }
                                    item(key = typeKey) {
                                        SubGroupHeader(type, typeMobs.size, subGroups.size, typeOpen) {
                                            if (typeOpen) groupExpanded[typeKey] = false
                                            else { groupExpanded.keys.filter { it.startsWith("type:$eco:") }.forEach { groupExpanded[it] = false }; groupExpanded[typeKey] = true }
                                        }
                                    }
                                    if (typeOpen) {
                                        if (subGroups.size <= 1) {
                                            items(typeMobs, key = { it.key }) { mob -> MobRow(vm, mob) }
                                        } else {
                                            subGroups.entries.sortedBy { if (it.key == type) "" else it.key }.forEach { (subName, subMobs) ->
                                                val subKey = "sub:$eco:$type:$subName"
                                                val subOpen = groupExpanded[subKey] == true
                                                item(key = subKey) {
                                                    SubSubHeader(subName, subMobs.size, subOpen) {
                                                        if (subOpen) groupExpanded[subKey] = false
                                                        else { groupExpanded.keys.filter { it.startsWith("sub:$eco:$type:") }.forEach { groupExpanded[it] = false }; groupExpanded[subKey] = true }
                                                    }
                                                }
                                                if (subOpen) items(subMobs, key = { it.key }) { mob -> MobRow(vm, mob) }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } else {
                        items(mobList, key = { it.key }) { mob -> MobRow(vm, mob) }
                    }
                }
            } else if (ui.mode == "jobs") {
                JobListContent(vm)
            } else if (ui.mode == "events") {
                EventsContent(vm)
            } else if (ui.mode == "chains") {
                SkillchainContent(vm)
            } else if (ui.mode == "hobbies") {
                HobbiesContent(vm)
            } else if (ui.mode == "trusts") {
                TrustsContent(vm)
            } else if (ui.mode == "content") {
                ContentTabContent(vm)
            } else if (ui.mode == "maps") {
                val zoneList = if (ui.zoneFilter == "all") ui.zoneResults
                else ui.zoneResults.filter { vm.zoneType(it).equals(ui.zoneFilter, true) }
                val zoneGroups = remember(zoneList, ui.zoneView) {
                    if (ui.zoneView == "region") zoneList.groupBy { vm.zoneRegion(it) }.toSortedMap() else null
                }
                LazyColumn(Modifier.fillMaxSize()) {
                    if (zoneGroups != null) {
                        zoneGroups.forEach { (reg, list) ->
                            val open = groupExpanded[reg] == true
                            item(key = "reg_$reg") { GroupHeader(reg, list.size, open) { if (open) groupExpanded[reg] = false else { groupExpanded.clear(); groupExpanded[reg] = true } } }
                            if (open) items(list, key = { it.id }) { zone -> ZoneRow(vm, zone) }
                        }
                    } else {
                        items(zoneList, key = { it.id }) { zone -> ZoneRow(vm, zone) }
                    }
                }
            } else {
                LazyColumn(Modifier.fillMaxSize()) {
                    items(ui.results, key = { it.id }) { item ->
                        Row(Modifier.fillMaxWidth().clickable { vm.select(item) },
                            verticalAlignment = Alignment.CenterVertically) {
                            Box(Modifier.width(3.dp).height(38.dp).background(AccentGreen.copy(alpha = 0.55f)))
                            Column(Modifier.padding(horizontal = 14.dp, vertical = 10.dp)) {
                                Text(vm.label(item), color = TextSoft, maxLines = 1,
                                    overflow = TextOverflow.Ellipsis, fontWeight = FontWeight.Medium)
                                if (item.category.isNotBlank())
                                    Text(item.category, color = TextMuted, fontSize = 11.sp, maxLines = 1)
                            }
                        }
                        HorizontalDivider(color = CharcoalDark)
                    }
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun WorldDropdown(world: String, onPick: (String) -> Unit) {
    var open by remember { mutableStateOf(false) }
    ExposedDropdownMenuBox(expanded = open, onExpandedChange = { open = it }) {
        OutlinedButton(
            onClick = { open = true },
            modifier = Modifier.menuAnchor().width(170.dp),
            contentPadding = PaddingValues(horizontal = 12.dp, vertical = 6.dp)
        ) {
            Text(world, color = TextPrimary, fontSize = 14.sp, maxLines = 1,
                overflow = TextOverflow.Ellipsis, modifier = Modifier.weight(1f))
            Icon(Icons.Filled.ArrowDropDown, null, tint = TextPrimary)
        }
        ExposedDropdownMenu(expanded = open, onDismissRequest = { open = false }) {
            Worlds.names.forEach { w ->
                DropdownMenuItem(text = { Text(w) }, onClick = { open = false; onPick(w) })
            }
        }
    }
}

@Composable
private fun PopulationStrip(vm: MobileWatchViewModel) {
    val ui = vm.ui
    Box(Modifier.fillMaxWidth().background(Brush.verticalGradient(listOf(CharcoalDark, PopStripTint)))) {
        Column(Modifier.fillMaxWidth().padding(horizontal = 14.dp, vertical = 8.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(Modifier.size(8.dp).background(AccentGreen, CircleShape))
                Spacer(Modifier.width(8.dp))
                Text(ui.world, color = AccentGold, fontWeight = FontWeight.SemiBold, fontSize = 15.sp, maxLines = 1)
            }
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                Text(ui.population, color = AccentGreen, fontWeight = FontWeight.Medium,
                    fontSize = 14.sp, maxLines = 1, modifier = Modifier.weight(1f))
                TextButton(
                    onClick = { vm.refreshPopulation() },
                    contentPadding = PaddingValues(horizontal = 12.dp, vertical = 4.dp)
                ) { Text("Refresh", fontSize = 14.sp, maxLines = 1) }
            }
        }
    }
}

/** Family icon from assets on a light tile (JPGs have white backgrounds). */
@Composable
private fun FamilyIcon(vm: MobileWatchViewModel, family: String, size: Dp) {
    val ctx = LocalContext.current
    val path = remember(family) { vm.mobIconPath(family) }
    val bmp = remember(path) {
        path?.let { p ->
            runCatching { ctx.assets.open(p).use { BitmapFactory.decodeStream(it)?.asImageBitmap() } }.getOrNull()
        }
    }
    Surface(shape = RoundedCornerShape(10.dp), color = Color(0xFFECECEC), modifier = Modifier.size(size)) {
        if (bmp != null) {
            Image(bmp, family, modifier = Modifier.fillMaxSize().padding(2.dp), contentScale = ContentScale.Fit)
        } else {
            Box(Modifier.fillMaxSize().padding(6.dp), contentAlignment = Alignment.Center) {
                Icon(painterResource(R.drawable.ic_mob_placeholder), null, tint = TextMuted)
            }
        }
    }
}

@Composable
private fun MobDetailScreen(vm: MobileWatchViewModel) {
    val mob = vm.ui.selectedMob ?: return
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(mob.name, onBack = { vm.clearMob() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize().padding(horizontal = 16.dp)) {
            item { WikiLinks(mob.name) }
            item {
                Spacer(Modifier.height(6.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    SubtypeImage(vm.iconForMob(mob), 84.dp)
                    Spacer(Modifier.width(14.dp))
                    Column {
                        if (mob.family.isNotEmpty())
                            Text(mob.family, color = AccentGold, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        vm.ecosystemOf(mob)?.takeIf { it.isNotBlank() }?.let {
                            Text(it, color = TextMuted, fontSize = 11.sp)
                        }
                        // With no zone context the header can only show the GLOBAL lv band, which is a
                        // summary across independent per-zone ranges — say so rather than let it read as
                        // one continuous range. The real per-zone values are in the Zones section.
                        val zoneLvls = mob.zones.mapNotNull { it.second }.distinct()
                        val lvlText = if (vm.ui.mobLevelCtx.isNotEmpty()) "Lv ${vm.ui.mobLevelCtx}" else mob.levelText
                        if (lvlText.isNotEmpty()) Text(lvlText, color = TextSoft, fontSize = 13.sp)
                        if (vm.ui.mobLevelCtx.isEmpty() && zoneLvls.size > 1)
                            Text("varies by zone \u2014 see Zones", color = TextMuted, fontSize = 11.sp)
                        val tags = buildList {
                            if (mob.aggro) add("Aggressive"); if (mob.links) add("Links"); if (mob.nm) add("NM")
                        }
                        if (tags.isNotEmpty()) Text(tags.joinToString("  \u00b7  "), color = TextMuted, fontSize = 12.sp)
                    }
                }
            }
            item {
                Spacer(Modifier.height(8.dp))
                CollapsibleSection("Details") {
                    SectionCard(color = Panel) {
                        if (mob.detects.isNotEmpty()) InfoRow("Detects", mob.detects, AccentGold)
                        if (mob.job.isNotEmpty()) InfoRow("Job", listOf(mob.job), TextSoft)
                        if (mob.respawnText.isNotEmpty()) InfoRow("Respawn", listOf(mob.respawnText), TextSoft)
                        if (mob.crystal.isNotEmpty()) InfoRow("Crystal", listOf(mob.crystal), JobsBlue)
                        if (mob.spawn.isNotEmpty()) InfoRow("Spawn", listOf(mob.spawn), AccentGreen)
                        if (mob.farm.isNotEmpty()) FarmingBlock(mob.farm)
                        if (mob.drops.isNotEmpty()) InfoRow("Drops", listOf(mob.drops), AccentGold)
                        val resistSets = vm.resistSets(mob.family)
                        val hasMods = mob.weaknesses.isNotEmpty() || mob.strengths.isNotEmpty()
                        // A family with resist sets shows the swipeable grid, but a member with its
                        // OWN distinct grid (e.g. Glassy Craver's fixed Geas Fete resists) shows that.
                        val ownGridMatchesASet = resistSets.any {
                            it.weaknesses == mob.weaknesses && it.strengths == mob.strengths
                        }
                        if (resistSets.isNotEmpty() && (!hasMods || ownGridMatchesASet))
                            SwipeableResistGrid(resistSets, mob.weaknesses, mob.strengths)
                        else if (hasMods) ResistGrid(mob.weaknesses, mob.strengths, mob.absorb)
                        ModRow("Weak to", mob.weaknesses.filter { it.first !in RES_KNOWN })
                        ModRow("Strong", mob.strengths.filter { it.first !in RES_KNOWN })
                        if (mob.immune.isNotEmpty()) InfoRow("Immune", mob.immune, AccentGold)
                        if (mob.absorb.isNotEmpty()) InfoRow("Absorbs", mob.absorb, JobsBlue)
                        if (mob.weaknesses.isEmpty() && mob.strengths.isEmpty() &&
                            mob.immune.isEmpty() && mob.absorb.isEmpty()) {
                            Text("No notable damage modifiers.", color = TextMuted, fontSize = 12.sp)
                        }
                    }
                }
            }
            if (mob.abilities.isNotEmpty()) {
                item {
                    CollapsibleSection("Abilities") {
                        SectionCard(color = Panel) {
                            mob.abilities.forEachIndexed { i, a ->
                                AbilityRow(vm, a, showDivider = i != mob.abilities.lastIndex)
                            }
                        }
                    }
                }
            }
            // Always rendered, even with no data: an empty Zones card flags a mob still needing zones.
            item {
                CollapsibleSection("Zones") {
                    SectionCard(color = Panel) {
                        mob.zones.forEachIndexed { i, z ->
                            MobZoneRow(z.first, z.second, showDivider = i != mob.zones.lastIndex)
                        }
                    }
                }
            }
            if (mob.spells.isNotEmpty()) {
                item {
                    CollapsibleSection("Spells") {
                        SectionCard(color = Panel) {
                            Text(mob.spells.joinToString(", "), color = TextSoft, fontSize = 13.sp)
                        }
                    }
                }
            }
            val generalNotes = buildList {
                addAll(mob.notes)
                addAll(vm.subtypeNotes(mob))
                addAll(vm.familyNotes(mob.family))
            }.distinct()
            if (generalNotes.isNotEmpty()) { item { GeneralNotesSection(generalNotes) } }
            item { MobNotes(vm, mob.key) }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun SubtypeImage(path: String?, size: Dp) {
    val ctx = LocalContext.current
    val bmp = remember(path) {
        path?.let { p -> runCatching { ctx.assets.open(p).use { BitmapFactory.decodeStream(it)?.asImageBitmap() } }.getOrNull() }
    }
    Surface(shape = RoundedCornerShape(10.dp), color = Color(0xFFECECEC), modifier = Modifier.size(size)) {
        if (bmp != null) Image(bmp, null, modifier = Modifier.fillMaxSize().padding(2.dp), contentScale = ContentScale.Fit)
        else Box(Modifier.fillMaxSize().padding(6.dp), contentAlignment = Alignment.Center) {
            Icon(painterResource(R.drawable.ic_mob_placeholder), null, tint = TextMuted)
        }
    }
}

/** A sub-type reprints the family's info with its own image + resistances (e.g. Lynx, Skormoth). */
@Composable
private fun SubtypeDetailScreen(vm: MobileWatchViewModel) {
    val base = vm.ui.selectedMob ?: return
    val sub = vm.ui.selectedSubtype ?: return
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(sub.name, onBack = { vm.clearSubtype() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize().padding(horizontal = 16.dp)) {
            item {
                Spacer(Modifier.height(6.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    SubtypeImage(sub.image ?: vm.mobIconPath(base.family), 84.dp)
                    Spacer(Modifier.width(14.dp))
                    Column {
                        Text(sub.name, color = AccentGold, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                        Text("Sub-type of ${base.family}", color = TextSoft, fontSize = 13.sp)
                    }
                }
            }
            item {
                Spacer(Modifier.height(8.dp))
                CollapsibleSection("Details") {
                    SectionCard(color = Panel) {
                        if (base.job.isNotEmpty()) InfoRow("Job", listOf(base.job), TextSoft)
                        if (base.crystal.isNotEmpty()) InfoRow("Crystal", listOf(base.crystal), JobsBlue)
                        if (sub.weaknesses.isNotEmpty() || sub.strengths.isNotEmpty())
                            ResistGrid(sub.weaknesses, sub.strengths, emptyList())
                        else
                            Text("Same resistances as ${base.family}.", color = TextMuted, fontSize = 12.sp)
                    }
                }
            }
            if (base.abilities.isNotEmpty()) {
                item {
                    CollapsibleSection("Abilities") {
                        SectionCard(color = Panel) {
                            base.abilities.forEachIndexed { i, a ->
                                AbilityRow(vm, a, showDivider = i != base.abilities.lastIndex)
                            }
                        }
                    }
                }
            }
            val notes = buildList {
                addAll(sub.notes)
                addAll(vm.familyNotes(base.family))
            }.distinct()
            if (notes.isNotEmpty()) { item { GeneralNotesSection(notes) } }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun GeneralNotesSection(notes: List<String>) {
    if (notes.isEmpty()) return
    CollapsibleSection("General Notes") {
        SectionCard(color = Panel) {
            notes.forEach { n ->
                Row(Modifier.fillMaxWidth().padding(vertical = 2.dp)) {
                    Text("\u2022", color = TextMuted, fontSize = 13.sp, modifier = Modifier.padding(end = 8.dp))
                    Text(n, color = TextSoft, fontSize = 13.sp, lineHeight = 18.sp)
                }
            }
        }
    }
}

private fun elemColor(name: String): Color = when (name) {
    "Fire" -> Color(0xFFE58A6A)
    "Ice" -> Color(0xFF9BD3E0)
    "Wind" -> Color(0xFF9AD39A)
    "Earth" -> Color(0xFFC9B37A)
    "Lightning" -> Color(0xFFD98AD9)
    "Water" -> Color(0xFF7FB0DC)
    "Light" -> Color(0xFFEDEDED)
    "Dark" -> Color(0xFFB89AE0)
    else -> TextSoft   // physical: Slashing / Piercing / H2H / Impact
}

// Wiki resistance box: top row = damage types, bottom row = elements (in wiki order).
private val ELEM_ORDER = listOf("Fire", "Wind", "Lightning", "Light", "Ice", "Earth", "Water", "Dark")
private val ELEM_SET = ELEM_ORDER.toSet()
// display label -> the wk/st names that feed it (Blunt is stored as "Impact")
private val PHYS_SPECS = listOf(
    "Physical" to listOf("Physical"),
    "Magical" to listOf("Magical"),
    "Breath" to listOf("Breath"),
    "Slashing" to listOf("Slashing"),
    "Blunt" to listOf("Blunt", "Impact"),
    "H2H" to listOf("H2H", "Hand-to-Hand"),
    "Piercing" to listOf("Piercing"),
    "Ranged" to listOf("Ranged", "Ranged Attacks"),
)
private val ELEM_SPECS = ELEM_ORDER.map { it to listOf(it) }
// every name the grid already accounts for, so leftover modifiers can still be listed as text
private val RES_KNOWN = (ELEM_ORDER + PHYS_SPECS.flatMap { it.second }).toSet()

/** "+30%" -> 130, "-50%" -> 50, null/garbage -> null. */
/** "+30%" -> "130%", "-12.5%" -> "87.5%", null/garbage -> null. */
private fun parsePctDelta(delta: String?): String? {
    val s = delta?.trim()?.removeSuffix("%") ?: return null
    val v = s.toDoubleOrNull() ?: return null
    val pct = 100 + v
    return if (pct == pct.toLong().toDouble()) "${pct.toLong()}%" else "$pct%"
}

@Composable
private fun ResCell(label: String, pct: String?, state: Int, absorbs: Boolean, modifier: Modifier) {
    val valColor = when {
        absorbs -> JobsBlue
        state > 0 -> AccentGreen
        state < 0 -> AccentRed
        else -> TextMuted
    }
    val valText = when {
        absorbs -> "Abs"
        pct != null -> pct
        state > 0 -> "Weak"
        state < 0 -> "Res"
        else -> "100%"
    }
    Column(modifier, horizontalAlignment = Alignment.CenterHorizontally) {
        Text(label, color = elemColor(label), fontSize = 10.sp, fontWeight = FontWeight.Medium, maxLines = 1)
        Text(valText, color = valColor, fontSize = 13.sp, fontWeight = FontWeight.Bold)
    }
}

@Composable
private fun ResistRows(
    specs: List<Pair<String, List<String>>>,
    weak: Map<String, String?>, strong: Map<String, String?>, absorbSet: Set<String>
) {
    for (base in specs.indices step 4) {
        Row(Modifier.fillMaxWidth().padding(vertical = 3.dp)) {
            for (c in 0 until 4) {
                val idx = base + c
                if (idx < specs.size) {
                    val (label, names) = specs[idx]
                    var pct: String? = "100%"; var state = 0
                    for (n in names) {
                        if (weak.containsKey(n)) { pct = parsePctDelta(weak[n]); state = 1; break }
                        if (strong.containsKey(n)) { pct = parsePctDelta(strong[n]); state = -1; break }
                    }
                    ResCell(label, pct, state, label in absorbSet, Modifier.weight(1f))
                } else Spacer(Modifier.weight(1f))
            }
        }
    }
}

/** Recreates the wiki strength/weakness box: damage types on top, elements below. green = weak, red = resist. */
@Composable
private fun ResistGrid(
    weaknesses: List<Pair<String, String?>>,
    strengths: List<Pair<String, String?>>,
    absorb: List<String>
) {
    val weak = weaknesses.toMap()
    val strong = strengths.toMap()
    val absorbSet = absorb.toSet()
    Column(Modifier.fillMaxWidth().padding(vertical = 2.dp)) {
        Text("Resistances", color = TextMuted, fontSize = 12.sp, modifier = Modifier.padding(bottom = 4.dp))
        ResistRows(PHYS_SPECS, weak, strong, absorbSet)
        Spacer(Modifier.height(2.dp))
        ResistRows(ELEM_SPECS, weak, strong, absorbSet)
    }
}

/** Resist box for families that shift resistances mid-fight — shows one named set at a time with < > to cycle.
 *  Opens on the set matching the mob's own wk/st (its color), else the first set. */
@Composable
private fun SwipeableResistGrid(
    sets: List<ResistSet>,
    mobWeak: List<Pair<String, String?>> = emptyList(),
    mobStrong: List<Pair<String, String?>> = emptyList()
) {
    if (sets.isEmpty()) return
    val startIdx = remember(sets, mobWeak, mobStrong) {
        sets.indexOfFirst { it.weaknesses == mobWeak && it.strengths == mobStrong }.let { if (it >= 0) it else 0 }
    }
    var idx by remember(startIdx) { mutableStateOf(startIdx) }
    val set = sets[idx.coerceIn(0, sets.size - 1)]
    val weak = set.weaknesses.toMap()
    val strong = set.strengths.toMap()
    Column(
        Modifier
            .fillMaxWidth()
            .padding(vertical = 2.dp)
            // Swipe left/right to cycle sets, in addition to the arrows. Horizontal-drag detection
            // waits for horizontal touch-slop, so vertical drags fall through to the mob card's
            // LazyColumn scroll untouched. One cycle fires per swipe past the threshold (on drag end).
            .then(
                if (sets.size > 1) Modifier.pointerInput(sets) {
                    var dx = 0f
                    val threshold = 36.dp.toPx()
                    detectHorizontalDragGestures(
                        onDragStart = { dx = 0f },
                        onDragEnd = {
                            when {
                                dx <= -threshold -> idx = (idx + 1) % sets.size
                                dx >= threshold -> idx = (idx - 1 + sets.size) % sets.size
                            }
                        },
                        onHorizontalDrag = { change, amount -> dx += amount; change.consume() }
                    )
                } else Modifier
            )
    ) {
        Row(Modifier.fillMaxWidth().padding(bottom = 4.dp), verticalAlignment = Alignment.CenterVertically) {
            Text("Resistances", color = TextMuted, fontSize = 12.sp, maxLines = 1, softWrap = false, modifier = Modifier.weight(1f))
            if (sets.size > 1) Text("\u2039", color = AccentGold, fontSize = 20.sp, fontWeight = FontWeight.Bold,
                modifier = Modifier.clickable { idx = (idx - 1 + sets.size) % sets.size }.padding(horizontal = 10.dp))
            Text(set.label, color = TextPrimary, fontSize = 12.sp, fontWeight = FontWeight.Medium)
            if (sets.size > 1) Text("\u203a", color = AccentGold, fontSize = 20.sp, fontWeight = FontWeight.Bold,
                modifier = Modifier.clickable { idx = (idx + 1) % sets.size }.padding(horizontal = 10.dp))
        }
        ResistRows(PHYS_SPECS, weak, strong, emptySet())
        Spacer(Modifier.height(2.dp))
        ResistRows(ELEM_SPECS, weak, strong, emptySet())
    }
}

@Composable
private fun ModRow(label: String, mods: List<Pair<String, String?>>) {
    if (mods.isEmpty()) return
    Row(Modifier.fillMaxWidth().padding(vertical = 3.dp)) {
        Text("$label:", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 92.dp))
        Text(
            buildAnnotatedString {
                mods.forEachIndexed { i, (n, p) ->
                    if (i > 0) withStyle(SpanStyle(color = TextMuted)) { append("   ") }
                    withStyle(SpanStyle(color = elemColor(n))) { append(n) }
                    if (p != null) withStyle(SpanStyle(color = TextMuted)) { append(" $p") }
                }
            },
            fontSize = 13.sp
        )
    }
}

/** The pop path for a mob that has one — one line per step, in order. */
@Composable
private fun FarmingBlock(steps: List<String>) {
    Column(Modifier.padding(top = 6.dp, bottom = 2.dp)) {
        Text("Farming", color = AccentGold, fontSize = 13.sp, fontWeight = FontWeight.Bold)
        steps.forEach { step ->
            Row(Modifier.padding(top = 3.dp)) {
                Text("\u2022", color = TextMuted, fontSize = 13.sp, modifier = Modifier.padding(end = 6.dp))
                Text(step, color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp)
            }
        }
    }
}

@Composable
private fun InfoRow(label: String, values: List<String>, color: Color) {
    if (values.isEmpty()) return
    Row(Modifier.padding(vertical = 3.dp)) {
        Text("$label:", color = TextMuted, fontSize = 13.sp, maxLines = 1, modifier = Modifier.widthIn(min = 92.dp).padding(end = 6.dp))
        Text(values.joinToString(", "), color = color, fontSize = 13.sp)
    }
}

/** One row of the mob card's Zones section: zone name, plus its level range in that zone when known. */
@Composable
private fun MobZoneRow(zone: String, levels: String?, showDivider: Boolean) {
    Row(Modifier.fillMaxWidth().padding(vertical = 5.dp), verticalAlignment = Alignment.CenterVertically) {
        Text(zone, color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
        if (!levels.isNullOrBlank())
            Text(if (levels.firstOrNull()?.isDigit() == true) "Lv $levels" else levels, color = AccentGold, fontSize = 12.sp)
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun PhysRow(phys: Map<String, Double>) {
    if (phys.isEmpty()) return
    val labels = mapOf("slashing" to "Slashing", "piercing" to "Piercing", "h2h" to "H2H", "impact" to "Blunt")
    val txt = phys.entries.joinToString(", ") { "${labels[it.key] ?: it.key} \u00d7${it.value}" }
    Row(Modifier.padding(vertical = 3.dp)) {
        Text("Physical:", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 92.dp))
        Text(txt, color = TextSoft, fontSize = 13.sp)
    }
}

@Composable
private fun SectionHeader(title: String) {
    Spacer(Modifier.height(14.dp))
    Text(title, color = HeaderL1, fontWeight = FontWeight.Bold, fontSize = 14.sp)
    Spacer(Modifier.height(2.dp))
}

/**
 * The top-level entry of a flat tab menu (Jobs, Content, the Chains reference link).
 *
 * Tabs whose top level is a GROUP get [GroupHeader]; tabs whose top level is a flat menu used to
 * hand-roll a Text row, which is how three of them drifted to white while the rest read gold.
 * Everything at level 1 goes through here or GroupHeader now — both use HeaderL1.
 */
@Composable
private fun TopLevelRow(
    label: String,
    enabled: Boolean = true,
    trailing: String? = null,
    subtitle: String? = null,
    // 0 when the caller's own column already insets (the Chains tab does)
    insetDp: Int = 16,
    onClick: () -> Unit,
) {
    Row(
        Modifier.fillMaxWidth()
            .then(if (enabled) Modifier.clickable { onClick() } else Modifier)
            .padding(horizontal = insetDp.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(Modifier.weight(1f)) {
            Text(label, color = if (enabled) HeaderL1 else TextMuted,
                fontWeight = FontWeight.Bold, fontSize = 16.sp)
            if (!subtitle.isNullOrBlank())
                Text(subtitle, color = TextMuted, fontSize = 11.sp, modifier = Modifier.padding(top = 1.dp))
        }
        if (trailing != null) Text(trailing, color = TextMuted, fontSize = 12.sp)
    }
    HorizontalDivider(color = CharcoalDark)
}

/**
 * CollapsibleSection's header row on its own, for LazyColumn use — the section body has to stay
 * lazy (the Trusts roster is 122 rows), so it cannot be a content lambda.
 */
@Composable
private fun SectionToggleRow(title: String, expanded: Boolean, count: Int? = null, onClick: () -> Unit) {
    Spacer(Modifier.height(14.dp))
    Row(
        Modifier.fillMaxWidth().clickable { onClick() }.padding(horizontal = 16.dp, vertical = 2.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(title, color = HeaderL1, fontWeight = FontWeight.Bold, fontSize = 14.sp,
            modifier = Modifier.weight(1f))
        if (count != null) Text(count.toString(), color = TextMuted, fontSize = 12.sp,
            modifier = Modifier.padding(end = 4.dp))
        Icon(if (expanded) Icons.Filled.ArrowDropUp else Icons.Filled.ArrowDropDown, null, tint = TextMuted)
    }
    Spacer(Modifier.height(2.dp))
}

@Composable
private fun CollapsibleSection(title: String, initiallyExpanded: Boolean = false, stateKey: String = title, persist: Boolean = true, subtitle: String? = null, titleColor: Color = HeaderL1, content: @Composable () -> Unit) {
    val visit = LocalPageVisit.current
    val expandedState = if (persist) rememberSaveable(key = "collapse_${stateKey}_$visit") { mutableStateOf(initiallyExpanded) }
                        else remember { mutableStateOf(initiallyExpanded) }
    var expanded by expandedState
    Spacer(Modifier.height(14.dp))
    Row(
        Modifier.fillMaxWidth().clickable { expanded = !expanded }.padding(vertical = 2.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // subtitle = an optional 2nd line under the header (Apex/Locus puts the zone's level band there)
        Column(Modifier.weight(1f)) {
            Text(title, color = titleColor, fontWeight = FontWeight.Bold, fontSize = 14.sp)
            if (!subtitle.isNullOrBlank())
                Text(subtitle, color = TextMuted, fontSize = 11.sp, modifier = Modifier.padding(top = 1.dp))
        }
        Icon(if (expanded) Icons.Filled.ArrowDropUp else Icons.Filled.ArrowDropDown, null, tint = TextMuted)
    }
    Spacer(Modifier.height(2.dp))
    if (expanded) content()
}

@Composable
private fun AbilityRow(vm: MobileWatchViewModel, name: String, showDivider: Boolean = true) {
    val info = remember(name) { vm.ability(name) }
    var open by remember { mutableStateOf(false) }
    Column(
        Modifier.fillMaxWidth()
            .clickable(enabled = info?.desc != null) { open = !open }
            .padding(vertical = 7.dp)
    ) {
        Text(name, color = AccentRed, fontSize = 13.sp, fontWeight = FontWeight.Medium)
        if (info != null) {
            val t = info.type; val el = info.element
            if (!t.isNullOrBlank() || !el.isNullOrBlank())
                Text(
                    buildAnnotatedString {
                        if (!t.isNullOrBlank()) withStyle(SpanStyle(color = TextMuted)) { append(t) }
                        if (!el.isNullOrBlank()) {
                            if (!t.isNullOrBlank()) withStyle(SpanStyle(color = TextMuted)) { append("  \u00b7  ") }
                            withStyle(SpanStyle(color = elemColor(el))) { append(el) }
                        }
                    },
                    fontSize = 11.sp, modifier = Modifier.padding(start = 14.dp, top = 1.dp)
                )
            val fx = info.effects.joinToString(", ")
            val line = listOfNotNull(info.target, fx.ifEmpty { null }).joinToString("  \u2192  ")
            if (line.isNotEmpty())
                Text(line, color = TextPrimary, fontSize = 12.sp,
                    modifier = Modifier.padding(start = 14.dp, top = 2.dp))
        }
        if (open && info?.desc != null) {
            Text(info.desc, color = TextMuted, fontSize = 12.sp, modifier = Modifier.padding(top = 3.dp))
            info.notes?.let { Text(it, color = TextMuted, fontSize = 11.sp, modifier = Modifier.padding(top = 2.dp)) }
            info.range?.let { Text("Range: $it", color = TextMuted, fontSize = 11.sp, modifier = Modifier.padding(top = 2.dp)) }
        }
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun DetailScreen(vm: MobileWatchViewModel) {
    val ui = vm.ui
    val item = ui.selected ?: return
    val ctx = LocalContext.current
    fun open(url: String) = ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))

    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(item.name, onBack = { vm.back() }, trailing = "[${item.id}]") },
        bottomBar = { PopulationStrip(vm) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize().padding(horizontal = 16.dp)) {
            item {
                Spacer(Modifier.height(10.dp))
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    Text(metaLine(item), color = TextMuted, fontSize = 13.sp, modifier = Modifier.weight(1f))
                    if (item.stack > 1) Text("Stacks to ${item.stack}", color = TextSoft, fontSize = 13.sp)
                }
                if (item.desc.isNotEmpty()) {
                    Spacer(Modifier.height(8.dp))
                    Surface(color = CharcoalDark, shape = RoundedCornerShape(8.dp), modifier = Modifier.fillMaxWidth()) {
                        Text(item.desc, color = TextSoft, fontSize = 13.sp,
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp))
                    }
                }
                val jobs = FfxiDecode.jobs(item.jobsMask)
                if (jobs.isNotEmpty()) { Spacer(Modifier.height(6.dp)); Text("Jobs:  $jobs", color = JobsBlue, fontSize = 13.sp) }
                Spacer(Modifier.height(10.dp))
                val nm = item.name.replace(" ", "_")
                val linkPad = PaddingValues(horizontal = 4.dp, vertical = 6.dp)
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    OutlinedButton(onClick = { open("https://www.ffxiah.com/item/${item.id}") },
                        modifier = Modifier.weight(1f), contentPadding = linkPad) {
                        Text("FFXIAH", fontSize = 12.sp, maxLines = 1)
                    }
                    OutlinedButton(onClick = { open("https://www.bg-wiki.com/ffxi/$nm") },
                        modifier = Modifier.weight(1f), contentPadding = linkPad) {
                        Text("BG-wiki", fontSize = 12.sp, maxLines = 1)
                    }
                    OutlinedButton(onClick = { open("https://ffxiclopedia.fandom.com/wiki/$nm") },
                        modifier = Modifier.weight(1f), contentPadding = linkPad) {
                        Text("FFXIclopedia", fontSize = 11.sp, maxLines = 1)
                    }
                }
                Spacer(Modifier.height(10.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Server:", color = TextMuted, fontSize = 13.sp)
                    Spacer(Modifier.width(8.dp))
                    WorldDropdown(ui.world, vm::setWorld)
                }
                if (item.stack > 1) {
                    Spacer(Modifier.height(12.dp))
                    FilterRow(ui.filter, vm::setFilter)
                }
                Spacer(Modifier.height(8.dp))
                SectionCard(color = Panel) {
                    Text("On sale now:  ${onsaleText(ui.onsaleSingle)} single  /  ${onsaleText(ui.onsaleStack)} stack",
                        color = AccentGold, fontSize = 13.sp)
                    SummaryLine(vm)
                }
                Spacer(Modifier.height(10.dp))
                Text("Auction history", color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                Spacer(Modifier.height(2.dp))
            }
            if (ui.historyLoading) {
                item { Box(Modifier.fillMaxWidth().padding(16.dp), Alignment.Center) { CircularProgressIndicator(color = AccentGreen) } }
            } else if (ui.historyNote != null) {
                item { Text(ui.historyNote!!, color = TextMuted, modifier = Modifier.padding(vertical = 12.dp)) }
            } else {
                items(vm.visibleSales()) { s -> SaleRowView(s) }
            }
            item { CrossServerSection(vm) }
        }
    }
}

@Composable
private fun SectionCard(color: Color, content: @Composable ColumnScope.() -> Unit) {
    Surface(color = color, shape = RoundedCornerShape(12.dp), shadowElevation = 3.dp, modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(12.dp), content = content)
    }
}

@Composable
private fun FilterRow(current: String, onPick: (String) -> Unit) {
    Row {
        listOf("all" to "All", "single" to "Singles", "stack" to "Stacks").forEach { (key, label) ->
            FilterChip(
                selected = current == key, onClick = { onPick(key) }, label = { Text(label) },
                colors = FilterChipDefaults.filterChipColors(selectedContainerColor = Selection, selectedLabelColor = TextPrimary),
                modifier = Modifier.padding(end = 6.dp)
            )
        }
    }
}

@Composable
private fun SummaryLine(vm: MobileWatchViewModel) {
    val sales = vm.visibleSales()
    if (sales.isEmpty()) return
    val prices = sales.map { it.price }.sorted()
    val lo = prices.first(); val hi = prices.last()
    val med = if (prices.size % 2 == 1) prices[prices.size / 2] else (prices[prices.size / 2 - 1] + prices[prices.size / 2]) / 2
    Spacer(Modifier.height(6.dp))
    SummaryRow("low ", lo, AccentGreen)
    SummaryRow("med ", med, AccentGold)
    SummaryRow("high", hi, AccentRed)
}

@Composable
private fun SummaryRow(label: String, value: Int, labelColor: Color) {
    Text(
        buildAnnotatedString {
            withStyle(SpanStyle(color = labelColor)) { append("$label  ") }
            withStyle(SpanStyle(color = TextPrimary)) { append("%,d g".format(value)) }
        },
        fontSize = 13.sp, fontFamily = FontFamily.Monospace
    )
}

@Composable
private fun SaleRowView(s: SaleRow) {
    Column(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
        Text(fmtDate(s.date), color = TextMuted, fontSize = 12.sp)
        Row(Modifier.fillMaxWidth().padding(top = 2.dp), horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically) {
            Text(
                buildAnnotatedString {
                    withStyle(SpanStyle(color = JobsBlue)) { append(s.seller) }
                    withStyle(SpanStyle(color = TextMuted)) { append(" \u2192 ") }
                    withStyle(SpanStyle(color = JobsBlue)) { append(s.buyer) }
                },
                fontSize = 12.sp, modifier = Modifier.weight(1f)
            )
            Text("%,d g%s".format(s.price, if (s.stack) "  (stack)" else ""),
                color = TextPrimary, fontSize = 13.sp, fontWeight = FontWeight.SemiBold, fontFamily = FontFamily.Monospace)
        }
        HorizontalDivider(color = CharcoalDark, modifier = Modifier.padding(top = 6.dp))
    }
}

@Composable
private fun CrossServerSection(vm: MobileWatchViewModel) {
    val ui = vm.ui
    val noun = if (ui.crossForm == "stack") "stacks" else "singles"
    Spacer(Modifier.height(14.dp))
    SectionCard(color = Panel) {
        Text("Median by server", color = TextMuted, fontSize = 12.sp)
        Spacer(Modifier.height(8.dp))
        when {
            ui.crossLoading -> Row(verticalAlignment = Alignment.CenterVertically) {
                CircularProgressIndicator(Modifier.size(16.dp), color = AccentGreen, strokeWidth = 2.dp)
                Spacer(Modifier.width(8.dp)); Text("comparing servers\u2026", color = TextMuted, fontSize = 12.sp)
            }
            ui.crossRanking.isEmpty() -> Text("no $noun history on any server", color = TextMuted, fontSize = 12.sp)
            else -> {
                val last = ui.crossRanking.size - 1
                ui.crossRanking.forEachIndexed { i, (world, med) ->
                    val color = when (i) { 0 -> AccentGreen; last -> AccentRed; else -> TextSoft }
                    Row(Modifier.fillMaxWidth().padding(vertical = 3.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                        Text(world, color = color, fontSize = 13.sp,
                            fontWeight = if (world == ui.world) FontWeight.Bold else FontWeight.Normal)
                        Text("%,d g".format(med), color = color, fontSize = 13.sp, fontFamily = FontFamily.Monospace)
                    }
                }
            }
        }
    }
    Spacer(Modifier.height(16.dp))
}

@Composable
private fun ZoneBanner(banner: String) {
    val ctx = LocalContext.current
    val bmp = remember(banner) {
        runCatching { ctx.assets.open("zonebanners/$banner.jpg").use { BitmapFactory.decodeStream(it)?.asImageBitmap() } }.getOrNull()
    }
    if (bmp != null) {
        Image(bmp, banner, modifier = Modifier.fillMaxWidth().aspectRatio(2f), contentScale = ContentScale.Crop)
    }
}

// Header image for a Content page — 16:9 source, shown edge to edge above the sections.
@Composable
private fun ContentBanner(banner: String) {
    val ctx = LocalContext.current
    val bmp = remember(banner) {
        runCatching { ctx.assets.open("zonebanners/$banner.jpg").use { BitmapFactory.decodeStream(it)?.asImageBitmap() } }.getOrNull()
    }
    if (bmp != null) {
        Image(bmp, banner, modifier = Modifier.fillMaxWidth().aspectRatio(16f / 9f)
            .padding(bottom = 4.dp), contentScale = ContentScale.Crop)
    }
}

@Composable
private fun ZoneNmRow(vm: MobileWatchViewModel, nm: ZoneNm, showDivider: Boolean) {
    Column(Modifier.fillMaxWidth().clickable { vm.selectMobByName(nm.name, nm.level) }.padding(vertical = 7.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(nm.name, color = AccentRed, fontWeight = FontWeight.Bold, fontSize = 15.sp, modifier = Modifier.weight(1f))
            if (nm.level.isNotEmpty()) Text("Lv ${nm.level}", color = TextMuted, fontSize = 12.sp)
        }
        if (nm.spawn.isNotEmpty()) Text(nm.spawn, color = TextSoft, fontSize = 12.sp)
        if (nm.drops.isNotEmpty()) Text("Drops: ${nm.drops}", color = AccentGold, fontSize = 12.sp)
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun ZoneMobRow(vm: MobileWatchViewModel, zm: ZoneMob, showDivider: Boolean) {
    Row(
        Modifier.fillMaxWidth().clickable { vm.selectMobByName(zm.name, zm.level) }.padding(vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(zm.name, color = TextSoft, fontSize = 14.sp, modifier = Modifier.weight(1f))
        if (zm.level.isNotEmpty()) Text("Lv ${zm.level}", color = TextMuted, fontSize = 12.sp)
        Icon(Icons.Filled.ArrowForward, null, tint = TextMuted, modifier = Modifier.size(16.dp))
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun ZoneBattleRow(b: ZoneBattle, showDivider: Boolean) {
    val ctx = LocalContext.current
    Column(
        Modifier.fillMaxWidth().clickable {
            val u = "https://www.bg-wiki.com/ffxi/" + b.name.replace(" ", "_")
            runCatching { ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(u))) }
        }.padding(vertical = 7.dp)
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(b.name, color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 14.sp, modifier = Modifier.weight(1f))
            Text(if (b.cap.equals("Uncapped", true)) "Uncapped" else "Lv ${b.cap}", color = TextMuted, fontSize = 12.sp)
        }
        if (b.type.isNotEmpty()) Text(b.type, color = AccentGold, fontSize = 12.sp, modifier = Modifier.padding(top = 1.dp))
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun ZoneQuestRow(quest: ZoneQuest, showDivider: Boolean) {
    val ctx = LocalContext.current
    Column(
        Modifier.fillMaxWidth().clickable {
            val u = "https://www.bg-wiki.com/ffxi/" + quest.name.replace(" ", "_")
            runCatching { ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(u))) }
        }.padding(vertical = 7.dp)
    ) {
        Text(quest.name, color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 14.sp)
        if (quest.npc.isNotEmpty()) Text(
            buildAnnotatedString {
                withStyle(SpanStyle(color = AccentGold)) { append("Starting NPC: ") }
                withStyle(SpanStyle(color = TextSoft)) { append(quest.npc) }
            },
            fontSize = 12.sp, modifier = Modifier.padding(top = 1.dp)
        )
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun ZoneAssaultRow(assault: ZoneAssault, showDivider: Boolean) {
    val ctx = LocalContext.current
    Column(
        Modifier.fillMaxWidth().clickable {
            val u = "https://www.bg-wiki.com/ffxi/" + assault.name.replace(" ", "_")
            runCatching { ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(u))) }
        }.padding(vertical = 7.dp)
    ) {
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Text(assault.name, color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 14.sp, modifier = Modifier.weight(1f))
            if (assault.rank.isNotEmpty()) Text(assault.rank, color = AccentGold, fontSize = 13.sp)
        }
        if (assault.objective.isNotEmpty()) Text(assault.objective, color = TextSoft, fontSize = 12.sp, modifier = Modifier.padding(top = 1.dp))
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun ZoneProcRowView(p: ZoneProcRow, showDivider: Boolean) {
    Column(Modifier.fillMaxWidth().padding(vertical = 7.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(p.types, color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 14.sp, modifier = Modifier.weight(1f))
            Text(p.currency, color = AccentGold, fontSize = 12.sp)
        }
        Text(
            "0:00-8:00  ${p.w1}    8:00-16:00  ${p.w2}    16:00-0:00  ${p.w3}",
            color = TextPrimary, fontSize = 12.sp, modifier = Modifier.padding(top = 1.dp)
        )
        if (p.jobs.isNotEmpty()) Text(p.jobs, color = TextMuted, fontSize = 12.sp, modifier = Modifier.padding(top = 1.dp))
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun HobbiesContent(vm: MobileWatchViewModel) {
    val sections = listOf(
        "Crafting" to listOf(
            "alchemy" to "Alchemy", "bonecraft" to "Bonecraft", "clothcraft" to "Clothcraft",
            "cooking" to "Cooking", "goldsmithing" to "Goldsmithing", "leathercraft" to "Leathercraft",
            "smithing" to "Smithing", "woodworking" to "Woodworking", "synergy" to "Synergy"
        ),
        "Collecting" to listOf(
            "fishing" to "Fishing",
            "gardening" to "Gardening",
            "harvesting" to "Harvesting",
            "mining" to "Mining",
            "excavation" to "Excavation",
            "logging" to "Logging",
            "clamming" to "Clamming"
        ),
        "Chocobo" to listOf(
            "raising" to "Chocobo Breeding",
            "digging" to "Chocobo Digging",
            "racing" to "Chocobo Racing"
        ),
        "Mog Garden" to listOf(
            "moggarden" to "Mog Garden",
            "monsterrearing" to "Monster Rearing"
        ),
        "Monstrosity" to listOf(
            "monstrosity" to "Monstrosity"
        )
    )
    val ready = setOf("fishing", "cooking", "goldsmithing", "digging", "alchemy", "smithing", "clothcraft", "leathercraft", "bonecraft", "woodworking", "synergy", "gardening", "harvesting", "mining", "excavation", "logging", "raising", "racing", "clamming", "moggarden", "monsterrearing", "monstrosity")
    val expanded = rememberSaveable(
        saver = listSaver(
            save = { map -> map.filterValues { it }.keys.toList() },
            restore = { keys -> mutableStateMapOf<String, Boolean>().apply { keys.forEach { put(it, true) } } }
        ),
        // rev 396: keyed on the page visit, exactly like CollapsibleSection, so
        // leaving the tab and coming back opens the list fully collapsed again.
        key = "hobby_sections_${LocalPageVisit.current}"
    ) { mutableStateMapOf<String, Boolean>() }
    LazyColumn(Modifier.fillMaxSize()) {
        sections.forEach { (section, list) ->
            val open = expanded[section] == true
            item(key = "hdr:$section") {
                GroupHeader(section, null, open) { expanded[section] = !open }
            }
            if (open) {
                items(list, key = { it.first }) { (k, lbl) ->
                    val active = k in ready
                    Row(
                        Modifier.fillMaxWidth()
                            .then(if (active) Modifier.clickable { vm.selectHobby(k) } else Modifier)
                            .padding(horizontal = 16.dp, vertical = 14.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(lbl, color = if (active) TextSoft else TextMuted, fontWeight = FontWeight.Medium,
                            fontSize = 16.sp, modifier = Modifier.weight(1f))
                        if (!active) Text("Soon", color = TextMuted, fontSize = 12.sp)
                    }
                    HorizontalDivider(color = CharcoalDark)
                }
            }
        }
    }
}

// ==========================  CONTENT TAB  ==================================
// A *content type* is an activity with its own areas, its own roster and its own
// rules. The Bestiary's "Content" view answers "which mobs belong to this?"; this
// tab is the other half — the activity itself and its areas.
//
// Each content type gets one page: a write-up section at the top (empty for now)
// and every area listed underneath. Opening an area gives that area's own page.
//
// DYNAMIS AND DYNAMIS DIVERGENCE ARE SEPARATE CONTENT TYPES, not two sections of
// one. They share maps and a name and nothing else — different level bands,
// different roster, different boss chain, different strategy. They also live under
// different tag groups in the mob data ("Dynamis" vs "Dynamis D"), so the split
// here matches the split there.

private val DynamisAreas = listOf(
    "Original" to listOf(
        "Dynamis-Bastok", "Dynamis-San d'Oria", "Dynamis-Windurst", "Dynamis-Jeuno",
        "Dynamis-Beaucedine", "Dynamis-Xarcabard"
    ),
    "Dreamworld" to listOf(
        "Dynamis-Valkurm", "Dynamis-Buburimu", "Dynamis-Qufim", "Dynamis-Tavnazia"
    )
)

private val DivergenceAreas = listOf(
    "Areas" to listOf(
        "Dynamis-Bastok [D]", "Dynamis-San d'Oria [D]", "Dynamis-Windurst [D]", "Dynamis-Jeuno [D]"
    )
)

private fun areaGroupsFor(contentKey: String) =
    if (contentKey == "dynamisd") DivergenceAreas else DynamisAreas

private fun contentTitle(contentKey: String) =
    if (contentKey == "dynamisd") "Dynamis Divergence" else "Dynamis"

// Divergence zones are tagged under the separate "Dynamis D" group (rev 192 schema).
private fun dynamisTagGroup(zone: String): String =
    if (zone.endsWith("[D]")) "Dynamis D" else "Dynamis"

// Fight order inside an area page: the last fight first, then back down the chain.
private fun bossOrder(role: String): Int = when {
    role.equals("Arch Mega", ignoreCase = true) -> 0
    role.equals("Disjoined", ignoreCase = true) -> 0
    role.equals("Mega", ignoreCase = true) -> 1
    role.equals("Boss", ignoreCase = true) -> 1
    role.equals("Midboss", ignoreCase = true) -> 2
    else -> 3
}

private fun bossLabel(role: String): String? = when {
    role.equals("Arch Mega", ignoreCase = true) -> "Arch Mega Boss"
    role.equals("Mega", ignoreCase = true) -> "Mega Boss"
    role.equals("Disjoined", ignoreCase = true) -> "Disjoined Boss"
    role.equals("Boss", ignoreCase = true) -> "Zone Boss"
    role.equals("Midboss", ignoreCase = true) -> "Mid-Boss"
    role.equals("TE", ignoreCase = true) -> "Time Extension"
    else -> null
}

// Entry write-up for a content type, split by the same Original / Dreamworld grouping
// the area list uses. Deliberately NO entrance locations here — those come next, in a
// dedicated place. Text is paraphrased from BG-wiki's "Entry Requirements".
@Composable
private fun EnterLine(text: String, indent: Int = 0) {
    Row(Modifier.fillMaxWidth().padding(start = (indent * 14).dp, top = 3.dp, bottom = 3.dp)) {
        Text("\u2022", color = TextMuted, fontSize = 13.sp, modifier = Modifier.width(16.dp))
        Text(text, color = TextSoft, fontSize = 13.sp, lineHeight = 18.sp)
    }
}

@Composable
private fun EnterHeading(text: String) {
    Text(text, color = AccentGold, fontWeight = FontWeight.SemiBold, fontSize = 13.sp,
        modifier = Modifier.padding(top = 10.dp, bottom = 2.dp))
}

@Composable
private fun EnteringBody(contentKey: String) {
    if (contentKey == "dynamisd") {
        Column(Modifier.fillMaxWidth().padding(bottom = 4.dp)) {
            EnterLine("Divergence reuses the four original city maps with a level-127-and-up roster and its own three-step boss chain (Mid-Boss, Zone Boss, then a Disjoined Boss).")
            EnterLine("Entry follows the same Vial of Shrouded Sand and Prismatic Hourglass requirements as original Dynamis, entered through the corresponding city zone.")
            EnterLine("The individual per-area entry steps go here later.")
        }
        return
    }
    Column(Modifier.fillMaxWidth().padding(bottom = 4.dp)) {
        EnterHeading("Original")
        EnterLine("Be level 65 or higher.")
        EnterLine("Reach Rank 6 or higher in one of the three nations' mission lines.")
        EnterLine("Zone into Xarcabard for a cutscene, then examine any Trail Markings to receive the Vial of Shrouded Sand.", 1)
        EnterLine("The Beastmen-stronghold Goblins will then sell the permanent Prismatic Hourglass for 50,000 gil. The old Timeless and Perpetual Hourglasses are retired.", 1)
        EnterLine("With the Vial and an Hourglass you may enter any original city zone once per day (resets at Japan midnight).")
        EnterLine("Clearing a zone's Zone Boss unlocks the next zones; the \"Rhapsody in Azure\" reward grants unlimited entry.", 1)
        EnterLine("Enter by interacting with that zone's Trail Markings. Parties are 1\u201318 players and every member needs the Hourglass; Trusts may be called.")

        EnterHeading("Dreamworld")
        EnterLine("Complete Promathia Mission 3-5.")
        EnterLine("Hold the same Vial and Hourglass Key Items as above.")
        EnterLine("You may enter Buburimu, Qufim and Valkurm once per day; clearing each Zone Boss unlocks further zones.")
        EnterLine("Tavnazia additionally requires clearing the other three Dreamworld areas first.", 1)
        EnterLine("Enter by interacting with that zone's Hieroglyphics. Same 1\u201318 party rule and Hourglass requirement; Trusts may be called.")
    }
}

// Time Extension summary for a content type. Divergence is deliberately different:
// its areas do NOT get the Granules of Time campaign, only the level-75 era zones do.
@Composable
private fun TimeExtensionBody(contentKey: String) {
    val divergence = contentKey == "dynamisd"
    Column(Modifier.fillMaxWidth().padding(bottom = 4.dp)) {
        EnterLine("The clock starts at 60 minutes (Earth time) the moment you enter.")
        EnterLine("Five NM statues extend it. Each gauges as \"Impossible to Gauge\" and drops a Granules of Time Key Item \u2014 Crimson, Azure, Amber, Alabaster or Obsidian.")
        EnterLine("The granules vanish when you leave the zone, and no single statue gives an extension twice in the same run.", 1)
        EnterHeading("Granules of Time campaign")
        if (divergence) {
            EnterLine("Divergence areas are NOT part of this campaign \u2014 only the level-75 era zones are.")
        } else {
            EnterLine("During this Monthly Adventurer Campaign, every extension in a zone is granted automatically each time you zone into any Dynamis area, so the statues don't need hunting.")
            EnterLine("It runs at most one month at a time, and it covers the level-75 era zones only \u2014 Divergence is excluded.", 1)
        }
    }
}

@Composable
private fun Placeholder() {
    Text("Not written yet.", color = TextMuted, fontSize = 13.sp,
        modifier = Modifier.padding(vertical = 6.dp))
}

@Composable
private fun ContentTabContent(vm: MobileWatchViewModel) {
    val ready = setOf("dynamis", "dynamisd", "geasfete", "omen", "odyssey", "apexlocus", "sortie", "unity", "vagary",
        "abyssea", "mastertrials", "limbus", "ultimate")
    // alphabetical by label
    val types = listOf(
        "abyssea" to "Abyssea", "apexlocus" to "Apex / Locus",
        "dynamis" to "Dynamis", "dynamisd" to "Dynamis Divergence",
        "geasfete" to "Geas Fete",
        "limbus" to "Limbus", "mastertrials" to "Master Trials",
        "odyssey" to "Odyssey", "omen" to "Omen",
        "sortie" to "Sortie", "ultimate" to "Ultimate Weapons",
        "unity" to "Unity", "vagary" to "Vagary"
    )
    LazyColumn(Modifier.fillMaxSize()) {
        items(types, key = { it.first }) { (k, lbl) ->
            val active = k in ready
            TopLevelRow(lbl, enabled = active, trailing = if (active) null else "Soon") {
                vm.selectContent(k)
            }
        }
    }
}

@Composable
private fun ContentTypeScreen(vm: MobileWatchViewModel) {
    val key = vm.ui.selectedContent ?: return
    val title = contentTitle(key)
    val groups = areaGroupsFor(key)
    val expanded = rememberSaveable(
        saver = listSaver(
            save = { map -> map.filterValues { it }.keys.toList() },
            restore = { keys -> mutableStateMapOf<String, Boolean>().apply { keys.forEach { put(it, true) } } }
        ),
        // rev 396: keyed on the page visit, exactly like CollapsibleSection, so
        // leaving the tab and coming back opens the list fully collapsed again.
        key = "content_areas_${LocalPageVisit.current}"
    ) { mutableStateMapOf<String, Boolean>() }
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(title, onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_dynamis") }
            item(key = "top") {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Entering", stateKey = "content:$key:entering") {
                        EnteringBody(key)
                    }
                    CollapsibleSection("Time Extensions", stateKey = "content:$key:te") {
                        TimeExtensionBody(key)
                    }
                    CollapsibleSection("Zones", stateKey = "content:$key:zones") {
                        val flatAreas = groups.size == 1  // single area group (Divergence): list cities directly, no area header
                        groups.forEach { (group, areas) ->
                            val open = flatAreas || expanded[group] == true
                            if (!flatAreas) {
                                Row(
                                    Modifier.fillMaxWidth().clickable { expanded[group] = !open }
                                        .padding(vertical = 8.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(group, color = AccentGold, fontWeight = FontWeight.SemiBold,
                                        fontSize = 13.sp, modifier = Modifier.weight(1f))
                                    Icon(if (open) Icons.Filled.ArrowDropUp else Icons.Filled.ArrowDropDown, null, tint = TextMuted)
                                }
                            }
                            if (open) {
                                areas.forEach { z ->
                                    Row(
                                        Modifier.fillMaxWidth().clickable { vm.selectContentZone(z) }
                                            .padding(start = 8.dp, top = 11.dp, bottom = 11.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Icon(Icons.Filled.Place, null, tint = AccentGreen, modifier = Modifier.size(18.dp))
                                        Spacer(Modifier.width(10.dp))
                                        Text(z, color = TextSoft, fontWeight = FontWeight.Medium,
                                            fontSize = 15.sp, modifier = Modifier.weight(1f))
                                    }
                                    HorizontalDivider(color = CharcoalDark)
                                }
                            }
                        }
                    }
                    Spacer(Modifier.height(6.dp))
                }
            }
        }
    }
}

// Omen is a single-zone content type (Reisenjima Henge), so it gets its own page rather than the
// Dynamis zone-list shape: a Getting Started / Floors / Objectives / Rewards guide from BG-wiki.
@Composable
private fun OmenScreen(vm: MobileWatchViewModel) {
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Omen", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_omen") }
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Getting Started", stateKey = "omen:start", persist = false) {
                        FactRow("Eligibility", "Complete the final chapter of Rhapsodies of Vana'diel; every party member needs a Mystical Canteen.")
                        FactRow("Mystical Canteen", "Speak to Incantrix (near the final RoV ethereal ingress) for one \u2014 one per person at a time. Incantrix stores up to 3 charges, one every 20 hours (Earth time).")
                        FactRow("Entry", "Select \"Omen\" at the earthly concrescence in Reisenjima (leader only) to teleport the party to Reisenjima Henge; each canteen is consumed on entry.")
                        FactRow("Party", "1-18 players; entering as an alliance, only the leader applies. Objectives scale only up to a 6-person party.")
                        FactRow("Time Limit", "Starts at 10 minutes; +10 per ethereal ingress; 50 minutes max. The \"smaller light\" path adds +30 instead.")
                    }
                    CollapsibleSection("Floors", stateKey = "omen:floors", persist = false) {
                        Text("An ethereal ingress opens after each floor's primary objective is met; step through to descend.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("1st", "Tigers & Flies (Sweetwater) plus Transcendent NMs. A random objective opens the ingress.")
                        FactRow("2nd", "Beetles & Leeches. Then pick a light: the larger light leads to the 3rd-floor mid-boss; the smaller light adds +30 min and takes the express route toward Ou.")
                        FactRow("3rd (larger light)", "One of three Glassy mid-bosses at random \u2014 Glassy Craver, Glassy Gorger, or Glassy Thinker. Beating it opens an ingress that lets you pick which Caturae you fight in the final area.")
                        FactRow("4th", "Transcendent NMs + Sweetwater regulars whose family depends on the path (Skeletons/Ghosts, Treants/Doomed, Elementals/Worms, Frogs/Bats, Hippogryphs/Pugils \u2026). Random objective; the ingress either exits or enters Ou's battlefield.")
                        FactRow("5th \u2014 Caturae", "Fu, Kyou, Kei, Gin, Kin \u2014 one per path \u2014 and Ou, the smaller-light final boss.")
                        Text("Ou's battlefield opens only if the party leader holds all 5 Bead Key Items from the other five Caturae; every enemy must be defeated, the entry player must be alive on the final kill, and all party members lose their Bead Key Items.",
                            color = AccentRed, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(top = 6.dp))
                    }
                    CollapsibleSection("Objectives", stateKey = "omen:obj", persist = false) {
                        FactRow("Reward", "Every 5 objectives completed rewards a Paragon Job Card.")
                        FactRow("Main (1st/2nd/4th)", "A random objective: vanquish one specific mob, N Sweetwater mobs, all Transcended, all monsters, or a free VR floor.")
                        FactRow("Main (3rd/5th)", "Defeat the floor boss. Bonus floors: open a set number of chests.")
                        EnterHeading("Additional objectives")
                        Text("Shown once a foe detects you. N = party or alliance size, capped at 6.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp,
                            modifier = Modifier.padding(top = 2.dp, bottom = 2.dp))
                        EnterLine("Vanquish N foes (only one kill credited per attack)")
                        EnterLine("Use 2\u00d7N job abilities on your foes")
                        EnterLine("Cast 3\u00d7N spells on your foes")
                        EnterLine("Execute N skillchains \u2014 consecutive, a length-N+1 chain (Immanence excluded)")
                        EnterLine("Perform 3\u00d7N magic bursts")
                        EnterLine("Deal 3\u00d7N critical hits (max one crit credited per weapon skill)")
                        EnterLine("Use 3\u00d7N elemental weapon skills")
                        EnterLine("Use 3\u00d7N physical weapon skills")
                        EnterLine("Use 5\u00d7N weapon skills")
                        EnterLine("Reduce a foe's HP by 2,000+ in one auto-attack (whole round summed)")
                        EnterLine("Reduce a foe's HP by 30,000+ with one weapon skill (skillchain damage counts)")
                        EnterLine("Reduce a foe's HP by 30,000+ with one magic burst (pet / Lunge excluded)")
                        EnterLine("Reduce a foe's HP by 15,000+ with one non-burst magic attack")
                        EnterLine("Restore at least 500 HP ten times")
                    }
                    CollapsibleSection("Bosses", stateKey = "omen:bosses", persist = false) {
                        val bossOrder = listOf("Glassy Craver", "Glassy Gorger", "Glassy Thinker",
                            "Fu", "Kyou", "Kei", "Gin", "Kin", "Ou")
                        vm.mobsForContent("Omen", "Bosses")
                            .sortedBy { bossOrder.indexOf(it.name).let { i -> if (i < 0) 99 else i } }
                            .forEach { OdyMobRow(vm, it, "Omen") }
                    }
                    CollapsibleSection("Rewards", stateKey = "omen:rewards", persist = false) {
                        FactRow("Job Cards", "Paragon Job Cards upgrade Reforged Artifact Armor +1. Earned every 5 objectives, every 5 zone-ins, and per number of omens farmed. Trade 5 of one type for 1 of another via Coelestrox.")
                        FactRow("Scales", "Upgrade +2 armor to Reforged Artifact Armor +3. 1-2 always drop from a 5th-floor boss; also from Sweetwater foes (Nov 2021). A Distorted fragment is needed if you never upgraded a +2 to +3 before that update.")
                        FactRow("Boss Rewards", "Reforged Artifact Armor +2 / +3 appear as spoils in the Treasure Pool when a boss is beaten.")
                        FactRow("Omens Currency", "Normal mobs drop a number 1-999; a random draw on entry sets the Free Floor number, so killing everything maximizes the chance (no duplicate numbers per run).")
                        FactRow("Bonus Floor", "Warping up from floor 3 or 5 can rarely land on a treasure-chest floor (job cards, a Mystical Canteen KI, gil, or Omen gear).")
                        EnterHeading("Gear by boss")
                        FactRow("Glassy Craver", "Nusku Shield; Anu Torque, Sherida Earring; Hope Crystal")
                        FactRow("Glassy Gorger", "Enki Strap, Erra Pendant, Kishar Ring; Fulfillment Crystal")
                        FactRow("Glassy Thinker", "Adapa Shield; Adad Amulet, Knobkierrie; Thought Crystal")
                        FactRow("Fu", "Nisroch Jerkin; Niqmaddu Ring, Shulmanu Collar; Fu's Scale; Moonbow Stone")
                        FactRow("Kyou", "Udug Jacket; Enmerkar Earring, Iskur Gorget; Kyou's Scale; Moonbow Cloth")
                        FactRow("Kei", "Ammurapi Shield; Shamash Robe; Lugalbanda Earring; Kei's Scale; Moonbow Urushi")
                        FactRow("Gin", "Ashera Harness; Dingir Ring, Yamarang; Gin's Scale; Moonbow Leather")
                        FactRow("Kin", "Dagon Breastplate; Ilabrat Ring, Utu Grip; Kin's Scale; Moonbow Steel")
                        FactRow("Ou", "Regal hands (Captain's Gloves, Cuffs, Gauntlets, Gloves); Regal Belt / Earring / Gem / Necklace / Ring; all five Caturae Scales; Moonbow mats + Moonlight Coral")
                    }
                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

// Odyssey (Sheol) is single-zone-family content like Omen, so it gets a guide page rather than the
// Dynamis zone-list. Built from BG-wiki: overview + mechanics + Sheol A/B/C + Sheol Gaol. The named NMs
// are also tagged into the "Odyssey" content section of the bestiary. "More to come" (Nostos regulars,
// full per-NM pop/SP tables) — this is the first pass.
@Composable
private fun OdyBlock(title: String, body: String) {
    Text(title, color = AccentGold, fontWeight = FontWeight.SemiBold, fontSize = 12.sp,
        modifier = Modifier.padding(top = 8.dp, bottom = 2.dp))
    Text(body, color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp)
}

// A clickable NM row for the Odyssey guide — same tap-through as the bestiary/Dynamis lists.
@Composable
private fun OdyMobRow(vm: MobileWatchViewModel, mob: Mob, zone: String, levelText: String? = null) {
    Row(
        Modifier.fillMaxWidth().clickable { vm.selectMob(mob, zone) }.padding(vertical = 7.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(Modifier.weight(1f)) {
            Text(mob.name, color = AccentRed, fontSize = 14.sp, fontWeight = FontWeight.Medium)
            if (mob.family.isNotBlank()) Text(mob.family, color = TextMuted, fontSize = 10.sp)
        }
        Text(levelText ?: if (mob.levelLo > 0) "Lv ${mob.levelLo}" else "", color = TextMuted, fontSize = 12.sp)
    }
    HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun OdysseyScreen(vm: MobileWatchViewModel) {
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Odyssey", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_odyssey") }
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Overview", stateKey = "ody:overview", persist = false) {
                        Text("Odyssey is exploratory battle content in the Walk of Echoes. Each instance is a Sheol \u2014 a multi-floor descent whose Nostos foes and NMs drop Lustreless materials (Scales, Hides, Wings) used to augment Unity (UNM) equipment. There are three exploration tiers \u2014 Sheol A, B and C \u2014 plus Sheol Gaol, a boss gauntlet whose rewards buy and rank up weapons and armor.",
                            color = TextSoft, fontSize = 13.sp, lineHeight = 18.sp)
                    }
                    CollapsibleSection("Getting In", stateKey = "ody:in", persist = false) {
                        FactRow("Moglophone", "Each player needs a Moglophone (Key Item). Get one from the Pilgrim Moogle in Rabao (examine the ??? at G-6). One held at a time; a new one every 20 hours (Earth time).")
                        FactRow("Entry", "Examine the Veridical Conflux in Rabao (G-6) to enter. 1-6 players; Trusts are allowed but capped by the number of real players who entered.")
                        FactRow("Progression", "Complete each Sheol's Records of Eminence objective to unlock the next: A \u2192 B \u2192 C \u2192 Gaol.")
                        FactRow("Sheol Gaol entry", "Needs 3 Moglophone IIs. You get 3 free after clearing the Sheol C RoE; further ones cost 3,000 Moogle Segments each. Each boss attempt consumes one. You must have at least 3 jobs at level 99.")
                    }
                    CollapsibleSection("Nostos & Foes", stateKey = "ody:foes", persist = false) {
                        OdyBlock("Nostos", "The common enemies. All aggro by their family's usual detection PLUS Sight, spawn in clusters of ~10, do NOT link, and can be Charmed. Hide works against them except the scent-trackers. 1 Izzat per 5 defeated.")
                        OdyBlock("Agon Halos & Beastmen", "Beastmen guard glowing Agon Halos and are semi-invisible until the Halo is destroyed. They have True Sight + True Sound, link with each other, and can't be slept or enfeebled until the Halo falls. The Halo pulses elemental damage. Clear them all for 10 Izzat, Moogle Segments, and an Ethereal Junction.")
                        OdyBlock("Notorious Monsters", "Spawn from Ethereal Junctions by trading the right UNM pop item. They wield SP abilities and reset enmity, and drop the Lustreless materials. Reduced AoE damage applies to everything here (like Domain Invasion / Divergence).")
                    }
                    CollapsibleSection("Chests & Mimics", stateKey = "ody:chests", persist = false) {
                        Text("Chests upgrade in a chain: Chest \u2192 Coffer \u2192 Aurum Strongbox, each richer than the last. Open them by spending Izzat or by using Thief tools (Thief's Tools / Living Key / Skeleton Key). Contents go to the treasure pool.",
                            color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp)
                        Text("A chest can instead be a Mimic \u2014 a tool used on it fails and it becomes an NM with high attack/defence, reduced magic & skillchain damage, a draw-in, and a wide aggro range.",
                            color = AccentRed, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(top = 6.dp))
                    }
                    CollapsibleSection("Izzat, Segments & Mastery", stateKey = "ody:currency", persist = false) {
                        FactRow("Izzat", "Temporary, party-shared, lost on leaving. 1 per 5 monsters, 10 per Agon Halo cleared. Spend it to pop NMs from Ethereal Junctions and to open chests.")
                        FactRow("Moogle Segments", "Persistent points. Buy Moglophone IIs and Lustreless items with them. Earned per Sheol (roughly A 5-17, B 13-23, C 25-31 per foe) plus from chests, coffers and strongboxes.")
                        FactRow("Moogle Mastery", "A stacking buff in all Odyssey areas: +item level per 5 tiers (max +9) and \u22122% damage taken per 3 tiers (max \u221215%). Raised by defeating Nostos totals, NMs and opening strongboxes. Caps at 15 per zone \u2014 45 total across A/B/C.")
                    }
                    CollapsibleSection("Rewards", stateKey = "ody:rewards", persist = false) {
                        FactRow("Lustreless materials", "Sheol A drops Scales, B drops Hides, C drops Wings \u2014 the augment currency for UNM gear.")
                        FactRow("UNM upgrade", "After a Sheol's RoE, upgrade Unity NM equipment to R15: 1,191 Lustreless items of that tier plus a 30,000-Accolade fee.")
                        FactRow("Otherworldly Vortex", "Examine it (each character does so individually) for a personal reward of gil and Large Lustreless Boxes.")
                        FactRow("Campaigns", "The Great Odyssey campaign raises job points / segments by +50% and doubles boxes; the PLUS version doubles job points / segments and adds +50% gil.")
                    }
                    CollapsibleSection("Sheol A", stateKey = "ody:a", persist = false) {
                        FactRow("Rules", "30-minute limit. Indi-spells \u221275% effect; AoE deals \u221290% to secondary targets. Mob HP roughly 30k-65k.")
                        FactRow("Layout", "Otherworldly Vortex on floor 7. Agon Halos on floors 1/3/5/7 (guarded by Quadav, Orc, Yagudo). Three Translocators warp between areas.")
                        CollapsibleSection("Notorious Monsters", stateKey = "ody:a:nms", persist = false) {
                            vm.mobsForContent("Odyssey", "Sheol A").sortedBy { it.name }.forEach { OdyMobRow(vm, it, "Sheol A") }
                        }
                    }
                    CollapsibleSection("Sheol B", stateKey = "ody:b", persist = false) {
                        FactRow("Rules", "30-minute limit. Indi-spells \u221285% effect; AoE \u221290% to secondaries. Each monster additionally resists one specific damage type by \u221225%.")
                        FactRow("Layout", "Otherworldly Vortex on floor 5. Agon Halos on floors 1/3/5/6 (Antica, Sahagin, Tonberry).")
                        CollapsibleSection("Notorious Monsters", stateKey = "ody:b:nms", persist = false) {
                            vm.mobsForContent("Odyssey", "Sheol B").sortedBy { it.name }.forEach { OdyMobRow(vm, it, "Sheol B") }
                        }
                    }
                    CollapsibleSection("Sheol C", stateKey = "ody:c", persist = false) {
                        FactRow("Rules", "30-minute limit. Indi-spells \u221295% effect; AoE \u221290% to secondaries. Each monster resists one specific damage type by \u221250%.")
                        FactRow("Layout", "Otherworldly Vortex on floor 4. Agon Halos on every floor (Lamia, Troll, Mamool Ja).")
                        CollapsibleSection("Notorious Monsters", stateKey = "ody:c:nms", persist = false) {
                            Text("Each carries a full 2-hour ability.", color = TextMuted, fontSize = 11.sp,
                                modifier = Modifier.padding(bottom = 2.dp))
                            vm.mobsForContent("Odyssey", "Sheol C").sortedBy { it.name }.forEach { OdyMobRow(vm, it, "Sheol C") }
                        }
                    }
                    CollapsibleSection("Sheol Gaol", stateKey = "ody:gaol", persist = false) {
                        Text("A boss gauntlet, not an exploration floor. From a 15-minute waiting area you may take on up to 3 bosses per entry (45 min max), but never the same main job twice in a run. Support Jobs are restricted and Geomancy is \u221285% on the boss. Beating one costs the gil price shown; augmenting is done afterward via Vengeance.",
                            color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp)
                        val gaolMobs = vm.mobsForContent("Odyssey", "Sheol Gaol")
                        val atonements = listOf(
                            "Atonement 1" to "2M gil \u2014 Hesperiidae, Epitaph, Neo Animator, Coiste Bodhar lines",
                            "Atonement 2" to "3M gil \u2014 Acrontica, Beithir Ring, Tsuru, Schere Earring, Tellen Belt, Obstinate Sash",
                            "Atonement 3" to "4.5M weapon / 6M armor \u2014 Ikenga's, Gleti's, Sakpata's, Agwu's, Bunzi's, Mpaca's sets",
                            "Atonement 4" to "7.5M gil \u2014 the Nyame armor set"
                        )
                        atonements.forEach { (at, cap) ->
                            val ms = gaolMobs.filter { vm.contentRoleOf(it, "Odyssey", "Sheol Gaol") == at }.sortedBy { it.name }
                            if (ms.isNotEmpty()) {
                                CollapsibleSection(at, stateKey = "ody:gaol:${at.replace(' ', '_')}", persist = false) {
                                    Text(cap, color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp,
                                        modifier = Modifier.padding(bottom = 2.dp))
                                    ms.forEach { OdyMobRow(vm, it, "Sheol - Gaol") }
                                }
                            }
                        }
                        OdyBlock("Vengeance & RP", "Each boss has Vengeance tiers. Defeat one at Vengeance +0 to unlock its gear at rank 15; beating it at higher Vengeance earns Reinforcement Points (RP) that push the augment cap higher \u2014 +15 \u2192 rank 20, +20 \u2192 rank 25, +25 \u2192 rank 30. RP needed climbs steeply per rank (about 44,020 total to reach rank 30).")
                    }
                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

// Sortie — Outer Ra'Kaznar (U), Aug 2022. Guide page in the Omen/Odyssey shape: collapsible
// sections, all default-collapsed and persist=false so leaving the page resets them. The Bosses
// section reads the content tags live (Sortie: Bosses: Minor|Major|Aminon) and links to the bestiary.
@Composable
private fun SortieScreen(vm: MobileWatchViewModel) {
    var openMap by remember { mutableStateOf<SortieMap?>(null) }
    BackHandler(enabled = openMap != null) { openMap = null }
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar(
                openMap?.title ?: "Sortie",
                onBack = { if (openMap != null) openMap = null else vm.clearContent() }
            )
        }
    ) { pad ->
      Box(Modifier.padding(pad).fillMaxSize()) {
        LazyColumn(Modifier.fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_sortie") }
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Maps", stateKey = "sortie:maps", persist = false) {
                        Text("Composite sector maps — tap one to open it full screen, then pinch to zoom and drag to pan.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp,
                            modifier = Modifier.padding(bottom = 4.dp))
                        SORTIE_MAPS.forEach { m -> SortieMapRow(m) { openMap = m } }
                    }
                    CollapsibleSection("Overview", stateKey = "sortie:overview", persist = false) {
                        Text("Exploratory battle content through an alternative Outer Ra'Kaznar, sharded into eight " +
                            "unequal sectors A-H. Sectors A-D are the ground floor, E-H the basement. Materials earned " +
                            "here buy Reforged Empyrean Armor +2/+3 and feed Prime Weapon upgrades.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Each sector holds", "Groups of enemies from one or more families of a single type, one roaming minor NM, one major NM behind a Diaphanous Gadget, and a Diaphanous Bitzer. Ground-floor sectors also have a Diaphanous Device plus unlocked and Locked Gates.")
                        FactRow("Unlocks", "Entering a Sortie instance unlocks all 5 pieces of Reforged Empyrean +2 for that job for reforging. Reaching any area via a Bitzer (entering the basement) unlocks all 5 pieces of +3.")
                        FactRow("Combat rules", "Enemies take full damage from AoE magic and abilities and keep their family's normal damage-type resistances. Geomancy is full-strength on regular enemies but -50% on NMs.")
                        FactRow("Aggro", "Every foe in Sortie is aggressive, and not all of them follow their family's normal detection rules.")
                    }
                    CollapsibleSection("Getting In", stateKey = "sortie:entry", persist = false) {
                        FactRow("Eligibility", "Complete the Seekers of Adoulin mission The Light Within and hold the Scintillating Rhapsody from The Orb's Radiance.")
                        FactRow("Entry item", "Every player needs a Shiny Ra'Kaznarian plate, first acquired from Ruspix in Leafallia.")
                        FactRow("Entrance", "Kamihr Drifts Bivouac #4 — the Diaphanous Transposer. Parties of 1-6; Trusts allowed, capped by the open party slots at the time of entry.")
                        FactRow("Time limit", "1 hour, and it cannot be extended. Everyone is ejected when it expires, or if 3 minutes pass with the whole party knocked out. Each player gets an Obsidian Wing to leave early.")
                        FactRow("Plate recharge", "On entry your Shiny plate becomes a Dull Ra'Kaznarian plate and takes twenty hours to recharge. Walking up to the Transposer with a full plate turns it Shiny again — no need to talk to Ruspix.")
                        FactRow("Ruspix's plate", "Earned after your first foray. 20 hours after entering, it accumulates 1 second of charge per 5 real seconds, up to 72,000 seconds (20 hours). Spend it to instantly fill a Dull plate — it only consumes what's needed.")
                        Text("Wait until right before you enter to spend Ruspix's plate: any delay afterwards recharges the Ruspix plate at the same 5:1 rate instead of your now-full Shiny plate.",
                            color = AccentRed, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(top = 6.dp))
                    }
                    CollapsibleSection("Progression Items", stateKey = "sortie:items", persist = false) {
                        Text("You start with access to Sector A only. Hidden objectives reward temporary items that open the rest of the map.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Ra'Kaznar Keys", "Open their matching Locked Gates. Kept for the run despite being temporary items.")
                        FactRow("Ra'Kaznar Plates", "Used on the Diaphanous Devices near the central elevator shaft — teleport around the map and rematerialize enemies you have already cleared.")
                        FactRow("Ra'Kaznar Shards & Fragments", "Teleport to the NM arenas via the Diaphanous Gadgets in the map corners. Consumed when you beat the NM inside. Each basement NM needs the shard from beating the matching NM upstairs.")
                        FactRow("Ra'Kaznar Metals & Seal", "Protect against specific abilities used by the NM beyond that Gadget. Consumed on the kill, or after blocking the technique a set number of times.")
                        FactRow("Ra'Kaznar Sheets", "Used on the Diaphanous Bitzers at the central elevator shaft — transport to basement sectors E through H.")
                    }
                    CollapsibleSection("Objectives & Chests", stateKey = "sortie:obj", persist = false) {
                        Text("Completing a hidden objective spawns a chest and posts the group's progress to everyone's chat log. Chests always grant the same reward to every party member and never disappear if left unopened.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Brown chests", "Guaranteed temporary items for traversal or major-NM access.")
                        FactRow("Blue caskets, red coffers, aurum coffers", "May hold JSE Earrings, Reforged Empyrean +2/+3 upgrade items, and Prime Weapon upgrade items, alongside Old Cases, sapphires and starstones.")
                        EnterHeading("Where you must be standing")
                        EnterLine("Anywhere on the ground floor for chests from sectors A-D")
                        EnterLine("In the boss area — not necessarily inside the door — for major NM rewards")
                        EnterLine("In the same sector for chests from basement sectors E-H")
                        Text("Blood Pacts satisfy no magic or Weapon Skill objective. A player who is disconnected when a chest opens does not get the temporary item inside and may be unable to progress. Opening two chests within 400ms stacks the Gallimaufry but yields only one temporary item, which can stall the group.",
                            color = AccentRed, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(top = 6.dp))
                    }
                    CollapsibleSection("Sectors & Foes", stateKey = "sortie:sectors", persist = false) {
                        Text("Each sector's regular foes carry its prefix. Detection here does not always match the family's usual rules.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("A — Abject", "Acuex, Leech, Hecteyes. Lv 119-121.")
                        FactRow("B — Biune", "Elemental, Umbril, Porxie. Lv 123-125.")
                        FactRow("C — Cachaemic", "Ghost, Skeleton, Corse. Lv 127-129.")
                        FactRow("D — Demisang", "Fomor. Lv 131-133.")
                        FactRow("E — Esurient", "Slime, Slug, Flan. Lv 134-136.")
                        FactRow("F — Fetid", "Elemental (Baelfyr, Gefyrst, Ungeweder, Byrgen), Veela. Lv 135-137.")
                        FactRow("G — Gyvewrapped", "Hound, Dullahan, Vampyr. Lv 136-138.")
                        FactRow("H — Haughty", "Fomor, in job flavours. Lv 137-139.")
                        FactRow("Naakuals", "Lv 140 mini-Naakuals — Bztavian, Rockfin, Gabbrath, Waktza, Yggdreant, Cehuetzi — appear as basement coffer objectives.")
                        EnterHeading("Basement Reives")
                        Text("Each basement sector has a Colonization Reive style encounter that shuts a door until it is cleared, and it is cleared by completing that sector's Coffer objective. Be careful — there is no escape but the objective.",
                            color = AccentRed, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(vertical = 4.dp))
                        EnterLine("E — 5 minutes after entering the sector")
                        EnterLine("F — have a player leave the sector and return")
                        EnterLine("G — clear all hounds and dullahans in the reive room")
                        EnterLine("H — clear a full party of Haughty fomor in order: PLD, DRK, BST, BRD, RNG, SAM, NIN, DRG")
                    }
                    CollapsibleSection("Bosses", stateKey = "sortie:bosses", persist = false) {
                        val sectorOf = mapOf(
                            "Abject Obdella" to "A", "Biune Porxie" to "B", "Cachaemic Bhoot" to "C",
                            "Demisang Deleterious" to "D", "Esurient Botulus" to "E", "Fetid Ixion" to "F",
                            "Gyvewrapped Naraka" to "G", "Haughty Tulittia" to "H",
                            "Ghatjot" to "A", "Leshonn" to "B", "Skomora" to "C", "Degei" to "D",
                            "Dhartok" to "E", "Gartell" to "F", "Triboulex" to "G", "Aita" to "H"
                        )
                        val order = listOf("A", "B", "C", "D", "E", "F", "G", "H")
                        fun bySector(list: List<Mob>) =
                            list.sortedBy { order.indexOf(sectorOf[it.name] ?: "").let { i -> if (i < 0) 99 else i } }

                        EnterHeading("Minor NMs")
                        Text("One roams each sector and drops a coffer once its objective is met. They can be found on Widescan and spawn anywhere within their sector.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        bySector(vm.mobsForContent("Sortie", "Bosses").filter {
                            vm.contentRoleOf(it, "Sortie", "Bosses") == "Minor"
                        }).forEach { OdyMobRow(vm, it, "Sortie") }

                        Spacer(Modifier.height(10.dp))
                        EnterHeading("Major NMs")
                        Text("Reached through the Diaphanous Gadget of that sector while holding its Plate. Once you claim one the arena door shuts until the boss dies or all enmity drops — make sure everyone is inside first.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        bySector(vm.mobsForContent("Sortie", "Bosses").filter {
                            vm.contentRoleOf(it, "Sortie", "Bosses") == "Major"
                        }).forEach { OdyMobRow(vm, it, "Sortie") }

                        val aminon = vm.mobsForContent("Sortie", "Bosses").filter {
                            vm.contentRoleOf(it, "Sortie", "Bosses") == "Aminon"
                        }
                        if (aminon.isNotEmpty()) {
                            Spacer(Modifier.height(10.dp))
                            EnterHeading("Aminon")
                            Text("The Sector E true boss — 30,000 Gallimaufry, a Ra'Kaznar Starstone and an Old Case +1.",
                                color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                            aminon.forEach { OdyMobRow(vm, it, "Sortie") }
                        }
                    }
                    CollapsibleSection("Gallimaufry", stateKey = "sortie:galli", persist = false) {
                        FactRow("Earning it", "Vanquishing monsters, opening chests and defeating NMs. Regular enemies pay (level - 109) x 3; minor NMs pay about 5x what their level suggests.")
                        FactRow("Rematerialized foes", "Reduced by roughly (2 + sector) x 3 each time, and 5x that for minor NMs.")
                        FactRow("Cap", "100,000 held at once, raised to 100,000,000 once you finish The Voracious Resurgence missions.")
                        EnterHeading("Regular foes, by sector")
                        FactRow("A / B / C / D", "30-36 · 42-48 · 54-60 · 66-72")
                        FactRow("E / F / G / H", "75-81 · 78-84 · 81-87 · 84-90")
                        FactRow("Naakuals (Lv 140)", "93")
                        EnterHeading("NMs")
                        FactRow("Minor", "Obdella 195 · Porxie 255 · Bhoot 315 · Deleterious 375 · Botulus 435 · Ixion 450 · Naraka 465 · Tulittia 480")
                        FactRow("Major", "2,000 for the ground floor four (Ghatjot, Leshonn, Skomora, Degei); 10,000 for the basement four (Dhartok, Gartell, Triboulex, Aita); 30,000 for Aminon.")
                        EnterHeading("Chests")
                        FactRow("Sectors A-D", "Chest 100 · Casket 100 · Coffer 500 · Aurum Coffer 1,000")
                        FactRow("Sectors E-H", "Chest 100 · Casket 300 · Coffer 1,500 · Aurum Coffer 3,000")
                    }
                    CollapsibleSection("Rewards", stateKey = "sortie:rewards", persist = false) {
                        FactRow("Old Cases", "The earring source. An Old Case usually yields a random job's NQ earring and rarely a +1; an Old Case +1 usually yields NQ and rarely a +2; an Old Case +2 always yields a +2.")
                        FactRow("Sapphires & Starstones", "Ra'Kaznar Sapphires come from ground-floor chests and NMs, Ra'Kaznar Starstones from the basement. They feed the Reforged Empyrean +2/+3 upgrades.")
                        FactRow("Eikondrites, Octahedrites, Hexahedrites", "Prime Weapon upgrade materials — eikondrite for a stage 1 weapon (ground floor), octahedrite for stage 2 and hexahedrite for stage 3 (basement).")
                        FactRow("Major NM shards", "Each ground-floor major NM also hands over the Shard or Fragment that opens the matching basement arena.")
                        EnterHeading("JSE earrings by job")
                        FactRow("WAR / MNK / WHM", "Boii · Bhikku · Ebers")
                        FactRow("BLM / RDM / THF", "Wicce · Lethargy · Skulker's")
                        FactRow("PLD / DRK / BST", "Chevalier's · Heathen's · Nukumi")
                        FactRow("BRD / RNG / SAM", "Fili · Amini · Kasuga")
                        FactRow("NIN / DRG / SMN", "Hattori · Peltast's · Beckoner's")
                        FactRow("BLU / COR / PUP", "Hashishin · Chasseur's · Karagoz")
                        FactRow("DNC / SCH / GEO / RUN", "Maculele · Arbatel · Azimuth · Erilaz")
                        EnterHeading("Earring augments")
                        Text("Augments roll randomly but coherently — if a slot carries two statistics they always move together, so you never get the worst accuracy alongside the best double attack.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("NQ", "A fixed job bonus plus slot [1] only: Accuracy & Magic Accuracy +6 to +10.")
                        FactRow("+1", "Slots [1] and [2]: Accuracy & Magic Accuracy +11 to +15, plus a second job-flavoured slot (Store TP, Critical Hit Rate, Damage Taken, Double Attack, Weapon Skill Damage, Enmity).")
                        FactRow("+2", "Slots [1], [2] and [3]: Accuracy & Magic Accuracy +16 to +20, the job-flavoured slot at its best tier, and a stat pair such as STR & VIT or INT & MND at +7 to +15.")
                    }
                    Spacer(Modifier.height(24.dp))
                }
            }
        }
        val om = openMap
        if (om != null) SortieMapOverlay(om)
      }
    }
}

// ---- Sortie maps --------------------------------------------------------------------------------
// Composite sector maps supplied by the user (2048x2048 each), bundled in assets/contentmaps/.
// Ground floor = sectors A-D, basement = sectors E-H, matching the "Sectors & Foes" section above.
private class SortieMap(val title: String, val asset: String, val blurb: String)

private val SORTIE_MAPS = listOf(
    SortieMap(
        "Ground Floor — Sectors A-D",
        "contentmaps/sortie_top.jpg",
        "Start, the Diaphanous Device and the four ground-floor sectors, with the lettered gates, " +
        "party-count doors and the major NM arenas (Ghatjot, Leshonn, Skomora, Degei)."
    ),
    SortieMap(
        "Basement — Sectors E-H",
        "contentmaps/sortie_bottom.jpg",
        "The four basement sectors and their Bitzer letters, the Naakual pool, and the major NM " +
        "arenas (Dhartok, Gartell, Triboulex, Aita) plus Aminon."
    )
)

@Composable
private fun SortieMapRow(map: SortieMap, onClick: () -> Unit) {
    Column(Modifier.fillMaxWidth().clickable(onClick = onClick).padding(vertical = 8.dp)) {
        Text(map.title, color = AccentGold, fontWeight = FontWeight.SemiBold, fontSize = 14.sp)
        Text(map.blurb, color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp,
            modifier = Modifier.padding(start = 12.dp, top = 1.dp))
    }
    HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun SortieMapOverlay(map: SortieMap) {
    val ctx = LocalContext.current
    val bmp = remember(map.asset) {
        runCatching {
            ctx.assets.open(map.asset).use { BitmapFactory.decodeStream(it)?.asImageBitmap() }
        }.getOrNull()
    }
    Box(Modifier.fillMaxSize().background(Charcoal), contentAlignment = Alignment.Center) {
        if (bmp != null) ZoomableImage(bmp)
        else Text("Map not available", color = TextMuted, fontSize = 13.sp)
    }
}

// ---- Master Trials ------------------------------------------------------------------------------
// Seven uncapped 1-6 player battlefields bought from Emporox with Potpourri. Rosters come from the
// "Master Trials: <battlefield>" tags; anything not yet in the bestiary is named in `extra`.
private class MTrial(
    val name: String, val entry: String, val cost: String, val where: String,
    val reward: String, val cast: String, val extra: String = "", val party: String = "1-6 players"
)

private val MASTER_TRIALS = listOf(
    MTrial("Black and White", "Treatise on Monochromacy", "250 Potpourri",
        "Trade the entry item to the Runic Seal in Alzadaal Undersea Ruins (I-9)", "Fermion Sword",
        "Alexander, Odin and the nine Valkyries"),
    MTrial("Unafraid of the Dark", "Gloomy Charm", "250 Potpourri",
        "Home Point: Valdeaunia Front > Castle Zvahl Keep (S) (#1)", "Irradiance Blade",
        "The Shadow Lord and the three Beastmen Leaders"),
    MTrial("Sealed Fate", "Beckoning Bell", "250 Potpourri",
        "Home Point: Lumoria > The Garden of Ru'Hmet (#1)", "Aphelion Knuckles",
        "Arch-Ultima Weapon and Arch-Omega Weapon"),
    MTrial("Heroines Combat II", "Letter from Reisenjima", "5 Potpourri",
        "Reisenjima > Reisenjima Sanctorium (Portal #6)", "Mizukage Naginata",
        "Iroha, Lion, Prishe, Nashmeira, Lilisette and Arciela",
        "Iroha and Nashmeira are not in the bestiary yet."),
    MTrial("Crystal Paradise", "Crystal Paradise", "250 Potpourri",
        "Home Point: Celestial Nexus - Tu'Lia > The Shrine of Ru'Avitau (#1)", "Hedron Dagger",
        "Eald'narche, Kam'lanaut and five Ark Angels"),
    MTrial("Oathsworn Blade", "Oathsworn Blade", "250 Potpourri",
        "Home Point: Ra'Kaznar Inner Court > Ra'Kaznar Inner Court (#1)", "Celestial Spear",
        "August, Teodor and the Naakuals",
        "The Naakuals — Bztavian, Rockfin, Gabbrath, Yggdreant, Waktza and Cehuetzi — are not in the bestiary yet."),
    MTrial("Wings of War", "Wing of War (key item)", "250 Potpourri",
        "Home Point: Valdeaunia > Castle Zvahl Keep (#1)", "Ohakari", "Chaos and Bahamut",
        party = "3-6 players")
)

// ---- Geas Fete ----------------------------------------------------------------------------------
// The Eschan / Reisenjima notorious-monster ladder. Rosters are read live from the `content`
// tags ("Geas Fete: <zone>: <group>"), so adding a mob is a data change, never a screen change.
private val GEAS_ZONES = listOf("Escha ZiTah" to "Escha - Zi'Tah",
                                "Escha RuAun" to "Escha - Ru'Aun",
                                "Reisenjima" to "Reisenjima")

private val GEAS_GROUP_ORDER = listOf("Tier 1", "Tier 2", "Tier 3", "HELM",
                                      "Ark Angels", "Heavenly Beasts", "Nazar")

private val GEAS_TRINKET_NPC = mapOf(
    "Escha ZiTah" to "Affi", "Escha RuAun" to "Dremi", "Reisenjima" to "Shiftrix")

private class Aeonic(val weapon: String, val ws: String, val type: String, val job: String,
                     val fragment: String, val attestation: String, val nm: String)

private val AEONICS = listOf(
    Aeonic("Godhands", "Shijin Spiral", "Hand-to-Hand", "MNK, PUP", "Mystic", "Might", "Mildaunegeux (H-10)"),
    Aeonic("Aeneas", "Exenterator", "Dagger", "THF, BRD, DNC", "Ornate", "Celerity", "Quiebitiel (G-10)"),
    Aeonic("Sequence", "Requiescat", "Sword", "RDM, PLD, BLU", "Holy", "Glory", "Goublefaupe (I-7)"),
    Aeonic("Lionheart", "Resolution", "Great Sword", "RUN", "Intricate", "Righteousness", "Goublefaupe (I-7)"),
    Aeonic("Tri-edge", "Ruinator", "Axe", "BST", "Runaeic", "Bravery", "Dagourmarche (G-9)"),
    Aeonic("Chango", "Upheaval", "Great Axe", "WAR", "Seraphic", "Force", "Goublefaupe (I-7)"),
    Aeonic("Anguta", "Entropy", "Scythe", "DRK", "Tenebrous", "Vigor", "Velosareon (J-8)"),
    Aeonic("Trishula", "Stardiver", "Polearm", "DRG", "Stellar", "Fortitude", "Dagourmarche (G-9)"),
    Aeonic("Heishi Shorinken", "Blade: Shun", "Katana", "NIN", "Demoniac", "Legerity", "Mildaunegeux (H-10)"),
    Aeonic("Dojikiri Yasutsuna", "Tachi: Shoha", "Great Katana", "SAM", "Divine", "Decisiveness", "Velosareon (J-8)"),
    Aeonic("Tishtrya", "Realmrazer", "Club", "WHM, GEO", "Heavenly", "Sacrifice", "Quiebitiel (G-10)"),
    Aeonic("Khatvanga", "Shattersoul", "Staff", "BLM, SMN, SCH", "Celestial", "Virtue", "Dagourmarche (G-9)"),
    Aeonic("Fail-Not", "Apex Arrow", "Bow", "RNG", "Snarled", "Transcendence", "Velosareon (J-8)"),
    Aeonic("Fomalhaut", "Last Stand", "Gun", "RNG, COR", "Ethereal", "Accuracy", "Mildaunegeux (H-10)"),
    Aeonic("Marsyas", "Honor March", "Instrument", "BRD", "Mysterial", "Harmony", "Quiebitiel (G-10)"),
    Aeonic("Srivatsa", "\u2014", "Shield", "PLD", "Supernal", "Invulnerability", "Goublefaupe (I-7)")
)

@Composable
private fun GeasFeteScreen(vm: MobileWatchViewModel) {
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Geas Fete", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_geasfete") }
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {

                    CollapsibleSection("Overview", stateKey = "gf:overview", persist = false) {
                        Text("A ladder of notorious monsters spread across the three Eschan zones and " +
                            "Reisenjima. Every one of them is popped on purpose \u2014 nothing here spawns on its own.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Calling one forth", "Two key items, both consumed when the monster appears: a tribulens (a radialens since the November 2015 update), bought with escha silt, and a \"grisly trinket\" specific to that monster.")
                        FactRow("What they drop", "Experience and capacity points, escha silt, Escha Beads, a piece of equipment specific to that monster, the items used to augment it, and that monster's Vorseal.")
                        FactRow("Unlocking the ladder", "Beat two Tier 1 monsters in a zone and the NPC unlocks one Tier 2 pop item. Every Tier 1 and Tier 2 monster must be cleared before Tier 3 opens. Clearing a whole tier group grants access to the whole of the next one.")
                        FactRow("The special tiers", "HELM, Ark Angels, Heavenly Beasts and Nazar sit outside the numbered tiers. Their grisly trinkets want particular items \u2014 anything from Heavenly Beast seal tatters to HELM items won in the Eschan zones.")
                    }

                    CollapsibleSection("How to participate", stateKey = "gf:how", persist = false) {
                        EnterLine("One to eighteen players. Trusts are allowed.")
                        EnterLine("HP does not scale below three people \u2014 a duo fights the same monster a full party does.", 1)
                        EnterLine("Every member needs a tribulens; only the leader needs the grisly trinket.")
                        EnterLine("The leader spawns it by inspecting a ??? \u2014 each monster has its own set of camps in the zone.")
                        EnterHeading("Where the trinkets come from")
                        GEAS_ZONES.forEach { (tag, label) ->
                            EnterLine("$label \u2014 trade with ${GEAS_TRINKET_NPC[tag]}.", 1)
                        }
                    }

                    CollapsibleSection("Campaigns", stateKey = "gf:campaigns", persist = false) {
                        EnterHeading("Geas Fete Campaign")
                        EnterLine("Double escha silt from monsters in every Escha area, Reisenjima included.")
                        EnterHeading("Geas Fete Campaign \u2014 PLUS!")
                        EnterLine("Double silt, and personal rewards go up by two slots: you also receive an Eschalixir, Eschalixir +1 and Eschalixir +2.")
                        EnterLine("It does not add an equipment drop \u2014 the first slot is still the only one that can hand you a piece of gear directly.", 1)
                        EnterLine("In Reisenjima the extra slots pay out Pellucid, Fern or Taupe Stones instead.", 1)
                        EnterHeading("Reisenjima Geas Fete Equipment Campaign")
                        EnterLine("Opens one additional direct-drop slot on Reisenjima Geas Fete monsters \u2014 a second chance at the gear itself.")
                    }

                    GEAS_ZONES.forEach { (tag, label) ->
                        val mobs = vm.mobsForContent("Geas Fete", tag)
                        val byGroup = mobs.groupBy { vm.contentRoleOf(it, "Geas Fete", tag) }
                        CollapsibleSection(label, stateKey = "gf:$tag", persist = false,
                            subtitle = "${mobs.size} monsters") {
                            GEAS_GROUP_ORDER.forEach { grp ->
                                val list = byGroup[grp].orEmpty()
                                if (list.isNotEmpty()) {
                                    EnterHeading(grp)
                                    list.sortedBy { it.name }.forEach { OdyMobRow(vm, it, tag) }
                                }
                            }
                        }
                    }

                    CollapsibleSection("Aeonic Weapons", stateKey = "gf:aeonic", persist = false,
                        subtitle = "clears every Geas Fete monster") {
                        Text("A complete clear \u2014 every Geas Fete monster in all three Eschan zones \u2014 is " +
                            "what the Aeonic weapons ask for. The sixteen of them, the Fragment and " +
                            "Attestation each one wants and the whole acquisition chain live under " +
                            "Content \u203a Ultimate Weapons.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(vertical = 4.dp))
                    }

                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

// ---- Ultimate Weapons ---------------------------------------------------------------------------
// One home for all five ultimate lines: Relic, Mythic (+ Ergon), Empyrean, Aeonic and Prime.
// Pure reference - no mob data, so nothing here reads the bestiary.
private class UltWeapon(val name: String, val ws: String, val type: String, val job: String,
                        val detail: String = "")

private val RELIC_W = listOf(
    UltWeapon("Spharai", "Final Heaven", "Hand-to-Hand", "MNK", "base from Dynamis - Windurst"),
    UltWeapon("Mandau", "Mercy Stroke", "Dagger", "RDM, THF, BRD", "base from Dynamis - Windurst"),
    UltWeapon("Excalibur", "Knights of Round", "Sword", "RDM, PLD", "base from Dynamis - Windurst"),
    UltWeapon("Ragnarok", "Scourge", "Great Sword", "WAR, PLD, DRK", "base from Dynamis - Bastok"),
    UltWeapon("Guttler", "Onslaught", "Axe", "BST", "base from Dynamis - Bastok"),
    UltWeapon("Bravura", "Metatron Torment", "Great Axe", "WAR", "base from Dynamis - San d'Oria"),
    UltWeapon("Apocalypse", "Catastrophe", "Scythe", "DRK", "base from Dynamis - Bastok"),
    UltWeapon("Gungnir", "Geirskogul", "Polearm", "DRG", "base from Dynamis - San d'Oria"),
    UltWeapon("Kikoku", "Blade: Metsu", "Katana", "NIN", "base from Dynamis - San d'Oria"),
    UltWeapon("Amanomurakumo", "Tachi: Kaiten", "Great Katana", "SAM", "base from Dynamis - Bastok"),
    UltWeapon("Mjollnir", "Randgrith", "Club", "WHM", "base from Dynamis - Windurst"),
    UltWeapon("Claustrum", "Gates of Tartarus", "Staff", "BLM, SMN", "base from Dynamis - Jeuno"),
    UltWeapon("Yoichinoyumi", "Namas Arrow", "Bow", "RNG, SAM", "base from Dynamis - Jeuno"),
    UltWeapon("Annihilator", "Coronach", "Gun", "RNG", "base from Dynamis - San d'Oria"),
    UltWeapon("Gjallarhorn", "\u2014", "Instrument", "BRD", "base from Dynamis - Jeuno"),
    UltWeapon("Aegis", "\u2014", "Shield", "PLD", "base from Dynamis - Jeuno")
)

private val RELIC_LOCATIONS = listOf(
    "Hand-to-Hand" to "Castle Oztroja (G/H-5/6) \u2014 top of the tower past the password trap door",
    "Dagger" to "The Sanctuary of Zi'Tah (L-10) \u2014 a path that leads off the map",
    "Sword" to "Dragon's Aery (G-7) \u2014 in the pond",
    "Great Sword" to "Beaucedine Glacier (G-10) \u2014 at the frozen pond",
    "Axe" to "Western Altepa Desert (H-7)",
    "Great Axe" to "Ru'Lude Gardens (H-9) \u2014 at the fountain",
    "Scythe" to "North Gustaberg (F-7) \u2014 beneath the waterfall, via Dangruf Wadi",
    "Polearm" to "Ru'Aun Gardens (G-6) \u2014 behind the fallen pillar near Byakko",
    "Katana" to "Sea Serpent Grotto (C-10) on map 3",
    "Great Katana" to "Horlais Peak \u2014 in the hot spring",
    "Club" to "The Sanctuary of Zi'Tah (H-8)",
    "Staff" to "Ifrit's Cauldron (H-7) on map 7 \u2014 inside the crater",
    "Bow" to "Cape Teriggan (H-9) \u2014 at the seashore",
    "Gun" to "Metalworks \u2014 inside the Gunpowder Room",
    "Instrument" to "Valley of Sorrows \u2014 north side, mouth of a cave at (H-7), enter via Cape Teriggan (J-8)",
    "Shield" to "Carpenters' Landing (H-10) \u2014 enter from Jugner Forest (E-6)"
)

private val MYTHIC_W = listOf(
    UltWeapon("Conqueror", "King's Justice", "Great Axe", "WAR"),
    UltWeapon("Glanzfaust", "Ascetic's Fury", "Hand-to-Hand", "MNK"),
    UltWeapon("Yagrush", "Mystic Boon", "Club", "WHM"),
    UltWeapon("Laevateinn", "Vidohunir", "Staff", "BLM"),
    UltWeapon("Murgleis", "Death Blossom", "Sword", "RDM"),
    UltWeapon("Vajra", "Mandalic Stab", "Dagger", "THF"),
    UltWeapon("Burtgang", "Atonement", "Sword", "PLD"),
    UltWeapon("Liberator", "Insurgency", "Scythe", "DRK"),
    UltWeapon("Aymur", "Primal Rend", "Axe", "BST"),
    UltWeapon("Carnwenhan", "Mordant Rime", "Dagger", "BRD"),
    UltWeapon("Gastraphetes", "Trueflight", "Crossbow", "RNG"),
    UltWeapon("Kogarasumaru", "Tachi: Rana", "Great Katana", "SAM"),
    UltWeapon("Nagi", "Blade: Kamu", "Katana", "NIN"),
    UltWeapon("Ryunohige", "Drakesbane", "Polearm", "DRG"),
    UltWeapon("Nirvana", "Garland of Bliss", "Staff", "SMN"),
    UltWeapon("Tizona", "Expiacion", "Sword", "BLU"),
    UltWeapon("Death Penalty", "Leaden Salute", "Gun", "COR"),
    UltWeapon("Kenkonken", "Stringing Pummel", "Hand-to-Hand", "PUP"),
    UltWeapon("Terpsichore", "Pyrrhic Kleos", "Dagger", "DNC"),
    UltWeapon("Tupsimati", "Omniscience", "Staff", "SCH"),
    UltWeapon("Idris", "Exudation", "Club", "GEO", "Ergon"),
    UltWeapon("Epeolatry", "Dimidiation", "Great Sword", "RUN", "Ergon")
)

private val EMPY_W = listOf(
    UltWeapon("Verethragna", "Victory Smite", "Hand-to-Hand", "MNK, PUP", "Two-leaf Chloris Bud \u00b7 Ulhuadshi's Fang \u00b7 Dragua's Scale \u00b7 Riftcinder"),
    UltWeapon("Twashtar", "Rudra's Storm", "Dagger", "THF, BRD, DNC", "Glavoid Shell \u00b7 Itzpapalotl's Scale \u00b7 Orthrus's Claw \u00b7 Riftdross"),
    UltWeapon("Almace", "Chant du Cygne", "Sword", "RDM, PLD, BLU", "Helm of Briareus \u00b7 Sobek's Skin \u00b7 Apademak's Horn \u00b7 Riftcinder"),
    UltWeapon("Caladbolg", "Torcleaver", "Great Sword", "PLD, DRK", "Carabosse's Gem \u00b7 Cirein-croin's Lantern \u00b7 Isgebind's Heart \u00b7 Riftdross"),
    UltWeapon("Farsha", "Cloudsplitter", "Axe", "WAR, BST", "Fistule Discharge \u00b7 Bukhis's Wing \u00b7 Alfard's Fang \u00b7 Riftcinder"),
    UltWeapon("Ukonvasara", "Ukko's Fury", "Great Axe", "WAR", "Glavoid Shell \u00b7 Itzpapalotl's Scale \u00b7 Orthrus's Claw \u00b7 Riftdross"),
    UltWeapon("Redemption", "Quietus", "Scythe", "DRK", "Two-leaf Chloris Bud \u00b7 Ulhuadshi's Fang \u00b7 Dragua's Scale \u00b7 Riftcinder"),
    UltWeapon("Rhongomiant", "Camlann's Torment", "Polearm", "DRG", "Two-leaf Chloris Bud \u00b7 Ulhuadshi's Fang \u00b7 Dragua's Scale \u00b7 Riftcinder"),
    UltWeapon("Kannagi", "Blade: Hi", "Katana", "NIN", "Helm of Briareus \u00b7 Sobek's Skin \u00b7 Apademak's Horn \u00b7 Riftdross"),
    UltWeapon("Masamune", "Tachi: Fudo", "Great Katana", "SAM", "Carabosse's Gem \u00b7 Cirein-croin's Lantern \u00b7 Isgebind's Heart \u00b7 Riftcinder"),
    UltWeapon("Gambanteinn", "Dagan", "Club", "WHM", "Fistule Discharge \u00b7 Bukhis's Wing \u00b7 Alfard's Fang \u00b7 Riftdross"),
    UltWeapon("Hvergelmir", "Myrkr", "Staff", "BLM, SMN, SCH", "Kukulkan's Fang \u00b7 Sedna's Tusk \u00b7 Azdaja's Horn \u00b7 Riftdross"),
    UltWeapon("Gandiva", "Jishnu's Radiance", "Bow", "RNG", "Fistule Discharge \u00b7 Bukhis's Wing \u00b7 Alfard's Fang \u00b7 Riftcinder"),
    UltWeapon("Armageddon", "Wildfire", "Gun", "RNG, COR", "Carabosse's Gem \u00b7 Cirein-croin's Lantern \u00b7 Isgebind's Heart \u00b7 Riftdross"),
    UltWeapon("Daurdabla", "\u2014", "Instrument", "BRD", "Iron Plate \u00b7 Colorless Soul \u00b7 Apademak's Horn \u00b7 Riftcinder"),
    UltWeapon("Ochain", "\u2014", "Shield", "PLD", "Iron Plate \u00b7 Colorless Soul \u00b7 Azdaja's Horn \u00b7 Riftdross")
)

private val PRIME_W = listOf(
    UltWeapon("Varga Purnikawa", "Maru Kala", "Hand-to-Hand", "MNK, PUP", "Prime Fists"),
    UltWeapon("Mpu Gandring", "Ruthless Stroke", "Dagger", "RDM, THF, BRD, DNC", "Prime Dagger"),
    UltWeapon("Caliburnus", "Imperator", "Sword", "RDM, PLD, BLU", "Prime Sword"),
    UltWeapon("Helheim", "Fimbulvetr", "Great Sword", "WAR, PLD, DRK, RUN", "Prime Blade"),
    UltWeapon("Spalirisos", "Blitz", "Axe", "BST", "Prime Pickaxe"),
    UltWeapon("Laphria", "Disaster", "Great Axe", "WAR", "Prime Great Axe"),
    UltWeapon("Foenaria", "Origin", "Scythe", "DRK", "Prime Scythe"),
    UltWeapon("Gae Buide", "Diarmuid", "Polearm", "DRG", "Prime Lance"),
    UltWeapon("Dokoku", "Zesho Meppo", "Katana", "NIN", "Genshitanto"),
    UltWeapon("Kusanagi", "Tachi: Mumei", "Great Katana", "SAM", "Genshito"),
    UltWeapon("Lorg Mor", "Dagda", "Club", "WHM, GEO", "Prime Maul"),
    UltWeapon("Opashoro", "Oshala", "Staff", "BLM, SMN, SCH", "Prime Staff"),
    UltWeapon("Pinaka", "Sarv", "Archery", "RNG", "Prime Bow"),
    UltWeapon("Earp", "Terminus", "Marksmanship", "RNG, COR", "Prime Gun"),
    UltWeapon("Duban", "\u2014", "Shield", "PLD", "Prime Shield"),
    UltWeapon("Loughnashade", "Aria of Passion (song)", "Instrument", "BRD", "Prime Horn")
)

@Composable
private fun UltWeaponRow(w: UltWeapon) {
    Column(Modifier.fillMaxWidth().padding(vertical = 5.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(w.name, color = AccentRed, fontSize = 14.sp, fontWeight = FontWeight.Medium,
                modifier = Modifier.weight(1f))
            Text(w.job, color = TextMuted, fontSize = 11.sp)
        }
        Text("${w.type} \u00b7 ${w.ws}", color = TextSoft, fontSize = 12.sp)
        if (w.detail.isNotBlank())
            Text(w.detail, color = TextMuted, fontSize = 11.sp, lineHeight = 15.sp)
    }
    HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun UltimateWeaponsScreen(vm: MobileWatchViewModel) {
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Ultimate Weapons", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {

                    CollapsibleSection("Overview", stateKey = "uw:overview", persist = false) {
                        Text("Five separate lines of high-damage, low-delay weapons, each tied to its own " +
                            "content and each carrying a weapon skill of its own. They all end up in the " +
                            "same place: Oboro in Port Jeuno at (E-6).",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Relic", "Dynamis. Built out of Ancient Currency, an Attestation and a Fragment. 16 weapons.")
                        FactRow("Mythic", "Upgraded Vigil Weapons from the Nyzul Isle Investigation, behind the Captain mercenary rank. 20 weapons, plus 2 Ergon.")
                        FactRow("Ergon", "The mythic equivalent for Rune Fencer and Geomancer, added May 2014. There will never be Ergon weapons for any other job.")
                        FactRow("Empyrean", "Trial of the Magians, fed by Abyssea and Voidwatch notorious monsters. 16 weapons.")
                        FactRow("Aeonic", "A complete Geas Fete clear across all three Eschan zones, for the Seekers of Adoulin jobs. 16 weapons.")
                        FactRow("Prime", "The Voracious Resurgence and Sortie. 16 weapons, and the only line gated by real-world time.")
                    }

                    CollapsibleSection("Relic", stateKey = "uw:relic", persist = false,
                        subtitle = "Dynamis \u00b7 16 weapons") {
                        Text("Costly rather than rare \u2014 everything the upgrade wants can be bought, farmed " +
                            "or shouted for. The stage 3 weapon skill works only inside Dynamis; the finished " +
                            "weapon works anywhere.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        EnterHeading("Currency")
                        EnterLine("Trade 100 single pieces to a Goblin for one 100-piece, in three zones:")
                        EnterLine("Lootblox in Davoi \u2014 M. Silverpiece and R. Goldpiece.", 1)
                        EnterLine("Haggleblix in Beadeaux \u2014 100 Byne Bill and 10,000 Byne Bill.", 1)
                        EnterLine("Antiqix in Castle Oztroja \u2014 L. Jadeshell and R. Stripeshell.", 1)
                        EnterLine("The final stage wants 100 of the 100-piece, and 30 come back when the weapon is finished.")
                        EnterLine("Trade the exact amount \u2014 those NPCs also hand out other Dynamis drops for 100 pieces.", 1)
                        EnterHeading("Upgrade process (Switchstix, Castle Zvahl Baileys I-8)")
                        EnterLine("Stage 1 \u2014 trade the base weapon and three items, speak to him, then trade the currency. One game day.")
                        EnterLine("Stage 1 \u21d2 2 \u2014 same shape, two Earth hours.")
                        EnterLine("Stage 2 \u21d2 3 \u2014 trade the weapon and the required Attestation, then the currency. One Earth hour.")
                        EnterLine("Stage 3 \u21d2 completion \u2014 no visit and no wait: trade the items and currency to a blank target at the location for your weapon type. 3,000 of the 10,000 Ancient Currency comes back.")
                        EnterHeading("Attestation and Fragment")
                        EnterLine("The Attestation comes from a Hydra-corps NM in Dynamis Divergence \u2014 acquire that NM's Parchment first (the same table the Aeonic line uses).")
                        EnterLine("The Fragment comes from Dynamis - Xarcabard: take the Goad from your weapon type's Satellite Weapon and trade it near where that Satellite Weapon spawns to summon the Animated Weapon.", 1)
                        EnterLine("Necropsyche drops off the Vanguard Dragons on the approach to where Dynamis Lord spawns.", 1)
                        EnterHeading("Completion locations")
                        RELIC_LOCATIONS.forEach { (t, where) -> EnterLine("$t \u2014 $where", 1) }
                        EnterHeading("The sixteen")
                        RELIC_W.forEach { UltWeaponRow(it) }
                    }

                    CollapsibleSection("Mythic & Ergon", stateKey = "uw:mythic", persist = false,
                        subtitle = "Nyzul Isle \u00b7 20 + 2 weapons") {
                        Text("Mythics are upgraded Vigil Weapons out of the Nyzul Isle Investigation. Their " +
                            "weapon skills unlock through the matching version of Unlocking a Myth.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        EnterHeading("Mythic acquisition")
                        EnterLine("Captain mercenary rank comes first \u2014 it is what opens the questline.")
                        EnterLine("An Imperial Heist \u2192 Duties, Tasks, and Deeds \u2192 Forging a New Myth \u2192 Coming Full Circle.", 1)
                        EnterLine("From there the level 99 variants come through the Trial of the Magians.", 1)
                        EnterHeading("Ergon \u2014 Rune Fencer and Geomancer")
                        EnterLine("The mythic equivalent for the two jobs that never got one. Their weapon skills come from Rune Fencing the Night Away and Geomancerrific instead.")
                        EnterLine("Legend rank in every coalition is the gate.", 1)
                        EnterLine("Step 1 \u2014 the job's own quest, Saved by the Bell or Quiescence: a subjob-locked BCNM and 100 Pinches of High-Purity Bayld.", 1)
                        EnterLine("Step 2 \u2014 200 Ghastly Stones, one random crafting drop from each Delve I megaboss, 500 Pinches.", 1)
                        EnterLine("Step 3 \u2014 200 Verdigris Stones, one from each Delve II megaboss, 2,500 Pinches.", 1)
                        EnterLine("Step 4 \u2014 200 Wailing Stones, a Pristine Yggrete Crystal (2,500,000 Mweya Plasm) and 9,999 Pinches. That yields the initial item level 119.", 1)
                        EnterLine("Dropped a Lexeme Blade or Nodal Wand? Talk to Geosuke until Runje Desaali asks about it, say yes, and pay her 1,000,000 gil to recraft it at the stage you were on.", 1)
                        EnterLine("Ergon weapons lack the 30% damage boost a mythic gets from its own weapon skill \u2014 but since October 2018 they do carry an Afterglow.", 1)
                        EnterHeading("The twenty-two")
                        MYTHIC_W.forEach { UltWeaponRow(it) }
                    }

                    CollapsibleSection("Empyrean", stateKey = "uw:empy", persist = false,
                        subtitle = "Abyssea \u00b7 Trial of the Magians \u00b7 16 weapons") {
                        Text("Built through the Trial of the Magians on materials from Abyssea notorious " +
                            "monsters and from Voidwatch. Relic-equivalent, aimed at the Aht Urhgan and " +
                            "Wings of the Goddess jobs.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        EnterHeading("The trial ladder")
                        EnterLine("Level 80 \u2014 x50 of the tier's item. Level 85 \u2014 x50 or x75. Level 90 \u2014 x75.")
                        EnterLine("Level 95 \u2014 Heavy Metal Plate x1500 for every weapon in the line.", 1)
                        EnterLine("Level 99 \u2014 Riftcinder or Riftdross x60, depending on the weapon.", 1)
                        EnterLine("Ochain and Daurdabla give something other than a weapon skill, and they stop at 99 II \u2014 there is no 119 variant for either.", 1)
                        EnterHeading("The sixteen")
                        Text("The trail below runs level 80 \u00b7 85 \u00b7 90 \u00b7 99.",
                            color = TextMuted, fontSize = 11.sp,
                            modifier = Modifier.padding(bottom = 2.dp))
                        EMPY_W.forEach { UltWeaponRow(it) }
                    }

                    CollapsibleSection("Aeonic", stateKey = "uw:aeonic", persist = false,
                        subtitle = "Geas Fete \u00b7 16 weapons") {
                        Text("Relic-equivalent weapons for the Seekers of Adoulin jobs, and the only line " +
                            "that asks for a complete clear: every Geas Fete monster in all three Eschan zones.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        EnterHeading("Getting started")
                        EnterLine("The Scintillating Rhapsody key item from the final Rhapsodies of Vana'diel mission opens the hidden area in Reisenjima where Emporox and Temprix live.")
                        EnterLine("Temprix wants Escha Beads for \"secrets\" \u2014 first 10, then 100, then 1000, then a single one. Scroll the menu down; the later options stay hidden until you do.", 1)
                        EnterLine("He then sells the Malformed base key item for 50,000 Escha Beads, matched to the job you are on.", 1)
                        EnterHeading("The clear")
                        EnterLine("Zone by zone, in order: all of Escha - Zi'Tah, then talk to Temprix; then all of Escha - Ru'Aun; then all of Reisenjima.")
                        EnterLine("Any job may do the killing, and Temprix tracks what is left. The monster must die claimed, and a Primeval Brew voids the win.", 1)
                        EnterLine("Then a Fragment and an Attestation, exactly as the Relic line takes them \u2014 Satellite Weapon Goad in Dynamis - Xarcabard, Hydra-corps NM in Divergence.", 1)
                        EnterLine("One game day later Temprix hands over the weapon and the title Herald of a New Age, at item level 119.", 1)
                        EnterHeading("The sixteen")
                        AEONICS.forEach { a ->
                            UltWeaponRow(UltWeapon(a.weapon, a.ws, a.type, a.job,
                                "${a.fragment} Fragment \u00b7 Attestation of ${a.attestation} \u2014 ${a.nm}"))
                        }
                    }

                    CollapsibleSection("Prime", stateKey = "uw:prime", persist = false,
                        subtitle = "Sortie \u00b7 16 weapons \u00b7 six months minimum") {
                        Text("Teased during the early development of The Voracious Resurgence. The first " +
                            "stage arrived in September 2022, the second that November, and the last three " +
                            "in May 2023.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Starting out", "Finish Voracious Resurgence Mission 9-4 \"The Prime Weapons\" and speak to Oggbi. Gama-Shama in the Silver Knife then sells a base Prime Weapon for 10,000 Gallimaufry, and handles every upgrade after it.")
                        FactRow("The weapon skill", "Stage 3 unlocks it, but only inside Sortie. Stage 4 lets you use it anywhere, and also lets the Diaphanous Gadget select Hard Mode Aminon.")
                        FactRow("The real gate", "Six months, minimum \u2014 you can only obtain five Voracious Psyche a month, and the finished weapon wants thirty.")
                        EnterHeading("Stage costs")
                        EnterLine("Stage 1 \u2014 10,000 Gallimaufry.")
                        EnterLine("Stage 2 \u2014 10,000 Gallimaufry, Eikondrite \u00d71.")
                        EnterLine("Stage 3 \u2014 1,000,000 Gallimaufry, Octahedrite \u00d72, Voracious Psyche \u00d75.")
                        EnterLine("Stage 4 \u2014 2,500,000 Gallimaufry, Hexahedrite \u00d73, Voracious Psyche \u00d710.")
                        EnterLine("Stage 5 \u2014 5,000,000 Gallimaufry, Mesosiderite \u00d74, Voracious Psyche \u00d715.")
                        EnterHeading("Cumulative")
                        EnterLine("Stage 3 \u2014 1,020,000 Gallimaufry and 5 Psyche. About one month.", 1)
                        EnterLine("Stage 4 \u2014 3,520,000 Gallimaufry and 15 Psyche. About three months.", 1)
                        EnterLine("Stage 5 \u2014 8,520,000 Gallimaufry and 30 Psyche. About six months.", 1)
                        EnterLine("Item levels run 119 at stage 3, 119 II at stage 4 and 119 III at stage 5.", 1)
                        EnterLine("You cannot hold two of the same Prime Weapon even at different stages, and the NPC will not re-issue a stage 1 for one you threw away.", 1)
                        EnterHeading("The sixteen")
                        PRIME_W.forEach { UltWeaponRow(it) }
                    }

                    CollapsibleSection("Further upgrades \u2014 Oboro", stateKey = "uw:oboro", persist = false,
                        subtitle = "Port Jeuno (E-6)") {
                        Text("Every line except Prime finishes the same way, and only the currency changes.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Initial item level 119", "The level 99 variant plus 300 of the line's stone: Plutons for Relic, Beitetsu for Mythic and Ergon, Riftborn Boulders for Empyrean.")
                        FactRow("Completed item level 119", "The item level 119 variant plus 10,000 of the same stone. A 119 already carrying an Afterglow needs only one.")
                        FactRow("119 III", "Augmented by Oboro once the prerequisites are met. For Relic that is either a Tarutaru Mask of Light from Dynamis - Windurst (D) or 10,000 job points deposited across fifteen real-world weeks.")
                        FactRow("The exceptions", "Ochain and Daurdabla have no 119 variant \u2014 99 II is their finished form. Epeolatry and Idris start at 119 I and skip the first step.")
                    }

                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

@Composable
private fun MasterTrialsScreen(vm: MobileWatchViewModel) {
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Master Trials", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_mastertrials") }
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Overview", stateKey = "mt:overview", persist = false) {
                        Text("Deliberately punishing battlefields for players stretching a job to its limits. " +
                            "Every trial is uncapped, runs an hour, and takes one to six players.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Eligibility", "Level 99 and the Job Master title — you must hold job master status on the job you intend to play here — plus completion of the Rhapsodies of Vana'diel missions.")
                        FactRow("Buying in", "Speak to Emporox in Reisenjima and exchange 250 Potpourri, which is stored Merit Points, for access to one of the seven battlefields. Heroines' Combat II is the cheap one at 5 merit points.")
                        FactRow("Party", "One to six players, and only one of them needs to hold the entry item.")
                        FactRow("Time", "Sixty minutes. You may stay three more minutes after the battle ends, and you leave when the clock runs out or when someone uses the Fireflies temporary item.")
                    }
                    MASTER_TRIALS.forEach { t ->
                        CollapsibleSection(t.name, stateKey = "mt:${t.name}", persist = false,
                            subtitle = t.cast) {
                            FactRow("Entry item", "${t.entry} · ${t.cost}")
                            FactRow("Where", t.where)
                            FactRow("Party / cap", "${t.party} · level uncapped · 60 minutes")
                            FactRow("Reward", t.reward)
                            if (t.extra.isNotBlank())
                                Text(t.extra, color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp,
                                    modifier = Modifier.padding(top = 4.dp))
                            Spacer(Modifier.height(4.dp))
                            vm.mobsForContent("Master Trials", t.name)
                                .sortedBy { it.name }
                                .forEach { OdyMobRow(vm, it, t.name) }
                        }
                    }
                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

// ---- Limbus (119) -------------------------------------------------------------------------------
// The June 2025 rebuild: an open battlefield across the Apollyon and Temenos zones of Al'Taieu.
private class LimbusRoamer(val apollyon: String, val temenos: String, val job: String)

private val LIMBUS_ROAMERS = listOf(
    LimbusRoamer("Pummeler", "Agoge", "Warrior"), LimbusRoamer("Anchorite", "Hesychast", "Monk"),
    LimbusRoamer("Theophany", "Piety", "White Mage"), LimbusRoamer("Spaekona", "Archmage", "Black Mage"),
    LimbusRoamer("Atrophy", "Vitiation", "Red Mage"), LimbusRoamer("Pillager", "Plunderer", "Thief"),
    LimbusRoamer("Reverence", "Caballarius", "Paladin"), LimbusRoamer("Ignominy", "Fallen", "Dark Knight"),
    LimbusRoamer("Totemic", "Ankusa", "Beastmaster"), LimbusRoamer("Brioso", "Bihu", "Bard"),
    LimbusRoamer("Orion", "Arcadian", "Ranger"), LimbusRoamer("Wakido", "Sakonji", "Samurai"),
    LimbusRoamer("Hachiya", "Mochizuki", "Ninja"), LimbusRoamer("Vishap", "Pteroslaver", "Dragoon"),
    LimbusRoamer("Convoker", "Glyphic", "Summoner"), LimbusRoamer("Assimilator", "Luhlaza", "Blue Mage"),
    LimbusRoamer("Laksamana", "Lanun", "Corsair"), LimbusRoamer("Foire", "Pitre", "Puppetmaster"),
    LimbusRoamer("Maxixi", "Horos", "Dancer"), LimbusRoamer("Academic", "Pedagogy", "Scholar"),
    LimbusRoamer("Runeist", "Futhark", "Rune Fencer"), LimbusRoamer("Geomancy", "Bagua", "Geomancer")
)

@Composable
private fun LimbusScreen(vm: MobileWatchViewModel) {
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Limbus", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_limbus") }
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Overview", stateKey = "lb:overview", persist = false) {
                        Text("Rebuilt in the June 2025 update. Where the old Limbus was a sealed battlefield, " +
                            "this one is open — the Apollyon and Temenos zones of Al'Taieu, taken offline for " +
                            "years, reopened as ilvl 119 content. The three areas are physically separate and " +
                            "reached only through the Dimensional Portals at their crags or the Lumoria Home Points.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Eligibility", "Chains of Promathia Chapter 8: Garden of Antiquity, and the Rhapsodies of Vana'diel mission The Orb's Radiance.")
                        FactRow("Key items", "The Scintillating Rhapsody plus a White Card for Temenos or a Black Card for Apollyon. They enter as temporary key items and convert to permanent ones so entry never consumes them — anyone holding a card from before June 2025 keeps it.")
                        FactRow("White Card", "Examine the ??? in Al'Taieu at (H-5), in the northern section near the Holla entrance, or defeat a single Aw'euvhi after entering Al'Taieu from the Crag of Holla portal or Lumoria Home Point #1.")
                        FactRow("Black Card", "Examine the ??? at (D-8) west or (L-8) east, or defeat a single Aw'euvhi after entering from the Crag of Dem or Crag of Mea, or Home Point #2 or #3.")
                        FactRow("Party", "Solo, party, or an alliance up to eighteen. Solo players and single parties may summon up to three alter egos; the usual rule blocking Trust magic at seven or more players still applies.")
                    }
                    CollapsibleSection("Getting In & Content Level", stateKey = "lb:entry", persist = false) {
                        FactRow("Temenos", "Head north from Al'Taieu (H-4) and zone in. Without the Rhapsody and a White Card you are removed after 15 seconds.")
                        FactRow("Apollyon", "Examine either Swirling Vortex, at (E-6) or (K-6) in Al'Taieu. Without the Rhapsody and a Black Card you cannot be transported.")
                        FactRow("Setting the level", "Speak to the Temenos or Apollyon Operator — a Spheroid — and set your Content Level anywhere from 119 to 135, then take the transporter platform and pick a sector and floor.")
                        FactRow("How levels work", "Monsters check as level 150 until something happens. The moment one is aggroed or detects a player, it snaps to that player's chosen content level and stays there until it is defeated and respawns, or goes passive and walks home. Actions taken before that can look like they failed even when the log says otherwise — a Silence that lands on a passive caster will still show it casting.")
                        FactRow("Data", "Killing foes earns \"data\", scaling with the floors as you climb. The rate depends on the level gap and on party size, and anything ten or more levels below your selection awards nothing at all. A bar in the top-left shows your level and the current floor's progress; fill it and it rolls over into that floor's Temporary Item.")
                        Text("Temporary Items from the same floor do not stack, and they stay in your inventory until a chest is opened. Leaving the zone or changing difficulty only resets progress toward the next item — it never takes the ones you hold.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(top = 4.dp))
                        EnterHeading("Sectors")
                        FactRow("Temenos", "Northern Tower F1-F4 · Western Tower F1-F4 · Eastern Tower F1-F4 · Central Temenos F1-F3 · Central Temenos Basement (NM arena)")
                        FactRow("Apollyon", "NW Apollyon F1-F5 · SW Apollyon F1-F4 · NE Apollyon F1-F5 · SE Apollyon F1-F4 · Central Apollyon (NM arena)")
                    }
                    CollapsibleSection("Notorious Monsters", stateKey = "lb:nms", persist = false) {
                        Text("Since the September 2025 update NMs appear in both zones. Their levels are fixed and ignore your content level, there is no claiming and no time limit, and anyone in the zone can join in. Beating them upgrades that zone's chests for every player on the server for the next four Conquest Tallies. A defeated-but-unkilled NM stays put and its HP never recovers.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Unique Data", "Damaging an NM, or being in the party or alliance that does, fills the Unique Data bar. A full bar opens any one chest in that zone.")
                        EnterHeading("Central NMs")
                        Text("Four tiers, spawned by completing the zone's hidden objectives. Clearing tier one reveals the objectives that spawn tier two, and so on. The further you get, the richer next month's chests — and all three sets can only be cleared once per month.",
                            color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        listOf("Apollyon", "Temenos").forEach { zone ->
                            listOf("Tier 1" to "Brown Chest", "Tier 2" to "Red Chest",
                                   "Tier 3" to "Gold Chest").forEach { (tier, chest) ->
                                val mobs = vm.mobsForContent("Limbus", zone)
                                    .filter { vm.contentRoleOf(it, "Limbus", zone) == tier }
                                    .sortedBy { it.name }
                                if (mobs.isNotEmpty()) {
                                    EnterHeading("$zone $tier — $chest")
                                    mobs.forEach { OdyMobRow(vm, it, zone) }
                                }
                            }
                            EnterHeading("$zone Tier 4 — Black Chest")
                            Text(if (zone == "Apollyon") "Apollyon Shades" else "Temenos Echos",
                                color = TextSoft, fontSize = 13.sp, modifier = Modifier.padding(bottom = 4.dp))
                        }
                        FactRow("Objectives", "All hidden, but the zone operator tracks your progress, so they can be found by testing one at a time. They reset with each new tier, scale to the server's population, and are server-wide — anyone who works on them advances them for everybody. Observed types: defeat N mob types, open N chests, defeat N roaming NMs, spawn N ???, and collect N units.")
                        EnterHeading("Roaming NMs")
                        Text("Mannequins that spawn at random spots. Up to four per zone per day, one per sector, each as a random job, respawning once a day at JP midnight. Only four can be up at a time — kill one before its sector will give another. Twenty-two is the most that can be killed between monthly tabulations.",
                            color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        LIMBUS_ROAMERS.forEach { r ->
                            FactRow(r.job, "${r.apollyon} (Apollyon) · ${r.temenos} (Temenos)")
                        }
                    }
                    CollapsibleSection("Chests & Units", stateKey = "lb:chests", persist = false) {
                        FactRow("Opening one", "A chest sits at the end of each sector, and opening it needs every Temporary Item from every floor of every sector in that area. It pays a flat 3,000 or 5,000 units.")
                        FactRow("The bonus chest", "One chest per wing is chosen at random to pay 5,000 units and carry a better chance at Alabaster Matter in Temenos or Murky Matter in Apollyon. It stays the bonus until it is opened, then another is drawn — possibly the same one again.")
                        FactRow("Gold chests", "As the bonus: 5,000 units, 2 of your race's Shard, 2-7 synthesis materials and 1 Matter. Otherwise: 3,000 units, 1 Shard, 0-3 synthesis materials and 0-1 Matter.")
                        FactRow("Verification keys", "Your first chest in Temenos gives the Temenos verification key, which begins Relic +4 reforging; your first in Apollyon gives the Apollyon verification key for Artifact +4. Those first chests also hand over an Alabaster Matter and a Murky Matter respectively.")
                        FactRow("Weekly cap", "Five chests per zone per Conquest Tally — five in each of Apollyon and Temenos. Past the fifth you stop receiving Temporary Items until the weekly reset, though Unique Data can still open chests beyond the cap.")
                        FactRow("Units", "Up to 70,000 of each per week. An unfilled allowance carries over, so one week can reach 140,000. The first five chests each week each raise your holding cap by 3,000 — 15,000 a week — which changes what you can hold, not what you can earn.")
                        FactRow("The ???", "A shimmering effect in Apollyon, a dark cloud in Temenos, spawned where a specific monster dies — /check shows it as \"Impossible to gauge!\". Examining it pays 3,000 units and, once per week per zone, a Temenos or Apollyon Code for opening its chest. Two distinct ??? in a week means 6,000 units.")
                        EnterHeading("Support effects")
                        FactRow("Delineated Grace", "Accuracy, Ranged Accuracy and Magic Accuracy — open the Temenos chest.")
                        FactRow("Angelic Grace", "Base stats (STR, DEX, VIT, AGI, INT, MND, CHR) — open the Apollyon chest.")
                        FactRow("Vital Grace", "Max HP and reduced experience loss — hold both of the above, then open a chest in either zone.")
                        Text("Support effects strengthen with how many chests the whole world has opened, apply automatically on entering either zone, and last for the player's stay. Up to three show in the status bar, and either Operator can confirm them.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(top = 4.dp))
                    }
                    CollapsibleSection("Reforged Armor +4", stateKey = "lb:reforge", persist = false) {
                        Text("Apollyon Units take Reforged Artifact +3 to +4 at the Apollyon Furnace; Temenos Units take Reforged Relic +3 to +4 at the Temenos Furnace. Trade the piece while holding the units and the upgraded item lands in your inventory.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Cost per slot", "Head 20,000 · Body 30,000 · Hands 15,000 · Legs 25,000 · Feet 10,000 — the same for both Artifact and Relic.")
                    }
                    CollapsibleSection("SU4 / SU5 Gear", stateKey = "lb:su", persist = false) {
                        FactRow("How it works", "Trade a Devoid item and the matching Jewel to either Furnace. Devoid items are crafted from Limbus materials; a Jewel comes from trading 1 Alabaster Matter, 1 Murky Matter and 5 Shards. NQ and HQ1 are SU4, HQ2 is SU5, and all three take the same augments.")
                        FactRow("Reinforcement", "Trade the piece and its Jewel back to a Furnace. Thirty ranks of Reinforcement Points, with the Rank 30 augments listed per set.")
                        EnterHeading("Armor sets")
                        FactRow("Justice / Magnificent / Duty", "Shard of Justice ⇒ Jewel of Destiny · MNK, THF, BST, PUP, DNC · Rank 30: Accuracy & Magic Accuracy +30, Store TP +6-8, Triple Attack +3-5%, Pet: Accuracy & Magic Accuracy +30")
                        FactRow("Hope / Perfection / Revelation", "Shard of Hope ⇒ Jewel of Revelation · WAR, BRD, NIN · Rank 30: Accuracy, Ranged Accuracy & Magic Accuracy +30, Double Attack +6-8%, Physical Damage Limit +5-7%")
                        FactRow("Trust / Prestige / Sworn", "Shard of Trust ⇒ Jewel of Camaraderie · WHM, RDM, PLD, DRK, BLU, RUN · Rank 30: Accuracy & Magic Accuracy +30, Triple Attack +6-8%, Phalanx received +4-6")
                        FactRow("Bravery / Intrepid / Indomitable", "Shard of Bravery ⇒ Jewel of Persistence · BLM, SMN, SCH, GEO · Rank 30: Magic Accuracy +30, Magic Attack Bonus +28-32, Blood Pact damage +10-12, Pet: Accuracy & Magic Accuracy +30")
                        FactRow("Mercy / Grace / Clemency", "Shard of Mercy ⇒ Jewel of Affection · RNG, SAM, DRG, COR · Rank 30: Accuracy, Ranged Accuracy & Magic Accuracy +30, Enmity -8 to -10, Quadruple Attack +4-6%, Pet: Accuracy & Magic Accuracy +30")
                        EnterHeading("Weapons")
                        Text("Same idea, but the Devoid weapon pairs with an Auge Scintistone — 1 Alabaster Matter, 1 Murky Matter and 5 Shards, one of each kind. Reinforce with the weapon, another Scintistone and units from either zone.",
                            color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Auge Knuckles", "MNK, PUP · Rank 30: Damage +19, Attack +100, HP +300, Pet damage +5%")
                        FactRow("Auge Knife", "RDM, THF, BRD, DNC · Damage +14, Attack +50, HP +150")
                        FactRow("Auge Sword", "WAR, PLD, DRK · Damage +19, Attack +50, HP +150")
                        FactRow("Auge Saber", "RDM, BLU, COR · Damage +18, Magic Damage +25, HP +150")
                        FactRow("Auge Claymore", "WAR, PLD, DRK, RUN · Damage +35, Attack +70, HP +200")
                        FactRow("Auge Axe", "BST · Damage +20, Attack +50, HP +150, Pet damage +5%")
                        FactRow("Auge Chopper", "WAR · Damage +37, Attack +70, HP +200")
                        FactRow("Auge Scythe", "DRK · Damage +39, Attack +70, HP +200")
                        FactRow("Auge Halberd", "DRG · Damage +29, Attack +70, HP +200")
                        FactRow("Auge Shinobi-gatana", "NIN · Damage +17, Attack & Ranged Attack +50, HP +150")
                        FactRow("Auge Katana", "SAM · Damage +33, Attack +70, HP +200")
                        FactRow("Auge Maul", "WHM, GEO · Damage +25, Magic Damage +25, HP +150")
                        FactRow("Auge Staff", "BLM, SMN, SCH · Damage +27, Magic Damage +30, HP +200, Blood Pact damage +10")
                        FactRow("Auge Bow", "RNG · Damage +35, Ranged Attack +100, HP +300")
                        FactRow("Auge Grip", "All jobs · Attack +30, Magic Damage +20, HP +100")
                        FactRow("Auge Shield", "PLD · Attack +50, HP +150, VIT +30")
                    }
                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

// ---- Abyssea ------------------------------------------------------------------------------------
// The nine field areas (plus Empyreal Paradox), each with its real-world Cavernous Maw and the NM
// roster read live off the "Abyssea: Abyssea-<zone>" content tags.
private class AbyZone(val tag: String, val label: String, val maw: String, val scenario: String)

private val ABYSSEA_ZONES = listOf(
    AbyZone("Abyssea-Konschtat", "Abyssea - Konschtat", "Konschtat Highlands (I-12)", "Vision"),
    AbyZone("Abyssea-La Theine", "Abyssea - La Theine", "La Theine Plateau (E-4)", "Vision"),
    AbyZone("Abyssea-Tahrongi", "Abyssea - Tahrongi", "Tahrongi Canyon (H-12)", "Vision"),
    AbyZone("Abyssea-Attohwa", "Abyssea - Attohwa", "Buburimu Peninsula (F-7)", "Scars"),
    AbyZone("Abyssea-Misareaux", "Abyssea - Misareaux", "Valkurm Dunes (I-9)", "Scars"),
    AbyZone("Abyssea-Vunkerl", "Abyssea - Vunkerl", "Jugner Forest (J-8)", "Scars"),
    AbyZone("Abyssea-Altepa", "Abyssea - Altepa", "South Gustaberg (J-10)", "Heroes"),
    AbyZone("Abyssea-Uleguerand", "Abyssea - Uleguerand", "Xarcabard (H-8)", "Heroes"),
    AbyZone("Abyssea-Grauberg", "Abyssea - Grauberg", "North Gustaberg (G-7), north-east corner", "Heroes"),
    AbyZone("Abyssea-Empyreal Paradox", "Abyssea - Empyreal Paradox", "Qufim Island (F-7)", "Heroes")
)

@Composable
private fun AbysseaScreen(vm: MobileWatchViewModel) {
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Abyssea", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_abyssea") }
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Overview", stateKey = "aby:overview", persist = false) {
                        Text("A parallel Vana'diel released across three expansion scenarios, where the beastmen won " +
                            "the Crystal War and the survivors huddle in small campsites. Its nine field areas are " +
                            "packed with monsters and remain a source of end-game armor, the fastest experience at " +
                            "higher levels, and heavy item and gil farming.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Vision of Abyssea", "Konschtat · La Theine · Tahrongi")
                        FactRow("Scars of Abyssea", "Attohwa · Misareaux · Vunkerl")
                        FactRow("Heroes of Abyssea", "Altepa · Uleguerand · Grauberg (and Empyreal Paradox)")
                        Text("Using Tractor costs you Visitant Status and all of your lights.",
                            color = AccentRed, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(top = 6.dp))
                    }
                    CollapsibleSection("Getting In", stateKey = "aby:entry", persist = false) {
                        FactRow("Starting out", "Zone into Port Jeuno on a level 30+ job. A cutscene plays and \"A Journey Begins\" is flagged in your log — the first quest of the storyline.")
                        FactRow("Entry", "Teleport through a Cavernous Maw. Each of the nine zones has its own, and you need at least one Traverser stone. Stones start accumulating after \"The Truth Beckons\", the second storyline quest.")
                        FactRow("Service NPCs", "They hand out Traverser stones. Joachim in Port Jeuno (H-8) is the main one and the only NPC who advances the storyline quests. Also Erich (Port Bastok K-11), Fabricius (Port Windurst L-6), Gilburt (Port San d'Oria I-8), Fabien (Ru'Lude Gardens H-10), Adrian (Chocobo Circuit H-8) and Jerrett (Heavens Tower).")
                        FactRow("Teleport NPCs — 200 Cruor", "Horst (Port Jeuno H-8), Ernst (Port Bastok K-11), Willis (Port Windurst K-6), Ivan (Port San d'Oria I-8), Vincent (Ru'Lude Gardens H-10), Cyril (Chocobo Circuit H-8), Kierron (Heavens Tower). They only warp you to a maw whose zone quest you have started, and they can check your Cruor balance.")
                    }
                    CollapsibleSection("Traverser Stones", stateKey = "aby:stones", persist = false) {
                        FactRow("How many you hold", "Three to start. Each Abyssite of Avarice — Vermillion, Viridian, Ivory — adds one, up to six.")
                        FactRow("How long they last", "30 minutes each. Every Abyssite of Sojourn adds 3 minutes up to 18 extra: Emerald, Indigo, Ivory, Jade, Sapphire and Scarlet.")
                        FactRow("How fast they return", "One every 20 hours. Each Abyssite of Celerity — Azure, Crimson, Ivory — cuts 4 hours off, down to an 8-hour recharge per stone.")
                        FactRow("Extending time inside", "High-level Blue Sturdy Pyxides give 10 minutes per box unlocked.")
                    }
                    CollapsibleSection("Lights", stateKey = "aby:lights", persist = false) {
                        Text("Defeating a monster or opening a Red Sturdy Pyxis can leave you aglow with a light. Notorious monsters give roughly double, and \"Ephemeral\" monsters can randomly give 2x, 4x, 8x or 16x of one colour.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Pearlescent — cap 230", "Frequency of all chests. Red Pyxis effect, or a melee hit, job ability, Summoner's avatar or DoT killing blow.")
                        FactRow("Azure — cap 255", "Frequency and potency of Blue Pyxides. Red Pyxis effect, or finish with magic.")
                        FactRow("Ruby — cap 255", "Frequency and potency of Red Pyxides. Red Pyxis effect, or finish with a melee weapon skill.")
                        FactRow("Amber — cap 255", "Frequency and potency of Gold Pyxides. Red Pyxis effect, or finish with a magical weapon skill.")
                        FactRow("Golden — cap 200", "Experience points from defeated mobs. Higher-potency Red Pyxis effect.")
                        FactRow("Silvery — cap 200", "Cruor from defeated mobs. Higher-potency Red Pyxis effect.")
                        FactRow("Ebon — cap 200", "Officially it raises the potency of all lights, though the exact effect is still unknown. Higher-potency Red Pyxis effect, and defeating notorious monsters.")
                        Text("Ruby, azure and amber are guaranteed when the proper final blow lands. Pearlescent is NOT guaranteed that way unless the target was a notorious monster.",
                            color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(top = 4.dp))
                    }
                    CollapsibleSection("Sturdy Pyxides", stateKey = "aby:pyxides", persist = false) {
                        FactRow("Blue", "Temporary items, experience points, Cruor and time extensions.")
                        FactRow("Red", "The lights — pearlescent, azure, ruby, amber, golden, silvery and ebon.")
                        FactRow("Gold", "Higher-level temporary items, NM pop items, Empyrean foot armor, augmented equipment and NM key items.")
                        FactRow("Destroying one", "Pays Cruor by chest level — 10 for the weakest, up to 50 for the strongest.")
                    }
                    CollapsibleSection("Staggering NMs", stateKey = "aby:stagger", persist = false) {
                        Text("Staggering stops an Abyssea NM acting for a moment and carries a reward on top. Two large exclamation points appear over it, coloured by which weakness you hit. Repeating the same colour weakens the effect each time — shorter stagger, less influence on drops — and can eventually send the monster into Raged mode. Weaknesses cannot be triggered while the NM is casting, stunned, or readying a TP move.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 6.dp))
                        EnterHeading("Yellow — a spell")
                        Text("Blocks spellcasting. The element depends on the Vana'diel day the NM was claimed (free-roaming) or spawned (force-popped): the day itself, the day before and the day after, so 21 possible spells at any time. The trigger is always one specific spell.",
                            color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Firesday", "Fire III · Fire IV · Firaga III · Flare · Katon: Ni · Ice Threnody · Heat Breath")
                        FactRow("Earthsday", "Stone III · Stone IV · Stonega III · Quake · Doton: Ni · Lightning Threnody · Magnetite Cloud")
                        FactRow("Watersday", "Water III · Water IV · Waterga III · Flood · Suiton: Ni · Fire Threnody · Maelstrom")
                        FactRow("Windsday", "Aero III · Aero IV · Aeroga III · Tornado · Huton: Ni · Earth Threnody · Mysterious Light")
                        FactRow("Iceday", "Blizzard III · Blizzard IV · Blizzaga III · Freeze · Hyoton: Ni · Wind Threnody · Ice Break")
                        FactRow("Lightningday", "Thunder III · Thunder IV · Thundaga III · Burst · Raiton: Ni · Water Threnody · Mind Blast")
                        FactRow("Lightsday", "Banish II · Banish III · Banishga II · Holy · Flash · Dark Threnody · Radiant Breath")
                        FactRow("Darksday", "Drain · Aspir · Dispel · Bio II · Kurayami: Ni · Light Threnody · Eyes On Me")
                        Text("Reward: more Empyrean Armor upgrade items, and more crafting materials or spell scrolls from monsters that do not drop armor items. A BLM/BRD reaches 35 of the 56 spells; BLU/NIN adds another 15; the last 6 need WHM/RDM or WHM/SCH.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(top = 2.dp))
                        EnterHeading("Blue — a physical weapon skill")
                        Text("Blocks TP moves. The weapon type depends on the game time the NM was claimed or force-spawned. Reward: a greater chance of its rare loot.",
                            color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Piercing — 6:00 to 14:00", "Dagger: Shadowstitch, Dancing Edge, Shark Bite, Evisceration · Polearm: Skewer, Wheeling Thrust, Impulse Drive · Archery: Sidewinder, Blast Arrow, Arching Arrow, Empyreal Arrow · Marksmanship: Slug Shot, Blast Shot, Heavy Shot, Detonator")
                        FactRow("Slashing — 14:00 to 22:00", "Sword: Vorpal Blade, Swift Blade, Savage Blade · Great Sword: Spinning Slash, Ground Strike · Axe: Mistral Axe, Decimation · Great Axe: Full Break, Steel Cyclone · Scythe: Cross Reaper, Spiral Hell · Katana: Blade: Ten, Blade: Ku · Great Katana: Tachi: Gekko, Tachi: Kasha")
                        FactRow("Blunt — 22:00 to 6:00", "Hand-to-Hand: Raging Fists, Spinning Attack, Howling Fist, Dragon Kick, Asuran Fists · Club: Skullbreaker, True Strike, Judgment, Hexa Strike, Black Halo · Staff: Heavy Swing, Shell Crusher, Full Swing, Spirit Taker, Retribution")
                        Text("A Monk covers every blunt weapon skill except Judgment and Hexa Strike during 22:00-6:00 — subbing WAR, WHM, PLD, DRK, SAM, BLU or GEO adds Judgment, leaving only a 7% chance the trigger is Hexa Strike.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(top = 2.dp))
                        EnterHeading("Red — an elemental weapon skill")
                        Text("Stops the NM completely. Which elemental weapon skill triggers it is random.",
                            color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("The list", "Dagger: Cyclone, Energy Drain · Sword: Red Lotus Blade, Seraph Blade · Great Sword: Freezebite · Scythe: Shadow of Death · Polearm: Raiden Thrust · Katana: Blade: Ei · Great Katana: Tachi: Jinpu, Tachi: Koki · Club: Seraph Strike · Staff: Earth Crusher, Sunburst")
                        FactRow("Reward", "Guarantees the NM's Atma to everyone in the alliance, provided the player who triggered it is still there, and guarantees the key item used to pop further NMs — that one goes only to whoever claimed or force-popped the monster.")
                        Text("A second red proc DECREASES the chance of the key item and Atma dropping. After the first one, stop using anything on the proc list so you do not accidentally proc again and lose the guarantee.",
                            color = AccentRed, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(top = 4.dp))
                        FactRow("Abyssite of discernment", "Holding it gives you hints: casting magic hints at the yellow element, an elemental weapon skill hints at the red element, and a physical weapon skill hints at the blue weapon type. A hint only narrows the list — it does not mean everything of that element or type will work.")
                    }
                    CollapsibleSection("Quests", stateKey = "aby:quests", persist = false) {
                        Text("The main storyline gates on how many Storyline Zone Quests you have cleared.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Vision — no zone quests", "A Journey Begins (Traverser stone) · The Truth Beckons · Dawn of Death (Joachim starts storing stones; maw teleports for a Cruor fee)")
                        FactRow("Vision — any 3", "First Contact (Lunar abyssite, Ivory abyssite of fortune, Ivory abyssite of acumen) · An Officer and a Pirate · Heart of Madness")
                        FactRow("Scars — any 5", "Tenuous Existence (Ivory abyssite of the reaper, Ivory abyssite of perspicacity) · Champions of Abyssea")
                        FactRow("Heroes — any 7", "A Sea Dog's Summons (Ivory abyssite of guerdon, Lunar abyssite) · Death and Rebirth")
                        FactRow("Heroes — all 9", "Emissaries of God (Ivory abyssite of prosperity, Ivory abyssite of destiny) · Beneath a Blood-red Sky (Abyssite of discernment) · The Wyrm God (Crimson traverser stones) · Meanwhile, Back on Abyssea · A Moonlight Requite (Abyssite of the cosmos)")
                        EnterHeading("Storyline Zone Quests")
                        FactRow("The Forbidden Frontier", "Konschtat — To Paste a Peiste · La Theine — A Goldstruck Gigas · Tahrongi — Megadrile Menace")
                        FactRow("Scars of Abyssea", "Attohwa — A Fluttery Fiend · Misareaux — A Delectable Demon · Vunkerl — The Beast of Bastore")
                        FactRow("Heroes of Abyssea", "Altepa — A Beaked Blusterer · Uleguerand — A Man-eating Mite · Grauberg — An Ulcerous Uragnite")
                        Text("Each zone also carries a long list of ordinary zone quests, plus the Dominion Ops in the Heroes areas. A quest that will not appear usually needs a prerequisite or more fame in that zone.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(top = 2.dp))
                    }
                    CollapsibleSection("Goals & Titles", stateKey = "aby:goals", persist = false) {
                        Text("Nothing has to be accomplished inside, but each zone suggests three goals, tracked by the Abyssea Achievement Tracker there.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Complete every quest in the area", "8,000 Cruor")
                        FactRow("Obtain every Ancient Abyssite in the area", "10,000 Cruor")
                        FactRow("Obtain every Atma available in the area", "12,000 Cruor")
                        FactRow("Titles by zones fully completed", "1 Visitor · 2 Friend · 3 Warrior · 4 Stormer · 5 Devastator · 6 Hero · 7 Champion · 8 Conqueror · 9 Savior of Abyssea")
                    }
                    CollapsibleSection("Battle Content Campaign", stateKey = "aby:campaign", persist = false) {
                        Text("One Abyssea campaign may run in a given month, bundling several bonuses. All six ran during the first one; later campaigns only carried gifts 2, 3, 4 and 6, and anyone who already claimed a reward cannot claim it again — gift 6 is the one that keeps mattering. A blue treasure chest appears near Horst in Port Jeuno (H-8); opening it the first time confers gifts 2, 4 and 5.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Gift 1", "All three Abyssea add-ons registered free — this one only ran during the 2013 Vana'versary.")
                        FactRow("Gift 2 — eleven Atma", "Stout Arm, Allure, Voracious Violet, Stormbird, Gnarled Horn, Razed Ruins, Sanguine Scythe, Minikin Monstrosity, Omnipotent, Stronghold, Merciless Matriarch.")
                        FactRow("Gifts 3 & 4", "One Lunar abyssite, and 100,000 Cruor.")
                        FactRow("Gift 5", "Hold six Traverser stones at once for the duration.")
                        FactRow("Gift 6", "Entering an Abyssea area sets pearlescent, azure, golden and silvery light to their maximum values.")
                    }
                    CollapsibleSection("Zones & Notorious Monsters", stateKey = "aby:zones", persist = false) {
                        Text("Tap any monster for its bestiary entry.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 2.dp))
                        ABYSSEA_ZONES.forEach { z ->
                            CollapsibleSection(z.label, stateKey = "aby:z:${z.tag}", persist = false,
                                subtitle = "${z.scenario} · maw at ${z.maw}") {
                                // Zone Boss floats to the top, then the NMs, then the ordinary adversaries.
                                val rank = mapOf("Zone Boss" to 0, "NM" to 1, "Adversary" to 2, "Bastion" to 3)
                                vm.mobsForContent("Abyssea", z.tag)
                                    .sortedWith(compareBy(
                                        { rank[vm.contentRoleOf(it, "Abyssea", z.tag)] ?: 1 },
                                        { it.name }))
                                    .forEach { mob ->
                                        val role = vm.contentRoleOf(mob, "Abyssea", z.tag)
                                        OdyMobRow(vm, mob, z.tag,
                                            levelText = if (role == "NM" || role.isBlank()) null else role)
                                    }
                            }
                        }
                    }
                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

// Vagary — Xol Triumvirate battle content in the instanced Outer Ra'Kaznar (U), March 2015.
// Three gates, each with a Mega Boss, plus two more spawned from Prototype Pearls. Every NM row
// reads live off the "Vagary: <gate>: <role>" content tags and links into the bestiary.
@Composable
private fun VagaryScreen(vm: MobileWatchViewModel) {
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Vagary", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_vagary") }
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Overview", stateKey = "vag:overview", persist = false) {
                        Text("Added March 2015, Vagary pits pioneers against the Xol Triumvirate — the sinister force " +
                            "first seen in the Seekers of Adoulin storyline. It is where ilvl 119 Reforged Empyrean " +
                            "Armor +1 reforging begins, and it supplies the materials for Superior 2 armor and for " +
                            "taking Reforged Empyrean Armor to 119.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Does not scale", "Unlike most events, the opponents' stats and difficulty are the same no matter how many players come.")
                        FactRow("Zone & timer", "The instanced Outer Ra'Kaznar (U), 45 minutes.")
                        FactRow("Party", "3 to 18 players; only the leader needs the Prototype sigil pearl.")
                        EnterHeading("At a glance")
                        FactRow("Head — Palloritus", "Deathborne Gate · Fomor zone · Vial of Defiant Sweat · drops the fabricated pearl of impurity and ward of biting winds")
                        FactRow("Body — Plouton", "Any gate, any zone · Dark Matter · needs the Prototype pearl of the false king · drops the fabricated pearl and ward of the false king")
                        FactRow("Hands — Putraxia", "Duskbrood Gate · Elemental zone · Macuil Horn · drops the fabricated pearl of biting winds and ward of impurity")
                        FactRow("Legs — Perfidien", "Any gate, any zone · Tartarian Chain · needs the Prototype pearl of ashen wings · drops the fabricated pearl and ward of ashen wings")
                        FactRow("Feet — Rancibus", "Brash Gate · Leech zone · Vial of Plovid Effluvium · drops the fabricated pearl and ward of miasma")
                    }
                    CollapsibleSection("Getting In", stateKey = "vag:entry", persist = false) {
                        FactRow("Eligibility", "Seekers of Adoulin installed, level 95 or higher, and a party or alliance of 3 to 18. The leader must have progressed past mission 5-3-2 (Watery Grave); other members do not need it, though the lore is heavily intertwined.")
                        FactRow("Entry key item", "Trade vials of Befouled Water to the odyssean passage in Leafallia. Befouled Water drops from the Fomors in Outer Ra'Kaznar and Ra'Kaznar Inner Court — the quickest route is the Augural Conveyor to Outer Ra'Kaznar, then the path to the Inner Court.")
                        EnterHeading("Gates — all three need the same key items")
                        EnterLine("Deathborne Gate (M-7) — the Fomor zone, Palloritus")
                        EnterLine("Duskbrood Gate (N-6) — the Elemental zone, Putraxia")
                        EnterLine("Brash Gate (N-7) — the Leech zone, Rancibus")
                    }
                    CollapsibleSection("Deathborne Gate", stateKey = "vag:deathborne", persist = false) {
                        Text("Four waves, all Fomor-flavoured.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        EnterLine("Wave 1 — 20 Fomori (Codex of Etchings, Etched Memory)")
                        EnterLine("Wave 2 — 6 Corses and Lightreaper (Famine Sash, Feast Hose)")
                        EnterLine("Wave 3 — four parties of 3 Fomori (Focal Orb, Limbo Trousers)")
                        EnterLine("Boss wave — multiple Fomori alongside Palloritus")
                        VagaryNmList(vm, "Deathborne Gate")
                    }
                    CollapsibleSection("Duskbrood Gate", stateKey = "vag:duskbrood", persist = false) {
                        Text("An elemental zone. The elementals magic-aggro and link, and clearing every elemental of a type stops Putraxia absorbing that element and casting the matching magic.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Area 1", "Fire → Ice → Earth → Wind → boss hybrids → Thunder. Holds 5 Byrgen, 5 Gefyrst and Blightslither. Pull Blightslither first, then clear the hybrids — all of them must die to open the door to area 2.")
                        FactRow("Area 2", "Water → Light → boss hybrids → Dark. Holds 5 Baelfyr, 5 Ungeweder and Insidivo, which takes reduced magical damage. The Light elementals are in the south-eastern square room the map shows as blocked off — it is actually open.")
                        FactRow("Boss area", "Putraxia and one of each elemental. Kill Dark first to block Death, then Fire and Light so Scholar can use Fusion.")
                        VagaryNmList(vm, "Duskbrood Gate")
                    }
                    CollapsibleSection("Brash Gate", stateKey = "vag:brash", persist = false) {
                        Text("Six numbered columns stand in the middle of the room. Touch one and it despawns, scattering a wave of amorphs around the room. Five columns hold amorphs only; one holds the NM wave, and which one appears to be entirely random.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Amorphs", "Ravaging Acuex, Unabated Mush, Jaundiced Slime, Gangrenous Leech and Dreary Obdella — each takes heightened damage from one element.")
                        FactRow("Brimboil", "Splits when it takes roughly 3,500 damage in a single hit, and every copy splits the same way and casts Meteor with the original. Physical damage dealers should auto-attack without weapon skills; magic dealers should stick to low-tier nukes.")
                        FactRow("Reading the pillar", "\"Fragments of scattered memories begin to coalesce\" means Rancibus will not spawn. \"A thousand scattered memories begin to take shape\" means Rancibus spawns with that wave, or after a few more waves are cleared.")
                        VagaryNmList(vm, "Brash Gate")
                    }
                    CollapsibleSection("Additional NMs", stateKey = "vag:additional", persist = false) {
                        Text("Perfidien and Plouton can be spawned in any zone by completing three hidden objectives. They appear on whoever took the alliance in, wherever that player is, and both can be up at once. Each grants a 15-minute time extension when it dies.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                        VagaryNmList(vm, "Additional NMs")
                        EnterHeading("The element cloud")
                        Text("Just under 90% HP the NM shows a coloured cloud and aligns to a random element — never Light or Dark. It absorbs that element, takes nothing from the descendant element, and heavily resists everything else including physical damage. The cloud's colour is the element it is STRONG against; the element to use is two ascendant from it. Dealing more than a trickle of the aligned element inflicts Encumbrance on everyone, and the longer the boss heals, the longer it lasts.",
                            color = TextSoft, fontSize = 13.sp, lineHeight = 18.sp, modifier = Modifier.padding(bottom = 4.dp))
                        EnterLine("Magic of the weak element procs and announces the correct element to the alliance")
                        EnterLine("A skillchain of any level carrying that element procs and grants a large magic damage bonus")
                        EnterLine("Fail to proc in time and the NM warps out; after the burst window it picks a new element")
                        EnterLine("Never using elemental damage at all means no resistance builds — physical weapon skills that do not skillchain can take one down quickly")
                        EnterHeading("Spawn objectives")
                        FactRow("Perfidien — Prototype pearl of ashen wings, CL 130", "Defeat 5 enemies within 5 seconds of gaining enmity · perform a 4-step skillchain · defeat 5 enemies with magic bursts.")
                        FactRow("Plouton — Prototype pearl of the false king, CL 132", "Defeat 5 more enemies within 5 seconds of gaining enmity · perform a 6-step skillchain · magic burst for at least 5,000 damage without defeating the enemy, five times.")
                        Text("Objectives can be done in any order, and one enemy or one action can progress several. You must aggro an enemy before killing it for the speed objective to count.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(top = 2.dp))
                        FactRow("Watching the messages", "Ashen Wings goes Umbral Hue → Deeper Black Hue → \"indistinguishable from the dead of night\" and Perfidien spawns. False Kings goes Deeper Red Hue → Crimson Hue → \"indistinguishable from a pool of blood\" and Plouton spawns.")
                        FactRow("Death rules", "If anyone dies before the NM spawns, it can no longer be spawned that run. If anyone dies during the fight, the NM warps immediately and cannot be respawned. Only the player who brought the alliance in has their pearl consumed.")
                        EnterHeading("Obtaining the Prototype Pearls")
                        FactRow("Ashen wings", "Interact with the Odyssean Passage in Leafallia holding the fabricated pearls of impurity, biting winds and miasma. You must have completed the required Seekers missions and taken an alliance into Vagary at least once — and you must be holding a Prototype sigil pearl when the NMs die to receive their key items.")
                        FactRow("False king", "Same passage, holding the Fabricated pearl of ashen wings from Perfidien. Each pearl is consumed when its NM appears, and the fabricated pearls have to be farmed again.")
                    }
                    CollapsibleSection("Reward Redemption", stateKey = "vag:redeem", persist = false) {
                        Text("Collect all five Fabricated Wards — impurity (Putraxia), miasma (Rancibus), biting winds (Palloritus), ashen wings (Perfidien) and the false king (Plouton) — then click the Odyssean Passage in Leafallia (H-8) and trade the set for one of three choices.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        EnterLine("Any piece of equipment that drops off any monster in any Vagary zone, except Tartarus Platemail")
                        EnterLine("Any synthesis or upgrade material off the Mega Boss NMs, or an Etched Memory")
                        EnterLine("A reward at random — this pool can include Tartarus Platemail, any Mega Boss material, a Codex of Etchings or an Etched Memory")
                        FactRow("Vagary Campaign", "The monthly campaign raises the Codex of Etchings and Etched Memory drop rate, and turning in the five wards yields two items instead of one — the extra coming from the \"whatever the master deems worthy\" pool. Rare drops like Tartarus Platemail are far likelier during it; most of the ones in the game came from campaign months.")
                    }
                    CollapsibleSection("Boss Drops", stateKey = "vag:drops", persist = false) {
                        FactRow("Palloritus", "Vial of Defiant Sweat ×2-3, Defiant Scarf ×1-2, Achiuchikapu, Defiant Collar, Punchinellos, Rhadamanthus")
                        FactRow("Putraxia", "Macuil Horn ×2-3, Macuil Plating ×1-2, Acclimator, Crusher Gauntlets, Rumination Sash, Soulcleaver")
                        FactRow("Rancibus", "Vial of Plovid Effluvium ×2-3, Chunk of Plovid Flesh ×1-2, Cryptic Earring, Devivifier, Miasmic Pants, Mindmelter")
                        FactRow("Perfidien", "Tartarian Chain ×2-3, Tartarian Soul ×1-2, Count's Cuffs, Count's Garb, Enervating Earring, Etiolation Earring")
                        FactRow("Plouton", "Dark Matter ×2-3, Hades' Claw ×1-2, Befouled Crown, Incarnation Sash, Odium, and the very rare Tartarus Platemail")
                        FactRow("Tier NMs", "Blightslither — Supay Weskit, Umbra Strap · Insidivo — Avatara Slops, Vengeful Ring · Murkcrawler — Brahmastra, Rabid Visor · Brimboil — Deviant Necklace, Meekculler · Lightreaper — Famine Sash, Feast Hose")
                        FactRow("Trash", "Every wave and every column can drop a Codex of Etchings or an Etched Memory; wave 3 of the Deathborne Gate adds Focal Orb and Limbo Trousers.")
                    }
                    CollapsibleSection("Alternative Battlefields", stateKey = "vag:alt", persist = false) {
                        Text("Added October 2018 in Ra'Kaznar Turris as another way to unlock Reforged Empyrean Armor +1 through Monisette. You fight one Vagary boss of your choosing, with no drops at all — these exist purely to unlock the armor upgrade.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(bottom = 4.dp))
                        FactRow("Requirements", "1 to 6 players, every one holding a Prototype sigil pearl, which is consumed on entry. Trade a Befouled Water to the Odyssean Passage in Leafallia for another.")
                        FactRow("Missions", "Putraxia, Rancibus and Palloritus need Watery Grave; Perfidien needs Reckoning; Plouton needs Abomination.")
                        FactRow("Joining", "Inspect the Ominous Postern in Ra'Kaznar Turris and pick your battlefield. Home Point #1 in Ra'Kaznar Inner Court is the easy way in. 30 minutes, and a title on victory.")
                        FactRow("What you don't get", "No experience, capacity points or treasure, and they do not count toward the Vagary Records of Eminence objective.")
                        FactRow("Blue Magic", "They can still be used to learn spells — Cruel Joke from Palloritus, Cesspool from Rancibus, Tearing Gust from Putraxia.")
                    }
                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

// The NM rows for one Vagary section, ordered tier/wave first and the Mega Boss last, with the
// content tag's role segment (Tier I, Wave 2, Head …) as the right-hand label.
@Composable
private fun VagaryNmList(vm: MobileWatchViewModel, section: String) {
    val slots = setOf("Head", "Body", "Hands", "Legs", "Feet")
    val roleOrder = listOf("Wave 2", "Tier I", "Tier II")
    val mobs = vm.mobsForContent("Vagary", section).sortedBy {
        val role = vm.contentRoleOf(it, "Vagary", section)
        if (role in slots) 99 else roleOrder.indexOf(role).let { i -> if (i < 0) 50 else i }
    }
    mobs.forEach { m ->
        val role = vm.contentRoleOf(m, "Vagary", section)
        OdyMobRow(vm, m, "Vagary", levelText = if (role.isBlank()) null else role)
    }
}

// ---- Unity Concord -----------------------------------------------------------------------------
// A Unity Wanted battle as published by BG: the NM, the level/accolade band it sits in, its zone and
// the Unity Warp destination, plus the Wanted tier from the Category column. The roster is ordered by
// this table; the Mob object (and so the bestiary link) comes from the content tags.
private class UWanted(
    val key: String, val level: Int, val accolades: String,
    val zone: String, val warp: String, val tier: Int
)

private val UNITY_WANTED = listOf(
    UWanted("bounding belinda", 75, "200", "South Gustaberg", "E-7", 1),
    UWanted("hugemaw harold", 75, "200", "East Ronfaure", "G-9", 1),
    UWanted("prickly pitriv", 75, "200", "East Sarutabaruta", "J-8", 1),
    UWanted("ironhorn baldurno", 99, "400", "La Theine Plateau", "H-8", 1),
    UWanted("sleepy mabel", 99, "400", "Konschtat Highlands", "G-7", 1),
    UWanted("serpopard ninlil", 99, "400", "Tahrongi Canyon", "J-8", 1),
    UWanted("abyssdiver", 119, "1,500", "Buburimu Peninsula", "F-6", 1),
    UWanted("immanibugard", 119, "1,500", "Lufaise Meadows", "K-8", 2),
    UWanted("intuila", 119, "1,500", "Bibiki Bay", "I-6", 1),
    UWanted("jester malatrix", 119, "1,500", "Qufim Island", "I-8", 1),
    UWanted("orcfeltrap", 119, "1,500", "Carpenters' Landing", "I-11", 1),
    UWanted("sybaritic samantha", 119, "1,500", "Yuhtunga Jungle", "F-11", 1),
    UWanted("valkurm imperator", 119, "1,500", "Valkurm Dunes", "G-8", 1),
    UWanted("cactrot veloz", 122, "1,800", "Eastern Altepa Desert", "J-8", 1),
    UWanted("emperor arthro", 122, "1,800", "Jugner Forest", "I-8", 1),
    UWanted("garbage gel", 122, "1,800", "Bostaunieux Oubliette", "Map 2 D-9", 2),
    UWanted("joyous green", 122, "1,800", "Pashhow Marshlands", "E-12", 1),
    UWanted("keeper of heiligtum", 122, "1,800", "The Sanctuary of Zi'Tah", "K-12", 1),
    UWanted("tiyanak", 122, "1,800", "Misareaux Coast", "F-7", 2),
    UWanted("voso", 122, "1,800", "Labyrinth of Onzozo", "G-6", 2),
    UWanted("warblade beak", 122, "1,800", "Meriphataud Mountains", "F-11", 1),
    UWanted("woodland mender", 122, "1,800", "Yhoator Jungle", "J-7", 1),
    UWanted("arke", 125, "2,100", "Sauromugue Champaign", "J-6", 1),
    UWanted("ayapec", 125, "2,100", "The Boyahda Tree", "Map 2 F-6", 2),
    UWanted("azure-toothed clawberry", 125, "2,100", "Temple of Uggalepih", "Map 2 I-6", 2),
    UWanted("bakunawa", 125, "2,100", "Sea Serpent Grotto", "Map 4 L-5", 2),
    UWanted("beist", 125, "2,100", "Xarcabard", "J-9", 2),
    UWanted("centurio xx-i", 125, "2,100", "Quicksand Caves", "Map 1 J-5", 2),
    UWanted("coca", 125, "2,100", "Ifrit's Cauldron", "Map 3 K-6", 2),
    UWanted("douma weapon", 125, "2,100", "Ro'Maeve", "H-11", 1),
    UWanted("king uropygid", 125, "2,100", "Western Altepa Desert", "I-7", 1),
    UWanted("kubool ja's mhuufya", 125, "2,100", "Wajaom Woodlands", "I-10", 2),
    UWanted("largantua", 125, "2,100", "Beaucedine Glacier", "I-9", 1),
    UWanted("lumber jill", 125, "2,100", "Batallia Downs", "K-8", 1),
    UWanted("mephitas", 125, "2,100", "Garlaige Citadel", "Map 4 G-6", 2),
    UWanted("muut", 125, "2,100", "Attohwa Chasm", "F-7", 2),
    UWanted("specter worm", 125, "2,100", "Kuftal Tunnel", "Map 2 G-3", 2),
    UWanted("strix", 125, "2,100", "Rolanberry Fields", "D-11", 1),
    UWanted("vermillion fishfly", 125, "2,100", "Lufaise Meadows", "K-8", 2),
    UWanted("azrael", 128, "2,400", "Den of Rancor", "Map 2 G-12", 2),
    UWanted("borealis shadow", 128, "2,400", "Fei'Yin", "Map 1 F-11", 2),
    UWanted("camahueto", 128, "2,400", "Uleguerand Range", "E-9", 2),
    UWanted("carousing celine", 128, "2,400", "Fei'Yin", "Map 1 F-11", 2),
    UWanted("grand grenade", 128, "2,400", "Mount Zhayolm", "C-7", 2),
    UWanted("vedrfolnir", 128, "2,400", "Cape Teriggan", "H-7", 1),
    UWanted("vidmapire", 128, "2,400", "Alzadaal Undersea Ruins", "Map 5 G-9", 2),
    UWanted("volatile cluster", 128, "2,400", "Misareaux Coast", "F-7", 2),
    UWanted("glazemane", 128, "2,400", "Cape Teriggan", "H-7", 2),
    UWanted("wyvernhunter bambrox", 128, "2,400", "Gustav Tunnel", "Map 2 H-10", 2),
    UWanted("hidhaegg", 135, "3,100", "The Boyahda Tree", "Map 2 F-6", 2),
    UWanted("sovereign behemoth", 135, "3,100", "Behemoth's Dominion", "F-7", 2),
    UWanted("tolba", 135, "3,100", "Valley of Sorrows", "F-8", 2),
    UWanted("thu'ban", 135, "3,100", "Wajaom Woodlands", "I-10", 3),
    UWanted("sarama", 135, "3,100", "Mount Zhayolm", "C-7", 3),
    UWanted("shedu", 135, "3,100", "Caedarva Mire", "Map 4 H-9", 3),
    UWanted("tumult curator", 145, "4,100", "Aydeewa Subterrane", "Map 2 H-10", 3)
)

@Composable
private fun UnityNmRow(vm: MobileWatchViewModel, mob: Mob?, w: UWanted) {
    val name = mob?.name ?: w.key.replaceFirstChar { it.uppercase() }
    Row(
        Modifier.fillMaxWidth()
            .then(if (mob != null) Modifier.clickable { vm.selectMob(mob, w.zone) } else Modifier)
            .padding(vertical = 7.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(Modifier.weight(1f)) {
            Text(name, color = AccentRed, fontSize = 14.sp, fontWeight = FontWeight.Medium)
            Text(listOfNotNull(mob?.family?.ifBlank { null }, w.zone).joinToString(" · ") + "  (${w.warp})",
                color = TextMuted, fontSize = 10.sp, lineHeight = 14.sp)
        }
        Text("Wanted ${w.tier}", color = TextMuted, fontSize = 12.sp)
    }
    HorizontalDivider(color = CharcoalDark)
}

// Unity Concord — collaborative Records of Eminence factions, Accolades, and the 56 Wanted battles.
// Roster rows link straight into the bestiary via the "Unity: Wanted: Wanted N" content tags.
@Composable
private fun UnityScreen(vm: MobileWatchViewModel) {
    val byName = remember {
        vm.mobsForContent("Unity", "Wanted").associateBy { it.name.lowercase() }
    }
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Unity", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "banner") { ContentBanner("content_unity") }
            item(key = "body") {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Overview", stateKey = "unity:overview", persist = false) {
                        Text("A collaborative Records of Eminence event, added November 2014. You pledge to one of " +
                            "eleven Unity factions and earn Accolades — the Unity currency — for completing objectives. " +
                            "The headline rewards are the unique weapons and armor taken from Wanted Battles against " +
                            "notorious monsters.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FactRow("Weekly ranking", "Everyone's effort sets the faction's rank each week. Rank is an average of every member's individual evaluation, scored at one point per 1,000 Accolades earned through Records of Eminence.")
                        FactRow("Higher rank", "Increases the bonus from the Unity: stat on Unity weapons and armor.")
                        FactRow("Lower rank", "Increases the Capacity Point bonus: Bonus% = 2 x (Rank - 1), so 11th place gives +20%.")
                        FactRow("Accolade bonus", "+5% to Accolades gained for each ranking below 1st — Rank 11 receives +50%.")
                    }
                    CollapsibleSection("Getting Started", stateKey = "unity:start", persist = false) {
                        FactRow("Requirement", "Complete ten or more Records of Eminence objectives, then visit any San d'Oria, Bastok, Windurst or Adoulin area.")
                        FactRow("Joining", "Set the Records of Eminence objective \"All for One\" (under the Tutorial section of the RoE menu), speak to a Unity Service NPC and pick a faction.")
                        EnterHeading("Unity Service NPCs")
                        EnterLine("Urbiolaine — Southern San d'Oria (G-10)")
                        EnterLine("Igsli — Bastok Markets (E-11)")
                        EnterLine("Teldro-Kesdrodo — Windurst Woods (J-10)")
                        EnterLine("Yonolala — Windurst Woods (J-10)")
                        EnterLine("Nunaarl Bthtrogg — Western Adoulin (H-11)")
                        EnterHeading("Factions")
                        Text("Pieuje · Ayame · Invincible Shield · Apururu · Maat · Aldo · Jakoh Wahcondalo · Naja Salaheem · Flaviria · Sylvie · Yoran-Oran",
                            color = TextSoft, fontSize = 13.sp, lineHeight = 18.sp)
                        FactRow("Changing faction", "Pay Accolades to an A.M.A.N. representative — the fee scales with the ranking gap, and moving to a higher-ranked Unity costs more. After switching you cannot move again until the following Sunday at JST midnight, and you lose the prior and current week's evaluation points.")
                    }
                    CollapsibleSection("Accolades & Objectives", stateKey = "unity:accolades", persist = false) {
                        FactRow("Earning", "Records of Eminence objectives under the Unity section pay the most. Non-Unity objectives and certain monsters pay a small amount. Some Unity objectives are shared, others are faction-specific, and they count toward your 30-objective limit.")
                        FactRow("Cap", "Accolades cap at 99,999 held. Since the June 2020 update, Sparks of Eminence and Unity Accolades each have a 100,000-point weekly exchange limit that resets Sunday 8:00 a.m. PDT / 3:00 p.m. GMT.")
                        EnterHeading("Spending them")
                        EnterLine("Entering Wanted battles — 300 to 4,100 per NM spawn")
                        EnterLine("Purchasing items from Unity NPCs")
                        EnterLine("Enhancing Wanted-battle equipment — 1,000 to 10,000 per upgrade")
                        EnterLine("Teleporting to a Wanted staging area — 100 per warp")
                        EnterLine("Determining your faction rank")
                        FactRow("Unity Trusts", "Earn 5,000 Accolades in a tally period and your Unity leader becomes callable as an alter ego. Not earning enough in a later period can eventually lose them, and you need a partial evaluation of 5 before you can summon your leader.")
                        FactRow("Unity Chat", "Speak to your whole faction with /unity or /u, or set it as your default chat mode. Toggle it under Status > Unity > Unity Info.")
                        FactRow("Unity Lists", "The Unity menu lists members by faction, searchable like the area menus — handy for tracking down who defected where.")
                    }
                    CollapsibleSection("Wanted Battles", stateKey = "unity:wanted", persist = false) {
                        Text("Confrontation-style fights against a specific NM in a sealed area — no other player or monster can interfere. Flag them in the Records of Eminence menu under Unity; the zone, fight location, recommended level, cost and rewards are all listed there.",
                            color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        EnterLine("A party or alliance of 1 to 18 players, unsynced")
                        EnterLine("Only one person needs the objective set to start the fight — but only those who set it get rewards")
                        EnterLine("Fights are started at Ethereal Junctions, the way Planar Rifts work")
                        Text("Tumult Curator does not appear in the objective list until Thu'ban, Sarama and Shedu have been defeated.",
                            color = AccentRed, fontSize = 12.sp, lineHeight = 17.sp,
                            modifier = Modifier.padding(top = 6.dp))
                        Text("56 battles in total. The coordinate after each zone is the 100-Accolade Unity Warp destination.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp,
                            modifier = Modifier.padding(top = 8.dp, bottom = 2.dp))
                        UNITY_WANTED.groupBy { it.level }.toSortedMap().forEach { (lv, list) ->
                            CollapsibleSection("Lv $lv · ${list.first().accolades} accolades (${list.size})",
                                stateKey = "unity:wanted:$lv", persist = false) {
                                list.sortedBy { it.key }.forEach { w -> UnityNmRow(vm, byName[w.key], w) }
                            }
                        }
                    }
                    CollapsibleSection("Rewards", stateKey = "unity:rewards", persist = false) {
                        FactRow("Coffers", "Beating a Wanted NM gives you a coffer for that NM. It can hold the NQ or HQ version of that NM's equipment, that NM's upgrade material, other synthesis materials, or gil.")
                        FactRow("NQ to HQ", "Once you hold the NQ you can upgrade it at a Unity NPC for Accolades plus materials, whether or not you have ever beaten that NM. The work takes one Vana'diel day.")
                        FactRow("Augmenting a +1", "Since March 2020 the ilvl 119 +1 gear can be augmented through Odyssey, on a single ranked path. You must have cleared the matching wing of Sheol by reaching the exit.")
                        FactRow("Starting the path", "Trade the +1 item, one matching Lustreless item and 30,000 Accolades to a Unity NPC for the first rank.")
                        FactRow("Reinforcement Points", "One Lustreless Scale, Hide or Wing is +5 RP. Rank 15 is the cap and needs 5,955 RP — 1,191 Lustreless items in total (12 stacks and 3 single), counting the one that starts the process. Each item type only augments its own gear and they cannot substitute for each other.")
                        Text("Every reward below is grouped by slot. The x50 Lustreless material is the Odyssey augment path; the level 99 and lower sets use their own cheaper upgrade.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp,
                            modifier = Modifier.padding(top = 8.dp, bottom = 2.dp))
                        CollapsibleSection("Melee weapons", stateKey = "unity:rw:melee", persist = false) {
                            FactRow("Aizkora +1 (Great Axe)", "Azrael · Azrael's Eye x50 · Lustreless Hide · Acc & MAcc +45 / Triple Attack +3% / Quadruple Attack +3%")
                            FactRow("Anathema Harpe +1 (Dagger)", "Muut · Muut's Vestment x50 · Hide · DMG +20 / Acc & MAcc +40 / Critical Hit Rate +10%")
                            FactRow("Beheader +1 (Great Axe)", "Borealis Shadow · Ethereal Incense x50 · Hide · DMG +53 / Acc & MAcc +40 / Haste +10%")
                            FactRow("Buramgh +1 (Axe)", "Jester Malatrix · Jester Malatrix's Shard x50 · Scale · DMG +30 / Pet: Acc & MAcc +30 / Acc & MAcc +35")
                            FactRow("Combuster +1 (Sword)", "Hidhaegg · Hidhaegg's Scale x50 · Wing · DMG +19 / Acc & MAcc +40 / Store TP +10")
                            FactRow("Comeuppances +1 (H2H)", "Tumult Curator · Tumult's Blood x50 · Wing · DEX +20 / Acc & MAcc +40 / Store TP +10 / Pet: Acc & MAcc +40")
                            FactRow("Demers. Degen +1 (Sword)", "Bakunawa · Bakunawa's Ink x50 · Hide · Acc & MAcc +45 / DEX +10 / Sword Enhancement Spell Damage +50%")
                            FactRow("Emeici +1 (H2H)", "Garbage Gel · Jar of Garbage Gel's Mucus x50 · Scale · DMG +30 / Acc & MAcc +30 / Critical Hit Rate +10%")
                            FactRow("Fists of Fury +1 (H2H)", "Borealis Shadow · Ethereal Incense x50 · Hide · DMG +14 / Acc & MAcc +40 / Regen +5")
                            FactRow("Flyssa +1 (Sword)", "Shedu · Shedu's Mane x50 · Wing · DMG +10 / Acc & MAcc +40 / Damage taken -5%")
                            FactRow("Gae Derg +1 (Polearm)", "Coca · Coca's Wing x50 · Hide · DMG +62 / Acc & MAcc +40 / Store TP +8")
                            FactRow("Habilitator +1 (Axe)", "Thu'ban · Thu'ban's Scale x50 · Wing · DMG +21 / Acc & MAcc +40 / STR·DEX·CHR +10 / Pet: Acc & MAcc +40")
                            FactRow("Jugo Kukri +1 (Dagger)", "Vedrfolnir · Vedrfolnir's Wing x50 · Hide · DMG +13 / Acc & MAcc +40 / Evasion +20")
                            FactRow("Kladenets +1 (Great Sword)", "Specter Worm · Specter's Ore x50 · Hide · DMG +50 / Acc & MAcc +40 / Fast Cast +10%")
                            FactRow("Kunimune +1 (Great Katana)", "Keeper of Heiligtum · Heiligtum's Moss x50 · Scale · TP Bonus +500 / Acc & MAcc +30 / STR +10")
                            FactRow("Kustawi +1 (Dagger)", "Glazemane · Glazemane's Fang x50 · Hide · Ranged Attack +20 / Ranged Acc & MAcc +40 / Enmity -5")
                            FactRow("Loxotic Mace +1 (Club)", "Grand Grenade · G. Grenade's Ash x50 · Hide · DMG +33 / Acc & MAcc +40 / Weapon Skill Damage +10%")
                            FactRow("Mdomo Axe +1 (Axe)", "Kubool Ja's Mhuufya · Mhuufya's Beak x50 · Hide · DMG +24 / Acc & MAcc +40 / Pet: Acc & MAcc +50")
                            FactRow("Montante +1 (Great Sword)", "Sarama · Sarama's Hide x50 · Wing · DMG +20 / Acc & MAcc +40 / HP +100")
                            FactRow("Norifusa +1 (Great Katana)", "Volatile Cluster · V. Cluster's Ash x50 · Hide · DMG +10 / Acc & MAcc +40 / Skillchain Damage +20%")
                            FactRow("Nullis +1 (Great Sword)", "Hidhaegg · Hidhaegg's Scale x50 · Wing · DMG +33 / Acc & MAcc +40 / Dark magic skill +10")
                            FactRow("Perun +1 (Axe)", "Ayapec · Ayapec's Shell x50 · Hide · Ranged Attack +45 / Ranged Acc & MAcc +30 / Snapshot +5%")
                            FactRow("Pixquizpan +1 (Scythe)", "Wyvernhunter Bambrox · Bambrox's Shawl x50 · Hide · DMG +36 / Acc & MAcc +40 / Magic Attack Bonus +50")
                            FactRow("Pukulatmuj +1 (Sword)", "Arke · Arke's Wing x50 · Hide · DMG +38 / Acc & MAcc +30 / Sword Enhancement Spell Damage +150%")
                            FactRow("Raicho +1 (Katana)", "Vidmapire · Vidmapire's Claw x50 · Hide · DMG +20 / Acc & MAcc +40 / Magic Defense Bonus +5")
                            FactRow("Sangarius +1 (Sword)", "Lumber Jill · Vial of Lumber Jill's Spittle x50 · Hide · DMG +35 / Acc & MAcc +30 / Quadruple Attack +3%")
                            FactRow("Tancho +1 (Katana)", "Orcfeltrap · Orcfeltrap's Leaf x50 · Scale · DMG +25 / Acc, Ranged Acc & MAcc +20 / Magic Attack Bonus +20")
                            FactRow("Tanmogayi +1 (Sword)", "Sarama · Sarama's Hide x50 · Wing · DMG +11 / Acc & MAcc +40 / Attack +40")
                            FactRow("Ternion Dagger +1 (Dagger)", "Mephitas · Mephitas's Claw x50 · Hide · DMG +17 / Acc & MAcc +40 / Weapon Skill Damage +5%")
                            FactRow("Triska Scythe +1 (Scythe)", "Camahueto · Tuft of Camahueto's Fur x50 · Hide · DMG +56 / Acc & MAcc +40 / Critical Hit Rate +10%")
                            FactRow("Ushenzi +1 (Great Sword)", "Glazemane · Glazemane's Fang x50 · Hide · DMG +28 / Acc & MAcc +40 / Cure Potency Received +10%")
                        }
                        CollapsibleSection("Mage weapons", stateKey = "unity:rw:mage", persist = false) {
                            FactRow("Ababinili +1 (Staff)", "Arke · Arke's Wing x50 · Hide · Healing Magic Skill +10 / Enhancing Magic Skill +10 / Damage Taken -10%")
                            FactRow("Contemplator +1 (Staff)", "Tumult Curator · Tumult's Blood x50 · Wing · Magic Accuracy +70 / Enfeebling Magic Skill +20 / MND +10")
                            FactRow("Magesmasher +1 (Club)", "Strix · Strix's Tailfeather x50 · Hide · DMG +45 / Acc & MAcc +30 / Weapon Skill Damage +15%")
                            FactRow("Marin Staff +1 (Staff)", "Vedrfolnir · Vedrfolnir's Wing x50 · Hide · Magic Attack Bonus +40 / Acc & MAcc +40 / INT·MND +10")
                            FactRow("Pouwhenua +1 (Staff)", "Woodland Mender · Woodland Mender's Log x50 · Scale · DMG +45 / Acc & MAcc +30 / Store TP +10")
                            FactRow("Septoptic +1 (Club)", "Shedu · Shedu's Mane x50 · Wing · DMG +10 / Acc & MAcc +40 / Mag. Atk. Bns. +30")
                        }
                        CollapsibleSection("Ranged weapons", stateKey = "unity:rw:ranged", persist = false) {
                            FactRow("Antitail +1 (Throwing)", "Sovereign Behemoth · Sovereign's Hide x50 · Wing · Magic Evasion +15 / Double Attack +3")
                            FactRow("Imati +1 (Marksmanship)", "Wyvernhunter Bambrox · Bambrox's Shawl x50 · Hide · DMG +17 / Ranged Accuracy +40 / Snapshot +10%")
                            FactRow("Malison +1 (Marksmanship)", "Tolba · Tolba's Shell x50 · Wing · Ranged Attack +45 / Ranged Acc & MAcc +40 / DMG +5")
                            FactRow("Mengado +1 (Archery)", "Cactrot Veloz · Veloz's Needle x50 · Scale · Snapshot +15 / DMG +10 / Ranged Accuracy +20")
                            FactRow("Paloma Bow +1 (Archery)", "Borealis Shadow · Ethereal Incense x50 · Hide · DMG +9 / Ranged Accuracy +40 / Rapid Shot +15%")
                            FactRow("Wingcutter +1 (Throwing)", "Abyssdiver · Abyssdiver's Feather x50 · Scale · Accuracy +10 / Evasion +10")
                        }
                        CollapsibleSection("Shields & grips", stateKey = "unity:rw:shield", persist = false) {
                            FactRow("Ajax +1", "Coca · Coca's Wing x50 · Hide · Shield Block Rate +10% / Enhancing Magic Received Duration +10%")
                            FactRow("Deliverance +1", "Borealis Shadow · Ethereal Incense x50 · Hide · Acc & MAcc +30 / Shield Skill +10")
                            FactRow("Evalach +1", "Jester Malatrix · Jester Malatrix's Shard x50 · Scale · HP +150 / Shield Skill +10 / Acc & MAcc +20")
                            FactRow("Forfend +1", "Tolba · Tolba's Shell x50 · Wing · Accuracy +15 / Magic Accuracy +15 / Enhancing magic skill +10")
                            FactRow("Refined Grip +1", "Voso · Voso's Hide x50 · Scale · DEF +20 / Parrying Skill +10")
                            FactRow("Rigorous Grip +1", "Douma Weapon · Douma Weapon's Shard x50 · Hide · Attack +30 / STR +15")
                        }
                        CollapsibleSection("Armor (ilvl 119)", stateKey = "unity:rw:armor", persist = false) {
                            EnterHeading("Head")
                            FactRow("Adorned Helm +1", "Beist · Beist's Blood x50 · Hide · Acc & MAcc +45 / Attack +50 / All Base Stats +10")
                            FactRow("Alhazen Hat +1", "Azrael · Azrael's Eye x50 · Hide · All Base Stats +30 / Evasion +50 / Acc, Ranged Acc & MAcc +25")
                            FactRow("Blistering Sallet +1", "Vermilion Fishfly · Vermillion's Wing x50 · Hide · Acc & MAcc +45 / Critical Hit Rate +10% / STR·DEX +25")
                            FactRow("Hike Khat +1", "Ayapec · Ayapec's Shell x50 · Hide · Physical Damage Taken -10% / Pet: Damage Taken -5% / All Base Stats +10")
                            FactRow("Imp. Wing Hair. +1", "Valkurm Imperator · Valkurm Imperator's Wing x50 · Scale · Accuracy +35 / Magic Evasion +100 / Critical Hit Rate +10%")
                            FactRow("Loess Barbuta +1", "Hidhaegg · Hidhaegg's Scale x50 · Wing · Enmity +10 / Damage taken -10% / All Attr. +10")
                            FactRow("Stinger Helm +1", "King Uropygid · Uropygid's Needle x50 · Hide · Acc & MAcc +30 / Physical Damage Limit +5% / All Base Stats +10")
                            EnterHeading("Body")
                            FactRow("Agony Jerkin +1", "Voso · Voso's Hide x50 · Scale · Attack +60 / Store TP +10 / All Base Stats +10")
                            FactRow("Cohort Cloak +1", "Centurio XX-I · Centurio's Armor x50 · Hide · Magic Accuracy +100 / Magic Attack Bonus +100 / All Base Stats +20")
                            FactRow("Emet Harness +1", "Largantua · Largantua's Shard x50 · Hide · Evasion +30 / Accuracy +40 / All Base Stats +10")
                            FactRow("Hime Domaru +1", "Beist · Beist's Blood x50 · Hide · Accuracy +45 / Double Attack +5% / All Base Stats +10")
                            FactRow("Lugra Cloak +1", "Tiyanak · Tiyanak's Fang x50 · Scale · Magic Accuracy +60 / Spell Interruption Rate -20% / All Base Stats +20")
                            FactRow("Obviation Cuirass +1", "Tolba · Tolba's Shell x50 · Wing · Magic Evasion +60 / Enmity +5 / All Attr. +10")
                            FactRow("Ros. Jaseran +1", "Woodland Mender · Mender's Log x50 · Scale · Magic Accuracy +45 / Damage Taken -5% / All Base Stats +10")
                            FactRow("Shomonjijoe +1", "Douma Weapon · Douma's Shard x50 · Hide · Avatar: TP Bonus +300 / Avatar: Acc & MAcc +30 / Avatar: All Base Stats +10")
                            FactRow("Tatena. Harama. +1", "Tumult Curator · Tumult's Blood x50 · Wing · Accuracy +30 / All Attr. +10 / Triple Attack +5%")
                            EnterHeading("Hands")
                            FactRow("Asteria Mitts +1", "Azure-toothed Clawberry · Clawberry's Coat x50 · Hide · MP +45 / Avatar: Acc & MAcc +40 / Avatar: Magic Burst Bonus +10%")
                            FactRow("Gazu Bracelets +1", "Carousing Celine · Celine's Vine x50 · Hide · Accuracy +50 / Haste +10% / All Base Stats +10")
                            FactRow("Kachi. Kote +1", "Muut · Muut's Vestment x50 · Hide · Attack +45 / Acc & MAcc +30 / All Base Stats +10")
                            FactRow("Lamassu Mitts +1", "Azure-toothed Clawberry · Clawberry's Coat x50 · Hide · Avatar: All Base Stats +30 / Avatar: Acc & MAcc +40 / Avatar Perpetuation Cost -5")
                            FactRow("Macabre Gaunt. +1", "Abyssdiver · Abyssdiver's Feather x50 · Scale · Magic Evasion +75 / Occasionally Resist Status Ailments +10 / All Base Stats +10")
                            FactRow("Shigure Tekko +1", "Warblade Beak · Warblade Beak's Hide x50 · Scale · Evasion +90 / Magic Evasion +80 / All Base Stats +10")
                            FactRow("Tatena. Gote +1", "Shedu · Shedu's Mane x50 · Wing · Accuracy +40 / All Attr. +10 / Triple Attack +4%")
                            EnterHeading("Legs")
                            FactRow("Assiduity Pants +1", "Intuila · Intuila's Hide x50 · Scale · Avatar: Acc & MAcc +35 / Avatar: All Base Stats +20 / MP +20")
                            FactRow("Augury Cuisses +1", "Emperor Arthro · Emperor Arthro's Shell x50 · Scale · Attack +60 / Magic Attack Bonus +30 / All Base Stats +10")
                            FactRow("Tatena. Haidate +1", "Sarama · Sarama's Hide x50 · Wing · Accuracy +60 / All Attr. +10 / Triple Attack +3%")
                            FactRow("Zoar Subligar +1", "Keeper of Heiligtum · Heiligtum's Moss x50 · Scale · Accuracy +30 / Critical Hit Rate +5% / All Base Stats +10")
                            EnterHeading("Feet")
                            FactRow("Hippomenes Socks +1", "Immanibugard · Immanibugard's Hide x50 · Scale · Resist Bind +45 / Evasion +20 / All Base Stats +10")
                            FactRow("Hygieia Clogs +1", "Camahueto · Tuft of Camahueto's Fur x50 · Hide · Cure Potency +15% / Healing Magic Skill +10 / All Base Stats +10")
                            FactRow("Jute Boots +1", "Strix · Strix's Tailfeather x50 · Hide · DEX·AGI +15 / Magic Evasion +30 / All Base Stats +10")
                            FactRow("Regal Pumps +1", "Valkurm Imperator · Valkurm Imperator's Wing x50 · Scale · Healing Magic Skill +10 / Enhancing Magic Skill +10 / All Base Stats +10")
                            FactRow("Tatena. Sune. +1", "Thu'ban · Thu'ban's Scale x50 · Wing · Accuracy +60 / All Attr. +10 / Triple Attack +3%")
                        }
                        CollapsibleSection("Accessories", stateKey = "unity:rw:acc", persist = false) {
                            FactRow("Acuity Belt +1", "Joyous Green · Clump of Joyous Green's Moss x50 · Scale · Magic Accuracy +15 / INT +10")
                            FactRow("Apeile Ring +1", "Immanibugard · Immanibugard's Hide x50 · Scale · DEF +20 / Magic Defense Bonus +5")
                            FactRow("Arete del Luna +1", "Cactrot Veloz · Veloz's Needle x50 · Scale · Resist Sleep +15 / Resist Charm +15")
                            FactRow("Aurist's Cape +1", "Volatile Cluster · V. Cluster's Ash x50 · Hide · Acc & MAcc +25 / INT·MND +25")
                            FactRow("Bathy Choker +1", "Bakunawa · Bakunawa's Ink x50 · Hide · Evasion +15 / Counter +10")
                            FactRow("Cacoethic Ring +1", "Vermilion Fishfly · Vermillion's Wing x50 · Hide · DEX +10 / AGI +10")
                            FactRow("Canto Necklace +1", "Joyous Green · Clump of Joyous Green's Moss x50 · Scale · Magic Accuracy +15 / CHR +10")
                            FactRow("Domin. Earring +1", "Sovereign Behemoth · Sovereign's Hide x50 · Wing · Accuracy +10 / DEX +6")
                            FactRow("Fi Follet Cape +1", "Vidmapire · Vidmapire's Claw x50 · Hide · Fast Cast +10% / Spell Interruption Rate -5%")
                            FactRow("Gelatinous Ring +1", "Garbage Gel · Jar of Garbage Gel's Mucus x50 · Scale · VIT +15 / HP +100")
                            FactRow("Ghastly Tathlum +1", "Specter Worm · Specter's Ore x50 · Hide · Magic Damage +10 / INT +5")
                            FactRow("Ground. Mantle +1", "Lumber Jill · Vial of Lumber Jill's Spittle x50 · Hide · Accuracy +15 / DEX +10")
                            FactRow("Handler's Earring +1", "Warblade Beak · Warblade Beak's Hide x50 · Scale · Pet: Acc & MAcc +15 / Accuracy +10")
                            FactRow("Kentarch Belt +1", "Centurio XX-I · Centurio's Armor x50 · Hide · STR +10 / DEX +10")
                            FactRow("Loricate Torque +1", "Sovereign Behemoth · Sovereign's Hide x50 · Wing · DEF +45 / Spell interruption rate down 5%")
                            FactRow("Lugra Earring +1", "Tiyanak · Tiyanak's Fang x50 · Scale · DEF +20 / STR·DEX·VIT·INT +8")
                            FactRow("Mephitas's Ring +1", "Mephitas · Mephitas's Claw x50 · Hide · Conserve MP +15 / INT +5")
                            FactRow("Metamorph Ring +1", "Sybaritic Samantha · Sybaritic Samantha's Vine x50 · Scale · Magic Accuracy +10 / INT·MND·CHR +10")
                            FactRow("Nourish. Earring +1", "Intuila · Intuila's Hide x50 · Scale · Resist Silence +15 / Spell Interruption Rate -5%")
                            FactRow("Odnowa Earring +1", "Carousing Celine · Celine's Vine x50 · Hide · DEF +30 / Damage Taken -3%")
                            FactRow("Sailfi Belt +1", "Emperor Arthro · Emperor Arthro's Shell x50 · Scale · STR +15 / Double Attack +5%")
                            FactRow("Seeth. Bomblet +1", "Grand Grenade · G. Grenade's Ash x50 · Hide · STR +10 / Haste +5%")
                            FactRow("Shinjutsu-no-Obi +1", "Orcfeltrap · Orcfeltrap's Leaf x50 · Scale · Conserve MP +15 / Fast Cast +5%")
                            FactRow("Unmoving Collar +1", "Sybaritic Samantha · Samantha's Vine x50 · Scale · DEF +30 / HP +200")
                            FactRow("Vim Torque +1", "Thu'ban · Thu'ban's Scale x50 · Wing · Accuracy +15 / Store TP +10")
                            FactRow("Warder's Charm +1", "Largantua · Largantua's Shard x50 · Hide · Skillchain Damage +15% / Magic Burst Bonus +10%")
                            FactRow("Zwazo Earring +1", "Kubool Ja's Mhuufya · Mhuufya's Beak x50 · Hide · HP +45 / Shield Block Rate +3%")
                        }
                        CollapsibleSection("Level 99 and lower gear", stateKey = "unity:rw:old", persist = false) {
                            Text("The low-level Wanted NMs feed the older sets. These upgrade for Accolades plus a few materials instead of the x50 Lustreless path, and take no Odyssey augments.",
                                color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(bottom = 4.dp))
                            EnterHeading("Level 99 — 30x material, 5,000 Accolades")
                            FactRow("Damani Horn +1", "Sleepy Mabel · Strand of Sleepy Mabel's Fur")
                            FactRow("Thorfinn Shield +1", "Ironhorn Baldurno · Ironhorn Baldurno's Horn")
                            FactRow("Cloud Hairpin +1", "Serpopard Ninlil · Serpopard Ninlil's Bone")
                            EnterHeading("Level 98 and lower — 3x material, 1,000 Accolades each")
                            FactRow("Bounding Belinda · Bounding Belinda's Hide", "Adsilio Boots +1, and the Aurore set: Beret, Doublet, Gloves, Brais, Gaiters")
                            FactRow("Hugemaw Harold · Chunk of Harold Hugemaw's Red Ore", "The Perle set: Salade, Hauberk, Moufles, Brayettes, Sollerets")
                            FactRow("Prickly Pitriv · Prickly Pitriv's Thread", "Dew Silk Cape +1, and the Teal set: Chapeau, Saio, Cuffs, Slops, Pigaches")
                        }
                    }
                    CollapsibleSection("Campaigns", stateKey = "unity:campaigns", persist = false) {
                        FactRow("Double Unity Accolade", "Accolades from Records of Eminence objectives and from vanquishing monsters are doubled.")
                        FactRow("Unity Wanted", "Wanted battles pay twice the rewards — Wanted I, II and III objectives yield 2 treasure chests instead of 1.")
                        Text("Two Monthly Adventurer Campaigns can run in any given month.",
                            color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp, modifier = Modifier.padding(top = 4.dp))
                    }
                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

// Apex / Locus content category — every Apex and Locus mob (matched by name prefix), grouped by the zones
// they appear in. Pure name-prefix query so it always reflects the current roster; no content tags needed.
@Composable
private fun ApexLocusScreen(vm: MobileWatchViewModel) {
    // (zone, "Lv 125-127" or "", mobs paired with that zone's own level range) ordered by level,
    // plus whatever still has no zone recorded.
    val data = remember {
        val mobs = vm.mobsByNamePrefix("Apex ", "Locus ")
        val byZone = linkedMapOf<String, MutableList<Pair<Mob, String?>>>()
        val levels = mutableMapOf<String, MutableList<Int>>()
        val noZone = mutableListOf<Mob>()
        mobs.forEach { m ->
            val zs = m.zones.filter { it.first.isNotBlank() }
            if (zs.isEmpty()) { noZone.add(m); return@forEach }
            zs.forEach { (z, range) ->
                byZone.getOrPut(z) { mutableListOf() }.add(m to range)
                range?.split("-")?.mapNotNull { it.trim().toIntOrNull() }
                    ?.let { levels.getOrPut(z) { mutableListOf() }.addAll(it) }
            }
        }
        val ordered = byZone.entries.sortedWith(
            compareBy({ levels[it.key]?.minOrNull() ?: Int.MAX_VALUE }, { it.key })
        ).map { e ->
            val lo = levels[e.key]?.minOrNull()
            val hi = levels[e.key]?.maxOrNull()
            val band = if (lo == null || hi == null) "" else "Lv $lo-$hi"
            Triple(e.key, band, e.value.sortedBy { it.first.name })
        }
        ordered to noZone.sortedBy { it.name }
    }
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Apex / Locus", onBack = { vm.clearContent() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize().padding(horizontal = 16.dp)) {
            item {
                Text("Every Apex and Locus monster, grouped by the zones it appears in and ordered by level. " +
                    "Tap any for its full entry — spawn counts and the accuracy needed for a 95% hit rate are in its notes.",
                    color = TextMuted, fontSize = 12.sp, lineHeight = 17.sp, modifier = Modifier.padding(vertical = 8.dp))
                data.first.forEach { (zone, band, list) ->
                    CollapsibleSection(zone, stateKey = "apexlocus:$zone", persist = false,
                        subtitle = band.ifBlank { null }) {
                        list.forEach { (mob, range) ->
                            OdyMobRow(vm, mob, zone, levelText = range?.let { "Lv $it" })
                        }
                    }
                }
                if (data.second.isNotEmpty()) {
                    CollapsibleSection("Zone not recorded", stateKey = "apexlocus:none", persist = false) {
                        data.second.forEach { OdyMobRow(vm, it, "") }
                    }
                }
                Spacer(Modifier.height(24.dp))
            }
        }
    }
}
private class AreaInfo(
    val facts: List<Pair<String, String>> = emptyList(),
    val warning: String? = null,
    val farming: List<FarmStep> = emptyList(),
    val weakening: List<WeakenNM> = emptyList(),                    // boss-weakening NMs (Dreamland farming pt. 2)
    val procWindows: List<ProcWindow> = emptyList(),               // Dreamland stagger windows
    val relicArmor: List<Pair<String, String>> = emptyList(),   // piece, job/slot
    val relicAccessories: List<Pair<String, String>> = emptyList(), // piece, job (Dreamland Nightmare drops)
    val relicWeapons: List<String> = emptyList(),
    val attestations: List<Pair<String, String>> = emptyList(), // name, weapon type
    val attestationsLabel: String = "Attestations",
    val currencies: List<String> = emptyList(),
    val miscItems: List<String> = emptyList(),
)

private class FarmStep(
    val trigger: String,      // what you farm / trade
    val from: String,         // where it comes from
    val target: String,       // the NM it spawns
    val at: String,           // location
    val yields: String,       // what the NM gives
)

// A boss-weakening NM (Dreamland). Kill it before the fight; its drop strips one
// of the boss's abilities. Rendered as the second part of the Farming section.
private class WeakenNM(
    val nm: String,           // NM name + location, e.g. "Stihi (I-6)"
    val spawn: String,        // "Timed \u2014 20 min" / "Lottery"
    val item: String,         // the weakening item it drops
    val removes: String,      // the boss ability/abilities it removes
)

// A Dreamland stagger window. Each genus group must be staggered a specific way
// depending on the Earth-time window; the correct stagger drops that group's currency.
private class ProcWindow(
    val families: String,     // genus group, e.g. "Goobbue, Manticore, Treant"
    val w1: String,           // stagger method for 00:00-08:00 (Earth time)
    val w2: String,           // 08:00-16:00
    val w3: String,           // 16:00-00:00
    val currency: String,     // currency the correct stagger drops
    val jobs: String,         // accessory jobs the group drops for
)

private val SANDORIA_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Trail Markings — Southern San d'Oria (M-5)",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Rank 6, Level 65+",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Hydra Corps Command Scepter",
        "Title" to "Dynamis-San d'Oria Interloper",
        "Time Limit" to "60 minutes",
        "Boss" to "Overlord's Tombstone",
    ),
    warning = "Beware of Orc NMs — they use Fanatic Dance, an AoE Charm.",
    farming = listOf(
        FarmStep("Barbaric Bijou", "the opening Notorious Monsters", "Overlord's Tombstone",
            "I-7, North San d'Oria entrance", "Fiendish Tome: Chapter 1 + Montiont Silverpiece"),
        FarmStep("Odious Scale", "Vanguard Predator / Vexer / Footsoldier / Pillager", "Bladeburner Rokgevok",
            "L-10, East Ronfaure exit", "Fiendish Tome: Chapter 2 + Oneiros Sash"),
        FarmStep("Odious Leather", "Vanguard Bugler / Gutslasher / Trooper / Grappler", "Steelshank Kratzvatz",
            "I-11, Chocobo Stables", "Fiendish Tome: Chapter 3 + Oneiros Cappa"),
        FarmStep("Odious Cryptex", "Vanguard Backstabber / Neckchopper / Dollmaster", "Bloodfist Voshgrosh",
            "G-10, East Ronfaure entrance", "Fiendish Tome: Chapter 4 + Oneiros Belt"),
        FarmStep("Odious Strongbox", "Vanguard Hawker / Impaler / Mesmerizer", "Spellspear Djokvukk",
            "B-6, Caffaule's Manor", "Fiendish Tome: Chapter 5 + Oneiros Cape"),
        FarmStep("Fiendish Tomes: Chapters 1-5", "the five Zone-Boss NMs above", "Arch Overlord Tombstone",
            "I-7, North San d'Oria entrance", "Oneiros Lance / Cest / Helm + Montiont Silverpiece"),
    ),
    relicArmor = listOf(
        "Argute Bracers" to "SCH Hands", "Bard's Roundlet" to "BRD Head",
        "Cleric's Cap" to "WHM Head", "Commodore Trews" to "COR Legs",
        "Duelist's Boots" to "RDM Feet", "Koga Hakama" to "NIN Legs",
        "Melee Hose" to "MNK Legs", "Mirage Bazubands" to "BLU Hands",
        "Monster Trousers" to "BST Legs", "Pantin Babouches" to "PUP Feet",
        "Scout's Braccae" to "RNG Legs", "Summoner's Pigaches" to "SMN Feet",
        "Valor Gauntlets" to "PLD Hands", "Warrior's Calligae" to "WAR Feet",
        "Wyrm Greaves" to "DRG Feet",
    ),
    relicWeapons = listOf("Ihintanto (NIN)", "Relic Bhuj (WAR)", "Relic Gun (RNG)", "Relic Lance (DRG)"),
    currencies = listOf("Ordelle Bronzepiece", "Montiont Silverpiece"),
    miscItems = listOf("Sparkling Stone", "Fresh Orc Liver", "Griffon Hide", "Giant Frozen Head",
        "Gold Beastcoin", "Infinity Core", "Mtl. Beastcoin"),
)

private val WINDURST_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Trail Markings — Windurst Walls (C-12)",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Rank 6, Level 65+",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Hydra Corps Lantern",
        "Title" to "Dynamis-Windurst Interloper",
        "Time Limit" to "60 minutes",
        "Boss" to "Tzee Xicu Idol",
    ),
    warning = "Beware of Vanguard's Crows — they cast Silencega if left unsilenced or awake. Echo Drops are a necessity for everyone.",
    farming = listOf(
        FarmStep("Divine Bijou", "the opening Notorious Monsters", "Tzee Xicu Idol",
            "K-13, Windurst Woods entrance", "Fiendish Tome: Chapter 11 + Lungo-Nango Jadeshell"),
        FarmStep("Odious Necklace", "Vanguard Salvager / Oracle / Visionary / Inciter", "Xuu Bhoqa the Enigma",
            "E-7, Koru-Moru's Manor", "Fiendish Tome: Chapter 12 + Oneiros Ring"),
        FarmStep("Odious Feather", "Vanguard Exemplar / Liberator / Partisan / Prelate", "Fuu Tzapo the Blessed",
            "E-5, Yoran-Oran's Manor", "Fiendish Tome: Chapter 13 + Oneiros Earring"),
        FarmStep("Odious Holy Water", "Vanguard Assassin / Chanter / Priest", "Naa Yixo the Stillrage",
            "G-3, House of the Hero", "Fiendish Tome: Chapter 14 + Mujin Band"),
        FarmStep("Odious Quipo", "Vanguard Skirmisher / Sentinel / Persecutor / Ogresoother", "Tee Zaksa the Ceaseless",
            "H-7, Heaven's Tower", "Fiendish Tome: Chapter 15 + Oneiros Torque"),
        FarmStep("Fiendish Tomes: Chapters 11-15", "the five Zone-Boss NMs above", "Arch Tzee Xicu Idol",
            "K-13, Windurst Woods entrance", "Mujin Tanto / Necklace / Oneiros Headgear + Lungo-Nango Jadeshell"),
    ),
    relicArmor = listOf(
        "Abyss Gauntlets" to "DRK Hands", "Argute Loafers" to "SCH Feet",
        "Assassin's Bonnet" to "THF Head", "Cleric's Duckbills" to "WHM Feet",
        "Etoile Bangles" to "DNC Hands", "Koga Hatsuburi" to "NIN Head",
        "Mirage Charuqs" to "BLU Feet", "Monster Helm" to "BST Head",
        "Pantin Dastanas" to "PUP Hands", "Saotome Haidate" to "SAM Legs",
        "Scout's Bracers" to "RNG Hands", "Sorcerer's Gloves" to "BLM Hands",
        "Summoner's Spats" to "SMN Legs", "Valor Leggings" to "PLD Feet",
        "Warrior's Mask" to "WAR Head",
    ),
    relicWeapons = listOf("Relic Dagger (BRD/RDM/THF)", "Relic Knuckles (MNK)", "Relic Maul (WHM)", "Relic Sword (PLD/RDM)"),
    currencies = listOf("Tukuku Whiteshell", "Lungo-Nango Jadeshell"),
    miscItems = listOf("Colossal Skull", "Lancewood Log", "Relic Iron", "Sparkling Stone",
        "Gold Beastcoin", "Infinity Core", "Mythril Beastcoin"),
)

private val BASTOK_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Trail Markings — Bastok Mines (K-8)",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Rank 6, Level 65+",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Hydra Corps Eyeglass",
        "Title" to "Dynamis-Bastok Interloper",
        "Time Limit" to "60 minutes",
        "Boss" to "Gu'Dha Effigy",
    ),
    warning = "Beware of Vanguard's Scorpions — pets of Vanguard Beasttender, they cast Breakga if left unsilenced.",
    farming = listOf(
        FarmStep("Steelwall Bijou", "the opening Notorious Monsters", "Gu'Dha Effigy",
            "H-10, near the Gustaberg exit", "Fiendish Tome: Chapter 6 + 100 Byne Bill"),
        FarmStep("Odious Charm", "Vanguard Defender / Vindicator / Kusa", "Zo'Pha Forgesoul",
            "E-8, near the depot ramp", "Fiendish Tome: Chapter 7 + Oneiros Rope"),
        FarmStep("Odious Backscale", "Vanguard Drakekeeper / Militant / Vigilante / Hatamoto", "Ra'Gho Darkfount",
            "D-7, Zeruhn Mines entrance", "Fiendish Tome: Chapter 8 + Mujin Obi"),
        FarmStep("Odious Engraving", "Vanguard Beasttender / Constable / Purloiner / Undertaker", "Va'Zhe Pummelsong",
            "F-5, Bastok Markets entrance", "Fiendish Tome: Chapter 9 + Oneiros Harp"),
        FarmStep("Odious Letterbox", "Vanguard Minstrel / Protector / Thaumaturge", "Bu'Bho Truesteel",
            "J-7, near the Alchemy guild", "Fiendish Tome: Chapter 10 + Oneiros Pebble"),
        FarmStep("Fiendish Tomes: Chapters 6-10", "the five Zone-Boss NMs above", "Arch Gu'Dha Effigy",
            "H-10, near the Gustaberg exit", "Oneiros Axe / Annulet / Barbut + 100 Byne Bill"),
    ),
    relicArmor = listOf(
        "Abyss Sollerets" to "DRK Feet", "Argute Pants" to "SCH Legs",
        "Assassin's Vest" to "THF Body", "Bard's Cuffs" to "BRD Hands",
        "Commodore Bottes" to "COR Feet", "Duelist's Gloves" to "RDM Hands",
        "Etoile Tiara" to "DNC Head", "Melee Gaiters" to "MNK Feet",
        "Mirage Shalwar" to "BLU Legs", "Monster Jackcoat" to "BST Body",
        "Saotome Kote" to "SAM Hands", "Sorcerer's Tonban" to "BLM Legs",
        "Summoner's Bracers" to "SMN Hands", "Valor Coronet" to "PLD Head",
        "Wyrm Brais" to "DRG Legs",
    ),
    relicWeapons = listOf("Ito (SAM)", "Relic Axe (BST)", "Relic Blade (DRK/PLD/WAR)", "Relic Scythe (DRK)"),
    currencies = listOf("One Byne Bill", "One Hundred Byne Bill"),
    miscItems = listOf("Slime Juice", "Sparkling Stone", "Wootz Ore", "Gold Beastcoin",
        "Mythril Beastcoin", "Infinity Core"),
)

private val JEUNO_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Trail Markings — Ru'Lude Gardens (I-9)",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Level 65+, Mission 5-2 for your nation",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Hydra Corps Tactical Map",
        "Title" to "Dynamis-Jeuno Interloper",
        "Time Limit" to "60 minutes",
        "Boss" to "Goblin Golem",
    ),
    warning = "Beware of Vanguard's Slimes — pets of Vanguard Pathfinder, they cast Paralyga if left unsilenced.",
    farming = listOf(
        FarmStep("Roving Bijou", "the opening Notorious Monsters", "Goblin Golem",
            "H-11, Upper Jeuno entrance", "Fiendish Tome: Chapter 16 + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
        FarmStep("Odious Cup", "Vanguard Necromancer / Tinkerer / Ambusher / Enchanter", "Quicktrix Hexhands",
            "H-6, Palace Stairs", "Fiendish Tome: Chapter 17 + Mujin Mantle"),
        FarmStep("Odious Die", "Vanguard Armorer / Dragontamer / Welldigger / Shaman", "Feralox Honeylips",
            "G-6, Palace west room", "Fiendish Tome: Chapter 18 + Oneiros Tathlum"),
        FarmStep("Odious Mask", "Vanguard Alchemist / Hitman / Maestro", "Scourquix Scaleskin",
            "I-6, Palace east room", "Fiendish Tome: Chapter 19 + Oneiros Pearl"),
        FarmStep("Odious Grenade", "Vanguard Ronin / Smithy / Pathfinder / Pitfighter", "Wilywox Tenderpalm",
            "H-5, \"Maat's house\"", "Fiendish Tome: Chapter 20 + Mujin Stud"),
        FarmStep("Fiendish Tomes: Chapters 16-20", "the five Zone-Boss NMs above", "Arch Goblin Golem",
            "H-11, Upper Jeuno entrance", "Oneiros Knife / Grip / Coif + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
    ),
    relicArmor = listOf(
        "Abyss Flanchard" to "DRK Legs", "Assassin's Poulaines" to "THF Feet",
        "Bard's Slippers" to "BRD Feet", "Cleric's Pantaloons" to "WHM Legs",
        "Commodore Gants" to "COR Hands", "Duelist's Tights" to "RDM Legs",
        "Etoile Shoes" to "DNC Feet", "Koga Kyahan" to "NIN Feet",
        "Melee Gloves" to "MNK Hands", "Pantin Churidars" to "PUP Legs",
        "Saotome Sune-Ate" to "SAM Feet", "Scout's Beret" to "RNG Head",
        "Sorcerer's Sabots" to "BLM Feet", "Warrior's Mufflers" to "WAR Hands",
        "Wyrm Finger Gauntlets" to "DRG Hands",
    ),
    relicWeapons = listOf("Relic Bow (RNG/SAM)", "Relic Horn (BRD)", "Relic Shield (PLD)", "Relic Staff (BLM/SMN)"),
    currencies = listOf("One Byne Bill", "One Hundred Byne Bill", "Tukuku Whiteshell",
        "Lungo-Nango Jadeshell", "Ordelle Bronzepiece", "Montiont Silverpiece"),
    miscItems = listOf("Sparkling Stone", "Goblin Grease", "Gold Beastcoin",
        "Infinity Core", "Mythril Beastcoin"),
)

private val BEAUCEDINE_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Trail Markings — Beaucedine Glacier (F-11)",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Rank 6, Level 65, and all four Hydra Corps key items (Command Scepter, Lantern, Eyeglass, Tactical Map) from the city zones",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Hydra Corps Insignia",
        "Title" to "Dynamis-Beaucedine Interloper",
        "Time Limit" to "60 minutes",
        "Boss" to "Angra Mainyu",
    ),
    warning = "The first Northland zone — entry needs the key items earned from all four city Dynamis zones.",
    farming = listOf(
        FarmStep("Leering Bijou", "the opening Notorious Monsters", "Angra Mainyu",
            "J-5, Fei'Yin entrance", "Fiendish Tome: Chapter 21 + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
        FarmStep("Odious Talisman", "Hydra Black Mage / Paladin / Ranger / Summoner", "Taquede",
            "G-9, on top of the cliff", "Fiendish Tome: Chapter 22 + Ryuga Sune-Ate"),
        FarmStep("Odious Bell", "Hydra Beastmaster / Dark Knight / Red Mage / Samurai", "Pignonpausard",
            "H-7, dead-end cliff", "Fiendish Tome: Chapter 23 + Khthonios Mask"),
        FarmStep("Odious Root", "Hydra Bard / Monk / Ninja / Warrior", "Hitaume",
            "G-8", "Fiendish Tome: Chapter 24 + Khthonios Gloves"),
        FarmStep("Odious Mirror", "Hydra Dragoon / Thief / White Mage", "Cavanneche",
            "F-7, Nue's Tower", "Fiendish Tome: Chapter 25 + Khthonios Helm"),
        FarmStep("Fiendish Tomes: Chapters 21-25", "the five Zone-Boss NMs above", "Arch Angra Mainyu",
            "J-5, Fei'Yin entrance", "Avesta Bangles / Chtonic Staff / Oneiros Cluster + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
    ),
    relicArmor = listOf(
        "Abyss Cuirass" to "DRK Body", "Argute Gown" to "SCH Body",
        "Assassin's Culottes" to "THF Legs", "Bard's Justaucorps" to "BRD Body",
        "Cleric's Bliaut" to "WHM Body", "Commodore Frac" to "COR Body",
        "Duelist's Tabard" to "RDM Body", "Etoile Tights" to "DNC Legs",
        "Koga Chainmail" to "NIN Body", "Melee Cyclas" to "MNK Body",
        "Mirage Jubbah" to "BLU Body", "Monster Gaiters" to "BST Feet",
        "Pantin Tobe" to "PUP Body", "Saotome Domaru" to "SAM Body",
        "Scout's Socks" to "RNG Feet", "Sorcerer's Coat" to "BLM Body",
        "Summoner's Doublet" to "SMN Body", "Valor Breeches" to "PLD Legs",
        "Warrior's Cuisses" to "WAR Legs", "Wyrm Mail" to "DRG Body",
    ),
    attestations = listOf(
        "Attestation of Accuracy" to "Marksmanship", "Attestation of Bravery" to "Axe",
        "Attestation of Celerity" to "Dagger", "Attestation of Decisiveness" to "Great Katana",
        "Attestation of Force" to "Great Axe", "Attestation of Fortitude" to "Polearm",
        "Attestation of Glory" to "Sword", "Attestation of Harmony" to "Music",
        "Attestation of Invulnerability" to "Shield", "Attestation of Legerity" to "Katana",
        "Attestation of Might" to "Hand-to-Hand", "Attestation of Righteousness" to "Great Sword",
        "Attestation of Sacrifice" to "Club", "Attestation of Transcendence" to "Bow",
        "Attestation of Vigor" to "Scythe", "Attestation of Virtue" to "Staff",
    ),
    currencies = listOf("One Byne Bill", "One Hundred Byne Bill", "Tukuku Whiteshell",
        "Lungo-Nango Jadeshell", "Ordelle Bronzepiece", "Montiont Silverpiece"),
    miscItems = listOf("Copy of \"Ginuva's Battle Theory\"", "Copy of \"Schultz Stratagems\"",
        "Infinity Core", "Gold Beastcoin", "Mythril Beastcoin", "Sparkling Stone",
        "Colossal Skull", "Goblin Grease", "Fresh Orc Liver", "Griffon Hide", "Wootz Ore"),
)

private val XARCABARD_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Trail Markings — Xarcabard (J-9)",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Rank 6, Level 65, and the Hydra Corps Insignia key item from Dynamis-Beaucedine",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Hydra Corps Battle Standard; unlocks the Atma of the Rescuer",
        "Title" to "Dynamis-Xarcabard Interloper / Lifter of Shadows",
        "Time Limit" to "60 minutes",
        "Boss" to "Dynamis Lord",
    ),
    warning = "The final Northland zone — entry needs the Hydra Corps Insignia earned in Dynamis-Beaucedine.",
    farming = listOf(
        FarmStep("Trade Shrouded Bijou", "near the Castle Zvahl entrance", "Dynamis Lord",
            "E-8", "Fiendish Tome: Chapter 26 + Shadow Ring, Shadow Mantle"),
        FarmStep("Trade Odious Skull", "at the ??? point", "Duke Haures",
            "J-7", "Fiendish Tome: Chapter 27 + Demonry Sash"),
        FarmStep("Trade Odious Horn", "at the ??? point", "Marquis Caim",
            "J-6", "Fiendish Tome: Chapter 28 + Demonry Core"),
        FarmStep("Trade Vial of Odious Blood", "at the ??? point", "Baron Avnas",
            "I-5", "Fiendish Tome: Chapter 29 + Demonry Ring"),
        FarmStep("Trade Odious Pen", "at the ??? point", "Count Haagenti",
            "F-7", "Fiendish Tome: Chapter 30 + Demonry Stone"),
        FarmStep("Trade Fiendish Tome Chapters 26-30", "near the Castle Zvahl entrance", "Arch Dynamis Lord",
            "E-8", "Sagasinger, Archon Cape, Archon Ring, Talekeeper"),
    ),
    relicArmor = listOf(
        "Abyss Burgeonet" to "DRK Head", "Argute Mortarboard" to "SCH Head",
        "Assassin's Armlets" to "THF Hands", "Bard's Cannions" to "BRD Legs",
        "Cleric's Mitts" to "WHM Hands", "Commodore Tricorne" to "COR Head",
        "Duelist's Chapeau" to "RDM Head", "Etoile Casaque" to "DNC Body",
        "Koga Tekko" to "NIN Hands", "Melee Crown" to "MNK Head",
        "Mirage Keffiyeh" to "BLU Head", "Monster Gloves" to "BST Hands",
        "Pantin Taj" to "PUP Head", "Saotome Kabuto" to "SAM Head",
        "Scout's Jerkin" to "RNG Body", "Sorcerer's Petasos" to "BLM Head",
        "Summoner's Horn" to "SMN Head", "Valor Surcoat" to "PLD Body",
        "Warrior's Lorica" to "WAR Body", "Wyrm Armet" to "DRG Head",
    ),
    attestations = listOf(
        "Celestial Fragment" to "Staff", "Demonic Fragment" to "Katana",
        "Divine Fragment" to "Great Katana", "Ethereal Fragment" to "Marksmanship",
        "Heavenly Fragment" to "Club", "Holy Fragment" to "Sword",
        "Intricate Fragment" to "Great Sword", "Mysterial Fragment" to "Instrument",
        "Mystic Fragment" to "Hand-to-Hand", "Ornate Fragment" to "Dagger",
        "Runaeic Fragment" to "Axe", "Seraphic Fragment" to "Great Axe",
        "Snarled Fragment" to "Archery", "Stellar Fragment" to "Polearm",
        "Supernal Fragment" to "Shield", "Tenebrous Fragment" to "Scythe",
    ),
    attestationsLabel = "Fragments",
    currencies = listOf("One Byne Bill", "One Hundred Byne Bill", "Tukuku Whiteshell",
        "Lungo-Nango Jadeshell", "Ordelle Bronzepiece", "Montiont Silverpiece"),
    miscItems = listOf("Shadow Mantle (Dynamis Lord only)", "Shadow Ring (Dynamis Lord only)",
        "Shard of Necropsyche (Vanguard Dragon only)", "Copy of \"Ginuva's Battle Theory\"",
        "Copy of \"Schultz Stratagems\"", "Infinity Core", "Gold Beastcoin",
        "Mythril Beastcoin", "Sparkling Stone"),
)

// First Dreamworld area. Differs from the cities: entry is CoP-gated, it has the
// Somnial Threshold support-job mechanic, a Nightmare-Foe -> Lost-NM -> Arch Christelle
// farming ladder, the three time-of-day Proc Windows, and Nightmare-drop accessories.
private val VALKURM_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Hieroglyphics \u2014 Valkurm Dunes (G-7)/(H-7), behind the Outpost",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Rank 6, Level 65, Chains of Promathia 3-5: Darkness Named cleared",
        "Support Jobs" to "On entry you choose whether to lock your support job; re-enable it any time by examining the Somnial Threshold. Running with your subjob disabled gives about a 1% chance to White-stagger a mob, which makes it drop a 100-currency.",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Dynamis-Valkurm Sliver",
        "Title" to "Dynamis-Valkurm Interloper",
        "Time Limit" to "60 minutes",
        "Boss" to "Cirrate Christelle",
    ),
    farming = listOf(
        FarmStep("Creeper's Juju", "the Nightmare Foes", "Cirrate Christelle",
            "G-9", "Fiendish Tome II (Chapter 1) + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
        FarmStep("Nightmare Bud", "Nightmare Funguar (D-7), Flytrap (E/F-9), Fly (C-7)", "Lost Nant'ina",
            "G-7", "Fiendish Tome II (Chapter 2) + Moepapa Medal"),
        FarmStep("Nightmare Log", "Nightmare Hippogryph (D/E-8), Sheep (E-8), Sabotender (F-7)", "Lost Fairy Ring",
            "C-7", "Fiendish Tome II (Chapter 3) + Moepapa Stone"),
        FarmStep("Nightmare Water", "Nightmare Manticore (F-8), Treant (E-7), Goobbue (G-7)", "Lost Stcemqestcint",
            "E-7", "Fiendish Tome II (Chapter 4) + Moepapa Mace"),
        FarmStep("Trade Fiendish Tome II Chapters 1-4", "Cirrate Christelle and the three Lost NMs above", "Arch Christelle",
            "G-9", "Moepapa Annulet, Moepapa Pendant, Moepapa Ring + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
    ),
    weakening = listOf(
        WeakenNM("Fairy Ring (J-6)", "Timed \u2014 20 min", "Odorless Fungus", "Miasmic Breath, movement-speed boost"),
        WeakenNM("Stcemqestcint (J-7)", "Timed \u2014 20 min", "Redolent Root", "Vampiric Lash"),
        WeakenNM("Nant'ina (J-7)", "Timed \u2014 20 min", "Absorbent Moss", "Fragrant Breath, reduces Charm"),
    ),
    procWindows = listOf(
        ProcWindow("Goobbue, Manticore, Treant", "WS", "MA", "JA", "T. Whiteshell", "WHM, SAM, THF, BLM, BST"),
        ProcWindow("Fly, Flytrap, Funguar", "JA", "WS", "MA", "1 Byne Bill", "BLU, COR, DNC, PLD"),
        ProcWindow("Hippogryph, Sabotender, Sheep", "MA", "JA", "WS", "O. Bronzepiece", "NIN, WAR, BRD, SMN"),
    ),
    relicArmor = listOf(
        "Abyss Sollerets" to "DRK Feet", "Argute Bracers" to "SCH Hands",
        "Assassin's Bonnet" to "THF Head", "Bard's Slippers" to "BRD Feet",
        "Cleric's Duckbills" to "WHM Feet", "Commodore Trews" to "COR Legs",
        "Duelist's Boots" to "RDM Feet", "Etoile Bangles" to "DNC Hands",
        "Koga Hakama" to "NIN Legs", "Melee Gaiters" to "MNK Feet",
        "Mirage Charuqs" to "BLU Feet", "Monster Helm" to "BST Head",
        "Pantin Churidars" to "PUP Legs", "Saotome Sune-Ate" to "SAM Feet",
        "Scout's Bracers" to "RNG Hands", "Sorcerer's Sabots" to "BLM Feet",
        "Summoner's Spats" to "SMN Legs", "Valor Leggings" to "PLD Feet",
        "Warrior's Calligae" to "WAR Feet", "Wyrm Brais" to "DRG Legs",
    ),
    relicAccessories = listOf(
        "Assassin's Cape" to "THF", "Bard's Cape" to "BRD",
        "Cleric's Belt" to "WHM", "Commodore Belt" to "COR",
        "Etoile Cape" to "DNC", "Koga Sarashi" to "NIN",
        "Mirage Mantle" to "BLU", "Monster Belt" to "BST",
        "Saotome Koshi-Ate" to "SAM", "Sorcerer's Belt" to "BLM",
        "Summoner's Cape" to "SMN", "Valor Cape" to "PLD",
        "Warrior's Stone" to "WAR",
    ),
    relicWeapons = emptyList(), // Valkurm drops no relic weapons
    currencies = listOf("One Byne Bill", "One Hundred Byne Bill", "Ordelle Bronzepiece",
        "Montiont Silverpiece", "Tukuku Whiteshell", "Lungo-Nango Jadeshell"),
    miscItems = listOf(
        "Relic Armor -1 \u2014 the 20 head-slot -1 pieces (all jobs), from Nightmare Monsters",
        "Forgotten Touch (Relic +2, hands \u2014 AF2 upgrade)",
        "Copy of \"Ginuva's Battle Theory\"", "Gold Beastcoin",
    ),
)

// Second Dreamworld area. Same shape as Valkurm: CoP-gated entry, the Somnial Threshold
// support-job mechanic, a Nightmare-Foe -> Lost-NM -> Arch farming ladder with a five-NM
// weakening list (four timed + a Beastmen lottery), the time-of-day Proc Windows, and
// Nightmare-drop accessories. Boss = Apocalyptic Beast; the -1 set is the HANDS slot here.
private val BUBURIMU_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Hieroglyphics \u2014 Buburimu Peninsula (I-9); fastest entry is to exit from Mhaura",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Rank 6, Level 65, Chains of Promathia 3-5: Darkness Named cleared",
        "Support Jobs" to "On entry you choose whether to lock your support job; re-enable it any time by examining the Somnial Threshold. Running with your subjob disabled gives about a 1% chance to White-stagger a mob, which makes it drop a 100-currency.",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Dynamis-Buburimu Sliver",
        "Title" to "Dynamis-Buburimu Interloper",
        "Time Limit" to "60 minutes",
        "Boss" to "Apocalyptic Beast",
    ),
    farming = listOf(
        FarmStep("Revelatory Juju", "the Weaker Nightmare Foes", "Apocalyptic Beast",
            "G-7", "Fiendish Tome II (Chapter 5) + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
        FarmStep("Nightmare Shank", "Nightmare Mandragora (G-6), Eft (E-9), Bunny (E-7)", "Lost Stihi",
            "K-8", "Fiendish Tome II (Chapter 6) + Tjukurrpa Medal"),
        FarmStep("Nightmare Roast", "Nightmare Crawler (F-6), Raven (J-6), Uragnite (K-7)", "Lost Barong",
            "K-9/10", "Fiendish Tome II (Chapter 7) + Tjukurrpa Mantle"),
        FarmStep("Nightmare Loin", "Nightmare Scorpion (K-8), Crab (J-7), Goobbue (L-9)", "Lost Alklha",
            "D/E-7", "Fiendish Tome II (Chapter 8) + Tjukurrpa Gauntlets"),
        FarmStep("Nightmare Chop", "the Stronger Nightmare Foes", "Lost Aitvaras",
            "F-10", "Fiendish Tome II (Chapter 9) + Tjukurrpa Axe"),
        FarmStep("Trade Fiendish Tome II Chapters 5-9", "Apocalyptic Beast and the four Lost NMs above", "Arch Apocalyptic Beast",
            "G-7", "Tjukurrpa Belt, Tjukurrpa Annulet, Tjukurrpa Ring + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
    ),
    weakening = listOf(
        WeakenNM("Stihi (I-6)", "Timed \u2014 20 min", "Shadescale Skull", "Fire / Poison / Wind Breath"),
        WeakenNM("Barong (G-9)", "Timed \u2014 20 min", "Shadescale Femur", "Body Slam, Heavy Stomp"),
        WeakenNM("Alklha (J-7)", "Timed \u2014 20 min", "Shadescale Talon", "Chaos Blade, Petro Eyes"),
        WeakenNM("Aitvaras (J-8)", "Timed \u2014 20 min", "Shadescale Heart", "Void / Lode / Thornsong"),
        WeakenNM("Beastmen NMs", "Lottery", "Cagebeast Blood", "1-hour abilities"),
    ),
    procWindows = listOf(
        ProcWindow("Crab, Dhalmel, Scorpion", "WS", "MA", "JA", "T. Whiteshell", "PLD, BRD, DRG, MNK"),
        ProcWindow("Crawler, Raven, Uragnite", "JA", "WS", "MA", "1 Byne Bill", "DRK, BLU, RDM, NIN"),
        ProcWindow("Bunny, Eft, Mandragora", "MA", "JA", "WS", "O. Bronzepiece", "PUP, BLM, RNG, WAR"),
    ),
    relicArmor = listOf(
        "Abyss Gauntlets" to "DRK Hands", "Argute Loafers" to "SCH Feet",
        "Assassin's Vest" to "THF Body", "Bard's Roundlet" to "BRD Head",
        "Cleric's Cap" to "WHM Head", "Commodore Gants" to "COR Hands",
        "Duelist's Gloves" to "RDM Hands", "Etoile Tiara" to "DNC Head",
        "Koga Kyahan" to "NIN Feet", "Melee Hose" to "MNK Legs",
        "Mirage Shalwar" to "BLU Legs", "Monster Jackcoat" to "BST Body",
        "Pantin Babouches" to "PUP Feet", "Saotome Haidate" to "SAM Legs",
        "Scout's Braccae" to "RNG Legs", "Sorcerer's Gloves" to "BLM Hands",
        "Summoner's Bracers" to "SMN Hands", "Valor Gauntlets" to "PLD Hands",
        "Warrior's Mufflers" to "WAR Hands", "Wyrm Greaves" to "DRG Feet",
    ),
    relicAccessories = listOf(
        "Abyss Cape" to "DRK", "Bard's Cape" to "BRD",
        "Duelist's Belt" to "RDM", "Koga Sarashi" to "NIN",
        "Melee Cape" to "MNK", "Mirage Mantle" to "BLU",
        "Pantin Cape" to "PUP", "Scout's Belt" to "RNG",
        "Sorcerer's Belt" to "BLM", "Valor Cape" to "PLD",
        "Warrior's Stone" to "WAR", "Wyrm Belt" to "DRG",
    ),
    relicWeapons = emptyList(), // Buburimu drops no relic weapons
    currencies = listOf("One Byne Bill", "One Hundred Byne Bill", "Ordelle Bronzepiece",
        "Montiont Silverpiece", "Tukuku Whiteshell", "Lungo-Nango Jadeshell"),
    miscItems = listOf(
        "Relic Armor -1 \u2014 the 20 hands-slot -1 pieces (all jobs), from Nightmare Monsters",
        "Forgotten Step (Relic +2, feet \u2014 AF2 upgrade)",
        "Copy of \"Ginuva's Battle Theory\"", "Gold Beastcoin", "Mythril Beastcoin",
    ),
)

// Third Dreamworld area. Boss = Antaeus; Relic set is Level 73, the -1 set is the FEET slot,
// AF2 +2 = Forgotten Journey (legs). Three timed weakening NMs (no Beastmen lottery here).
// NOTE (open lg): the farming flowchart and the map footer disagree on whether Lost Stringes is
// Fnd. Tome II Ch 11 or Ch 12 (and Scolopendra the other) — followed the flowchart (Stringes=11).
private val QUFIM_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Hieroglyphics \u2014 Qufim Island (H-7)",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Rank 6, Level 65, Chains of Promathia 3-5: Darkness Named cleared",
        "Support Jobs" to "On entry you choose whether to lock your support job; re-enable it any time by examining the Somnial Threshold. Running with your subjob disabled gives about a 1% chance to White-stagger a mob, which makes it drop a 100-currency.",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Dynamis-Qufim Sliver",
        "Title" to "Dynamis-Qufim Interloper",
        "Time Limit" to "60 minutes",
        "Boss" to "Antaeus",
    ),
    farming = listOf(
        FarmStep("Undying Juju", "the Nightmare Foes", "Antaeus",
            "F-6", "Fiendish Tome II (Chapter 10) + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
        FarmStep("Nightmare Blood", "Nightmare Gaylas (I-9), Kraken (H-9), Roc (I-8)", "Lost Stringes",
            "I-11", "Fiendish Tome II (Chapter 11) + Aife's Medal"),
        FarmStep("Nightmare Shell", "Nightmare Snoll (H-6), Stirge (I-9), Weapon (I-8)", "Lost Scolopendra",
            "H-8", "Fiendish Tome II (Chapter 12) + Aife's Mantle"),
        FarmStep("Nightmare Shard", "Nightmare Diremite (I-9), Raptor (I-8), Tiger (I-7)", "Lost Suttung",
            "H-6", "Fiendish Tome II (Chapter 13) + Aife's Bow"),
        FarmStep("Trade Fiendish Tome II Chapters 10-13", "Antaeus and the three Lost NMs above", "Arch Antaeus",
            "F-6", "Aife's Annulet, Aife's Ring, Aife's Pumps + 100 Byne Bill, L. Jadeshell, M. Silverpiece"),
    ),
    weakening = listOf(
        WeakenNM("Stringes (G-6)", "Timed \u2014 20 min", "Perforated Wing", "Damage Boost"),
        WeakenNM("Scolopendra (F-8)", "Timed \u2014 20 min", "Sea Monk Venom", "Regen"),
        WeakenNM("Suttung (E-5)", "Timed \u2014 20 min", "Undying Moiety", "Damage Resistance"),
    ),
    procWindows = listOf(
        ProcWindow("Diremite, Raptor, Tiger", "WS", "MA", "JA", "T. Whiteshell", "SCH, COR, PUP, SAM, SMN"),
        ProcWindow("Gaylas, Kraken, Roc", "JA", "WS", "MA", "1 Byne Bill", "DRK, THF, RDM, RNG"),
        ProcWindow("Snoll, Stirge, Weapon", "MA", "JA", "WS", "O. Bronzepiece", "WHM, BST, MNK, DRG"),
    ),
    relicArmor = listOf(
        "Abyss Flanchard" to "DRK Legs", "Argute Pants" to "SCH Legs",
        "Assassin's Poulaines" to "THF Feet", "Bard's Cuffs" to "BRD Hands",
        "Cleric's Pantaloons" to "WHM Legs", "Commodore Bottes" to "COR Feet",
        "Duelist's Tights" to "RDM Legs", "Etoile Toe Shoes" to "DNC Feet",
        "Koga Hatsuburi" to "NIN Head", "Melee Gloves" to "MNK Hands",
        "Mirage Bazubands" to "BLU Hands", "Monster Trousers" to "BST Legs",
        "Pantin Dastanas" to "PUP Hands", "Saotome Kote" to "SAM Hands",
        "Scout's Beret" to "RNG Head", "Sorcerer's Tonban" to "BLM Legs",
        "Summoner's Pigaches" to "SMN Feet", "Valor Coronet" to "PLD Head",
        "Warrior's Mask" to "WAR Head", "Wyrm Finger Gauntlets" to "DRG Hands",
    ),
    relicAccessories = listOf(
        "Abyss Cape" to "DRK", "Argute Belt" to "SCH",
        "Assassin's Cape" to "THF", "Cleric's Belt" to "WHM",
        "Commodore Belt" to "COR", "Duelist's Belt" to "RDM",
        "Melee Cape" to "MNK", "Monster Belt" to "BST",
        "Pantin Cape" to "PUP", "Saotome Koshi-Ate" to "SAM",
        "Scout's Belt" to "RNG", "Summoner's Cape" to "SMN",
        "Wyrm Belt" to "DRG",
    ),
    relicWeapons = emptyList(), // Qufim drops no relic weapons
    currencies = listOf("One Byne Bill", "One Hundred Byne Bill", "Ordelle Bronzepiece",
        "Montiont Silverpiece", "Tukuku Whiteshell", "Lungo-Nango Jadeshell"),
    miscItems = listOf(
        "Relic Armor -1 \u2014 the 20 feet-slot -1 pieces (all jobs), from Nightmare Monsters",
        "Forgotten Journey (Relic +2, legs \u2014 AF2 upgrade)",
        "Copy of \"Ginuva's Battle Theory\"", "Gold Beastcoin", "Mythril Beastcoin",
    ),
)

// Fourth / last Dreamworld area, and the odd one out. Requires the Buburimu + Qufim + Valkurm
// Slivers to enter. NO single boss and NO Nightmare->Lost->Arch ladder: you trade a Herald's Juju
// to fight ONE of four random Diabolos suits (Heart/Diamond/Club/Spade). Relic is Level 74/75
// across TWO floors (40 pieces), the -1 set is Body & Legs dropped by the stagger windows (see
// Proc Windows, whose right column is the -1 drop, not accessories), Nightmare Taurus drops the
// 20-piece Hydra Armor set, and there are TWO AF2 pieces. Clearing also unlocks the Atma of Nightmares.
private val TAVNAZIA_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Hieroglyphics \u2014 Tavnazian Safehold (H-9), Basement",
        "Requirements" to "Vial of Shrouded Sand, Prismatic Hourglass, Rank 6, Level 65, Chains of Promathia 3-5: Darkness Named cleared, plus the Buburimu / Qufim / Valkurm Slivers",
        "Support Jobs" to "On entry you choose whether to lock your support job; re-enable it any time by examining the Somnial Threshold. Running with your subjob disabled gives about a 1% chance to White-stagger a mob, which makes it drop a 100-currency.",
        "Repeatable" to "Once per Japanese midnight (unlimited with the Rhapsody in Azure)",
        "Reward" to "Dynamis-Tavnazia Sliver; clearing also unlocks purchasing the Atma of Nightmares",
        "Title" to "Dynamis-Tavnazia Interloper (Diabolos Nox also grants Nightmare Illuminator)",
        "Time Limit" to "60 minutes",
        "Boss" to "Four Diabolos suits \u2014 Heart / Diamond / Club / Spade. Trade a Herald's Juju at the spawn point to fight one at random; each has different properties. Beat any one for the Sliver.",
    ),
    farming = listOf(
        FarmStep("Herald's Juju", "traded at the boss spawn location", "Random Diabolos suit \u2014 Heart / Diamond / Club / Spade",
            "boss arena", "One Mega Boss at random; each suit has different properties. Beat any one for the Dynamis-Tavnazia Sliver."),
        FarmStep("Trade Fiendish Tome II Chapters 14-17", "the four Diabolos suits", "Random Arch Diabolos \u2014 Nox / Umbra / Somnus / Letum",
            "boss arena", "One Arch Mega Boss at random. Diabolos Nox grants the Nightmare Illuminator title."),
    ),
    procWindows = listOf(
        ProcWindow("Leech, Worm", "WS", "MA", "JA", "T. Whiteshell", "Leech \u2192 Relic Body -1 \u00b7 Worm \u2192 Relic Legs -1"),
        ProcWindow("Bugard, Hornet", "JA", "WS", "MA", "1 Byne Bill", "Hornet \u2192 Relic Legs -1"),
        ProcWindow("Cluster, Makara", "MA", "JA", "WS", "O. Bronzepiece", "Cluster \u2192 Relic Body -1 \u00b7 Makara \u2192 Relic Legs -1"),
        ProcWindow("Taurus", "Any", "Any", "Any", "Any", "Hydra Armor (any window)"),
    ),
    relicArmor = listOf(
        "Abyss Burgeonet" to "DRK Head (2F)", "Abyss Cuirass" to "DRK Body (1F)",
        "Argute Gown" to "SCH Body (1F)", "Argute Mortarboard" to "SCH Head (2F)",
        "Assassin's Armlets" to "THF Hands (2F)", "Assassin's Culottes" to "THF Legs (1F)",
        "Bard's Cannions" to "BRD Legs (2F)", "Bard's Justaucorps" to "BRD Body (1F)",
        "Cleric's Bliaut" to "WHM Body (1F)", "Cleric's Mitts" to "WHM Hands (2F)",
        "Commodore Frac" to "COR Body (1F)", "Commodore Tricorne" to "COR Head (2F)",
        "Duelist's Chapeau" to "RDM Head (2F)", "Duelist's Tabard" to "RDM Body (1F)",
        "Etoile Casaque" to "DNC Body (2F)", "Etoile Tights" to "DNC Legs (1F)",
        "Koga Chainmail" to "NIN Body (1F)", "Koga Tekko" to "NIN Hands (2F)",
        "Melee Crown" to "MNK Head (2F)", "Melee Cyclas" to "MNK Body (1F)",
        "Mirage Jubbah" to "BLU Body (1F)", "Mirage Keffiyeh" to "BLU Head (2F)",
        "Monster Gaiters" to "BST Feet (1F)", "Monster Gloves" to "BST Hands (2F)",
        "Pantin Taj" to "PUP Head (2F)", "Pantin Tobe" to "PUP Body (1F)",
        "Saotome Domaru" to "SAM Body (1F)", "Saotome Kabuto" to "SAM Head (2F)",
        "Scout's Jerkin" to "RNG Body (2F)", "Scout's Socks" to "RNG Feet (1F)",
        "Sorcerer's Coat" to "BLM Body (1F)", "Sorcerer's Petasos" to "BLM Head (2F)",
        "Summoner's Doublet" to "SMN Body (1F)", "Summoner's Horn" to "SMN Head (2F)",
        "Valor Breeches" to "PLD Legs (1F)", "Valor Surcoat" to "PLD Body (2F)",
        "Warrior's Cuisses" to "WAR Legs (1F)", "Warrior's Lorica" to "WAR Body (2F)",
        "Wyrm Armet" to "DRG Head (2F)", "Wyrm Mail" to "DRG Body (1F)",
    ),
    relicWeapons = emptyList(), // Tavnazia drops no relic weapons
    currencies = listOf("One Byne Bill", "One Hundred Byne Bill", "Ordelle Bronzepiece",
        "Montiont Silverpiece", "Tukuku Whiteshell", "Lungo-Nango Jadeshell"),
    miscItems = listOf(
        "Relic Armor -1 \u2014 every job's Body -1 and Legs -1 (40 pieces); which one drops depends on the stagger window (see Proc Windows)",
        "Hydra Armor (from Nightmare Taurus) \u2014 20 pieces: mage set (Beret/Doublet/Gloves/Brais/Gaiters), melee set (Tiara/Harness/Mittens/Tights/Spats), tank set (Salade/Haubert/Moufles/Brayettes/Sollerets), Fellow set (Cap/Jupon/Bracers/Hose/Boots)",
        "Forgotten Thought (Relic +2, head) and Forgotten Hope (Relic +2, body) \u2014 AF2 upgrades",
        "Gold Beastcoin", "Mythril Beastcoin",
    ),
)

// First DIVERGENCE area (Dynamis-San d'Oria [D]). A different beast from both the cities and the
// Dreamworld: Level 95, 3-18 players, requires the Tavnazia Sliver + Empty Hourglass. No proc-window
// currency and no relic-drop set; instead a three-wave boss chain (mid-boss -> zone boss -> Disjoined)
// and a REFORGE mechanic (Footshard before the mid-boss + Voidfoot after -> Relic +2/+3 for this zone's
// slot; San d'Oria = FEET). Divergence "statues" carry an eye colour that flips damage taken; the
// Colorless one spawns the Goblin NM Aurix. Roster tagged rev-210 (auto-fills NM/Mobs).
private val SANDORIA_D_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Enigmatic Footprints \u2014 Southern San d'Oria (K-10), the tree near the gate (Home Point #2). Arrives at L-10.",
        "Requirements" to "Level 95, 3-18 players, Dynamis-Tavnazia Sliver, Empty Hourglass",
        "Reforge" to "San d'Oria [D] upgrades the Relic FEET slot. Footshard: <job> drops from that job's Orc before the mid-boss; Voidfoot: <job> from that job's Orc after. Trade both to reforge that job's relic feet to +2 / +3. (Bastok = Hands, Windurst = Head, Jeuno = Legs.)",
        "Divergence Statues" to "Statues carry an eye colour: Blue takes +25% magic / \u221275% physical damage; Green +25% physical / \u221275% magic; Red spawns higher-level Orc NMs with Orcish Counterstance (high-rate melee counter). A Colorless statue (no nameplate icon) replaces one random statue at a time \u2014 aggroing it also spawns the Goblin NM Aurix.",
        "Aurix" to "One per wave, from the current Colorless statue. Left undamaged ~2-3 min he flees, then respawns from another Colorless statue keeping his remaining HP; the hopping stops once he is defeated.",
        "Title" to "Trespasser (beat the mid-boss) \u2192 Infiltrator (beat Halphas) \u2192 Judge, Jury and Executioner (beat all four Divergence zones' wave-3 Disjoined bosses)",
    ),
    warning = "All Orcs are dual-job with 1-hour abilities from BOTH jobs (BST Orcs can Charm even with a pet out). Halphas and the Leader/Commander Orcs use Orcish Counterstance \u2014 a high-rate Counter against melee.",
    farming = listOf(
        FarmStep("there from the entrance", "wave-1 Corporal Tombstone statues (Squadron / Leader Orcs)", "Overseer's Tombstone \u2014 mid-boss",
            "I-8, near Northern San d'Oria", "+30 min & the Trespasser title. Squadron/Leader Orcs rarely drop Footshards + Rusted I. Cards before it dies; Black I. Cards drop after."),
        FarmStep("defeating the mid-boss", "wave-2 Regiment / Commander Orcs", "Halphas \u2014 zone boss (PLD/RUN/WAR/DRK)",
            "Mog House, M-5", "+30 min & the Infiltrator title; up to 3 Kindred's Medals + Volte Armor. Regiment/Commander Orcs rarely drop Voidfeet + Black I. Cards."),
        FarmStep("defeating Halphas", "wave-3 Volte Hydra Corps + Aurix", "Disjoined Elvaan \u2014 Fomor NM",
            "I-8, near Northern San d'Oria", "Old Identification Cards + Demon's Medals. Beat this plus the other three zones' Disjoined bosses for the Judge, Jury and Executioner title."),
    ),
    relicWeapons = emptyList(),
    currencies = listOf("Rusted I. Card", "Black I. Card", "Beastmen's Medal",
        "Kindred's Medal", "Old Identification Card", "Demon's Medal"),
    miscItems = listOf(
        "Reforged Relic Armor +2 / +3 \u2014 the zone's activity: reforge a job's relic FEET using its Footshard (pre-mid-boss) + Voidfoot (post-mid-boss) upgrade items",
        "Volte Armor Set \u2014 Volte Beret, Doublet, Gloves, Brais, Gaiters (rare drops from Red-eye Leader/Commander Orcs)",
    ),
)

// Second Divergence area (Dynamis-Bastok [D]). Same shape as San d'Oria [D] but the mobs are QUADAVs
// (not Orcs), the reforge slot is HANDS (Handshard -> Voidhand), the Red-eye statues field Wrath of
// Gu'Dha, and the boss chain is Mu'Sha Effigy -> Ka'Rho Fearsinger -> Disjoined Galka. Volte set here
// is the Harness set. Roster created/tagged this rev (Mu'Sha Effigy moved off its stray classic tag).
private val BASTOK_D_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Enigmatic Footprints \u2014 Bastok Mines (bottom-left of I-9, south of Home Point #1). Arrives at H-10.",
        "Requirements" to "Level 95, 3-18 players, Dynamis-Tavnazia Sliver, Empty Hourglass",
        "Reforge" to "Bastok [D] upgrades the Relic HANDS slot. Handshard: <job> drops from that job's Quadav before the mid-boss; Voidhand: <job> from that job's Quadav after. Trade both to reforge that job's relic hands to +2 / +3. (San d'Oria = Feet, Windurst = Head, Jeuno = Legs.)",
        "Divergence Statues" to "Statues carry an eye colour: Blue takes +30% magic / \u221295% physical damage; Green +30% physical / \u221295% magic; Red spawns higher-level Quadav NMs with Wrath of Gu'Dha (AoE knockback + super-gravity, absorbable by shadows). A Colorless statue (no nameplate icon) replaces one random statue at a time \u2014 aggroing it also spawns the Goblin NM Aurix.",
        "Aurix" to "One per wave, from the current Colorless statue. Left undamaged ~2-3 min he flees, then respawns from another Colorless statue keeping his remaining HP; the hopping stops once he is defeated.",
        "Title" to "Trespasser (beat the mid-boss) \u2192 Infiltrator (beat Ka'Rho Fearsinger) \u2192 Judge, Jury and Executioner (beat all four Divergence zones' wave-3 Disjoined bosses)",
    ),
    warning = "All Quadavs are dual-job with 1-hour abilities from BOTH jobs (BST Quadavs can Charm even with a pet out). Ka'Rho Fearsinger and the Leader/Commander Quadavs use Wrath of Gu'Dha \u2014 an AoE knockback with a super-gravity effect (absorbable by shadows).",
    farming = listOf(
        FarmStep("there from the entrance", "wave-1 Lithicthrower Image statues (Squadron / Leader Quadavs)", "Mu'Sha Effigy \u2014 mid-boss",
            "near Bastok Markets (top of F-5)", "+30 min & the Trespasser title. Squadron/Leader Quadavs rarely drop Handshards + Rusted I. Cards before it dies; Black I. Cards drop after."),
        FarmStep("defeating the mid-boss", "wave-2 Regiment / Commander Quadavs", "Ka'Rho Fearsinger \u2014 zone boss (MNK)",
            "near the Mog House (bottom-right of K-8)", "+30 min & the Infiltrator title; up to 3 Kindred's Medals + the Volte Harness set. Regiment/Commander Quadavs rarely drop Voidhands + Black I. Cards."),
        FarmStep("defeating Ka'Rho Fearsinger", "wave-3 Volte Hydra Corps + Aurix", "Disjoined Galka \u2014 Fomor NM",
            "near the zone to South Gustaberg (H-9)", "Old Identification Cards + Demon's Medals. Beat this plus the other three zones' Disjoined bosses for the Judge, Jury and Executioner title."),
    ),
    relicWeapons = emptyList(),
    currencies = listOf("Rusted I. Card", "Black I. Card", "Beastmen's Medal",
        "Kindred's Medal", "Old Identification Card", "Demon's Medal"),
    miscItems = listOf(
        "Reforged Relic Armor +2 / +3 \u2014 the zone's activity: reforge a job's relic HANDS using its Handshard (pre-mid-boss) + Voidhand (post-mid-boss) upgrade items",
        "Volte Armor Set (Harness set) \u2014 Volte Tiara, Harness, Mittens, Tights, Spats (rare drops from Red-eye Leader/Commander Quadavs; the zone boss Ka'Rho Fearsinger drops the full set)",
    ),
)

// Third Divergence area (Dynamis-Windurst [D]), the 13th of 14 area pages (Jeuno [D] still remains).
// Mobs are YAGUDOs, reforge slot is HEAD (Headshard -> Voidhead), the Red-eye statues field Doom, and the boss chain is
// Evincing Idol -> Fii Pexu the Eternal -> Disjoined Tarutaru. Volte set here is the Salade set. The
// Divergence statue colours here REDUCE damage taken (defensive) rather than amplify it. Roster
// created/tagged this rev (Evincing Idol moved off its stray classic tag).
private val WINDURST_D_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Enigmatic Footprints \u2014 Windurst Walls (H-7), Home Point #1, by Heavens Tower.",
        "Requirements" to "Level 95, 3-18 players, Dynamis-Tavnazia Sliver, Empty Hourglass",
        "Reforge" to "Windurst [D] upgrades the Relic HEAD slot. Headshard: <job> drops from that job's Yagudo before the mid-boss; Voidhead: <job> from that job's Yagudo after. Trade both to reforge that job's relic head to +2 / +3. (San d'Oria = Feet, Bastok = Hands, Jeuno = Legs.)",
        "Divergence Statues" to "Statues carry an eye colour: Blue takes \u221250% damage from all melee types; Green takes \u221233.3% from ranged and magic; Red spawns higher-level Yagudo NMs with Doom (a 10-count doom on one target, resistable). A Colorless statue (no nameplate icon) replaces one random statue at a time \u2014 aggroing it also spawns the Goblin NM Aurix.",
        "Aurix" to "One per wave, from the current Colorless statue. Left undamaged ~2-3 min he flees, then respawns from another Colorless statue keeping his remaining HP; the hopping stops once he is defeated.",
        "Title" to "Trespasser (beat the mid-boss) \u2192 Infiltrator (beat Fii Pexu the Eternal) \u2192 Judge, Jury and Executioner (beat all four Divergence zones' wave-3 Disjoined bosses)",
    ),
    warning = "All Yagudos are dual-job with 1-hour abilities from BOTH jobs (BST Yagudos can Charm even with a pet out). Fii Pexu the Eternal and the Leader/Commander Yagudos use Doom \u2014 a 10-count doom on the target (may be resisted).",
    farming = listOf(
        FarmStep("there from the entrance", "wave-1 Incarnation Icon statues (Squadron / Leader Yagudos)", "Evincing Idol \u2014 mid-boss",
            "near the zone to Windurst Waters (C-6)", "+30 min & the Trespasser title. Squadron/Leader Yagudos rarely drop Headshards + Rusted I. Cards before it dies; Black I. Cards drop after."),
        FarmStep("defeating the mid-boss", "wave-2 Regiment / Commander Yagudos", "Fii Pexu the Eternal \u2014 zone boss (THF)",
            "near the Mog House (bottom-right of K-8)", "+30 min & the Infiltrator title; up to 3 Kindred's Medals + the Volte Salade set. Regiment/Commander Yagudos rarely drop Voidheads + Black I. Cards."),
        FarmStep("defeating Fii Pexu the Eternal", "wave-3 Volte Hydra Corps + Aurix", "Disjoined Tarutaru \u2014 Fomor NM",
            "near Heaven's Tower (H-7)", "Old Identification Cards + Demon's Medals. Beat this plus the other three zones' Disjoined bosses for the Judge, Jury and Executioner title."),
    ),
    relicWeapons = emptyList(),
    currencies = listOf("Rusted I. Card", "Black I. Card", "Beastmen's Medal",
        "Kindred's Medal", "Old Identification Card", "Demon's Medal"),
    miscItems = listOf(
        "Reforged Relic Armor +2 / +3 \u2014 the zone's activity: reforge a job's relic HEAD using its Headshard (pre-mid-boss) + Voidhead (post-mid-boss) upgrade items",
        "Volte Armor Set (Salade set) \u2014 Volte Salade, Haubert, Moufles, Brayettes, Sollerets (rare drops from Red-eye Leader/Commander Yagudos; the zone boss Fii Pexu the Eternal drops the full set)",
    ),
)

// Fourth/last Divergence area (Dynamis-Jeuno [D]) and the 14th / FINAL area page. Mobs are GOBLINs,
// reforge slot is LEGS (Legshard -> Voidleg), the Red-eye statues field Goblin Dice (a random-effect
// roll), and the boss chain is Impish Golem -> Obstatrix -> Disjoined Mithra. Volte set here is the Cap
// set. Roster created/tagged this rev (Impish Golem moved off its stray classic tag).
private val JEUNO_D_INFO = AreaInfo(
    facts = listOf(
        "Starting NPC" to "Enigmatic handprints \u2014 Ru'Lude Gardens (F-9), Home Point #3.",
        "Requirements" to "Level 95, 3-18 players, Dynamis-Tavnazia Sliver, Empty Hourglass",
        "Reforge" to "Jeuno [D] upgrades the Relic LEGS slot. Legshard: <job> drops from that job's Goblin before the mid-boss; Voidleg: <job> from that job's Goblin after. Trade both to reforge that job's relic legs to +2 / +3. (San d'Oria = Feet, Bastok = Hands, Windurst = Head.)",
        "Divergence Statues" to "Statues carry an eye colour: Blue takes +50% damage and its AoEs deal \u221299% to secondary targets; Green takes +20% damage and resists all Enfeebling Magic (incl. Sleep and Lullaby); Red spawns higher-level Goblin NMs with Goblin Dice. A Colorless statue (no nameplate icon) replaces one random statue at a time \u2014 aggroing it also spawns the Goblin NM Aurix.",
        "Aurix" to "One per wave, from the current Colorless statue. Left undamaged ~2-3 min he flees, then respawns from another Colorless statue keeping his remaining HP; the hopping stops once he is defeated.",
        "Title" to "Trespasser (beat the mid-boss) \u2192 Infiltrator (beat Obstatrix) \u2192 Judge, Jury and Executioner (beat all four Divergence zones' wave-3 Disjoined bosses)",
    ),
    warning = "All Goblins are dual-job with 1-hour abilities from BOTH jobs (BST Goblins can Charm even with a pet out). Obstatrix and the Leader/Commander Goblins use Goblin Dice \u2014 a roll with ~12 outcomes: a 2 restores nearby players' abilities, but others deal AoE damage, enfeeble, dispel, reset your TP, or fully restore the NM's HP.",
    farming = listOf(
        FarmStep("there from the entrance", "wave-1 Impish Statue statues (Squadron / Leader Goblins)", "Impish Golem \u2014 mid-boss",
            "top of the palace stairs (won't aggro if you hug the railing)", "+30 min & the Trespasser title. Squadron/Leader Goblins rarely drop Legshards + Rusted I. Cards before it dies; Black I. Cards drop after."),
        FarmStep("defeating the mid-boss", "wave-2 Regiment / Commander Goblins", "Obstatrix \u2014 zone boss (MNK)",
            "near the Mog House (bottom-right of K-8)", "+30 min & the Infiltrator title; up to 3 Kindred's Medals + the Volte Cap set. Regiment/Commander Goblins rarely drop Voidlegs + Black I. Cards."),
        FarmStep("defeating Obstatrix", "wave-3 Volte Hydra Corps + Aurix", "Disjoined Mithra \u2014 Fomor NM",
            "near the zone to Upper Jeuno (H-10)", "Old Identification Cards + Demon's Medals. Beat this plus the other three zones' Disjoined bosses for the Judge, Jury and Executioner title."),
    ),
    relicWeapons = emptyList(),
    currencies = listOf("Rusted I. Card", "Black I. Card", "Beastmen's Medal",
        "Kindred's Medal", "Old Identification Card", "Demon's Medal"),
    miscItems = listOf(
        "Reforged Relic Armor +2 / +3 \u2014 the zone's activity: reforge a job's relic LEGS using its Legshard (pre-mid-boss) + Voidleg (post-mid-boss) upgrade items",
        "Volte Armor Set (Cap set) \u2014 Volte Cap, Jupon, Bracers, Hose, Boots (rare drops from Red-eye Leader/Commander Goblins; the zone boss Obstatrix drops the full set)",
    ),
)

private fun areaInfoFor(zone: String): AreaInfo = when (zone) {
    "Dynamis-San d'Oria" -> SANDORIA_INFO
    "Dynamis-Windurst" -> WINDURST_INFO
    "Dynamis-Bastok" -> BASTOK_INFO
    "Dynamis-Jeuno" -> JEUNO_INFO
    "Dynamis-Beaucedine" -> BEAUCEDINE_INFO
    "Dynamis-Xarcabard" -> XARCABARD_INFO
    "Dynamis-Valkurm" -> VALKURM_INFO
    "Dynamis-Buburimu" -> BUBURIMU_INFO
    "Dynamis-Qufim" -> QUFIM_INFO
    "Dynamis-Tavnazia" -> TAVNAZIA_INFO
    "Dynamis-San d'Oria [D]" -> SANDORIA_D_INFO
    "Dynamis-Bastok [D]" -> BASTOK_D_INFO
    "Dynamis-Windurst [D]" -> WINDURST_D_INFO
    "Dynamis-Jeuno [D]" -> JEUNO_D_INFO
    else -> AreaInfo()
}

@Composable
private fun FactRow(label: String, value: String) {
    Column(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
        Text(label, color = TextMuted, fontSize = 12.sp, fontWeight = FontWeight.SemiBold)
        Text(value, color = TextSoft, fontSize = 13.sp, lineHeight = 18.sp,
            modifier = Modifier.padding(start = 12.dp, top = 1.dp))
    }
}

@Composable
private fun DynamisZoneScreen(vm: MobileWatchViewModel) {
    val zone = vm.ui.selectedContentZone ?: return
    val group = dynamisTagGroup(zone)
    val mobs = remember(zone) { vm.mobsForContent(group, zone) }
    val nms = remember(mobs, zone) {
        mobs.filter { it.nm }.sortedWith(compareBy({ bossOrder(vm.contentRoleOf(it, group, zone)) }, { -it.levelLo }, { it.name }))
    }
    val te = remember(mobs, zone) {
        mobs.filter { vm.contentRoleOf(it, group, zone).equals("TE", ignoreCase = true) }
    }
    val regular = remember(mobs, zone) {
        mobs.filter { !it.nm }.sortedWith(compareBy({ -it.levelLo }, { it.name }))
    }
    val info = remember(zone) { areaInfoFor(zone) }
    val hasZone = remember(zone) { vm.hasZone(zone) }
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(zone, onBack = { vm.clearContentZone() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item(key = "head") {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {

                    CollapsibleSection("General Info", stateKey = "$zone:info") {
                        if (info.facts.isEmpty()) Placeholder()
                        else info.facts.forEach { (l, v) -> FactRow(l, v) }
                        if (hasZone) {
                            Row(
                                Modifier.fillMaxWidth().clickable { vm.openZoneDetailByName(zone) }
                                    .padding(top = 10.dp, bottom = 4.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(Icons.Filled.Place, null, tint = AccentGreen, modifier = Modifier.size(18.dp))
                                Spacer(Modifier.width(8.dp))
                                Text("Map & zone details", color = JobsBlue, fontSize = 13.sp,
                                    fontWeight = FontWeight.Medium)
                            }
                        }
                    }

                    if (te.isNotEmpty()) {
                        CollapsibleSection("Time Extension", stateKey = "$zone:te") {
                            te.forEach { mob ->
                                Column(
                                    Modifier.fillMaxWidth().clickable { vm.selectMob(mob, zone) }
                                        .padding(vertical = 8.dp)
                                ) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Text(mob.name, color = TextSoft, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                        Text(mob.drops, color = TextMuted, fontSize = 11.sp)
                                    }
                                    mob.notes.firstOrNull { it.contains("Granules of Time") && it.contains(zone) }?.let {
                                        Text(it, color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp,
                                            modifier = Modifier.padding(top = 4.dp))
                                    }
                                }
                                HorizontalDivider(color = CharcoalDark)
                            }
                            if (te.size == 4 && te.none { it.drops.contains("20 min") }) {
                                Text(
                                    "The last time extension is 20 minutes: a fifth statue spawns at random among the four locations above and grants +20 min (the four fixed statues each give +10).",
                                    color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp,
                                    modifier = Modifier.padding(top = 8.dp)
                                )
                            }
                        }
                    }

                    if (info.procWindows.isNotEmpty()) {
                        CollapsibleSection("Proc Windows", stateKey = "$zone:procs") {
                            Text(
                                "Stagger a mob with the method shown for its genus in the current Earth-time window to make it drop that group's currency. WS = weapon skill \u00b7 MA = magic \u00b7 JA = job ability.",
                                color = TextMuted, fontSize = 11.sp, lineHeight = 16.sp,
                                modifier = Modifier.padding(bottom = 8.dp)
                            )
                            Row(Modifier.fillMaxWidth().padding(bottom = 2.dp)) {
                                Spacer(Modifier.weight(1.5f))
                                Text("0-8", color = TextMuted, fontSize = 10.sp, textAlign = TextAlign.Center, modifier = Modifier.weight(1f))
                                Text("8-16", color = TextMuted, fontSize = 10.sp, textAlign = TextAlign.Center, modifier = Modifier.weight(1f))
                                Text("16-24", color = TextMuted, fontSize = 10.sp, textAlign = TextAlign.Center, modifier = Modifier.weight(1f))
                            }
                            info.procWindows.forEach { pw ->
                                Column(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Text(pw.families, color = TextSoft, fontSize = 12.sp, lineHeight = 16.sp, modifier = Modifier.weight(1.5f))
                                        Text(pw.w1, color = AccentGreen, fontSize = 13.sp, fontWeight = FontWeight.Medium, textAlign = TextAlign.Center, modifier = Modifier.weight(1f))
                                        Text(pw.w2, color = AccentGreen, fontSize = 13.sp, fontWeight = FontWeight.Medium, textAlign = TextAlign.Center, modifier = Modifier.weight(1f))
                                        Text(pw.w3, color = AccentGreen, fontSize = 13.sp, fontWeight = FontWeight.Medium, textAlign = TextAlign.Center, modifier = Modifier.weight(1f))
                                    }
                                    Row(Modifier.fillMaxWidth().padding(top = 3.dp), verticalAlignment = Alignment.CenterVertically) {
                                        Text(pw.currency, color = AccentGold, fontSize = 11.sp, modifier = Modifier.weight(1f))
                                        Text(pw.jobs, color = TextMuted, fontSize = 11.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1.3f))
                                    }
                                }
                                HorizontalDivider(color = CharcoalDark)
                            }
                        }
                    }

                    if (nms.isNotEmpty()) {
                        CollapsibleSection("Notorious Monsters", stateKey = "$zone:nms") {
                            info.warning?.let {
                                Text(it, color = AccentRed, fontSize = 12.sp, lineHeight = 17.sp,
                                    modifier = Modifier.padding(bottom = 6.dp))
                            }
                            nms.forEach { mob ->
                                val role = bossLabel(vm.contentRoleOf(mob, group, zone))
                                Row(
                                    Modifier.fillMaxWidth().clickable { vm.selectMob(mob, zone) }
                                        .padding(vertical = 7.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column(Modifier.weight(1f)) {
                                        Text(mob.name, color = AccentRed, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                                        if (role != null) Text(role, color = TextMuted, fontSize = 10.sp)
                                    }
                                    Text(if (mob.levelLo > 0) "Lv ${mob.levelLo}" else "",
                                        color = TextMuted, fontSize = 12.sp)
                                }
                                HorizontalDivider(color = CharcoalDark)
                            }
                        }
                    }

                    if (regular.isNotEmpty()) {
                        CollapsibleSection("Mobs", stateKey = "$zone:mobs") {
                            regular.forEach { mob ->
                                Row(
                                    Modifier.fillMaxWidth().clickable { vm.selectMob(mob, zone) }
                                        .padding(vertical = 7.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(mob.name, color = TextSoft, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                    Text(if (mob.levelLo > 0) "Lv ${mob.levelLo}" else "",
                                        color = TextMuted, fontSize = 12.sp)
                                }
                                HorizontalDivider(color = CharcoalDark)
                            }
                        }
                    }

                    if (info.farming.isNotEmpty() || info.weakening.isNotEmpty()) {
                        CollapsibleSection("Farming", stateKey = "$zone:farming") {
                            info.farming.forEach { step ->
                                Column(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                                    Text(step.target, color = AccentRed, fontSize = 13.sp, fontWeight = FontWeight.Medium)
                                    Text(step.at, color = TextMuted, fontSize = 11.sp)
                                    Text("Spawn: ${step.trigger}  (from ${step.from})", color = TextSoft, fontSize = 11.sp,
                                        lineHeight = 16.sp, modifier = Modifier.padding(top = 2.dp))
                                    Text("Drops: ${step.yields}", color = TextSoft, fontSize = 11.sp, lineHeight = 16.sp)
                                }
                                HorizontalDivider(color = CharcoalDark)
                            }
                            if (info.weakening.isNotEmpty()) {
                                Text("Weakening Items", color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(top = 10.dp, bottom = 2.dp))
                                Text("Kill these before the fight \u2014 each drops an item that strips one of the boss's abilities.",
                                    color = TextMuted, fontSize = 11.sp, lineHeight = 15.sp,
                                    modifier = Modifier.padding(bottom = 4.dp))
                                info.weakening.forEach { w ->
                                    Column(Modifier.fillMaxWidth().padding(vertical = 5.dp)) {
                                        Row(Modifier.fillMaxWidth()) {
                                            Text(w.nm, color = AccentRed, fontSize = 13.sp, fontWeight = FontWeight.Medium,
                                                modifier = Modifier.weight(1f))
                                            Text(w.spawn, color = TextMuted, fontSize = 11.sp)
                                        }
                                        Text("Drops: ${w.item}", color = TextSoft, fontSize = 11.sp,
                                            lineHeight = 16.sp, modifier = Modifier.padding(top = 2.dp))
                                        Text("Removes: ${w.removes}", color = TextSoft, fontSize = 11.sp, lineHeight = 16.sp)
                                    }
                                    HorizontalDivider(color = CharcoalDark)
                                }
                            }
                        }
                    }

                    val hasRewards = info.relicArmor.isNotEmpty() || info.relicAccessories.isNotEmpty() ||
                        info.relicWeapons.isNotEmpty() || info.attestations.isNotEmpty() ||
                        info.currencies.isNotEmpty() || info.miscItems.isNotEmpty()
                    if (hasRewards) {
                        CollapsibleSection("Rewards", stateKey = "$zone:rewards") {
                            if (info.currencies.isNotEmpty()) {
                                Text("Currency", color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(top = 4.dp, bottom = 2.dp))
                                Text(info.currencies.joinToString(", "), color = TextSoft, fontSize = 12.sp)
                            }
                            if (info.relicArmor.isNotEmpty()) {
                                Text("Relic Armor", color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(top = 8.dp, bottom = 2.dp))
                                info.relicArmor.forEach { (piece, slot) ->
                                    Row(Modifier.fillMaxWidth().padding(vertical = 2.dp)) {
                                        Text(piece, color = TextSoft, fontSize = 12.sp, modifier = Modifier.weight(1f))
                                        Text(slot, color = TextMuted, fontSize = 11.sp)
                                    }
                                }
                            }
                            if (info.relicAccessories.isNotEmpty()) {
                                Text("Relic Accessories", color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(top = 8.dp, bottom = 2.dp))
                                info.relicAccessories.forEach { (piece, job) ->
                                    Row(Modifier.fillMaxWidth().padding(vertical = 2.dp)) {
                                        Text(piece, color = TextSoft, fontSize = 12.sp, modifier = Modifier.weight(1f))
                                        Text(job, color = TextMuted, fontSize = 11.sp)
                                    }
                                }
                            }
                            if (info.relicWeapons.isNotEmpty()) {
                                Text("Relic Weapons", color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(top = 8.dp, bottom = 2.dp))
                                Text(info.relicWeapons.joinToString(", "), color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp)
                            }
                            if (info.attestations.isNotEmpty()) {
                                Text(info.attestationsLabel, color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(top = 8.dp, bottom = 2.dp))
                                info.attestations.forEach { (name, weapon) ->
                                    Row(Modifier.fillMaxWidth().padding(vertical = 2.dp)) {
                                        Text(name, color = TextSoft, fontSize = 12.sp, modifier = Modifier.weight(1f))
                                        Text(weapon, color = TextMuted, fontSize = 11.sp)
                                    }
                                }
                            }
                            if (info.miscItems.isNotEmpty()) {
                                Text("Misc. Items", color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(top = 8.dp, bottom = 2.dp))
                                Text(info.miscItems.joinToString(", "), color = TextSoft, fontSize = 12.sp, lineHeight = 17.sp)
                            }
                        }
                    }

                    Spacer(Modifier.height(24.dp))
                }
            }
        }
    }
}

@Composable
private fun FilterDropdown(label: String, value: String, options: List<String>, modifier: Modifier = Modifier, onSelect: (String) -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    Surface(color = Panel, shape = RoundedCornerShape(8.dp), modifier = modifier) {
        Box {
            Row(
                Modifier.fillMaxWidth().clickable { expanded = true }.padding(horizontal = 10.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    if (value == "All") label else value,
                    color = if (value == "All") TextMuted else AccentGreen,
                    fontSize = 12.sp, maxLines = 1, overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f, fill = false)
                )
                Icon(Icons.Filled.ArrowDropDown, null, tint = TextMuted, modifier = Modifier.size(18.dp))
            }
            DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
                (listOf("All") + options).forEach { opt ->
                    DropdownMenuItem(text = { Text(opt, fontSize = 13.sp) }, onClick = { expanded = false; onSelect(opt) })
                }
            }
        }
    }
}

@Composable
private fun FishingScreen(vm: MobileWatchViewModel) {
    val all = vm.fishList()
    var query by rememberSaveable { mutableStateOf("") }
    var fArea by rememberSaveable { mutableStateOf("All") }
    var fRod by rememberSaveable { mutableStateOf("All") }
    var fBait by rememberSaveable { mutableStateOf("All") }
    var fRank by rememberSaveable { mutableStateOf("All") }
    var fLevel by rememberSaveable { mutableStateOf("All") }
    var sortAz by rememberSaveable { mutableStateOf(false) }
    val areas = remember(all) { all.flatMap { f -> f.zones.map { it.name } }.distinct().sorted() }
    val rods = remember(all) { all.flatMap { f -> f.rods.map { it.name } }.distinct().sorted() }
    val baits = remember(all) { all.flatMap { f -> f.baits.map { it.name } }.distinct().sorted() }
    val ranks = remember(all) { all.map { it.rank }.distinct() }
    fun bucket(lv: Int): String = if (lv <= 10) "0-10" else "${(lv - 1) / 10 * 10 + 1}-${(lv - 1) / 10 * 10 + 10}"
    val levels = remember(all) { all.map { bucket(it.level) }.distinct().sortedBy { it.substringBefore('-').toInt() } }
    val list = all.filter { f ->
        (query.isBlank() || f.name.contains(query, true)) &&
        (fArea == "All" || f.zones.any { it.name == fArea }) &&
        (fRod == "All" || f.rods.any { it.name == fRod }) &&
        (fBait == "All" || f.baits.any { it.name == fBait }) &&
        (fRank == "All" || f.rank == fRank) &&
        (fLevel == "All" || bucket(f.level) == fLevel)
    }
    val shown = if (sortAz) list.sortedBy { it.name } else list
    val listState = rememberLazyListState()
    var sortNonce by remember { mutableStateOf(0) }
    LaunchedEffect(sortNonce) { if (sortNonce > 0) listState.scrollToItem(0) }
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar("Fishing", onBack = { vm.clearHobby() }, actions = {
                if (vm.hobbyInfo("fishing") != null) IconButton(onClick = { vm.openHobbyInfo() }) {
                    Icon(Icons.Filled.Info, "Guild Info", tint = AccentGold)
                }
            })
        }
    ) { pad ->
        Column(Modifier.padding(pad).fillMaxSize()) {
            OutlinedTextField(
                value = query, onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 4.dp),
                singleLine = true, shape = RoundedCornerShape(12.dp),
                leadingIcon = { Icon(Icons.Filled.Search, null) },
                trailingIcon = {
                    if (query.isNotEmpty()) IconButton(onClick = { query = "" }) {
                        Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                    }
                },
                placeholder = { Text("Search fish", maxLines = 1) }
            )
            Row(
                Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 2.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                FilterDropdown("Area", fArea, areas, Modifier.weight(1f)) { fArea = it }
                FilterDropdown("Rod", fRod, rods, Modifier.weight(1f)) { fRod = it }
                FilterDropdown("Bait", fBait, baits, Modifier.weight(1f)) { fBait = it }
            }
            Row(
                Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 2.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                FilterDropdown("Rank", fRank, ranks, Modifier.weight(1f)) { fRank = it }
                FilterDropdown("Level", fLevel, levels, Modifier.weight(1f)) { fLevel = it }
                Surface(color = Panel, shape = RoundedCornerShape(8.dp), modifier = Modifier.weight(1f)) {
                    Row(
                        Modifier.fillMaxWidth().clickable { sortAz = !sortAz; sortNonce++ }.padding(horizontal = 10.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center
                    ) {
                        Text(if (sortAz) "A-Z" else "By Level",
                            color = if (sortAz) AccentGreen else TextMuted, fontSize = 12.sp, maxLines = 1)
                    }
                }
            }
            LazyColumn(Modifier.fillMaxSize(), state = listState) {
                items(shown, key = { it.name }) { f ->
                    Column(
                        Modifier.fillMaxWidth().clickable { vm.selectFish(f) }
                            .padding(horizontal = 16.dp, vertical = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(f.name, color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 15.sp,
                                modifier = Modifier.weight(1f))
                            Text("Lv " + f.levelText.ifBlank { f.level.toString() }, color = AccentGold, fontSize = 12.sp)
                        }
                        Text(
                            listOf(f.rank, f.water).filter { it.isNotBlank() }.joinToString("  \u2022  "),
                            color = TextMuted, fontSize = 12.sp, modifier = Modifier.padding(top = 1.dp)
                        )
                    }
                    HorizontalDivider(color = CharcoalDark)
                }
            }
        }
    }
}

// Elemental color for a crystal/affinity label; falls back to gold.
private fun elementColor(el: String): Color = when (el.lowercase()) {
    "fire" -> Color(0xFFD98A7A)
    "ice" -> Color(0xFF9AC6D9)
    "wind" -> Color(0xFF9AD9AE)
    "earth" -> Color(0xFFCBB68A)
    "lightning", "thunder" -> Color(0xFFC9A8D9)
    "water" -> Color(0xFF8AAFD9)
    "light" -> Color(0xFFE6DCB0)
    "dark" -> Color(0xFFB0A6C4)
    "none" -> TextMuted
    else -> AccentGold
}

@Composable
private fun GardeningScreen(vm: MobileWatchViewModel) {
    val all = vm.plantings()
    val db = vm.gardening()
    var query by rememberSaveable { mutableStateOf("") }
    var fSeed by rememberSaveable { mutableStateOf("All") }
    var fCrystal by rememberSaveable { mutableStateOf("All") }
    var fPot by rememberSaveable { mutableStateOf("All") }
    val seeds = remember(all) { all.map { it.seed }.distinct() }
    val crystals = remember(all) { all.map { it.crystal }.distinct() }
    val pots = remember(db) { db?.pots ?: emptyList() }
    val list = all.filter { p ->
        (fSeed == "All" || p.seed == fSeed) &&
        (fCrystal == "All" || p.crystal == fCrystal || p.crystal2 == fCrystal) &&
        (fPot == "All" || fPot in p.potsUsed) &&
        (query.isBlank() || p.seed.contains(query, true) || p.results.any { it.name.contains(query, true) })
    }
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar("Gardening", onBack = { vm.clearHobby() }, actions = {
                if (vm.hobbyInfo("gardening") != null) IconButton(onClick = { vm.openHobbyInfo() }) {
                    Icon(Icons.Filled.Info, "Gardening Info", tint = AccentGold)
                }
            })
        }
    ) { pad ->
        Column(Modifier.padding(pad).fillMaxSize()) {
            OutlinedTextField(
                value = query, onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 4.dp),
                singleLine = true, shape = RoundedCornerShape(12.dp),
                leadingIcon = { Icon(Icons.Filled.Search, null) },
                trailingIcon = {
                    if (query.isNotEmpty()) IconButton(onClick = { query = "" }) {
                        Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                    }
                },
                placeholder = { Text("Search seed or harvest", maxLines = 1) }
            )
            Row(
                Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 2.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                FilterDropdown("Seed", fSeed, seeds, Modifier.weight(1f)) { fSeed = it }
                FilterDropdown("Crystal", fCrystal, crystals, Modifier.weight(1f)) { fCrystal = it }
                FilterDropdown("Pot", fPot, pots, Modifier.weight(1f)) { fPot = it }
            }
            LazyColumn(Modifier.fillMaxSize()) {
                items(list, key = { it.id }) { p ->
                    val matches = if (query.isBlank() || p.seed.contains(query, true)) emptyList()
                        else p.results.filter { it.name.contains(query, true) }.map { it.name }
                    Column(
                        Modifier.fillMaxWidth().clickable { vm.selectPlanting(p) }
                            .padding(horizontal = 16.dp, vertical = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(p.seed, color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 15.sp,
                                modifier = Modifier.weight(1f))
                            Text(
                                p.crystalLabel(),
                                color = elementColor(p.crystal2 ?: p.crystal), fontSize = 12.sp,
                                textAlign = TextAlign.End
                            )
                        }
                        Text(
                            if (matches.isNotEmpty()) matches.joinToString("  \u2022  ")
                            else p.results.joinToString("  \u2022  ") { it.name },
                            color = TextMuted, fontSize = 12.sp, maxLines = 2,
                            overflow = TextOverflow.Ellipsis, modifier = Modifier.padding(top = 1.dp)
                        )
                    }
                    HorizontalDivider(color = CharcoalDark)
                }
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun PlantingScreen(vm: MobileWatchViewModel) {
    val p = vm.ui.selectedPlanting ?: return
    val seed = vm.gardening()?.seed(p.seed)
    // Pots that actually carry a value anywhere in this planting, in canonical order.
    val potOrder = vm.gardening()?.pots ?: emptyList()
    val activePots = potOrder.filter { it in p.potsUsed }
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(p.seed, onBack = { vm.clearPlanting() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                    SectionCard(color = Panel) {
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                            Text(if (p.crystal2 != null) "Crystals" else "Crystal", color = TextMuted, fontSize = 13.sp, modifier = Modifier.weight(1f))
                            Text(p.crystalLabel(),
                                color = elementColor(p.crystal2 ?: p.crystal), fontSize = 13.sp, fontWeight = FontWeight.Medium,
                                textAlign = TextAlign.End)
                        }
                        if (seed != null) {
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text("Plant Type", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(seed.type, color = TextSoft, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text("Affinity", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(seed.affinity, color = elementColor(seed.affinity), fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                        }
                    }
                }
            }
            // One card per harvest result, listing per-pot yields as inline chips.
            items(p.results, key = { it.name }) { r ->
                Column(Modifier.padding(horizontal = 16.dp, vertical = 4.dp)) {
                    SectionCard(color = Panel) {
                        Text(r.name, color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 15.sp,
                            modifier = Modifier.padding(bottom = 6.dp))
                        FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            activePots.forEach { pot ->
                                val v = r.pots[pot]
                                if (v != null) {
                                    Surface(color = Charcoal, shape = RoundedCornerShape(6.dp)) {
                                        Row(Modifier.padding(horizontal = 8.dp, vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                            Text(pot, color = TextMuted, fontSize = 11.sp)
                                            Spacer(Modifier.width(6.dp))
                                            Text(v, color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.Medium)
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun HarvestingScreen(vm: MobileWatchViewModel) {
    val zones = vm.harvestZones()
    var query by rememberSaveable { mutableStateOf("") }
    val shown = if (query.isBlank()) zones else zones.filter { z ->
        z.name.contains(query, true) || z.items.any { it.name.contains(query, true) }
    }
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar("Harvesting", onBack = { vm.clearHobby() }, actions = {
                if (vm.hobbyInfo("harvesting") != null) IconButton(onClick = { vm.openHobbyInfo() }) {
                    Icon(Icons.Filled.Info, "Harvesting Info", tint = AccentGold)
                }
            })
        }
    ) { pad ->
        Column(Modifier.padding(pad).fillMaxSize()) {
            OutlinedTextField(
                value = query, onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 4.dp),
                singleLine = true, shape = RoundedCornerShape(12.dp),
                leadingIcon = { Icon(Icons.Filled.Search, null) },
                trailingIcon = {
                    if (query.isNotEmpty()) IconButton(onClick = { query = "" }) {
                        Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                    }
                },
                placeholder = { Text("Search zones or harvest items", maxLines = 1) }
            )
            LazyColumn(Modifier.fillMaxSize()) {
                items(shown, key = { it.name }) { z ->
                    val matches = if (query.isBlank() || z.name.contains(query, true)) emptyList()
                        else z.items.filter { it.name.contains(query, true) }
                    Column(
                        Modifier.fillMaxWidth().clickable { vm.selectHarvestZone(z) }
                            .padding(horizontal = 16.dp, vertical = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(z.name, color = TextSoft, fontWeight = FontWeight.Medium,
                                fontSize = 15.sp, modifier = Modifier.weight(1f))
                            Text("${z.items.size} items", color = TextMuted, fontSize = 12.sp)
                        }
                        if (matches.isNotEmpty()) {
                            Row {
                                matches.take(4).forEachIndexed { i, m ->
                                    Text((if (i > 0) "  " else "") + m.name, color = digRarityColor(m.rarity), fontSize = 12.sp)
                                }
                                if (matches.size > 4) Text("  +${matches.size - 4}", color = TextMuted, fontSize = 12.sp)
                            }
                        }
                    }
                    HorizontalDivider(color = CharcoalDark)
                }
            }
        }
    }
}

@Composable
private fun HarvestZoneScreen(vm: MobileWatchViewModel) {
    val z = vm.ui.selectedHarvestZone ?: return
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(z.name, onBack = { vm.clearHarvestZone() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                    SectionCard(color = Panel) {
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text("Harvest Items", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                            Text("${z.items.size} items", color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                        }
                        z.items.forEachIndexed { i, h ->
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text(h.name, color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                if (h.rarity.isNotBlank()) Text(h.rarity, color = digRarityColor(h.rarity),
                                    fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun MiningScreen(vm: MobileWatchViewModel) {
    val zones = vm.mineZones()
    var query by rememberSaveable { mutableStateOf("") }
    val shown = if (query.isBlank()) zones else zones.filter { z ->
        z.name.contains(query, true) || z.items.any { it.name.contains(query, true) }
    }
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar("Mining", onBack = { vm.clearHobby() }, actions = {
                if (vm.hobbyInfo("mining") != null) IconButton(onClick = { vm.openHobbyInfo() }) {
                    Icon(Icons.Filled.Info, "Mining Info", tint = AccentGold)
                }
            })
        }
    ) { pad ->
        Column(Modifier.padding(pad).fillMaxSize()) {
            OutlinedTextField(
                value = query, onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 4.dp),
                singleLine = true, shape = RoundedCornerShape(12.dp),
                leadingIcon = { Icon(Icons.Filled.Search, null) },
                trailingIcon = {
                    if (query.isNotEmpty()) IconButton(onClick = { query = "" }) {
                        Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                    }
                },
                placeholder = { Text("Search zones or mining items", maxLines = 1) }
            )
            LazyColumn(Modifier.fillMaxSize()) {
                items(shown, key = { it.name }) { z ->
                    val matches = if (query.isBlank() || z.name.contains(query, true)) emptyList()
                        else z.items.filter { it.name.contains(query, true) }
                    Column(
                        Modifier.fillMaxWidth().clickable { vm.selectMineZone(z) }
                            .padding(horizontal = 16.dp, vertical = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(z.name, color = TextSoft, fontWeight = FontWeight.Medium,
                                fontSize = 15.sp, modifier = Modifier.weight(1f))
                            Text("${z.items.size} items", color = TextMuted, fontSize = 12.sp)
                        }
                        if (matches.isNotEmpty()) {
                            Row {
                                matches.take(4).forEachIndexed { i, m ->
                                    Text((if (i > 0) "  " else "") + m.name, color = digRarityColor(m.rarity), fontSize = 12.sp)
                                }
                                if (matches.size > 4) Text("  +${matches.size - 4}", color = TextMuted, fontSize = 12.sp)
                            }
                        }
                    }
                    HorizontalDivider(color = CharcoalDark)
                }
            }
        }
    }
}

@Composable
private fun MineZoneScreen(vm: MobileWatchViewModel) {
    val z = vm.ui.selectedMineZone ?: return
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(z.name, onBack = { vm.clearMineZone() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                    SectionCard(color = Panel) {
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text("Mining Items", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                            Text("${z.items.size} items", color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                        }
                        z.items.forEachIndexed { i, h ->
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text(h.name, color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                if (h.rarity.isNotBlank()) Text(h.rarity, color = digRarityColor(h.rarity),
                                    fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun ExcavationScreen(vm: MobileWatchViewModel) {
    val zones = vm.excZones()
    var query by rememberSaveable { mutableStateOf("") }
    val shown = if (query.isBlank()) zones else zones.filter { z ->
        z.name.contains(query, true) || z.items.any { it.name.contains(query, true) }
    }
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar("Excavation", onBack = { vm.clearHobby() }, actions = {
                if (vm.hobbyInfo("excavation") != null) IconButton(onClick = { vm.openHobbyInfo() }) {
                    Icon(Icons.Filled.Info, "Excavation Info", tint = AccentGold)
                }
            })
        }
    ) { pad ->
        Column(Modifier.padding(pad).fillMaxSize()) {
            OutlinedTextField(
                value = query, onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 4.dp),
                singleLine = true, shape = RoundedCornerShape(12.dp),
                leadingIcon = { Icon(Icons.Filled.Search, null) },
                trailingIcon = {
                    if (query.isNotEmpty()) IconButton(onClick = { query = "" }) {
                        Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                    }
                },
                placeholder = { Text("Search zones or excavation items", maxLines = 1) }
            )
            LazyColumn(Modifier.fillMaxSize()) {
                items(shown, key = { it.name }) { z ->
                    val matches = if (query.isBlank() || z.name.contains(query, true)) emptyList()
                        else z.items.filter { it.name.contains(query, true) }
                    Column(
                        Modifier.fillMaxWidth().clickable { vm.selectExcZone(z) }
                            .padding(horizontal = 16.dp, vertical = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(z.name, color = TextSoft, fontWeight = FontWeight.Medium,
                                fontSize = 15.sp, modifier = Modifier.weight(1f))
                            Text("${z.items.size} items", color = TextMuted, fontSize = 12.sp)
                        }
                        if (matches.isNotEmpty()) {
                            Row {
                                matches.take(4).forEachIndexed { i, m ->
                                    Text((if (i > 0) "  " else "") + m.name, color = digRarityColor(m.rarity), fontSize = 12.sp)
                                }
                                if (matches.size > 4) Text("  +${matches.size - 4}", color = TextMuted, fontSize = 12.sp)
                            }
                        }
                    }
                    HorizontalDivider(color = CharcoalDark)
                }
            }
        }
    }
}

@Composable
private fun ExcZoneScreen(vm: MobileWatchViewModel) {
    val z = vm.ui.selectedExcZone ?: return
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(z.name, onBack = { vm.clearExcZone() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                    SectionCard(color = Panel) {
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text("Excavation Items", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                            Text("${z.items.size} items", color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                        }
                        z.items.forEachIndexed { i, h ->
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text(h.name, color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                if (h.rarity.isNotBlank()) Text(h.rarity, color = digRarityColor(h.rarity),
                                    fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun LoggingScreen(vm: MobileWatchViewModel) {
    val zones = vm.logZones()
    var query by rememberSaveable { mutableStateOf("") }
    val shown = if (query.isBlank()) zones else zones.filter { z ->
        z.name.contains(query, true) || z.items.any { it.name.contains(query, true) }
    }
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar("Logging", onBack = { vm.clearHobby() }, actions = {
                if (vm.hobbyInfo("logging") != null) IconButton(onClick = { vm.openHobbyInfo() }) {
                    Icon(Icons.Filled.Info, "Logging Info", tint = AccentGold)
                }
            })
        }
    ) { pad ->
        Column(Modifier.padding(pad).fillMaxSize()) {
            OutlinedTextField(
                value = query, onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 4.dp),
                singleLine = true, shape = RoundedCornerShape(12.dp),
                leadingIcon = { Icon(Icons.Filled.Search, null) },
                trailingIcon = {
                    if (query.isNotEmpty()) IconButton(onClick = { query = "" }) {
                        Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                    }
                },
                placeholder = { Text("Search zones or logging items", maxLines = 1) }
            )
            LazyColumn(Modifier.fillMaxSize()) {
                items(shown, key = { it.name }) { z ->
                    val matches = if (query.isBlank() || z.name.contains(query, true)) emptyList()
                        else z.items.filter { it.name.contains(query, true) }
                    Column(
                        Modifier.fillMaxWidth().clickable { vm.selectLogZone(z) }
                            .padding(horizontal = 16.dp, vertical = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(z.name, color = TextSoft, fontWeight = FontWeight.Medium,
                                fontSize = 15.sp, modifier = Modifier.weight(1f))
                            Text("${z.items.size} items", color = TextMuted, fontSize = 12.sp)
                        }
                        if (matches.isNotEmpty()) {
                            Row {
                                matches.take(4).forEachIndexed { i, m ->
                                    Text((if (i > 0) "  " else "") + m.name, color = digRarityColor(m.rarity), fontSize = 12.sp)
                                }
                                if (matches.size > 4) Text("  +${matches.size - 4}", color = TextMuted, fontSize = 12.sp)
                            }
                        }
                    }
                    HorizontalDivider(color = CharcoalDark)
                }
            }
        }
    }
}

@Composable
private fun LogZoneScreen(vm: MobileWatchViewModel) {
    val z = vm.ui.selectedLogZone ?: return
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(z.name, onBack = { vm.clearLogZone() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                    SectionCard(color = Panel) {
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text("Logging Items", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                            Text("${z.items.size} items", color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                        }
                        z.items.forEachIndexed { i, h ->
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text(h.name, color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                if (h.rarity.isNotBlank()) Text(h.rarity, color = digRarityColor(h.rarity),
                                    fontSize = 11.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

private fun digRarityColor(r: String): Color = when (r.uppercase().trimEnd('-')) {
    "VC", "C" -> TextMuted
    "U" -> TextSoft
    "R" -> TextPrimary
    "VR" -> AccentGreen
    "SR" -> AccentGold
    else -> TextMuted
}

@Composable
private fun DiggingScreen(vm: MobileWatchViewModel) {
    val zones = vm.digZones()
    var query by rememberSaveable { mutableStateOf("") }
    val shown = if (query.isBlank()) zones else zones.filter { z ->
        z.name.contains(query, true) || z.all.any { it.name.contains(query, true) }
    }
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar("Chocobo Digging", onBack = { vm.clearHobby() }, actions = {
                if (vm.hobbyInfo("digging") != null) IconButton(onClick = { vm.openHobbyInfo() }) {
                    Icon(Icons.Filled.Info, "Digging Info", tint = AccentGold)
                }
            })
        }
    ) { pad ->
        Column(Modifier.padding(pad).fillMaxSize()) {
            OutlinedTextField(
                value = query, onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 4.dp),
                singleLine = true, shape = RoundedCornerShape(12.dp),
                leadingIcon = { Icon(Icons.Filled.Search, null) },
                trailingIcon = {
                    if (query.isNotEmpty()) IconButton(onClick = { query = "" }) {
                        Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                    }
                },
                placeholder = { Text("Search zones or dig items", maxLines = 1) }
            )
            LazyColumn(Modifier.fillMaxSize()) {
                items(shown, key = { it.name }) { z ->
                    val matches = if (query.isBlank() || z.name.contains(query, true)) emptyList()
                        else z.all.filter { it.name.contains(query, true) }
                    Column(
                        Modifier.fillMaxWidth().clickable { vm.selectDigZone(z) }
                            .padding(horizontal = 16.dp, vertical = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(z.name, color = TextSoft, fontWeight = FontWeight.Medium,
                                fontSize = 15.sp, modifier = Modifier.weight(1f))
                            Text("${z.all.size} items", color = TextMuted, fontSize = 12.sp)
                        }
                        if (matches.isNotEmpty()) {
                            Row {
                                matches.take(4).forEachIndexed { i, m ->
                                    Text((if (i > 0) "  " else "") + m.name, color = digRarityColor(m.rarity), fontSize = 12.sp)
                                }
                                if (matches.size > 4) Text("  +${matches.size - 4}", color = TextMuted, fontSize = 12.sp)
                            }
                        }
                    }
                    HorizontalDivider(color = CharcoalDark)
                }
            }
        }
    }
}

@Composable
private fun DigZoneScreen(vm: MobileWatchViewModel) {
    val z = vm.ui.selectedDigZone ?: return
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(z.name, onBack = { vm.clearDigZone() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                    SectionCard(color = Panel) {
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text("Dig Pool", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                            Text("${z.all.size} items", color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                        }
                    }
                }
            }
            val sections = buildList {
                add("Dig Items" to z.items)
                if (z.burrow.isNotEmpty()) add("Burrow Items" to z.burrow)
                if (z.bore.isNotEmpty()) add("Bore Items" to z.bore)
            }
            sections.forEach { (title, list) ->
                item {
                    Column(Modifier.padding(horizontal = 16.dp)) {
                        CollapsibleSection(title) {
                            SectionCard(color = Panel) {
                                list.forEachIndexed { i, d ->
                                    Row(Modifier.fillMaxWidth().padding(vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                                        Text(d.name, color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                        if (d.rarity.isNotBlank()) Text(d.rarity, color = digRarityColor(d.rarity), fontSize = 11.sp, fontWeight = FontWeight.Bold)
                                    }
                                    if (i < list.lastIndex) HorizontalDivider(color = CharcoalDark)
                                }
                            }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

private val CraftKeys = setOf(
    "cooking", "goldsmithing", "alchemy", "bonecraft", "clothcraft",
    "leathercraft", "smithing", "woodworking", "synergy"
)

@Composable
private fun CraftScreen(vm: MobileWatchViewModel, craft: String) {
    val all = vm.recipeList(craft)
    var query by rememberSaveable { mutableStateOf("") }
    var fRank by rememberSaveable { mutableStateOf("All") }
    var fLevel by rememberSaveable { mutableStateOf("All") }
    var fIng by rememberSaveable { mutableStateOf("All") }
    var sortAz by rememberSaveable { mutableStateOf(false) }
    val ranks = remember(all) { all.map { it.rank }.distinct() }
    fun bucket(lv: Int): String = if (lv <= 10) "0-10" else "${(lv - 1) / 10 * 10 + 1}-${(lv - 1) / 10 * 10 + 10}"
    val levels = remember(all) { all.map { bucket(it.level) }.distinct().sortedBy { it.substringBefore('-').toInt() } }
    val ingredients = remember(all) {
        (all.map { it.crystal } + all.flatMap { r -> r.ingredients.map { it.name } })
            .filter { it.isNotBlank() }.distinct().sorted()
    }
    val list = all.filter { r ->
        (query.isBlank() || r.name.contains(query, true) || r.hq.any { it.name.contains(query, true) }) &&
        (fRank == "All" || r.rank == fRank) &&
        (fLevel == "All" || bucket(r.level) == fLevel) &&
        (fIng == "All" || r.crystal == fIng || r.ingredients.any { it.name == fIng })
    }
    val shown = if (sortAz) list.sortedBy { it.name } else list
    val listState = rememberLazyListState()
    var sortNonce by remember { mutableStateOf(0) }
    LaunchedEffect(sortNonce) { if (sortNonce > 0) listState.scrollToItem(0) }
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar(craft.replaceFirstChar { it.uppercase() }, onBack = { vm.clearHobby() }, actions = {
                if (vm.hobbyInfo(craft) != null) IconButton(onClick = { vm.openHobbyInfo() }) {
                    Icon(Icons.Filled.Info, "Guild Info", tint = AccentGold)
                }
            })
        }
    ) { pad ->
        Column(Modifier.padding(pad).fillMaxSize()) {
            OutlinedTextField(
                value = query, onValueChange = { query = it },
                modifier = Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 4.dp),
                singleLine = true, shape = RoundedCornerShape(12.dp),
                leadingIcon = { Icon(Icons.Filled.Search, null) },
                trailingIcon = {
                    if (query.isNotEmpty()) IconButton(onClick = { query = "" }) {
                        Icon(Icons.Filled.Close, "Clear", tint = TextMuted)
                    }
                },
                placeholder = { Text("Search recipes", maxLines = 1) }
            )
            Row(
                Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 2.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                FilterDropdown("Level", fLevel, levels, Modifier.weight(1f)) { fLevel = it }
                FilterDropdown("Rank", fRank, ranks, Modifier.weight(1f)) { fRank = it }
            }
            Row(
                Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 2.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                FilterDropdown("Ingredient", fIng, ingredients, Modifier.weight(2f)) { fIng = it }
                Surface(color = Panel, shape = RoundedCornerShape(8.dp), modifier = Modifier.weight(1f)) {
                    Row(
                        Modifier.fillMaxWidth().clickable { sortAz = !sortAz; sortNonce++ }.padding(horizontal = 10.dp, vertical = 8.dp),
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center
                    ) {
                        Text(if (sortAz) "A-Z" else "By Level",
                            color = if (sortAz) AccentGreen else TextMuted, fontSize = 12.sp, maxLines = 1)
                    }
                }
            }
            LazyColumn(Modifier.fillMaxSize(), state = listState) {
                items(shown, key = { it.id }) { r ->
                    Column(
                        Modifier.fillMaxWidth().clickable { vm.selectRecipe(r) }
                            .padding(horizontal = 16.dp, vertical = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(if (r.nqQty > 1) "${r.name} x${r.nqQty}" else r.name,
                                color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 15.sp,
                                modifier = Modifier.weight(1f))
                            Text("Lv " + r.levelText.ifBlank { r.level.toString() }, color = AccentGold, fontSize = 12.sp)
                        }
                        Text(
                            listOf(r.rank, r.crystal).filter { it.isNotBlank() }.joinToString("  \u2022  "),
                            color = TextMuted, fontSize = 12.sp, modifier = Modifier.padding(top = 1.dp)
                        )
                    }
                    HorizontalDivider(color = CharcoalDark)
                }
            }
        }
    }
}

@Composable
private fun RecipeDetailScreen(vm: MobileWatchViewModel) {
    val r = vm.ui.selectedRecipe ?: return
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(r.name, onBack = { vm.clearRecipe() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                    SectionCard(color = Panel) {
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text("Level", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                            Text(r.levelText.ifBlank { r.level.toString() }, color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                        }
                        HorizontalDivider(color = CharcoalDark)
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text("Rank", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                            Text(r.rank, color = TextPrimary, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                        }
                        if (r.crystal.isNotBlank()) {
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                Text("Crystal", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(r.crystal, color = TextPrimary, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                        }
                        if (r.sub.isNotBlank()) {
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                Text("Sub Craft", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(r.sub, color = TextPrimary, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                        }
                        if (r.keyItem.isNotBlank()) {
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                Text("Key Item", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(r.keyItem, color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                        }
                    }
                }
            }
            item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Yields") {
                        SectionCard(color = Panel) {
                            Row(Modifier.fillMaxWidth().padding(vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                                Text(if (r.nqQty > 1) "${r.name} x${r.nqQty}" else r.name,
                                    color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                Text("NQ", color = AccentGold, fontSize = 11.sp)
                            }
                            r.hq.forEachIndexed { i, h ->
                                HorizontalDivider(color = CharcoalDark)
                                Row(Modifier.fillMaxWidth().padding(vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                                    Text(if (h.qty > 1) "${h.name} x${h.qty}" else h.name,
                                        color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                    Text("HQ${i + 1}", color = AccentGreen, fontSize = 11.sp)
                                }
                            }
                        }
                    }
                }
            }
            if (r.ingredients.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Ingredients") {
                        SectionCard(color = Panel) {
                            if (r.crystal.isNotBlank()) {
                                Row(Modifier.fillMaxWidth().padding(vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                                    Text(r.crystal, color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                    Text("crystal", color = TextMuted, fontSize = 11.sp)
                                }
                                HorizontalDivider(color = CharcoalDark)
                            }
                            r.ingredients.forEachIndexed { i, g ->
                                Row(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                                    Text(if (g.qty > 1) "${g.name} x${g.qty}" else g.name,
                                        color = TextPrimary, fontSize = 14.sp)
                                }
                                if (i < r.ingredients.lastIndex) HorizontalDivider(color = CharcoalDark)
                            }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun HobbyInfoScreen(vm: MobileWatchViewModel, onBack: (() -> Unit)? = null) {
    val key = vm.ui.selectedHobby ?: return
    val info = vm.hobbyInfo(key) ?: return
    val title = when (key) {
        "raising" -> "Chocobo Breeding"
        "racing" -> "Chocobo Racing"
        "clamming" -> "Clamming"
        "moggarden" -> "Mog Garden"
        "monsterrearing" -> "Monster Rearing"
        "monstrosity" -> "Monstrosity"
        else -> key.replaceFirstChar { it.uppercase() } + " Info"
    }
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(title, onBack = onBack ?: { vm.closeHobbyInfo() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                    SectionCard(color = Panel) {
                        if (info.guild.isNotBlank()) {
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                Text("Guild", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(info.guild, color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                        }
                        if (info.hours.isNotBlank()) {
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                Text("Hours", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(info.hours, color = TextPrimary, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                        }
                        if (info.holiday.isNotBlank()) {
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                Text("Holiday", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(info.holiday, color = TextPrimary, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                        }
                        if (info.enroll.isNotBlank()) {
                            HorizontalDivider(color = CharcoalDark)
                            Text(info.enroll, color = TextPrimary, fontSize = 13.sp,
                                modifier = Modifier.padding(vertical = 6.dp))
                        }
                    }
                }
            }
            if (info.npcs.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Guild NPCs") {
                        info.npcs.forEach { grp ->
                            Text(grp.zone, color = AccentGold, fontSize = 13.sp, fontWeight = FontWeight.Bold,
                                modifier = Modifier.padding(top = 8.dp, bottom = 4.dp))
                            SectionCard(color = Panel) {
                                grp.rows.forEachIndexed { i, n ->
                                    Column(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                                        Row(verticalAlignment = Alignment.CenterVertically) {
                                            Text(n.name, color = JobsBlue, fontWeight = FontWeight.Medium,
                                                fontSize = 14.sp, modifier = Modifier.weight(1f))
                                            Text(n.loc, color = AccentGold, fontSize = 12.sp)
                                        }
                                        val sub = if (n.zone.isNotBlank() && n.zone != grp.zone)
                                            n.purpose + "  \u2022  " + n.zone else n.purpose
                                        if (sub.isNotBlank()) Text(sub, color = TextMuted, fontSize = 12.sp,
                                            modifier = Modifier.padding(top = 1.dp))
                                    }
                                    if (i < grp.rows.lastIndex) HorizontalDivider(color = CharcoalDark)
                                }
                            }
                        }
                    }
                }
            }
            items(info.items, key = { it.section }) { sec ->
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection(sec.section) {
                        if (sec.note.isNotBlank()) Text(sec.note, color = TextMuted, fontSize = 12.sp,
                            modifier = Modifier.padding(bottom = 4.dp))
                        SectionCard(color = Panel) {
                            sec.rows.forEachIndexed { i, r ->
                                Column(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                                    Text(r.name, color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 14.sp)
                                    if (r.bonus.isNotBlank()) Text(r.bonus, color = TextPrimary, fontSize = 12.sp,
                                        modifier = Modifier.padding(top = 1.dp))
                                    if (r.source.isNotBlank()) Text(r.source, color = TextMuted, fontSize = 12.sp,
                                        modifier = Modifier.padding(top = 1.dp))
                                }
                                if (i < sec.rows.lastIndex) HorizontalDivider(color = CharcoalDark)
                            }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun FishGearRow(g: FishGear, showDivider: Boolean) {
    Row(Modifier.fillMaxWidth().padding(vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
        Text(g.name,
            color = when { g.best -> AccentGreen; g.mayBreak -> AccentRed; else -> TextPrimary },
            fontWeight = if (g.best) FontWeight.Bold else FontWeight.Normal,
            fontSize = 14.sp, modifier = Modifier.weight(1f))
        if (g.mayBreak) Text("may break", color = AccentRed, fontSize = 11.sp)
        if (g.tooSmall) Text("fish may be too small", color = TextMuted, fontSize = 11.sp)
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun FishDetailScreen(vm: MobileWatchViewModel) {
    val f = vm.ui.selectedFish ?: return
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar(f.name, onBack = { vm.clearFish() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            item {
                Column(Modifier.padding(horizontal = 16.dp, vertical = 10.dp)) {
                    SectionCard(color = Panel) {
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text("Level", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                            Text(f.levelText.ifBlank { f.level.toString() }, color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                        }
                        HorizontalDivider(color = CharcoalDark)
                        Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                            Text("Rank", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                            Text(f.rank, color = TextPrimary, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                        }
                        if (f.water.isNotBlank()) {
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                Text("Type", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(f.water, color = TextPrimary, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                        }
                        if (f.keyItem.isNotBlank()) {
                            HorizontalDivider(color = CharcoalDark)
                            Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                Text("Key Item", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 88.dp))
                                Text(f.keyItem, color = AccentGold, fontSize = 13.sp, textAlign = TextAlign.End, modifier = Modifier.weight(1f))
                            }
                        }
                    }
                }
            }
            if (f.zones.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Areas") {
                        SectionCard(color = Panel) {
                            f.zones.forEachIndexed { i, z ->
                                Column(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                                    Text(z.name, color = if (z.best) AccentGreen else TextPrimary,
                                        fontWeight = if (z.best) FontWeight.Bold else FontWeight.Normal, fontSize = 14.sp)
                                    if (z.note.isNotBlank()) Text(z.note, color = TextMuted, fontSize = 12.sp,
                                        modifier = Modifier.padding(top = 1.dp))
                                }
                                if (i < f.zones.lastIndex) HorizontalDivider(color = CharcoalDark)
                            }
                        }
                    }
                }
            }
            if (f.rods.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Rods") {
                        SectionCard(color = Panel) {
                            f.rods.forEachIndexed { i, g -> FishGearRow(g, i < f.rods.lastIndex) }
                        }
                    }
                }
            }
            if (f.baits.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Bait") {
                        SectionCard(color = Panel) {
                            f.baits.forEachIndexed { i, g -> FishGearRow(g, i < f.baits.lastIndex) }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun ZoneReiveRow(reive: ZoneReive, showDivider: Boolean) {
    val ctx = LocalContext.current
    Column(
        Modifier.fillMaxWidth().clickable {
            val u = "https://www.bg-wiki.com/ffxi/" + reive.name.replace(" ", "_")
            runCatching { ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(u))) }
        }.padding(vertical = 7.dp)
    ) {
        Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
            Text(reive.name, color = JobsBlue, fontWeight = FontWeight.Medium, fontSize = 14.sp, modifier = Modifier.weight(1f))
            if (reive.ki.isNotEmpty()) Text("KI: " + reive.ki, color = AccentGold, fontSize = 13.sp)
        }
        if (reive.loc.isNotEmpty()) Text(reive.loc, color = TextSoft, fontSize = 12.sp, modifier = Modifier.padding(top = 1.dp))
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun ZoneDetailScreen(vm: MobileWatchViewModel) {
    val zone = vm.ui.selectedZone ?: return
    val info = vm.zoneInfo(zone.slug)
    Scaffold(containerColor = Charcoal, topBar = { GradientTopBar(zone.name, onBack = { vm.back() }) }) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            if (info != null && info.banner.isNotEmpty()) item { ZoneBanner(info.banner) }
            item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    Spacer(Modifier.height(10.dp))
                    WikiLinks(zone.name)
                    if (!info?.continent.isNullOrEmpty()) InfoRow("Continent", listOf(info!!.continent), AccentGold)
                    if (!info?.regionOverride.isNullOrEmpty()) InfoRow("Region", listOf(info!!.regionOverride), AccentGold)
                    else if (zone.region.isNotEmpty()) InfoRow("Region", listOf(zone.region), AccentGold)
                    if (!info?.type.isNullOrEmpty()) InfoRow("Zone", listOf(info!!.type), AccentGold)
                    if (!info?.weatherOverride.isNullOrEmpty()) InfoRow("Weather", listOf(info!!.weatherOverride), JobsBlue)
                    else InfoRow("Weather", zone.weather, JobsBlue)
                    if (!info?.footprint.isNullOrEmpty()) InfoRow("Goblin Footprint", listOf(info!!.footprint), AccentGold)
                    if (!info?.apparatus.isNullOrEmpty()) InfoRow("Strange Apparatus", listOf(info!!.apparatus), AccentGold)
                    Spacer(Modifier.height(12.dp))
                    if (info?.nomap != true) Button(
                        onClick = { vm.openMap() },
                        colors = ButtonDefaults.buttonColors(containerColor = Selection, contentColor = TextPrimary)
                    ) { Icon(Icons.Filled.Place, null); Spacer(Modifier.width(8.dp)); Text("View Map") }
                    if (info != null && info.connects.isNotEmpty()) {
                        Spacer(Modifier.height(6.dp))
                        var czExpanded by remember { mutableStateOf(false) }
                        Box {
                            OutlinedButton(
                                onClick = { czExpanded = true }, shape = RoundedCornerShape(10.dp),
                                colors = ButtonDefaults.outlinedButtonColors(contentColor = TextSoft)
                            ) {
                                Text("Connected Zones", fontSize = 13.sp)
                                Icon(Icons.Filled.ArrowDropDown, null)
                            }
                            DropdownMenu(expanded = czExpanded, onDismissRequest = { czExpanded = false }) {
                                info.connects.forEach { cz ->
                                    DropdownMenuItem(
                                        text = { Text(cz, color = TextSoft, fontSize = 14.sp) },
                                        onClick = { czExpanded = false; vm.selectZoneByName(cz) }
                                    )
                                }
                            }
                        }
                    }
                }
            }
            if (info != null && info.travel.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Travel") {
                        SectionCard(color = Panel) {
                            info.travel.forEachIndexed { i, tp ->
                                Row(
                                    Modifier.fillMaxWidth().padding(vertical = 6.dp),
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(tp.name, color = TextSoft, fontSize = 14.sp, modifier = Modifier.weight(1f))
                                    if (tp.coord.isNotEmpty()) Text(tp.coord, color = AccentGreen, fontSize = 13.sp)
                                }
                                if (i < info.travel.lastIndex) HorizontalDivider(color = CharcoalDark)
                            }
                        }
                    }
                }
            }
            if (info != null && info.transport.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Transportation") {
                        SectionCard(color = Panel) {
                            info.transport.forEachIndexed { ti, tr ->
                                Text(tr.name, color = AccentGold, fontWeight = FontWeight.SemiBold, fontSize = 14.sp,
                                    modifier = Modifier.padding(vertical = 4.dp))
                                Row(Modifier.fillMaxWidth().padding(vertical = 2.dp)) {
                                    Text("Boarding", color = TextMuted, fontSize = 12.sp, maxLines = 1, softWrap = false, modifier = Modifier.weight(1f))
                                    Text("Departure", color = TextMuted, fontSize = 12.sp, maxLines = 1, softWrap = false, modifier = Modifier.weight(1f))
                                    Text("Arrival", color = TextMuted, fontSize = 12.sp, maxLines = 1, softWrap = false, modifier = Modifier.weight(1f))
                                }
                                tr.rows.forEach { r ->
                                    Row(Modifier.fillMaxWidth().padding(vertical = 3.dp)) {
                                        Text(r.board, color = TextSoft, fontSize = 13.sp, modifier = Modifier.weight(1f))
                                        Text(r.depart, color = AccentGreen, fontSize = 13.sp, modifier = Modifier.weight(1f))
                                        Text(r.arrive, color = TextSoft, fontSize = 13.sp, modifier = Modifier.weight(1f))
                                    }
                                }
                                if (ti < info.transport.lastIndex) HorizontalDivider(color = CharcoalDark, modifier = Modifier.padding(vertical = 6.dp))
                            }
                        }
                    }
                }
            }
            if (info != null && info.battlefields.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Battlefields") {
                        SectionCard(color = Panel) {
                            info.battlefields.forEachIndexed { i, b -> ZoneBattleRow(b, i < info.battlefields.lastIndex) }
                        }
                    }
                }
            }
            if (info != null && info.reives.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Reives") {
                        SectionCard(color = Panel) {
                            info.reives.forEachIndexed { i, r -> ZoneReiveRow(r, i < info.reives.lastIndex) }
                        }
                    }
                }
            }
            if (info != null && info.quests.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Quests") {
                        SectionCard(color = Panel) {
                            info.quests.forEachIndexed { i, q -> ZoneQuestRow(q, i < info.quests.lastIndex) }
                        }
                    }
                }
            }
            if (info != null && info.assaults.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Assault Missions") {
                        SectionCard(color = Panel) {
                            info.assaults.forEachIndexed { i, a -> ZoneAssaultRow(a, i < info.assaults.lastIndex) }
                        }
                    }
                }
            }
            if (info != null && info.nms.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Notorious Monsters") {
                        SectionCard(color = Panel) {
                            info.nms.forEachIndexed { i, nm -> ZoneNmRow(vm, nm, i < info.nms.lastIndex) }
                        }
                    }
                }
            }
            if (info != null && info.geasfete.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Geas Fete") {
                        SectionCard(color = Panel) {
                            info.geasfete.forEachIndexed { gi, g ->
                                Text(
                                    g.title, color = AccentGold, fontWeight = FontWeight.Bold, fontSize = 13.sp,
                                    modifier = Modifier.padding(top = if (gi == 0) 0.dp else 10.dp, bottom = 2.dp)
                                )
                                g.rows.forEachIndexed { i, nm -> ZoneNmRow(vm, nm, i < g.rows.lastIndex) }
                            }
                        }
                    }
                }
            }
            if (info != null && info.mobs.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Mobs") {
                        SectionCard(color = Panel) {
                            info.mobs.forEachIndexed { i, zm -> ZoneMobRow(vm, zm, i < info.mobs.lastIndex) }
                        }
                    }
                }
            }
            if (info != null && info.procs.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Stagger Procs") {
                        SectionCard(color = Panel) {
                            info.procs.forEachIndexed { i, p -> ZoneProcRowView(p, i < info.procs.lastIndex) }
                        }
                    }
                }
            }
            if (info != null && info.notes.isNotEmpty()) item {
                Column(Modifier.padding(horizontal = 16.dp)) {
                    CollapsibleSection("Notes") {
                        SectionCard(color = Panel) {
                            info.notes.forEachIndexed { i, n ->
                                Row(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                                    Text("•", color = AccentGold, fontSize = 14.sp,
                                        modifier = Modifier.padding(end = 8.dp))
                                    Text(n, color = TextSoft, fontSize = 14.sp,
                                        modifier = Modifier.weight(1f))
                                }
                                if (i < info.notes.lastIndex) HorizontalDivider(color = CharcoalDark)
                            }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}
@Composable
private fun MapViewerScreen(vm: MobileWatchViewModel) {
    val zone = vm.ui.selectedZone ?: return
    val ctx = LocalContext.current
    var loading by remember(zone.slug) { mutableStateOf(true) }
    var maps by remember(zone.slug) { mutableStateOf<List<ImageBitmap>>(emptyList()) }
    LaunchedEffect(zone.slug) {
        loading = true
        maps = withContext(Dispatchers.IO) { MapLoader.loadAll(ctx, zone.id) }
        loading = false
    }
    val pagerState = rememberPagerState(pageCount = { maps.size })
    val mapId = "%02x_%d".format(zone.id, pagerState.currentPage)
    Scaffold(
        containerColor = Charcoal,
        topBar = {
            GradientTopBar(zone.name, onBack = { vm.closeMap() },
                trailing = if (maps.isNotEmpty()) "[$mapId]" else null)
        }
    ) { pad ->
        Box(Modifier.padding(pad).fillMaxSize(), contentAlignment = Alignment.Center) {
            when {
                loading -> CircularProgressIndicator(color = AccentGreen)
                maps.isEmpty() -> Column(
                    Modifier.padding(28.dp), horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text("Map not available", color = TextPrimary, fontWeight = FontWeight.Bold)
                    Spacer(Modifier.height(8.dp))
                    Text("Expected \"%02x_0.png\" (zone id in hex).".format(zone.id),
                        color = TextMuted, fontSize = 13.sp)
                    Spacer(Modifier.height(4.dp))
                    Text("Drop the map pack in assets/maps/ or host it at BASE_URL.",
                        color = TextMuted, fontSize = 12.sp)
                }
                else -> {
                    var zoomedIn by remember { mutableStateOf(false) }
                    LaunchedEffect(pagerState.currentPage) { zoomedIn = false }
                    Column(Modifier.fillMaxSize()) {
                        HorizontalPager(
                            state = pagerState,
                            userScrollEnabled = !zoomedIn,
                            modifier = Modifier.weight(1f)
                        ) { page ->
                            ZoomableImage(maps[page]) { z ->
                                if (page == pagerState.currentPage) zoomedIn = z
                            }
                        }
                        if (maps.size > 1) {
                            Text(
                                "Map ${pagerState.currentPage + 1} / ${maps.size}   \u2014   swipe to change",
                                color = TextMuted, fontSize = 12.sp,
                                modifier = Modifier.align(Alignment.CenterHorizontally).padding(8.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ZoomableImage(image: ImageBitmap, onZoomChange: (Boolean) -> Unit = {}) {
    var scale by remember { mutableStateOf(1f) }
    var offset by remember { mutableStateOf(Offset.Zero) }
    Box(
        Modifier.fillMaxSize().clipToBounds().pointerInput(Unit) {
            awaitEachGesture {
                awaitFirstDown(requireUnconsumed = false)
                do {
                    val event = awaitPointerEvent()
                    val pressedCount = event.changes.count { it.pressed }
                    // Only handle (and consume) when pinching or already zoomed; otherwise let
                    // single-finger drags fall through to the pager for swiping between maps.
                    if (pressedCount >= 2 || scale > 1f) {
                        scale = (scale * event.calculateZoom()).coerceIn(1f, 6f)
                        offset = if (scale > 1f) offset + event.calculatePan() else Offset.Zero
                        onZoomChange(scale > 1.05f)
                        event.changes.forEach { if (it.positionChanged()) it.consume() }
                    }
                } while (event.changes.any { it.pressed })
            }
        }
    ) {
        Image(
            image, "map",
            modifier = Modifier.fillMaxSize().graphicsLayer(
                scaleX = scale, scaleY = scale, translationX = offset.x, translationY = offset.y
            ),
            contentScale = ContentScale.Fit
        )
    }
}

private fun scColor(prop: String): Color = when (prop) {
    "Light", "Radiance", "Transfixion" -> Color(0xFFEDEDED)
    "Darkness", "Umbra", "Compression" -> Color(0xFFB89AE0)
    "Gravitation" -> Color(0xFFC29A6B)
    "Fragmentation" -> Color(0xFFF0A0DC)
    "Fusion" -> Color(0xFFE59A7A)
    "Liquefaction" -> Color(0xFFE38A6A)
    "Distortion" -> Color(0xFF7FB0DC)
    "Reverberation" -> Color(0xFF6FA8DC)
    "Induration" -> Color(0xFF9BD3E0)
    "Scission" -> Color(0xFFCBB57C)
    "Detonation" -> Color(0xFF9AD39A)
    "Impaction" -> Color(0xFFD98AD9)
    else -> TextSoft
}

@Composable
private fun PropsLine(props: List<String>, aeonic: String? = null) {
    Text(
        buildAnnotatedString {
            props.forEachIndexed { i, p ->
                if (i > 0) withStyle(SpanStyle(color = TextMuted)) { append("  ") }
                withStyle(SpanStyle(color = scColor(p))) { append(p) }
            }
            if (aeonic != null) {
                withStyle(SpanStyle(color = TextMuted)) { append("   \u00b7 aeonic ") }
                withStyle(SpanStyle(color = scColor(aeonic))) { append(aeonic) }
            }
        },
        fontSize = 11.sp
    )
}

@Composable
private fun WsNameRow(ws: WeaponSkill) {
    Column(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
        Text(ws.name, color = TextPrimary, fontWeight = FontWeight.Bold, fontSize = 15.sp)
        PropsLine(ws.props, ws.aeonic)
    }
}

@Composable
private fun DownArrow() {
    Text("\u2193", color = TextMuted, fontSize = 18.sp, modifier = Modifier.padding(start = 8.dp, top = 2.dp, bottom = 2.dp))
}

@Composable
private fun ScLink(st: SkillchainResult?) {
    Row(Modifier.fillMaxWidth().padding(vertical = 2.dp), verticalAlignment = Alignment.CenterVertically) {
        Text("\u2193", color = TextMuted, fontSize = 18.sp, modifier = Modifier.padding(start = 8.dp, end = 12.dp))
        if (st != null) {
            Surface(color = Selection, shape = RoundedCornerShape(8.dp)) {
                Column(Modifier.padding(horizontal = 12.dp, vertical = 6.dp)) {
                    Text("${st.name.uppercase()}  [Lv ${st.level}]", color = scColor(st.name),
                        fontWeight = FontWeight.Bold, fontSize = 14.sp)
                    if (st.elements.isNotEmpty())
                        Text("burst: ${st.elements.joinToString(", ")}", color = TextMuted, fontSize = 11.sp)
                }
            }
        }
    }
}

@Composable
private fun SlotSelector(vm: MobileWatchViewModel) {
    var open by remember { mutableStateOf(false) }
    var pickedType by remember { mutableStateOf<String?>(null) }
    Box(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
        Surface(
            color = Panel, shape = RoundedCornerShape(8.dp),
            modifier = Modifier.fillMaxWidth().clickable { open = true; pickedType = null }
        ) {
            Row(Modifier.padding(horizontal = 12.dp, vertical = 14.dp), verticalAlignment = Alignment.CenterVertically) {
                Text("Select a WS", color = TextMuted, fontSize = 14.sp, maxLines = 1, softWrap = false, modifier = Modifier.weight(1f))
                Icon(Icons.Filled.ArrowDropDown, null, tint = TextMuted)
            }
        }
        DropdownMenu(
            expanded = open, onDismissRequest = { open = false; pickedType = null },
            modifier = Modifier.heightIn(max = 440.dp)
        ) {
            val type = pickedType
            if (type == null) {
                vm.slotTypes().forEach { t ->
                    DropdownMenuItem(text = { Text(t, color = TextPrimary, fontSize = 14.sp) }, onClick = { pickedType = t })
                }
            } else {
                DropdownMenuItem(
                    text = { Text("\u2190  weapons", color = TextMuted, fontSize = 13.sp) },
                    onClick = { pickedType = null }
                )
                HorizontalDivider(color = CharcoalDark)
                vm.slotWsOf(type).forEach { w ->
                    DropdownMenuItem(
                        text = {
                            Column {
                                Text(w.name, color = TextPrimary, fontWeight = FontWeight.Medium, fontSize = 14.sp)
                                PropsLine(w.props, w.aeonic)
                            }
                        },
                        onClick = { open = false; pickedType = null; vm.scAddWs(w) }
                    )
                }
            }
        }
    }
}

@Composable
private fun SkillchainContent(vm: MobileWatchViewModel) {
    val chain = vm.ui.scChain
    val steps = vm.scSteps()
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 16.dp)) {
        Spacer(Modifier.height(12.dp))
        // The reference list sits above the builder: "what can this weapon do" before
        // "what chains into what".
        TopLevelRow("Weapon Skills", subtitle = "every weapon skill, by weapon", insetDp = 0) {
            vm.openWsList()
        }
        Spacer(Modifier.height(14.dp))
        chain.forEachIndexed { i, ws ->
            WsNameRow(ws)
            if (i < chain.lastIndex) ScLink(steps.getOrNull(i))
        }
        val canAdd = vm.scCanContinue() && vm.slotTypes().isNotEmpty()
        if (canAdd) {
            if (chain.isNotEmpty()) DownArrow()
            SlotSelector(vm)
        }
        if (chain.isNotEmpty()) {
            Spacer(Modifier.height(8.dp))
            TextButton(onClick = { vm.clearWs() }) { Text("Reset") }
        }
        Spacer(Modifier.height(24.dp))
    }
}

// =====================  WEAPON SKILL REFERENCE  ============================
// Every player weapon skill, weapon by weapon, in the wiki's own order (skill level,
// then the quest WS, then the REMA tiers). Reached from the top of the Chains tab.
//
// weaponskills.json deliberately stores NO chain properties — the line under each
// name is resolved live out of skillchains.json by name, so the builder and the
// reference can never drift apart. A WS the wiki prints as "No Property" has no
// entry there and says so; Automaton WS have no entry yet and stay silent rather
// than claiming they have none.
//
// Weapons open COLLAPSED: the page is 230 rows and the point is to pick a weapon.

/** "200" -> "Skill 200"; "(245)" -> Automaton's ranged value; anything else is the unlock class. */
private fun wsReqLabel(req: String): String = when {
    req.isBlank() -> ""
    req.all { it.isDigit() } -> "Skill $req"
    req.startsWith("(") && req.endsWith(")") && req.drop(1).dropLast(1).all { it.isDigit() } ->
        "Skill ${req.drop(1).dropLast(1)}  \u00b7  ranged"
    else -> req
}

@Composable
private fun WsRefRow(vm: MobileWatchViewModel, e: WsEntry) {
    val info = remember(e.name) { vm.wsChainInfo(e.name) }
    Column(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 9.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(e.name, color = TextPrimary, fontWeight = FontWeight.Medium, fontSize = 15.sp,
                modifier = Modifier.weight(1f))
            Text(wsReqLabel(e.req), color = AccentGold, fontSize = 12.sp)
        }
        when {
            info != null -> PropsLine(info.props, info.aeonic)
            e.noProp -> Text("No property", color = TextMuted, fontSize = 11.sp)
        }
    }
    HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun WeaponSkillListScreen(vm: MobileWatchViewModel) {
    val weapons = vm.wsWeapons()
    val expanded = rememberSaveable(
        saver = listSaver(
            save = { map -> map.filterValues { it }.keys.toList() },
            restore = { keys -> mutableStateMapOf<String, Boolean>().apply { keys.forEach { put(it, true) } } }
        ),
        // rev 396: keyed on the page visit, exactly like CollapsibleSection, so
        // leaving the tab and coming back opens the list fully collapsed again.
        key = "ws_weapons_${LocalPageVisit.current}"
    ) { mutableStateMapOf<String, Boolean>() }
    Scaffold(
        containerColor = Charcoal,
        topBar = { GradientTopBar("Weapon Skills", onBack = { vm.closeWsList() }) }
    ) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize()) {
            weapons.forEach { wpn ->
                val open = expanded[wpn.type] == true
                item(key = "wgrp:${wpn.type}") {
                    GroupHeader(wpn.type, wpn.ws.size, open) { expanded[wpn.type] = !open }
                }
                if (open) {
                    item(key = "wjobs:${wpn.type}") {
                        Column(Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)) {
                            if (wpn.jobs.isNotEmpty())
                                Text(wpn.jobs.joinToString("   "), color = JobsBlue, fontSize = 11.sp)
                            wpn.note?.let {
                                Text(it, color = TextMuted, fontSize = 11.sp, modifier = Modifier.padding(top = 3.dp))
                            }
                        }
                        HorizontalDivider(color = CharcoalDark)
                    }
                    items(wpn.ws, key = { "${wpn.type}|${it.name}" }) { e -> WsRefRow(vm, e) }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

// ============================  TRUSTS TAB  =================================
// Alter egos grouped by the role their Trust-spell icon carries on BG-wiki
// (Tank / Melee Fighter / Ranged Fighter / Caster / Healer / Support / Special).
// Every role renders even when empty — the empty groups ARE the intake to-do list,
// same principle as the Bestiary's zone view.

/** Trust portrait out of assets/trustart. Same loader shape as SubtypeImage, dark panel behind. */
@Composable
private fun TrustPortrait(path: String?, size: Dp) {
    val ctx = LocalContext.current
    val bmp = remember(path) {
        path?.let { p -> runCatching { ctx.assets.open(p).use { BitmapFactory.decodeStream(it)?.asImageBitmap() } }.getOrNull() }
    }
    Surface(shape = RoundedCornerShape(8.dp), color = Panel, modifier = Modifier.size(size)) {
        if (bmp != null) Image(bmp, null, modifier = Modifier.fillMaxSize(), contentScale = ContentScale.Crop)
    }
}

@Composable
private fun TrustRow(vm: MobileWatchViewModel, t: Trust) {
    Row(
        Modifier.fillMaxWidth().clickable { vm.selectTrust(t.name) }
            .padding(horizontal = 16.dp, vertical = 10.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        TrustPortrait(t.image, 44.dp)
        Spacer(Modifier.width(12.dp))
        Column(Modifier.weight(1f)) {
            Text(t.name, color = TextSoft, fontWeight = FontWeight.Medium, fontSize = 16.sp)
            if (t.job.isNotBlank()) Text(t.job, color = TextMuted, fontSize = 11.sp)
        }
    }
    HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun TrustsContent(vm: MobileWatchViewModel) {
    val roles = vm.trustRoles()
    val expanded = rememberSaveable(
        saver = listSaver(
            save = { map -> map.filterValues { it }.keys.toList() },
            restore = { keys -> mutableStateMapOf<String, Boolean>().apply { keys.forEach { put(it, true) } } }
        ),
        // rev 396: keyed on the page visit, exactly like CollapsibleSection, so
        // leaving the tab and coming back opens the list fully collapsed again.
        key = "trust_roles_${LocalPageVisit.current}"
    ) { mutableStateMapOf<String, Boolean>() }
    val rosterOpen = rememberSaveable(key = "trust_roster_${LocalPageVisit.current}") { mutableStateOf(false) }
    val info = vm.trustInfo()
    LazyColumn(Modifier.fillMaxSize()) {
        // The general reference sections sit above the roster, all collapsed. They are pure
        // data (trusts.json "info"), so another section needs no Kotlin.
        if (info.isNotEmpty()) item(key = "tinfo") {
            Column(Modifier.fillMaxWidth().padding(horizontal = 16.dp)) {
                info.forEach { sec -> TrustBulletSection(sec.title, sec.lines) }
                Spacer(Modifier.height(14.dp))
            }
        }
        // The whole roster lives under ONE top-level section, collapsed by default, so the tab
        // opens on the reference sections rather than seven role headers. Roles drop to level 2
        // (SubGroupHeader / HeaderL2) underneath it. Kept lazy on purpose — 122 rows.
        item(key = "troster") {
            SectionToggleRow("Alter Egos", rosterOpen.value, vm.trustCount()) {
                rosterOpen.value = !rosterOpen.value
            }
        }
        if (rosterOpen.value) roles.forEach { role ->
            val list = vm.trustsOf(role)
            val open = expanded[role] == true
            item(key = "trole:$role") {
                SubGroupHeader(role, list.size, 1, open) { expanded[role] = !open }
            }
            if (open) {
                if (list.isEmpty()) item(key = "tempty:$role") {
                    Text("Not filled in yet", color = TextMuted, fontSize = 13.sp,
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp))
                    HorizontalDivider(color = CharcoalDark)
                }
                items(list, key = { "$role|${it.name}" }) { t -> TrustRow(vm, t) }
            }
        }
        item { Spacer(Modifier.height(24.dp)) }
    }
}

/** One bullet; indent comes from the line's own leading spaces (2 per level). */
@Composable
private fun TrustBullet(line: String) {
    val indent = (line.takeWhile { it == ' ' }.length / 2).coerceIn(0, 3)
    Row(Modifier.fillMaxWidth().padding(start = (indent * 12).dp, top = 3.dp, bottom = 3.dp)) {
        Text("\u2022", color = TextMuted, fontSize = 13.sp, modifier = Modifier.padding(end = 6.dp))
        Text(line.trim(), color = TextSoft, fontSize = 13.sp)
    }
}

@Composable
private fun TrustBulletSection(title: String, lines: List<String>) {
    if (lines.isEmpty()) return
    CollapsibleSection(title) {
        SectionCard(color = Panel) { lines.forEach { TrustBullet(it) } }
    }
}

@Composable
private fun TrustScreen(vm: MobileWatchViewModel) {
    val name = vm.ui.selectedTrust ?: return
    val t = vm.trust(name) ?: return
    Scaffold(containerColor = Charcoal, topBar = { GradientTopBar(t.name, onBack = { vm.clearTrust() }) }) { pad ->
        Column(Modifier.padding(pad).fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 16.dp)) {
            WikiLinks(t.name)
            Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                TrustPortrait(t.image, 92.dp)
                Spacer(Modifier.width(14.dp))
                Column(Modifier.weight(1f)) {
                    Text(t.job, color = AccentGold, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                    Text(t.role, color = JobsBlue, fontSize = 12.sp, modifier = Modifier.padding(top = 2.dp))
                }
            }
            if (t.spells.isNotEmpty()) {
                CollapsibleSection("Spells") {
                    SectionCard(color = Panel) { Text(t.spells.joinToString(", "), color = TextSoft, fontSize = 13.sp) }
                }
            }
            if (t.abilities.isNotEmpty()) {
                CollapsibleSection("Abilities") {
                    SectionCard(color = Panel) { Text(t.abilities.joinToString(", "), color = TextSoft, fontSize = 13.sp) }
                }
            }
            if (t.ws.isNotEmpty()) {
                CollapsibleSection("Weapon Skills") {
                    SectionCard(color = Panel) {
                        t.ws.forEachIndexed { i, w ->
                            Text(w, color = AccentGold, fontSize = 13.sp, modifier = Modifier.padding(vertical = 3.dp))
                            if (i < t.ws.lastIndex) HorizontalDivider(color = CharcoalDark)
                        }
                    }
                }
            }
            TrustBulletSection("Acquisition", t.acquisition)
            TrustBulletSection("Special Features", t.features)
            TrustBulletSection("Trust Synergy", t.synergy)
            Spacer(Modifier.height(24.dp))
        }
    }
}

private fun agoText(epoch: Long): String {
    val secs = (System.currentTimeMillis() / 1000 - epoch).coerceAtLeast(0)
    return when {
        secs < 60 -> "just now"
        secs < 3600 -> "${secs / 60} min ago"
        secs < 86400 -> "${secs / 3600}h ago"
        else -> "${secs / 86400}d ago"
    }
}

@Composable
private fun EventsContent(vm: MobileWatchViewModel) {
    val ui = vm.ui
    var roe by remember { mutableStateOf(RoeSchedule.current()) }
    LaunchedEffect(Unit) {
        while (true) {
            roe = RoeSchedule.current()
            kotlinx.coroutines.delay(30_000)
        }
    }
    LaunchedEffect(ui.world) { vm.refreshDi(); vm.refreshNm() }
    LaunchedEffect(Unit) { vm.refreshSe() }
    Column(Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 12.dp)) {
        SectionHeader("Timed Records of Eminence")
        SectionCard(color = Panel) {
            Text(roe.current, color = AccentGold, fontWeight = FontWeight.Bold, fontSize = 16.sp)
            Text("changes in ${RoeSchedule.formatCountdown(roe.secondsLeft)}", color = TextMuted, fontSize = 12.sp)
            Spacer(Modifier.height(8.dp))
            Text("Next", color = TextMuted, fontSize = 11.sp)
            Text(roe.next, color = TextSoft, fontSize = 14.sp, fontWeight = FontWeight.Medium)
        }
        SectionHeader("Domain Invasion")
        SectionCard(color = Panel) {
            val di = ui.di
            when {
                ui.diLoading -> Row(verticalAlignment = Alignment.CenterVertically) {
                    CircularProgressIndicator(Modifier.size(16.dp), color = AccentGreen, strokeWidth = 2.dp)
                    Spacer(Modifier.width(8.dp))
                    Text("checking ${ui.world}\u2026", color = TextMuted, fontSize = 12.sp)
                }
                di != null -> {
                    Text("${ui.world}:  ${di.location}", color = AccentGold, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    di.updatedEpoch?.let { Text("reported ${agoText(it)}", color = TextMuted, fontSize = 12.sp) }
                    TextButton(onClick = { vm.refreshDi() }) { Text("Refresh") }
                }
                else -> {
                    Text("No current report for ${ui.world}.", color = TextMuted, fontSize = 13.sp)
                    TextButton(onClick = { vm.refreshDi() }) { Text("Retry") }
                }
            }
        }
        SectionHeader("Notorious Monsters")
        SectionCard(color = Panel) {
            when {
                ui.nmLoading -> Row(verticalAlignment = Alignment.CenterVertically) {
                    CircularProgressIndicator(Modifier.size(16.dp), color = AccentGreen, strokeWidth = 2.dp)
                    Spacer(Modifier.width(8.dp)); Text("checking ${ui.world}\u2026", color = TextMuted, fontSize = 12.sp)
                }
                ui.nm.isNotEmpty() -> {
                    ui.nm.forEachIndexed { i, e ->
                        Text(e.display, color = if (e.isQuestion) JobsBlue else AccentRed,
                            fontWeight = FontWeight.Medium, fontSize = 14.sp)
                        val sub = buildString {
                            append(e.enemy)
                            e.minsUpdate?.let { append("   \u00b7   ${it.toInt()} min ago") }
                        }
                        Text(sub, color = TextMuted, fontSize = 11.sp)
                        if (i < ui.nm.lastIndex) HorizontalDivider(color = CharcoalDark, modifier = Modifier.padding(vertical = 6.dp))
                    }
                    Spacer(Modifier.height(4.dp))
                    TextButton(onClick = { vm.refreshNm() }) { Text("Refresh") }
                }
                else -> {
                    Text("No active NM/??? reports for ${ui.world}.", color = TextMuted, fontSize = 13.sp)
                    TextButton(onClick = { vm.refreshNm() }) { Text("Retry") }
                }
            }
        }
        SectionHeader("Square Enix Events")
        SectionCard(color = Panel) {
            when {
                ui.seLoading -> Row(verticalAlignment = Alignment.CenterVertically) {
                    CircularProgressIndicator(Modifier.size(16.dp), color = AccentGreen, strokeWidth = 2.dp)
                    Spacer(Modifier.width(8.dp)); Text("loading events\u2026", color = TextMuted, fontSize = 12.sp)
                }
                ui.se.isNotEmpty() -> {
                    val ctx = LocalContext.current
                    ui.se.forEachIndexed { i, ev ->
                        Text(ev.title, color = AccentGold, fontWeight = FontWeight.Bold, fontSize = 14.sp)
                        if (ev.period.isNotBlank()) Text(ev.period, color = JobsBlue, fontSize = 11.sp)
                        if (ev.summary.isNotBlank()) Text(ev.summary, color = TextSoft, fontSize = 12.sp,
                            modifier = Modifier.padding(top = 2.dp))
                        if (ev.link.isNotBlank()) TextButton(
                            onClick = { ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(ev.link))) },
                            contentPadding = PaddingValues(0.dp)
                        ) { Text("Details") }
                        if (i < ui.se.lastIndex) HorizontalDivider(color = CharcoalDark, modifier = Modifier.padding(vertical = 8.dp))
                    }
                }
                else -> {
                    Text("Couldn't load the events feed.", color = TextMuted, fontSize = 13.sp)
                    TextButton(onClick = { vm.refreshSe() }) { Text("Retry") }
                }
            }
        }
        Spacer(Modifier.height(24.dp))
    }
}

@Composable
private fun MobNotes(vm: MobileWatchViewModel, mobKey: String) {
    var text by remember(mobKey) { mutableStateOf(vm.mobNote(mobKey)) }
    SectionHeader("Notes")
    OutlinedTextField(
        value = text,
        onValueChange = { text = it; vm.setMobNote(mobKey, it) },
        modifier = Modifier.fillMaxWidth(),
        placeholder = { Text("Your notes on this mob\u2026", color = TextMuted) },
        minLines = 3,
        singleLine = false,
        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Default),
        shape = RoundedCornerShape(12.dp),
        colors = OutlinedTextFieldDefaults.colors(
            focusedContainerColor = Panel,
            unfocusedContainerColor = Panel,
            focusedBorderColor = Selection,
            unfocusedBorderColor = CharcoalDark,
            focusedTextColor = TextPrimary,
            unfocusedTextColor = TextPrimary,
            cursorColor = AccentGreen,
        )
    )
}

@Composable
private fun WikiLinks(name: String) {
    val ctx = LocalContext.current
    val nm = name.replace(" ", "_")
    Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        OutlinedButton(
            onClick = { ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://www.bg-wiki.com/ffxi/$nm"))) },
            modifier = Modifier.weight(1f), contentPadding = PaddingValues(horizontal = 4.dp, vertical = 6.dp)
        ) { Text("BG-wiki", fontSize = 13.sp, maxLines = 1) }
        OutlinedButton(
            onClick = { ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://ffxiclopedia.fandom.com/wiki/$nm"))) },
            modifier = Modifier.weight(1f), contentPadding = PaddingValues(horizontal = 4.dp, vertical = 6.dp)
        ) { Text("FFXIclopedia", fontSize = 13.sp, maxLines = 1) }
    }
}

private const val DONATE_URL = "https://ko-fi.com/BalladOfWorms"

@Composable
private fun SettingsScreen(vm: MobileWatchViewModel) {
    val ctx = LocalContext.current
    val version = remember {
        runCatching {
            val info = ctx.packageManager.getPackageInfo(ctx.packageName, 0)
            @Suppress("DEPRECATION")
            "${info.versionName} (build ${info.versionCode})"
        }.getOrNull() ?: "\u2014"
    }
    Scaffold(containerColor = Charcoal, topBar = { GradientTopBar("Settings", onBack = { vm.closeSettings() }) }) { pad ->
        Column(Modifier.padding(pad).fillMaxSize().verticalScroll(rememberScrollState()).padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Image(painterResource(R.drawable.mobilewatch_logo), "MobileWatch", modifier = Modifier.size(48.dp))
                Spacer(Modifier.width(12.dp))
                Column {
                    Text("MobileWatch", color = AccentGold, fontWeight = FontWeight.Bold, fontSize = 22.sp)
                    Text("Version $version", color = TextMuted, fontSize = 13.sp)
                }
            }
            SectionHeader("Defaults")
            SectionCard(color = Panel) {
                Text("Default view when opening each search tab.", color = TextSoft, fontSize = 13.sp)
                Spacer(Modifier.height(10.dp))
                var defMob by remember { mutableStateOf(vm.defaultMobView()) }
                var defZone by remember { mutableStateOf(vm.defaultZoneView()) }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Bestiary", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 60.dp))
                    PickerButton("View", defMob, listOf("all" to "All", "family" to "Family", "zone" to "Zone", "content" to "Content")) {
                        defMob = it; vm.setDefaultMobView(it)
                    }
                }
                Spacer(Modifier.height(6.dp))
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text("Zones", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 60.dp))
                    PickerButton("View", defZone, listOf("all" to "All", "region" to "Region")) {
                        defZone = it; vm.setDefaultZoneView(it)
                    }
                }
            }
            SectionHeader("Support")
            SectionCard(color = Panel) {
                Text("If MobileWatch is useful to you, you can support development.",
                    color = TextSoft, fontSize = 13.sp)
                Spacer(Modifier.height(10.dp))
                Button(
                    onClick = { runCatching { ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(DONATE_URL))) } },
                    colors = ButtonDefaults.buttonColors(containerColor = AccentGold, contentColor = Charcoal)
                ) { Text("\u2615  Support on Ko-fi", fontWeight = FontWeight.SemiBold) }
            }
            SectionHeader("About")
            SectionCard(color = Panel) {
                Text("A Final Fantasy XI companion, built offline-first \u2014 everything but auction "
                    + "house prices and the live event feed works with no connection.",
                    color = TextSoft, fontSize = 13.sp)
                Spacer(Modifier.height(8.dp))
                AboutLine("Items", "Auction house prices by world, with sale history.")
                AboutLine("Events", "Live in-game campaigns and seasonal events.")
                AboutLine("Jobs", "All 22 jobs \u2014 traits, abilities, spells, pets and Corsair rolls.")
                AboutLine("Bestiary", "Every monster in the game, browsable by family, by zone or by "
                    + "content, with resistances, TP moves, spells, drops and notes.")
                AboutLine("Zones", "All 294 zones \u2014 maps, travel, battlefields, quests, NMs and mobs.")
                AboutLine("Content", "Endgame by activity, starting with Dynamis and Dynamis Divergence.")
                AboutLine("Hobbies", "Fishing, all nine crafts, Synergy, gardening, and the gathering "
                    + "and chocobo hobbies.")
                AboutLine("Trusts", "All 122 alter egos by role.")
                AboutLine("Chains", "Skillchains and the full weapon skill reference.")
                Spacer(Modifier.height(10.dp))
                Text("Data is compiled by hand from BG-wiki and checked against the game. If something "
                    + "looks wrong, it probably is \u2014 tell me and it gets fixed.",
                    color = TextMuted, fontSize = 12.sp)
                Text("by BalladOfWorms", color = TextMuted, fontSize = 12.sp, modifier = Modifier.padding(top = 8.dp))
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}

@Composable
private fun AboutLine(tab: String, what: String) {
    Row(Modifier.fillMaxWidth().padding(vertical = 3.dp)) {
        Text(tab, color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,
            maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 72.dp))
        Text(what, color = TextSoft, fontSize = 12.sp, modifier = Modifier.weight(1f))
    }
}

@Composable
private fun JobListContent(vm: MobileWatchViewModel) {
    LazyColumn(Modifier.fillMaxSize()) {
        items(vm.jobs(), key = { it.id }) { job ->
            TopLevelRow(job.name) { vm.selectJob(job) }
        }
    }
}

@Composable
private fun LevelRow(name: String, level: String, levelColor: Color, showDivider: Boolean, onClick: (() -> Unit)? = null) {
    Row(
        Modifier.fillMaxWidth().then(if (onClick != null) Modifier.clickable { onClick() } else Modifier)
            .padding(vertical = 5.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(name, color = TextPrimary, fontSize = 14.sp, modifier = Modifier.weight(1f))
        Text(if (level.firstOrNull()?.isDigit() == true) "Lv $level" else level, color = levelColor, fontSize = 12.sp)
    }
    if (showDivider) HorizontalDivider(color = CharcoalDark)
}

@Composable
private fun JobArt(code: String) {
    val ctx = LocalContext.current
    val bmp = remember(code) {
        runCatching { ctx.assets.open("jobart/$code.webp").use { BitmapFactory.decodeStream(it)?.asImageBitmap() } }.getOrNull()
    }
    if (bmp != null) {
        Surface(
            shape = RoundedCornerShape(12.dp), color = Panel, tonalElevation = 2.dp,
            modifier = Modifier.fillMaxWidth().padding(top = 10.dp).height(230.dp)
        ) {
            Image(bmp, code, modifier = Modifier.fillMaxSize().padding(4.dp), contentScale = ContentScale.Fit)
        }
    }
}

@Composable
private fun JobDetailScreen(vm: MobileWatchViewModel) {
    val job = vm.ui.selectedJob ?: return
    val traits = vm.jobTraits(job.id)
    val abilities = vm.jobAbilities(job.id)
    val spells = vm.jobSpells(job.id)
    val rolls = vm.jobRolls(job.id)
    val pets = vm.jobPets(job.id)
    Scaffold(containerColor = Charcoal, topBar = { GradientTopBar(job.name, onBack = { vm.back() }) }) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize().padding(horizontal = 16.dp)) {
            item { JobArt(job.code) }
            item { WikiLinks(job.name) }
            if (traits.isNotEmpty()) item {
                CollapsibleSection("Job Traits") {
                    SectionCard(color = Panel) {
                        traits.forEachIndexed { i, t -> LevelRow(t.name, t.levels, AccentGold, i < traits.lastIndex) }
                    }
                }
            }
            if (abilities.isNotEmpty()) item {
                CollapsibleSection("Job Abilities") {
                    SectionCard(color = Panel) {
                        abilities.forEachIndexed { i, a -> LevelRow(a.name, a.level.toString(), AccentGreen, i < abilities.lastIndex) }
                    }
                }
            }
            if (pets.isNotEmpty()) item {
                CollapsibleSection("Pets") {
                    SectionCard(color = Panel) {
                        pets.forEachIndexed { i, p ->
                            Row(
                                Modifier.fillMaxWidth().clickable { vm.selectPet(p) }.padding(vertical = 9.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column(Modifier.weight(1f)) {
                                    Text(p.name, color = TextPrimary, fontWeight = FontWeight.Medium, fontSize = 15.sp)
                                    val petSub = listOfNotNull(
                                        p.sub.ifBlank { null },
                                        if (p.level.isNotBlank() && p.cap.isNotBlank()) "Lv ${p.level}-${p.cap}" else null
                                    ).joinToString("  \u00b7  ")
                                    if (petSub.isNotEmpty()) Text(petSub, color = TextMuted, fontSize = 11.sp)
                                }
                                Icon(Icons.Filled.ArrowForward, null, tint = TextMuted, modifier = Modifier.size(18.dp))
                            }
                            if (i < pets.lastIndex) HorizontalDivider(color = CharcoalDark)
                        }
                    }
                }
            }
            if (rolls.isNotEmpty()) item {
                CollapsibleSection("Rolls") {
                    SectionCard(color = Panel) {
                        rolls.forEachIndexed { i, r -> LevelRow(r.name, r.level.toString(), AccentGold, i < rolls.lastIndex) }
                    }
                }
            }
            if (spells.isNotEmpty()) item {
                CollapsibleSection("Spells") {
                    SectionCard(color = Panel) {
                        spells.forEachIndexed { i, sp -> LevelRow(sp.name, sp.level, JobsBlue, i < spells.lastIndex, onClick = { vm.selectSpell(sp.name) }) }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun PetDetailScreen(vm: MobileWatchViewModel) {
    val pet = vm.ui.selectedPet ?: return
    // The facts block is Beastmaster-only; a Summoner avatar has none of these set and the
    // whole card is skipped, leaving its Blood Pact sections exactly as before.
    val facts = listOf(
        "Familiar" to pet.family, "Ecosystem" to pet.eco, "Jug" to pet.sub, "Job" to pet.job,
        "Level available" to pet.level, "Pet level cap" to pet.cap,
        "Hit points" to pet.hp, "Damage type" to pet.damage,
        "TP per hit" to pet.tp, "Duration" to pet.duration,
        "Attack" to pet.atkMod, "Defense" to pet.defMod
    ).filter { it.second.isNotBlank() }
    Scaffold(containerColor = Charcoal, topBar = { GradientTopBar(pet.name, onBack = { vm.clearPet() }) }) { pad ->
        LazyColumn(Modifier.padding(pad).fillMaxSize().padding(horizontal = 16.dp)) {
            item { WikiLinks(pet.name) }
            if (facts.isNotEmpty()) item {
                SectionCard(color = Panel) {
                    facts.forEach { (label, value) ->
                        InfoRow(label, listOf(value), if (label == "Jug") AccentGold else TextSoft)
                    }
                }
            } else if (pet.sub.isNotEmpty()) item {
                Text(pet.sub, color = AccentGold, fontSize = 13.sp, modifier = Modifier.padding(vertical = 4.dp))
            }
            if (pet.traits.isNotEmpty()) item {
                CollapsibleSection("Notable Traits") {
                    SectionCard(color = Panel) {
                        pet.traits.forEach { t ->
                            Text("\u2022  $t", color = TextSoft, fontSize = 13.sp,
                                modifier = Modifier.padding(vertical = 3.dp))
                        }
                    }
                }
            }
            if (pet.stats.isNotEmpty()) item {
                CollapsibleSection("Stats at level cap") {
                    SectionCard(color = Panel) {
                        pet.stats.forEach { (label, value) -> InfoRow(label, listOf(value), AccentGreen) }
                    }
                }
            }
            if (pet.notes.isNotEmpty()) item {
                CollapsibleSection("Notes") {
                    SectionCard(color = Panel) {
                        pet.notes.forEach { n ->
                            Text("\u2022  $n", color = TextSoft, fontSize = 13.sp,
                                modifier = Modifier.padding(vertical = 3.dp))
                        }
                    }
                }
            }
            if (pet.readyKnown) item {
                CollapsibleSection("Ready Abilities") {
                    SectionCard(color = Panel) {
                        if (pet.ready.isEmpty()) {
                            Text("This familiar has no Ready abilities.", color = TextMuted, fontSize = 13.sp)
                        } else pet.ready.forEachIndexed { i, r ->
                            Column(Modifier.fillMaxWidth().padding(vertical = 6.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Text(r.name, color = AccentRed, fontSize = 13.sp,
                                        fontWeight = FontWeight.Medium, modifier = Modifier.weight(1f))
                                    // the /bstpet index, where the page publishes one
                                    if (r.index.isNotBlank())
                                        Text("/bstpet ${r.index}", color = TextMuted, fontSize = 11.sp,
                                            modifier = Modifier.padding(end = 8.dp))
                                    if (r.charges.isNotBlank())
                                        Text(r.charges, color = AccentGold, fontSize = 11.sp)
                                }
                                if (r.skillchain.isNotBlank())
                                    Text("Skillchain: ${r.skillchain}", color = AccentGreen, fontSize = 11.sp,
                                        modifier = Modifier.padding(top = 2.dp))
                                if (r.desc.isNotBlank())
                                    Text(r.desc, color = TextSoft, fontSize = 12.sp,
                                        modifier = Modifier.padding(top = 2.dp))
                            }
                            if (i < pet.ready.lastIndex) HorizontalDivider(color = CharcoalDark)
                        }
                    }
                }
            }
            pet.sections.forEach { section ->
                item {
                    CollapsibleSection(section.title) {
                        SectionCard(color = Panel) {
                            section.items.forEachIndexed { i, ab -> LevelRow(ab.name, ab.level, AccentGold, i < section.items.lastIndex) }
                        }
                    }
                }
            }
            item { Spacer(Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun SpellDetailScreen(vm: MobileWatchViewModel) {
    val name = vm.ui.selectedSpell ?: return
    val info = vm.spellInfo(name)
    Scaffold(containerColor = Charcoal, topBar = { GradientTopBar(name, onBack = { vm.clearSpell() }) }) { pad ->
        Column(Modifier.padding(pad).fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 16.dp)) {
            WikiLinks(name)
            if (info != null) {
                SectionCard(color = Panel) {
                    if (info.type.isNotEmpty()) InfoRow("Type", listOf(info.type), TextSoft)
                    if (info.elem.isNotEmpty()) InfoRow("Element", listOf(info.elem), elemColor(info.elem))
                    if (info.skill.isNotEmpty()) InfoRow("Skill", listOf(info.skill), TextSoft)
                    InfoRow("MP", listOf(info.mp.toString()), AccentGreen)
                    InfoRow("Cast", listOf("${info.cast}s"), TextSoft)
                    InfoRow("Recast", listOf("${info.recast}s"), TextSoft)
                }
                if (info.jobs.isNotEmpty()) {
                    SectionHeader("Learned by")
                    SectionCard(color = Panel) {
                        info.jobs.forEachIndexed { i, pair ->
                            LevelRow(pair.first, pair.second, JobsBlue, i < info.jobs.lastIndex)
                        }
                    }
                }
            } else {
                Spacer(Modifier.height(12.dp))
                Text("No metadata for this spell.", color = TextMuted, fontSize = 13.sp)
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}

private fun metaLine(it: Item): String {
    // keep each chip on one line; wrapping only happens at the separators
    fun nb(s: String) = s.replace(" ", "\u00a0")
    val bits = ArrayList<String>()
    if (it.category.isNotBlank()) bits.add(nb(it.category))          // type of weapon / gear
    val lvl = when {
        it.ilevel > 0 -> "iLv ${it.ilevel}"
        it.level > 0 -> "Lv ${it.level}"
        else -> ""
    }
    if (lvl.isNotEmpty()) bits.add(nb(lvl))
    if (it.rareEx.isNotEmpty()) bits.add(nb(it.rareEx))
    return bits.joinToString("   \u00b7   ")
}
