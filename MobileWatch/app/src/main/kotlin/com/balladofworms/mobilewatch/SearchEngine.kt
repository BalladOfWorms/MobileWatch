package com.balladofworms.mobilewatch

import java.net.InetSocketAddress
import java.net.Socket
import java.security.MessageDigest
import java.util.Base64

/**
 * MobileWatch search-server engine — Kotlin port of the proven Python engine.
 *
 * Pure Kotlin/JVM (no Android imports), so this file drops unchanged into the
 * Android app. It speaks the FFXI search-server protocol: a Blowfish-encrypted
 * TCP request/reply on <world-ip>:54002, answered unauthenticated (no game
 * running). Validated byte-for-byte against the reference Python implementation
 * (MD5 framing, Blowfish key schedule incl. the signed-int8 quirk, enciphering,
 * and every request builder produce identical bytes).
 */
object SearchEngine {

    const val PORT = 54002
    private const val IXFF = 0x46465849
    private val KEY_SEED = byteArrayOf(
        0x30, 0x73, 0x3D, 0x6D, 0x3C, 0x31, 0x49, 0x5A,
        0x32, 0x7A, 0x42, 0x43, 0x63, 0x38, 0x7B, 0x7E
    )

    // Blowfish base P/S subkeys (little-endian u32 stream), base64-encoded.
    private const val SUBKEY_B64 =
        "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"

    private val baseP = IntArray(18)
    private val baseS = IntArray(1024)

    init {
        val sk = Base64.getDecoder().decode(SUBKEY_B64)
        for (i in 0 until 18) baseP[i] = u32le(sk, i * 4)
        for (i in 0 until 1024) baseS[i] = u32le(sk, 72 + i * 4)
    }

    // ---- little-endian byte helpers ----
    private fun u16le(b: ByteArray, o: Int) = (b[o].toInt() and 0xFF) or ((b[o + 1].toInt() and 0xFF) shl 8)
    private fun u32le(b: ByteArray, o: Int) = (b[o].toInt() and 0xFF) or
        ((b[o + 1].toInt() and 0xFF) shl 8) or ((b[o + 2].toInt() and 0xFF) shl 16) or
        ((b[o + 3].toInt() and 0xFF) shl 24)
    private fun putU16le(b: ByteArray, o: Int, v: Int) { b[o] = v.toByte(); b[o + 1] = (v ushr 8).toByte() }
    private fun putU32le(b: ByteArray, o: Int, v: Int) {
        b[o] = v.toByte(); b[o + 1] = (v ushr 8).toByte(); b[o + 2] = (v ushr 16).toByte(); b[o + 3] = (v ushr 24).toByte()
    }
    private fun md5(b: ByteArray): ByteArray = MessageDigest.getInstance("MD5").digest(b)

    // ---- Blowfish ----
    private fun tt(x: Int, s: IntArray): Int =
        ((s[256 + ((x ushr 8) and 0xFF)] and 1) xor 32) +
        ((s[768 + ((x ushr 24) and 0xFF)] and 1) xor 32) +
        s[512 + ((x ushr 16) and 0xFF)] + s[x and 0xFF]

    private fun encipher(xl0: Int, xr0: Int, p: IntArray, s: IntArray): IntArray {
        var xl = xl0; var xr = xr0
        for (i in 0 until 16) { xl = xl xor p[i]; xr = tt(xl, s) xor xr; val t = xl; xl = xr; xr = t }
        val t = xl; xl = xr; xr = t
        xr = xr xor p[16]; xl = xl xor p[17]
        return intArrayOf(xl, xr)
    }
    private fun decipher(xl0: Int, xr0: Int, p: IntArray, s: IntArray): IntArray {
        var xl = xl0; var xr = xr0
        for (i in 17 downTo 2) { xl = xl xor p[i]; xr = tt(xl, s) xor xr; val t = xl; xl = xr; xr = t }
        val t = xl; xl = xr; xr = t
        xr = xr xor p[1]; xl = xl xor p[0]
        return intArrayOf(xl, xr)
    }
    private fun blowfishInit(key: ByteArray): Pair<IntArray, IntArray> {
        val p = baseP.copyOf(); val s = baseS.copyOf()
        val n = key.size; var j = 0
        for (i in 0 until 18) {
            var data = 0
            repeat(4) { data = (data shl 8) or key[j].toInt(); j++; if (j >= n) j = 0 } // toInt() sign-extends: matches server's signed-int8 key
            p[i] = p[i] xor data
        }
        var dl = 0; var dr = 0
        var i = 0
        while (i < 18) { val e = encipher(dl, dr, p, s); dl = e[0]; dr = e[1]; p[i] = dl; p[i + 1] = dr; i += 2 }
        for (blk in 0 until 4) { var k = 0; while (k < 256) { val e = encipher(dl, dr, p, s); dl = e[0]; dr = e[1]; s[blk * 256 + k] = dl; s[blk * 256 + k + 1] = dr; k += 2 } }
        return Pair(p, s)
    }
    private fun cipherBlocks(buf: ByteArray, length: Int, p: IntArray, s: IntArray, decrypt: Boolean) {
        var tmp = (length - 12) / 4; tmp -= tmp % 2; var i = 0
        while (i < tmp) {
            val o = 8 + i * 4
            val r = if (decrypt) decipher(u32le(buf, o), u32le(buf, o + 4), p, s)
                    else encipher(u32le(buf, o), u32le(buf, o + 4), p, s)
            putU32le(buf, o, r[0]); putU32le(buf, o + 4, r[1]); i += 2
        }
    }

    // ---- little-endian bit packer (for the player-search filter payload) ----
    private fun packBE(t: ByteArray, value: Long, byteOff0: Int, bitOff0: Int, nbits: Int) {
        val byteOff = byteOff0 + (bitOff0 shr 3); val bitOff = bitOff0 and 7
        var bm = (-1L ushr (64 - nbits)) shl bitOff
        val v = (value shl bitOff) and bm; bm = bm.inv()
        val ab = (bitOff + nbits + 7) / 8
        var data = 0L
        for (c in 0 until ab) data = data or ((t[byteOff + c].toLong() and 0xFF) shl (8 * c))
        data = (data and bm) or v
        for (c in 0 until ab) t[byteOff + c] = ((data ushr (8 * c)) and 0xFF).toByte()
    }
    private fun packLE(t: ByteArray, value: Long, bitOff0: Int, nbits: Int): Int {
        val byteOff = bitOff0 shr 3; val bitOff = bitOff0 and 7
        val x = bitOff + nbits
        val need = if (x <= 8) 1 else if (x <= 16) 2 else if (x <= 32) 4 else 8
        val ab = (bitOff + nbits + 7) / 8
        val m = ByteArray(need)
        for (c in 0 until ab) m[need - 1 - c] = t[byteOff + c]
        packBE(m, value, 0, (need shl 3) - (bitOff + nbits), nbits)
        for (c in 0 until ab) t[byteOff + c] = m[need - 1 - c]
        return (byteOff shl 3) + bitOff + nbits
    }

    private fun finishAndEncrypt(buf: ByteArray, length: Int, keyTail: ByteArray) {
        val h = md5(buf.copyOfRange(0x08, length - 0x14))
        System.arraycopy(h, 0, buf, length - 0x14, 16)
        System.arraycopy(keyTail, 0, buf, length - 0x04, 4)
        val (p, s) = blowfishInit(md5(KEY_SEED + keyTail))
        cipherBlocks(buf, length, p, s, false)
    }
    private fun randKeyTail(): ByteArray {
        val b = ByteArray(4); java.security.SecureRandom().nextBytes(b); return b
    }

    // ---- request builders ----
    fun buildHistoryRequest(itemId: Int, stack: Boolean, keyTail: ByteArray = randKeyTail()): ByteArray {
        val length = 268; val buf = ByteArray(length)
        putU16le(buf, 0x00, length); putU32le(buf, 0x04, IXFF); putU16le(buf, 0x08, 184)
        buf[0x0A] = 0x80.toByte(); buf[0x0B] = (if (stack) 0x06 else 0x05).toByte()
        putU16le(buf, 0x12, itemId and 0xFFFF); buf[0x14] = 0x04.toByte(); buf[0x15] = (if (stack) 1 else 0).toByte()
        finishAndEncrypt(buf, length, keyTail); return buf
    }
    fun buildCategoryRequest(cat: Int, keyTail: ByteArray = randKeyTail()): ByteArray {
        val length = 268; val buf = ByteArray(length)
        putU16le(buf, 0x00, length); putU32le(buf, 0x04, IXFF); putU16le(buf, 0x08, 184)
        buf[0x0A] = 0x80.toByte(); buf[0x0B] = 0x15.toByte()
        putU16le(buf, 0x0E, 1); buf[0x12] = 1.toByte(); putU16le(buf, 0x14, 4); buf[0x16] = (cat and 0xFF).toByte()
        putU32le(buf, 0x18, 2); putU32le(buf, 0x1C, 2)
        finishAndEncrypt(buf, length, keyTail); return buf
    }
    fun buildMoreRequest(keyTail: ByteArray = randKeyTail()): ByteArray {
        val length = 76; val buf = ByteArray(length)
        putU16le(buf, 0x00, length); putU32le(buf, 0x04, IXFF); putU16le(buf, 0x08, 16)
        buf[0x0A] = 0x80.toByte(); buf[0x0B] = 0x10.toByte(); putU16le(buf, 0x10, 3); putU16le(buf, 0x12, 1)
        finishAndEncrypt(buf, length, keyTail); return buf
    }
    /** Player-search request. No filters -> reply's Total is the live population. */
    fun buildSearchRequest(job: Int? = null, searchAll: Boolean = true, keyTail: ByteArray = randKeyTail()): ByteArray {
        val pl = ByteArray(48); var off = 0
        if (job != null) { off = packLE(pl, 3, off, 5); off = packLE(pl, 0, off, 1); off = packLE(pl, 1, off, 1); off = packLE(pl, (job and 0x1F).toLong(), off, 5) }
        val nbytes = (off + 7) / 8
        val length = 76; val buf = ByteArray(length)
        putU16le(buf, 0x00, length); putU32le(buf, 0x04, IXFF); putU16le(buf, 0x08, 16)
        buf[0x0A] = 0x80.toByte(); buf[0x0B] = (if (searchAll) 0x00 else 0x03).toByte(); buf[0x10] = nbytes.toByte()
        System.arraycopy(pl, 0, buf, 0x11, nbytes)
        finishAndEncrypt(buf, length, keyTail); return buf
    }

    // ---- reply parsing ----
    private fun decodeName(raw: ByteArray): String {
        val z = raw.indexOf(0.toByte()); val end = if (z >= 0) z else raw.size
        return String(raw, 0, end, Charsets.ISO_8859_1).trim()
    }
    data class Sale(val price: Int, val date: Long, val seller: String, val buyer: String)
    data class History(val ok: Boolean, val itemId: Int = 0, val soldCount: Int = 0, val category: Int = 0, val sales: List<Sale> = emptyList())

    fun parseHistory(data: ByteArray, key2: ByteArray = ByteArray(4)): History {
        if (data.size < 28) return History(false)
        val buf = data.copyOf(); val length = u16le(buf, 0)
        if (length < 28 || length > buf.size) return History(false)
        val (p, s) = blowfishInit(md5(KEY_SEED + buf.copyOfRange(length - 4, length) + key2))
        cipherBlocks(buf, length, p, s, true)
        if (md5(buf.copyOfRange(8, length - 0x14)).let { !it.contentEquals(buf.copyOfRange(length - 0x14, length - 0x04)) }) return History(false)
        if ((buf[0x0B].toInt() and 0x1F) != 0x05 && (buf[0x0B].toInt() and 0x1F) != 0x06) return History(false)
        val itemId = u16le(buf, 0x18); val count = u32le(buf, 0x1A); val cat = u16le(buf, 0x1E)
        val marker = u16le(buf, 0x08); val nrec = maxOf(0, (marker - 0x20) / 40)
        val sales = ArrayList<Sale>()
        for (i in 0 until nrec) {
            val o = 0x20 + 40 * i; if (o + 40 > length - 0x14) break
            sales.add(Sale(u32le(buf, o), u32le(buf, o + 4).toLong() and 0xFFFFFFFFL,
                decodeName(buf.copyOfRange(o + 0x08, o + 0x18)), decodeName(buf.copyOfRange(o + 0x18, o + 0x28))))
        }
        return History(true, itemId, count, cat, sales)
    }

    /** Player-search reply carries the total match count (u16 @ 0x0E); reply type byte is 0x80. */
    fun parseSearchCount(data: ByteArray, key2: ByteArray = ByteArray(4)): Int? {
        if (data.size < 28) return null
        val buf = data.copyOf(); val length = u16le(buf, 0)
        if (length < 28 || length > buf.size) return null
        val (p, s) = blowfishInit(md5(KEY_SEED + buf.copyOfRange(length - 4, length) + key2))
        cipherBlocks(buf, length, p, s, true)
        if (buf[0x0B].toInt() and 0xFF != 0x80) return null
        return u16le(buf, 0x0E)
    }

    // ---- networking ----
    private fun recvPacket(sock: Socket, timeoutMs: Int): ByteArray {
        sock.soTimeout = timeoutMs
        val ins = sock.getInputStream(); val out = java.io.ByteArrayOutputStream(); val chunk = ByteArray(4096)
        try {
            while (true) {
                val n = ins.read(chunk); if (n <= 0) break
                out.write(chunk, 0, n)
                val d = out.toByteArray()
                if (d.size >= 2 && d.size >= u16le(d, 0)) break
            }
        } catch (_: java.net.SocketTimeoutException) {}
        return out.toByteArray()
    }
    private fun send(host: String, req: ByteArray, timeoutMs: Int): ByteArray {
        Socket().use { s -> s.connect(InetSocketAddress(host, PORT), timeoutMs); s.getOutputStream().write(req); return recvPacket(s, timeoutMs) }
    }

    fun queryHistory(host: String, itemId: Int, stack: Boolean, timeoutMs: Int = 8000): History =
        parseHistory(send(host, buildHistoryRequest(itemId, stack), timeoutMs))

    /** Live online population of one world (null if no/invalid reply). */
    fun queryPopulation(host: String, timeoutMs: Int = 8000): Int? =
        parseSearchCount(send(host, buildSearchRequest(), timeoutMs))

    /** Median of one item's recent single-sale prices on one world, or null. */
    fun medianPrice(host: String, itemId: Int, stack: Boolean = false, timeoutMs: Int = 6000): Int? {
        val h = try { queryHistory(host, itemId, stack, timeoutMs) } catch (_: Exception) { return null }
        if (!h.ok) return null
        val prices = h.sales.map { it.price }.filter { it > 0 }.sorted()
        if (prices.isEmpty()) return null
        val m = prices.size
        return if (m % 2 == 1) prices[m / 2] else ((prices[m / 2 - 1] + prices[m / 2]) / 2)
    }

    // ---- AH category listing (current on-sale counts per item) ----
    /** Parse one 0x95 listing page -> (itemId -> (singleCount, stackCount), total, isLast) or null. */
    private fun parseListing(data: ByteArray, key2: ByteArray): Triple<Map<Int, Pair<Int, Int>>, Int, Boolean>? {
        if (data.size < 2) return null
        val buf = data.copyOf(); val length = u16le(buf, 0)
        if (length < 28 || length > buf.size) return null
        val (p, s) = blowfishInit(md5(KEY_SEED + buf.copyOfRange(length - 4, length) + key2))
        cipherBlocks(buf, length, p, s, true)
        if (buf[0x0B].toInt() and 0xFF != 0x95) return null
        val total = u16le(buf, 0x0E)
        val end = u16le(buf, 0x08)
        val isLast = (buf[0x0A].toInt() and 0xFF) == 0x80
        val items = HashMap<Int, Pair<Int, Int>>()
        val n = maxOf(0, (end - 0x18) / 10)
        for (i in 0 until n) {
            val o = 0x18 + 10 * i; if (o + 10 > length) break
            items[u16le(buf, o)] = Pair(u32le(buf, o + 2), u32le(buf, o + 6))
        }
        return Triple(items, total, isLast)
    }

    /** Query one AH category and return itemId -> (singlesOnSale, stacksOnSale). 0xFFFFFFFF.toInt() = "none of that form". */
    fun queryCategoryCounts(host: String, cat: Int, timeoutMs: Int = 8000): Map<Int, Pair<Int, Int>> {
        val key2 = ByteArray(4)
        val items = HashMap<Int, Pair<Int, Int>>()
        Socket().use { sock ->
            sock.connect(InetSocketAddress(host, PORT), timeoutMs)
            sock.getOutputStream().write(buildCategoryRequest(cat))
            var guard = 0
            while (guard < 80) {
                val page = parseListing(recvPacket(sock, timeoutMs), key2) ?: break
                items.putAll(page.first)
                if (page.third || items.size >= page.second) break
                sock.getOutputStream().write(buildMoreRequest())
                guard++
            }
        }
        return items
    }
}

