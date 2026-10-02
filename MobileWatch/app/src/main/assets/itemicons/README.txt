Drop FFXI item icons here, named <itemID>.png
e.g.  28503.png   16384.png
(the 32x32 icons out of the client's item DATs -- use the OmniWatch extractor,
NOT a copy of the old icon_extractor.lua: the DAT record stride is 0x1400 now,
so the 2021 version produces junk.)

png is tried first, then webp, then jpg.

You do not have to bundle them. Three arrangements all work, and the app works
out which one you used on its own -- there is nothing to switch on:

  1) Bundled  -- put the files in this folder and rebuild. Works offline.
  2) Hosted   -- push them to an  icons/  folder beside  maps/  in the public
                 repo (see IconConfig.BASE_URL). Keeps the APK small; each icon
                 is cached on the device the first time it is shown.
  3) Both     -- e.g. gear bundled, everything else hosted.

Until icons exist the app shows none and reserves no space for them, so the
lists look exactly as they did before. Opening any single item on the Items tab
is what discovers a hosted set; after that the result rows show icons too.

This README is ignored -- only files with an image extension count.
