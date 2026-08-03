#!/usr/bin/env python3
"""
REV 411 — labels no longer break mid-word ("Bestiar / y", "G u i l d").

THREE SEPARATE BUGS THAT LOOK LIKE ONE
--------------------------------------
All three are label/value rows, and all three fail the same way on a phone with
a large display-font setting, but the causes differ:

1. THE WEIGHT TRAP  (18+ rows: Guild, Hours, Level, Rank, Plant Type, ...)
   Written as:
       Text("Guild",     ... modifier = Modifier.weight(1f))   <- LABEL weighted
       Text(info.guild,  ...)                                  <- VALUE unweighted
   A Row measures UNWEIGHTED children FIRST and gives weighted ones only what
   is left. So a long value ("Green Thumb Moogle / Chacharoon") takes the whole
   row and the label is squeezed toward zero width — which is why "Guild" came
   out as one letter per line. The weight is on exactly the wrong child.
   FIX: the label sizes to its own text and never wraps; the VALUE takes
   weight(1f) and wraps. Right-alignment is preserved with TextAlign.End.

2. HARD-CODED LABEL WIDTHS  (Settings > Defaults 60.dp, AboutLine 72.dp)
   `Modifier.width(60.dp)` is a fixed box, but `fontSize = 13.sp` GROWS with the
   user's font-scale setting. At large scale "Bestiary" no longer fits 60.dp and
   wraps to "Besti / ary". dp does not scale with fonts; sp does. Any fixed dp
   holding sp text is a latent break.
   FIX: `widthIn(min = ...)` — same column alignment when the text is small,
   room to grow when it is not.

3. maxLines = 1 IS NOT ENOUGH  (the two 92.dp resist-grid labels)
   maxLines caps the line COUNT but still lets the layout wrap and then clip.
   `softWrap = false` is what actually stops the break.

WHY NOT JUST WIDEN THE dp: because the next font-scale step breaks it again.
The row now measures itself from the text it is given, so it holds at any scale.
"""
import re
import sys

P = 'app/src/main/kotlin/com/balladofworms/mobilewatch/ui/MobileWatchApp.kt'
src = open(P, encoding='utf-8').read()
lines = src.split('\n')
orig = list(lines)

# A label sized to its own text, never broken. widthIn keeps the column aligned
# for short labels without capping long ones.
LABEL_MIN = 88

# --- 1. the weight trap ------------------------------------------------------
lab = re.compile(r'^(\s*)Text\("([^"]+)", color = TextMuted, fontSize = (\d+)\.sp, '
                 r'modifier = Modifier\.weight\(1f\)\)$')
val = re.compile(r'^(\s*)Text\((.+?), color = ([\w()\. ]+?), fontSize = (\d+)\.sp\)$')

fixed_pairs = []
i = 0
while i < len(lines) - 1:
    m = lab.match(lines[i])
    if m:
        v = val.match(lines[i + 1])
        if v:
            ind, label, size = m.group(1), m.group(2), m.group(3)
            lines[i] = ('%sText("%s", color = TextMuted, fontSize = %s.sp, maxLines = 1, '
                        'softWrap = false, modifier = Modifier.widthIn(min = %d.dp))'
                        % (ind, label, size, LABEL_MIN))
            lines[i + 1] = ('%sText(%s, color = %s, fontSize = %s.sp, textAlign = TextAlign.End, '
                            'modifier = Modifier.weight(1f))'
                            % (v.group(1), v.group(2), v.group(3), v.group(4)))
            fixed_pairs.append((i + 1, label))
            i += 2
            continue
    i += 1

print('=== 1. THE WEIGHT TRAP — label was weighted, value was not ===')
print('  rows repaired: %d' % len(fixed_pairs))
for ln, label in fixed_pairs:
    print('     line %-5d %s' % (ln, label))

# --- 2. hard-coded label widths ---------------------------------------------
print('\n=== 2. FIXED dp WIDTHS HOLDING sp TEXT ===')
FIXED = [
    ('Text("Bestiary", color = TextMuted, fontSize = 13.sp, modifier = Modifier.width(60.dp))',
     'Text("Bestiary", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, '
     'modifier = Modifier.widthIn(min = 60.dp))', 'Settings > Defaults'),
    ('Text("Zones", color = TextMuted, fontSize = 13.sp, modifier = Modifier.width(60.dp))',
     'Text("Zones", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, '
     'modifier = Modifier.widthIn(min = 60.dp))', 'Settings > Defaults'),
    ('Text(tab, color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,\n'
     '            modifier = Modifier.width(72.dp))',
     'Text(tab, color = AccentGold, fontSize = 12.sp, fontWeight = FontWeight.SemiBold,\n'
     '            maxLines = 1, softWrap = false, modifier = Modifier.widthIn(min = 72.dp))',
     'Settings > About (AboutLine)'),
]
text = '\n'.join(lines)
for old, new, where in FIXED:
    n = text.count(old)
    if n != 1:
        sys.exit('!! expected exactly 1 match for %s, found %d' % (where, n))
    text = text.replace(old, new)
    print('  %-32s width(...) -> widthIn(min = ...), softWrap = false' % where)

# --- 3. maxLines = 1 without softWrap = false --------------------------------
print('\n=== 3. maxLines = 1 CAPS THE LINE COUNT BUT STILL WRAPS THEN CLIPS ===')
SOFT = [
    ('Text("$label:", color = TextMuted, fontSize = 13.sp, maxLines = 1, '
     'modifier = Modifier.width(92.dp))',
     'Text("$label:", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, '
     'modifier = Modifier.widthIn(min = 92.dp))', 'resist grid label'),
    ('Text("Physical:", color = TextMuted, fontSize = 13.sp, maxLines = 1, '
     'modifier = Modifier.width(92.dp))',
     'Text("Physical:", color = TextMuted, fontSize = 13.sp, maxLines = 1, softWrap = false, '
     'modifier = Modifier.widthIn(min = 92.dp))', 'resist grid Physical'),
]
for old, new, where in SOFT:
    n = text.count(old)
    if n != 1:
        sys.exit('!! expected exactly 1 match for %s, found %d' % (where, n))
    text = text.replace(old, new)
    print('  %-32s + softWrap = false, widthIn' % where)

# --- guards ------------------------------------------------------------------
print('\n=== GUARDS ===')
for ch, cl in (('{', '}'), ('(', ')'), ('[', ']')):
    a, b = text.count(ch), text.count(cl)
    print('  %s %d  %s %d  %s' % (ch, a, cl, b, 'balanced' if a == b else '!! UNBALANCED !!'))
    assert a == b
assert 'TextAlign' in text and 'import androidx.compose.ui.text.style.TextAlign' in text
assert text.count('modifier = Modifier.weight(1f))\n') >= len(fixed_pairs)
leftover = re.findall(r'Text\("[^"]+", color = TextMuted, fontSize = \d+\.sp, '
                      r'modifier = Modifier\.weight\(1f\)\)', text)
print('  weighted labels still remaining: %d %s'
      % (len(leftover), [re.search(r'"([^"]+)"', s).group(1) for s in leftover]))
print('  line count: %d -> %d' % (len(orig), text.count('\n') + 1))

open(P, 'w', encoding='utf-8', newline='\n').write(text)
print('\nwritten: %s' % P)
