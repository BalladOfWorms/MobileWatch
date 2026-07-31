package com.balladofworms.mobilewatch

import android.app.Application
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

data class SaleRow(
    val price: Int, val date: Long, val seller: String, val buyer: String, val stack: Boolean
)

data class UiState(
    val ready: Boolean = false,
    val mode: String = "items",           // items | mobs
    val query: String = "",
    val results: List<Item> = emptyList(),
    val mobResults: List<Mob> = emptyList(),
    val selectedMob: Mob? = null,
    val selectedSubtype: SubType? = null,
    val mobLevelCtx: String = "",
    val mobView: String = "all",
    val zoneView: String = "all",
    val mobFilter: String = "all",
    val zoneFilter: String = "all",
    val zoneResults: List<Zone> = emptyList(),
    val selectedZone: Zone? = null,
    val showMap: Boolean = false,
    val scChain: List<WeaponSkill> = emptyList(),
    val showSettings: Boolean = false,
    val selectedJob: Job? = null,
    val selectedHobby: String? = null,
    val selectedContent: String? = null,       // Content tab: which content type (e.g. "dynamis")
    val selectedContentZone: String? = null,   // Content tab: which zone page inside it
    val selectedTrust: String? = null,         // Trusts tab: which alter ego's page is open
    val showWsList: Boolean = false,           // Chains tab: the full weapon-skill reference page
    val selectedFish: Fish? = null,
    val selectedRecipe: Recipe? = null,
    val selectedDigZone: DigZone? = null,
    val selectedPlanting: GardenPlanting? = null,
    val selectedHarvestZone: HarvestZone? = null,
    val selectedMineZone: MiningZone? = null,
    val selectedExcZone: ExcavationZone? = null,
    val selectedLogZone: LoggingZone? = null,
    val showHobbyInfo: Boolean = false,
    val selectedSpell: String? = null,
    val selectedPet: Pet? = null,
    val diLoading: Boolean = false,
    val di: DomainInvasion.DiInfo? = null,
    val diError: Boolean = false,
    val nmLoading: Boolean = false,
    val nm: List<WhereIsNm.NmEntry> = emptyList(),
    val nmError: Boolean = false,
    val seLoading: Boolean = false,
    val se: List<SeEvents.Event> = emptyList(),
    val seError: Boolean = false,
    val world: String = "Phoenix",
    val population: String = "\u2014",
    val selected: Item? = null,
    val historyLoading: Boolean = false,
    val history: List<SaleRow> = emptyList(),
    val onsaleSingle: Int? = null,
    val onsaleStack: Int? = null,
    val filter: String = "all",            // all | single | stack
    val crossLoading: Boolean = false,
    val crossRanking: List<Pair<String, Int>> = emptyList(), // world -> median, cheapest first
    val crossForm: String = "single",   // which form the ranking represents
    val historyNote: String? = null,
)

class MobileWatchViewModel(app: Application) : AndroidViewModel(app) {

    var ui by mutableStateOf(UiState())
        private set

    private val prefs = app.getSharedPreferences("mobilewatch", android.content.Context.MODE_PRIVATE)

    private var itemDb: ItemDb? = null
    private var mobDb: MobDb? = null
    private var zoneInfoDb: ZoneInfoDb? = null
    private var zoneDb: ZoneDb? = null
    private var scDb: SkillchainDb? = null
    private var jobDb: JobDb? = null
    private var fishDb: FishDb? = null
    private var hobbyInfoDb: HobbyInfoDb? = null
    private var recipeDb: RecipeDb? = null
    private var diggingDb: DiggingDb? = null
    private var gardeningDb: GardeningDb? = null
    private var harvestingDb: HarvestingDb? = null
    private var miningDb: MiningDb? = null
    private var excavationDb: ExcavationDb? = null
    private var loggingDb: LoggingDb? = null
    private var trustDb: TrustDb? = null
    private var wsListDb: WsListDb? = null
    private val crossCache = HashMap<Int, HashMap<String, List<Pair<String, Int>>>>()
    private var popToken = 0
    private var histToken = 0
    private var crossToken = 0

    init {
        ui = ui.copy(
            world = prefs.getString("world", "Phoenix") ?: "Phoenix",
            mobView = prefs.getString("defMobView", "all") ?: "all",
            zoneView = prefs.getString("defZoneView", "all") ?: "all"
        )
        viewModelScope.launch {
            val app = getApplication<Application>()
            val items = withContext(Dispatchers.IO) { ItemDb.load(app) }
            val mobs = withContext(Dispatchers.IO) { runCatching { MobDb.load(app) }.getOrNull() }
            val zinfo = withContext(Dispatchers.IO) { runCatching { ZoneInfoDb.load(app) }.getOrNull() }
            val zones = withContext(Dispatchers.IO) { runCatching { ZoneDb.load(app) }.getOrNull() }
            val scs = withContext(Dispatchers.IO) { runCatching { SkillchainDb.load(app) }.getOrNull() }
            val jobs = withContext(Dispatchers.IO) { runCatching { JobDb.load(app) }.getOrNull() }
            fishDb = withContext(Dispatchers.IO) { runCatching { FishDb.load(app) }.getOrNull() }
            hobbyInfoDb = withContext(Dispatchers.IO) { runCatching { HobbyInfoDb.load(app) }.getOrNull() }
            recipeDb = withContext(Dispatchers.IO) { runCatching { RecipeDb.load(app) }.getOrNull() }
            diggingDb = withContext(Dispatchers.IO) { runCatching { DiggingDb.load(app) }.getOrNull() }
            gardeningDb = withContext(Dispatchers.IO) { runCatching { GardeningDb.load(app) }.getOrNull() }
            harvestingDb = withContext(Dispatchers.IO) { runCatching { HarvestingDb.load(app) }.getOrNull() }
            miningDb = withContext(Dispatchers.IO) { runCatching { MiningDb.load(app) }.getOrNull() }
            excavationDb = withContext(Dispatchers.IO) { runCatching { ExcavationDb.load(app) }.getOrNull() }
            loggingDb = withContext(Dispatchers.IO) { runCatching { LoggingDb.load(app) }.getOrNull() }
            trustDb = withContext(Dispatchers.IO) { runCatching { TrustDb.load(app) }.getOrNull() }
            wsListDb = withContext(Dispatchers.IO) { runCatching { WsListDb.load(app) }.getOrNull() }
            itemDb = items
            mobDb = mobs
            zoneInfoDb = zinfo
            zoneDb = zones
            scDb = scs
            jobDb = jobs
            ui = ui.copy(ready = true)
            refreshPopulation()
        }
    }

    private fun host(): String? = Worlds.ip(ui.world)

    /** Results-list label with the REMA level/DMG suffix (raw name elsewhere). */
    fun label(item: Item): String = itemDb?.label(item) ?: item.name

    fun onQueryChange(q: String) {
        ui = when (ui.mode) {
            "mobs" -> ui.copy(query = q, mobResults = if (q.isBlank()) mobDb?.all() ?: emptyList() else mobDb?.search(q) ?: emptyList())
            "maps" -> ui.copy(query = q, zoneResults = if (q.isBlank()) zoneDb?.all() ?: emptyList() else zoneDb?.search(q) ?: emptyList())
            else -> ui.copy(query = q, results = if (q.isBlank()) itemDb?.all() ?: emptyList() else itemDb?.search(q) ?: emptyList())
        }
    }

    fun jobs(): List<Job> = jobDb?.jobs ?: emptyList()
    fun selectJob(job: Job) { ui = ui.copy(selectedJob = job) }
    fun fishList(): List<Fish> = fishDb?.fish ?: emptyList()
    fun selectHobby(k: String) { ui = ui.copy(selectedHobby = k, selectedFish = null, selectedRecipe = null, selectedDigZone = null, selectedPlanting = null, selectedHarvestZone = null, selectedMineZone = null, selectedExcZone = null, selectedLogZone = null, showHobbyInfo = false) }
    fun clearHobby() { ui = ui.copy(selectedHobby = null, selectedFish = null, selectedRecipe = null, selectedDigZone = null, selectedPlanting = null, selectedHarvestZone = null, selectedMineZone = null, selectedExcZone = null, selectedLogZone = null, showHobbyInfo = false) }
    fun selectFish(f: Fish) { ui = ui.copy(selectedFish = f) }
    fun clearFish() { ui = ui.copy(selectedFish = null) }
    fun hobbyInfo(k: String): HobbyInfo? = hobbyInfoDb?.infoFor(k)
    fun recipeList(craft: String): List<Recipe> = recipeDb?.recipesFor(craft) ?: emptyList()
    fun selectRecipe(r: Recipe) { ui = ui.copy(selectedRecipe = r) }
    fun clearRecipe() { ui = ui.copy(selectedRecipe = null) }
    fun digZones(): List<DigZone> = diggingDb?.zones ?: emptyList()
    fun selectDigZone(z: DigZone) { ui = ui.copy(selectedDigZone = z) }
    fun clearDigZone() { ui = ui.copy(selectedDigZone = null) }
    fun gardening(): GardeningDb? = gardeningDb
    fun plantings(): List<GardenPlanting> = gardeningDb?.plantings ?: emptyList()
    fun selectPlanting(p: GardenPlanting) { ui = ui.copy(selectedPlanting = p) }
    fun clearPlanting() { ui = ui.copy(selectedPlanting = null) }
    fun harvestZones(): List<HarvestZone> = harvestingDb?.zones ?: emptyList()
    fun selectHarvestZone(z: HarvestZone) { ui = ui.copy(selectedHarvestZone = z) }
    fun clearHarvestZone() { ui = ui.copy(selectedHarvestZone = null) }
    fun mineZones(): List<MiningZone> = miningDb?.zones ?: emptyList()
    fun selectMineZone(z: MiningZone) { ui = ui.copy(selectedMineZone = z) }
    fun clearMineZone() { ui = ui.copy(selectedMineZone = null) }
    fun excZones(): List<ExcavationZone> = excavationDb?.zones ?: emptyList()
    fun selectExcZone(z: ExcavationZone) { ui = ui.copy(selectedExcZone = z) }
    fun clearExcZone() { ui = ui.copy(selectedExcZone = null) }
    fun logZones(): List<LoggingZone> = loggingDb?.zones ?: emptyList()
    fun selectLogZone(z: LoggingZone) { ui = ui.copy(selectedLogZone = z) }
    fun clearLogZone() { ui = ui.copy(selectedLogZone = null) }
    fun openHobbyInfo() { ui = ui.copy(showHobbyInfo = true) }
    fun closeHobbyInfo() { ui = ui.copy(showHobbyInfo = false) }
    fun jobAbilities(id: Int): List<JobAbility> = jobDb?.abilitiesFor(id) ?: emptyList()
    fun jobTraits(id: Int): List<JobTrait> = jobDb?.traitsFor(id) ?: emptyList()
    fun jobSpells(id: Int): List<JobSpell> = jobDb?.spellsFor(id) ?: emptyList()
    fun jobRolls(id: Int): List<JobAbility> = jobDb?.rollsFor(id) ?: emptyList()
    fun selectSpell(name: String) { ui = ui.copy(selectedSpell = name) }
    fun clearSpell() { ui = ui.copy(selectedSpell = null) }
    fun spellInfo(name: String): SpellInfo? = jobDb?.spellInfoFor(name)
    /** Pets ordered by level cap, lowest first, then by name. Pets with no numeric cap are
     *  NOT sorted at all — they keep their file order and sit at the end. That matters: every
     *  Summoner avatar has a blank cap and the avatar list is in a deliberate order
     *  (Carbuncle, Ifrit, Shiva, ... then the spirits), which an alphabetical fallback would
     *  scramble. */
    fun jobPets(id: Int): List<Pet> {
        val all = jobDb?.petsFor(id) ?: emptyList()
        val (capped, uncapped) = all.partition { it.cap.toIntOrNull() != null }
        return capped.sortedWith(compareBy({ it.cap.toInt() }, { it.name })) + uncapped
    }
    fun selectPet(pet: Pet) { ui = ui.copy(selectedPet = pet) }
    fun clearPet() { ui = ui.copy(selectedPet = null) }

    fun openSettings() { ui = ui.copy(showSettings = true) }

    fun closeSettings() { ui = ui.copy(showSettings = false) }

    fun setMode(m: String) {
        if (m == ui.mode) return
        ui = ui.copy(mode = m, query = "",
            results = if (m == "items") itemDb?.all() ?: emptyList() else emptyList(),
            mobResults = if (m == "mobs") mobDb?.all() ?: emptyList() else emptyList(),
            zoneResults = if (m == "maps") zoneDb?.all() ?: emptyList() else emptyList(),
            selected = null, selectedMob = null, selectedSubtype = null, selectedZone = null, selectedJob = null,
            selectedHobby = null, selectedFish = null, selectedRecipe = null, selectedDigZone = null, selectedPlanting = null, selectedHarvestZone = null, selectedMineZone = null, selectedExcZone = null, selectedLogZone = null, showHobbyInfo = false,
            selectedContent = null, selectedContentZone = null,
            selectedTrust = null, showWsList = false)
    }

    // ---- Trusts tab --------------------------------------------------------
    fun trustRoles(): List<String> = trustDb?.roles ?: emptyList()
    fun trustsOf(role: String): List<Trust> = trustDb?.byRole(role) ?: emptyList()
    fun trust(name: String): Trust? = trustDb?.trust(name)
    fun trustInfo(): List<TrustInfo> = trustDb?.info ?: emptyList()
    /** Total alter egos, shown on the collapsed "Alter Egos" section header. */
    fun trustCount(): Int = trustDb?.trusts?.size ?: 0
    fun selectTrust(name: String) { ui = ui.copy(selectedTrust = name) }
    fun clearTrust() { ui = ui.copy(selectedTrust = null) }

    // ---- Weapon-skill reference (Chains tab) -------------------------------
    fun wsWeapons(): List<WsWeapon> = wsListDb?.weapons ?: emptyList()
    /** Chain properties for a listed WS, or null when it has none ("No Property"). */
    fun wsChainInfo(name: String): WeaponSkill? = scDb?.wsByName(name)
    fun openWsList() { ui = ui.copy(showWsList = true) }
    fun closeWsList() { ui = ui.copy(showWsList = false) }

    // ---- Content tab -------------------------------------------------------
    fun selectContent(k: String) { ui = ui.copy(selectedContent = k, selectedContentZone = null) }
    fun clearContent() { ui = ui.copy(selectedContent = null, selectedContentZone = null) }
    fun selectContentZone(zone: String) { ui = ui.copy(selectedContentZone = zone) }
    fun clearContentZone() { ui = ui.copy(selectedContentZone = null) }

    // Mobs carrying a `Group: Section` content tag, in the Content view's own order:
    // declared bosses first, then NMs, then regular; ties by level, then name.
    fun mobsForContent(group: String, section: String): List<Mob> {
        val hit = { t: String ->
            val p = t.split(":").map { it.trim() }
            p.getOrElse(0) { "" } == group && p.getOrElse(1) { "" } == section
        }
        return (mobDb?.all() ?: emptyList()).filter { m -> m.content.any(hit) }
    }

    // Mobs whose name starts with any of the given prefixes (e.g. "Apex ", "Locus ").
    fun mobsByNamePrefix(vararg prefixes: String): List<Mob> =
        (mobDb?.all() ?: emptyList()).filter { m -> prefixes.any { m.name.startsWith(it, ignoreCase = true) } }

    // The third `: Role` segment of a mob's tag for this group/section, or "".
    fun contentRoleOf(mob: Mob, group: String, section: String): String =
        mob.content.map { it.split(":").map { p -> p.trim() } }
            .firstOrNull { it.getOrElse(0) { "" } == group && it.getOrElse(1) { "" } == section }
            ?.getOrElse(2) { "" } ?: ""

    fun selectZone(zone: Zone) { ui = ui.copy(selectedZone = zone, showMap = false) }

    // Jump from a Content area page to that zone's full entry in the Zones tab (where
    // the map, if any, lives). Switches mode so the Zones-tab dispatch picks it up.
    fun openZoneDetailByName(name: String) {
        val z = zoneDb?.all()?.firstOrNull { it.name.equals(name, ignoreCase = true) } ?: return
        ui = ui.copy(mode = "maps", selectedZone = z, showMap = false,
            selectedContent = null, selectedContentZone = null)
    }

    fun hasZone(name: String): Boolean =
        zoneDb?.all()?.any { it.name.equals(name, ignoreCase = true) } == true

    fun selectZoneByName(name: String) {
        zoneDb?.all()?.firstOrNull { it.name.equals(name, ignoreCase = true) }?.let { selectZone(it) }
    }

    fun openMap() { ui = ui.copy(showMap = true) }

    fun closeMap() { ui = ui.copy(showMap = false) }

    // inZone carries the zone the user tapped THROUGH, so the detail header shows that
    // zone's own level rather than the flattened global lv band. Passing null (or a zone
    // the mob has no level for) CLEARS mobLevelCtx — without that, a level from a
    // previously-viewed mob leaks onto this one, since only clearMob()/back() reset it.
    fun selectMob(mob: Mob, inZone: String? = null) {
        val lvl = inZone?.let { z -> mob.zones.firstOrNull { it.first == z }?.second } ?: ""
        ui = ui.copy(selectedMob = mob, selectedSubtype = null, mobLevelCtx = lvl)
    }
    fun setMobView(v: String) { ui = ui.copy(mobView = v) }
    fun setZoneView(v: String) { ui = ui.copy(zoneView = v) }
    fun defaultMobView(): String = prefs.getString("defMobView", "all") ?: "all"
    fun defaultZoneView(): String = prefs.getString("defZoneView", "all") ?: "all"
    fun setDefaultMobView(v: String) { prefs.edit().putString("defMobView", v).apply(); ui = ui.copy(mobView = v) }
    fun setDefaultZoneView(v: String) { prefs.edit().putString("defZoneView", v).apply(); ui = ui.copy(zoneView = v) }
    fun setMobFilter(v: String) { ui = ui.copy(mobFilter = v) }
    fun setZoneFilter(v: String) { ui = ui.copy(zoneFilter = v) }
    fun clearMob() { ui = ui.copy(selectedMob = null, selectedSubtype = null, mobLevelCtx = "") }
    fun selectSubtype(sub: SubType) { ui = ui.copy(selectedSubtype = sub) }
    fun clearSubtype() { ui = ui.copy(selectedSubtype = null) }
    fun selectMobByName(name: String, level: String = "") { mobDb?.get(name.lowercase())?.let { ui = ui.copy(selectedMob = it, mobLevelCtx = level) } }
    fun zoneInfo(slug: String): ZoneInfo? = zoneInfoDb?.forSlug(slug)
    fun zoneType(zone: Zone): String = zoneInfoDb?.forSlug(zone.slug)?.type ?: ""
    fun zoneRegion(zone: Zone): String {
        val ov = zoneInfoDb?.forSlug(zone.slug)?.regionOverride
        return if (!ov.isNullOrBlank()) ov else zone.region.ifBlank { "Miscellaneous" }
    }

    /** Asset path for a family icon, or null. */
    fun mobIconPath(family: String): String? = mobDb?.iconPath(family)

    /** Per-mob user notes, persisted in prefs. */
    fun mobNote(key: String): String = prefs.getString("note_$key", "") ?: ""
    fun setMobNote(key: String, text: String) { prefs.edit().putString("note_$key", text).apply() }

    /** Ability description info, or null. */
    fun ability(name: String): AbilityInfo? = mobDb?.ability(name)
    fun familyNotes(family: String): List<String> = mobDb?.familyNotes(family) ?: emptyList()
    fun subtypes(family: String): List<SubType> = mobDb?.subtypes(family) ?: emptyList()
    fun resistSets(family: String): List<ResistSet> = mobDb?.resistSets(family) ?: emptyList()
    fun subtypeNotes(mob: Mob): List<String> =
        mob.sub?.let { s -> mobDb?.subtypes(mob.family)?.firstOrNull { it.name.equals(s, true) }?.notes } ?: emptyList()
    fun ecosystem(family: String): String? = mobDb?.ecosystem(family)
    fun ecosystemOf(mob: Mob): String? = mobDb?.ecosystemOf(mob)
    fun iconForMob(mob: Mob): String? = mobDb?.iconForMob(mob)

    fun setWorld(world: String) {
        if (world == ui.world) return
        ui = ui.copy(world = world)
        prefs.edit().putString("world", world).apply()
        refreshPopulation()
        ui.selected?.let { select(it) }   // re-pull the open item on the new world
    }

    private fun xsForm(): String = if (ui.filter == "stack") "stack" else "single"

    fun setFilter(f: String) {
        ui = ui.copy(filter = f)
        ui.selected?.let { loadCrossServer(it) }   // ranking follows the toggle
    }

    fun back() { ui = ui.copy(selected = null, selectedMob = null, selectedSubtype = null, mobLevelCtx = "", selectedZone = null, selectedJob = null, selectedSpell = null, selectedPet = null, showMap = false, history = emptyList(), crossRanking = emptyList(), historyNote = null) }

    fun refreshPopulation() {
        val h = host() ?: return
        val token = ++popToken
        ui = ui.copy(population = "\u2026")
        viewModelScope.launch {
            val total = withContext(Dispatchers.IO) {
                runCatching { SearchEngine.queryPopulation(h) }.getOrNull()
            }
            if (token != popToken) return@launch
            ui = ui.copy(population = if (total != null) "%,d online".format(total) else "no reply")
        }
    }

    private var nmToken = 0
    fun refreshNm() {
        val world = ui.world
        val token = ++nmToken
        ui = ui.copy(nmLoading = true, nmError = false)
        viewModelScope.launch {
            val list = withContext(Dispatchers.IO) { runCatching { WhereIsNm.fetch(world) }.getOrNull() }
            if (token != nmToken) return@launch
            ui = ui.copy(nmLoading = false, nm = list ?: emptyList(), nmError = list == null)
        }
    }

    private var seToken = 0
    fun refreshSe() {
        val token = ++seToken
        ui = ui.copy(seLoading = true, seError = false)
        viewModelScope.launch {
            val list = withContext(Dispatchers.IO) { runCatching { SeEvents.fetch() }.getOrNull() }
            if (token != seToken) return@launch
            ui = ui.copy(seLoading = false, se = list ?: emptyList(), seError = list == null)
        }
    }

    private var diToken = 0
    fun refreshDi() {
        val world = ui.world
        val token = ++diToken
        ui = ui.copy(diLoading = true, diError = false)
        viewModelScope.launch {
            val info = withContext(Dispatchers.IO) { runCatching { DomainInvasion.fetch(world) }.getOrNull() }
            if (token != diToken) return@launch
            ui = ui.copy(diLoading = false, di = info, diError = info == null)
        }
    }

    fun select(item: Item) {
        ui = ui.copy(selected = item, filter = "all", history = emptyList(),
            onsaleSingle = null, onsaleStack = null, historyLoading = true, historyNote = null)
        loadHistory(item)
        loadCrossServer(item)
    }

    private fun loadHistory(item: Item) {
        val h = host() ?: run { ui = ui.copy(historyLoading = false, historyNote = "No address for ${ui.world}"); return }
        val token = ++histToken
        viewModelScope.launch {
            val res = withContext(Dispatchers.IO) {
                val rows = ArrayList<SaleRow>()
                var single: Int? = null
                var stack: Int? = null
                var cat = -1
                for (isStack in listOf(false, true)) {
                    val hist = runCatching { SearchEngine.queryHistory(h, item.id, isStack) }.getOrNull()
                    if (hist != null && hist.ok) {
                        if (cat < 0) cat = hist.category
                        hist.sales.forEach { rows.add(SaleRow(it.price, it.date, it.seller, it.buyer, isStack)) }
                    }
                }
                if (cat >= 0) {
                    val listing = runCatching { SearchEngine.queryCategoryCounts(h, cat) }.getOrNull()
                    listing?.get(item.id)?.let { single = it.first; stack = it.second }
                }
                Triple(rows, single, stack)
            }
            if (token != histToken || ui.selected?.id != item.id) return@launch
            ui = ui.copy(
                historyLoading = false,
                history = res.first,
                onsaleSingle = res.second,
                onsaleStack = res.third,
                historyNote = if (res.first.isEmpty()) "No sales history / no answer" else null,
            )
        }
    }

    private fun loadCrossServer(item: Item) {
        val form = xsForm()
        crossCache[item.id]?.get(form)?.let {
            ui = ui.copy(crossRanking = it, crossForm = form, crossLoading = false); return
        }
        val token = ++crossToken
        val stack = form == "stack"
        ui = ui.copy(crossLoading = true, crossRanking = emptyList(), crossForm = form)
        viewModelScope.launch {
            val ranking = withContext(Dispatchers.IO) {
                Worlds.map.entries.map { (name, ip) ->
                    async {
                        val m = runCatching { SearchEngine.medianPrice(ip, item.id, stack) }.getOrNull()
                        if (m != null) name to m else null
                    }
                }.awaitAll().filterNotNull().sortedBy { it.second }
            }
            if (token != crossToken || ui.selected?.id != item.id || xsForm() != form) return@launch
            crossCache.getOrPut(item.id) { HashMap() }[form] = ranking
            ui = ui.copy(crossLoading = false, crossRanking = ranking, crossForm = form)
        }
    }

    // ---- skillchain calculator ----
    fun scSteps(): List<SkillchainResult> = scDb?.chain(ui.scChain) ?: emptyList()

    fun scAddWs(ws: WeaponSkill) { ui = ui.copy(scChain = ui.scChain + ws) }

    fun clearWs() { ui = ui.copy(scChain = emptyList()) }

    /** Another WS can be added unless we've reached a level-4 chain (or a length cap). */
    fun scCanContinue(): Boolean {
        if (ui.scChain.size >= 6) return false
        val steps = scSteps()
        return !(steps.isNotEmpty() && steps.last().level >= 4)
    }

    /** Valid weaponskills to add next: any opener at the start, else only WS that continue the chain. */
    fun scNextOptions(): List<WeaponSkill> {
        val db = scDb ?: return emptyList()
        val chain = ui.scChain
        return when {
            chain.isEmpty() -> db.weaponSkills
            chain.size == 1 -> db.weaponSkills.filter { db.chainsInto(chain[0].props, it.closingProps) }
            else -> {
                val last = scSteps().lastOrNull() ?: return emptyList()
                db.weaponSkills.filter { db.chainsInto(listOf(last.name), it.closingProps) }
            }
        }
    }

    fun slotTypes(): List<String> = scNextOptions().map { it.type }.distinct().sorted()

    fun slotWsOf(type: String): List<WeaponSkill> =
        scNextOptions().filter { it.type == type }.sortedBy { it.name }

    /** Sales filtered by the current single/stack toggle. */
    fun visibleSales(): List<SaleRow> = when (ui.filter) {
        "single" -> ui.history.filter { !it.stack }
        "stack" -> ui.history.filter { it.stack }
        else -> ui.history
    }.sortedByDescending { it.date }
}
