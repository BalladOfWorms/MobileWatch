package com.balladofworms.mobilewatch.music

// FINAL FANTASY XI's .bgw music files, decoded on the phone with no native code.
//
// A .bgw is a small header and PlayStation-style 4-bit ADPCM ("PS-ADPCM") with a configurable
// frame size and no flag byte, interleaved frame by frame between the channels. The header also
// carries the loop point, so a track can be looped exactly as the game loops it. The layout
// follows vgmstream's BGW reader (meta/bgw.c, coding/psx_decoder.c), and this decoder was
// checked sample-for-sample against vgmstream's output: it is bit-exact.
//
// Header (little-endian):
//   0x00  "BGMStream\0\0\0"
//   0x0c  codec            (0 = PS-ADPCM; 3 = ATRAC3, never used by the music, not supported)
//   0x10  file size
//   0x14  file id          (usually the track number)
//   0x18  block count      -> samples = blocks * blockAlign
//   0x1c  loop start block -> loop start sample = (loop - 1) * blockAlign, no loop if <= 0
//   0x20  sample rate, obfuscated: (u32@0x20 + u32@0x24) & 0x7FFFFFFF
//   0x28  data offset
//   0x2e  channels
//   0x2f  blockAlign       -> each frame is blockAlign/2 + 1 bytes = 1 header + blockAlign/2 data

class BgwInfo(
    val codec: Int,
    val fileSize: Long,
    val fileId: Int,
    val sampleRate: Int,
    val dataOffset: Int,
    val channels: Int,
    val blockAlign: Int,
    val totalSamples: Long,          // per channel
    val loopStart: Long?,            // per channel, null = plays once
    val fingerprint: String,         // header bytes 0x10..0x27 as hex: same for every copy of a file
    val header: ByteArray            // the raw header, so a cached library can rebuild this
) {
    val seconds: Double get() = if (sampleRate > 0) totalSamples.toDouble() / sampleRate else 0.0
    val playable: Boolean get() = codec == 0 && channels in 1..2 && blockAlign >= 2 && sampleRate > 0

    companion object {
        const val HEADER_BYTES = 0x30

        /** Parse a header; null if this isn't a BGW file. */
        fun parse(h: ByteArray): BgwInfo? {
            if (h.size < HEADER_BYTES) return null
            val magic = String(h, 0, 9, Charsets.US_ASCII)
            if (magic != "BGMStream") return null
            fun u32(o: Int): Long =
                (h[o].toLong() and 0xFF) or ((h[o + 1].toLong() and 0xFF) shl 8) or
                ((h[o + 2].toLong() and 0xFF) shl 16) or ((h[o + 3].toLong() and 0xFF) shl 24)
            val codec = u32(0x0c).toInt()
            val blocks = u32(0x18)
            val loop = u32(0x1c).toInt()          // signed read
            val rate = ((u32(0x20) + u32(0x24)) and 0x7FFFFFFF).toInt()
            val channels = h[0x2e].toInt()
            val align = h[0x2f].toInt() and 0xFF
            val total = blocks * align
            val loopStart = if (loop > 0) (loop - 1).toLong() * align else null
            val fp = buildString { for (i in 0x10 until 0x28) append("%02x".format(h[i].toInt() and 0xFF)) }
            return BgwInfo(
                codec = codec, fileSize = u32(0x10), fileId = u32(0x14).toInt(),
                sampleRate = rate, dataOffset = u32(0x28).toInt(), channels = channels,
                blockAlign = align, totalSamples = total,
                loopStart = loopStart?.takeIf { it in 0 until total },
                fingerprint = fp,
                header = h.copyOf(HEADER_BYTES)
            )
        }
    }
}

/**
 * Streams one track's audio as interleaved STEREO 16-bit PCM (a mono track is doubled), so the
 * player never holds more than the file itself in memory.
 *
 * The decoder's state at the loop start is remembered the first time it passes it, so looping
 * back costs nothing and joins seamlessly. Seeking re-decodes silently from the start (or from
 * the loop start when that's behind the target) -- quick, since it is simple integer maths.
 */
class BgwStream(private val data: ByteArray, val info: BgwInfo) {
    private val ch = info.channels
    private val frameBytes = info.blockAlign / 2 + 1
    private val samplesPerFrame = (frameBytes - 1) * 2
    private val h1 = IntArray(ch)
    private val h2 = IntArray(ch)
    private var loopH1: IntArray? = null
    private var loopH2: IntArray? = null

    /** Next sample (per channel) to be decoded. */
    var position: Long = 0
        private set

    fun reset() {
        position = 0
        h1.fill(0); h2.fill(0)
    }

    fun seek(target: Long) {
        val t = target.coerceIn(0, info.totalSamples)
        val ls = info.loopStart
        val s1 = loopH1
        val s2 = loopH2
        if (ls != null && s1 != null && s2 != null && t >= ls && (t < position || position < ls)) {
            position = ls
            s1.copyInto(h1); s2.copyInto(h2)
        } else if (t < position) {
            reset()
        }
        decode(null, 0, (t - position).toInt())
    }

    /**
     * Decode up to [frames] sample frames into [out] as interleaved stereo. Returns how many were
     * written; fewer than asked means the end of the track was reached.
     */
    fun read(out: ShortArray, frames: Int): Int = decode(out, 0, frames)

    private fun decode(out: ShortArray?, outFrame: Int, count: Int): Int {
        val left = (info.totalSamples - position).coerceAtLeast(0)
        val n = minOf(count.toLong(), left).toInt()
        var o = outFrame * 2
        for (k in 0 until n) {
            val s = position + k
            if (s == info.loopStart && loopH1 == null) {
                loopH1 = h1.copyOf(); loopH2 = h2.copyOf()
            }
            val frame = s / samplesPerFrame
            val i = (s % samplesPerFrame).toInt()
            var left16 = 0
            var right16 = 0
            for (c in 0 until ch) {
                val off = info.dataOffset + ((frame * ch + c) * frameBytes).toInt()
                if (off + 1 + i / 2 >= data.size) { break }
                val hdr = data[off].toInt() and 0xFF
                var coef = (hdr shr 4) and 0xF
                var shift = hdr and 0xF
                if (coef > 4) coef = 0
                if (shift > 12) shift = 9
                val byte = data[off + 1 + i / 2].toInt() and 0xFF
                val nib = if (i and 1 == 1) (byte shr 4) and 0xF else byte and 0xF
                var smp = ((nib shl 12) and 0xF000).toShort().toInt() shr shift
                smp += (COEF1[coef] * h1[c] + COEF2[coef] * h2[c]) shr 6
                if (smp > 32767) smp = 32767 else if (smp < -32768) smp = -32768
                h2[c] = h1[c]; h1[c] = smp
                if (c == 0) left16 = smp else right16 = smp
            }
            if (out != null) {
                out[o] = left16.toShort()
                out[o + 1] = (if (ch == 1) left16 else right16).toShort()
                o += 2
            }
        }
        position += n
        return n
    }

    companion object {
        private val COEF1 = intArrayOf(0, 60, 115, 98, 122)
        private val COEF2 = intArrayOf(0, 0, -52, -55, -60)
    }
}
