# MobileWatch

A native Android companion for **Final Fantasy XI** — Kotlin, Jetpack Compose,
Material 3 dark UI. Built by **BalladOfWorms**.

Almost all of it works with the phone in airplane mode: every reference table
ships inside the APK. Two things reach the network — live Auction House pricing,
which talks to the game's own search servers using the same protocol as the
desktop OmniWatch tools, and zone maps, which are fetched once per zone and then
cached on the device (see **Zone maps** below).

## The nine tabs

| Tab | What's in it |
| --- | --- |
| **Items** | 23,503 items. Search by name, live AH price history by world (Singles/Stacks, low/median/high), on-sale counts, world population, and a cross-server median ranking. |
| **Events** | Current in-game campaigns and seasonal events. |
| **Jobs** | All 22 jobs — traits, abilities, spells, Corsair rolls, and pet rosters: 98 Beastmaster jug familiars and 22 Summoner avatars. |
| **Bestiary** | **6,810 monsters** across 218 families, browsable by family, by zone or by content. Resist grid, immunities, absorbs, detection, drops, spawn conditions, per-zone level ranges, and **1,591 ability definitions** with target shape, element and effects. |
| **Zones** | 294 zones. Maps, travel and transport schedules, battlefields, quests, NM and mob rosters, connected-zone navigation. |
| **Content** | Endgame content organised by strategy — Dynamis and Dynamis Divergence, area by area, with boss tiers, time extensions, farming routes and rewards read live from the bestiary. |
| **Quests** | Every quest in the game's own quest log, 1,091 of them across the eleven sections the log itself uses — San d'Oria through Coalition. Tick one off as you finish it and the count on its area follows; tap the name for its BG-wiki page. |
| **Hobbies** | 22 hobbies: fishing, the nine crafts (cooking, goldsmithing, alchemy, smithing, clothcraft, leathercraft, bonecraft, woodworking, synergy), gardening, harvesting, mining, excavation, logging, chocobo digging/raising/racing, clamming, Mog Garden, Monstrosity. |
| **Trusts** | All 122 alter egos with portraits, grouped by role. |
| **Chains** | 230 weapon skills across 15 weapon types, plus the full skillchain and magic-burst tables. |

Swipe or use the mode menu to move between tabs — both walk the same list, so
they can never disagree about what comes next.

## Music

The **♪ button in the header** (between the logo and the world picker) opens a
player for FINAL FANTASY XI's soundtrack, built from the desktop **OmniPlayer**.

- Copy the game's music folders to the phone (`sound`, `sound2`, `sound3` … from
  your FFXI install, or just their `win\music\data` folders), and/or tracks
  exported as MP3, FLAC, WAV, OGG or M4A, then choose that folder in the player.
  Android's own folder picker is used, so no storage permission is needed.
- `.bgw` files are decoded in the app and **loop exactly the way the game loops
  them** — intro once, then the loop section seamlessly. The repeat button
  switches to playing each track once, then the next.
- Tracks are **named automatically** from OmniPlayer's catalogue of 216 tracks
  (title, composer, expansion and where it's heard), by the same rules: the
  `soundN` folder a file is in, what else is in its folder, or its remembered
  fingerprint. Other formats use their own tags.
- Favourites (heart), search, shuffle, and seeking.
- **Select tracks:** long-press a track (or use the select-all button in the top
  bar) to pick several; tap to add or remove. Select all takes every track in the
  list as shown, so after a search or the favourites filter, just those. Then
  favourite the whole selection at once, or play it as its own queue.
- **Plays in the background** — screen off, phone in your pocket, or another app in
  front — with **controls in the notification and on the lock screen** (previous,
  play/pause, next, seek, close). Headset and Bluetooth buttons work too. Tapping the
  notification opens the player.
- Pauses when headphones are unplugged or a call comes in; closing the notification,
  backing out of MobileWatch, or swiping it away in Recents stops the music.

**No music is included with MobileWatch.** It plays the files from your own copy
of the game. FINAL FANTASY XI's music is © SQUARE ENIX CO., LTD.

## Data is bundled

~61 MB of assets ride inside the app: `mobs.json`, `ffxi_items.json`,
`zones.json` / `zoneinfo.json`, `jobs.json`, `trusts.json`, `recipes.json`,
`weaponskills.json`, `skillchains.json`, the per-hobby tables, plus 217 family
icons, 166 monster renders, 296 zone banners and 122 trust portraits. Nothing to
download, nothing to configure.

`MobileWatch-Bestiary.md` at the project root is a generated plain-text dump of
the entire bestiary — one fact per line, every ability definition — regenerated
by `_project/gen_bestiary.py` whenever `mobs.json` changes.

## Zone maps

Zone maps are the one dataset **not** bundled, deliberately — a full FFXI map
pack would dominate the download. They are hosted in the `maps/` folder at the
root of this repository and fetched on demand:

```
https://raw.githubusercontent.com/BalladOfWorms/MobileWatch/main/maps/
```

Files use the standard pack naming that OmniWatch and OT use —
`<zoneID-in-hex>_<mapIndex>.<ext>`, e.g. `0a_0.png`, `118_0.gif`. Both the
zero-padded and bare hex spellings are tried, and `gif` / `png` / `jpg` /
`jpeg` / `webp` in that order.

`MapSupport.kt` resolves each zone as **assets → device cache → network**, then
writes a manifest of the resolved filenames to `cacheDir/maps/.idx_<zoneId>` so
every later view is pure cache with zero requests. An empty manifest records
"this zone has no maps" and is trusted for a week, so mapless zones stop
probing too.

Two consequences worth knowing: **the repository must stay public** (raw
.githubusercontent.com will not serve a private repo unattended), and the branch
and path in `BASE_URL` are load-bearing — renaming `main`, or moving `maps/`,
breaks map loading for every installed copy. Dropping the same files into
`app/src/main/assets/maps/` and rebuilding is the supported alternative; the
app prefers assets when they are present.

## Build & run

Android Studio → *File → Open* → this folder → sync → **Run ▶**.
Kotlin 2.0 + Compose BOM 2024.10, `minSdk 26`, `targetSdk 34`, JVM target 17.

For a signed release APK see **`_project/SIGNING.md`** — release signing reads
`keystore.properties` from the project root (gitignored; a template lives in
`keystore.properties.example`). Without that file the project still configures
and `assembleDebug` still works.

### A note on the package rename

The Gradle project, the Kotlin package and the Compose theme are all
`MobileWatch` / `com.balladofworms.mobilewatch`. The **`applicationId` is
deliberately still `com.balladofworms.auctionwatch`** — that string is the
identity Android installs under, so changing it would make the next build a
separate app installed *beside* the current one, leaving your saved mob notes
and view preferences behind in the old sandbox. It is a one-line change in
`app/build.gradle.kts` if you ever want it.

## Layout

```
app/src/main/kotlin/com/balladofworms/mobilewatch/
    MainActivity.kt              entry point
    MobileWatchViewModel.kt      all UI state; SharedPreferences named "mobilewatch"
    ui/MobileWatchApp.kt         every screen
    ui/theme/                    colours, type, MobileWatchTheme
    SearchEngine.kt              AH protocol client (Kotlin port of the desktop engine)
    *Db.kt                       one loader per asset file
app/src/main/assets/             all bundled data
    quests.json                  the quest log, by area
    elemicons/                   the eight element icons, drawn inline in item text
_project/                        data-build scripts, audits and notes (not compiled)
```

`_project/audit.py` reproduces every published data figure from the live
`mobs.json` and simulates `MobDb.load`'s strict parse — run it before shipping a
data change. `_project/fz.py` is the fuzzy item-name lookup used to validate
drops against `ffxi_items.json`.
