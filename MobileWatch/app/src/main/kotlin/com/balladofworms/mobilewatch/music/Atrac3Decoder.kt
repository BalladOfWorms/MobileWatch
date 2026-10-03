/*
 * ATRAC3 decoder -- a Kotlin port of FFmpeg's ATRAC3 decoder, for FINAL FANTASY XI's newer
 * .bgw music.
 *
 * Original C code: libavcodec/atrac3.c and libavcodec/atrac.c from FFmpeg
 *   Copyright (c) 2006-2008 Maxim Poliakovski
 *   Copyright (c) 2006-2008 Benjamin Larsson
 * Kotlin port for MobileWatch by BalladOfWorms.
 *
 * This file (only) is free software; you can redistribute it and/or modify it under the terms
 * of the GNU Lesser General Public License as published by the Free Software Foundation;
 * either version 2.1 of the License, or (at your option) any later version.
 *
 * It is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
 * the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details: https://www.gnu.org/licenses/lgpl-2.1.html
 *
 * Covers what FFXI uses: ATRAC3 in single-channel coding (each channel its own sound unit),
 * plus joint stereo for completeness. Output is float, about -1..1.
 */
package com.balladofworms.mobilewatch.music

import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.pow
import kotlin.math.sin
import kotlin.math.sqrt

class Atrac3Decoder(private val channels: Int, private val blockAlign: Int, jointStereo: Boolean) {

    private val codingMode = if (jointStereo) JOINT_STEREO else SINGLE

    // ── bit reader (MSB first) ───────────────────────────────────────
    private var buf = ByteArray(0)
    private var bitPos = 0
    private var bitEnd = 0

    private fun initBits(b: ByteArray, startByte: Int, bytes: Int) {
        buf = b; bitPos = startByte * 8; bitEnd = (startByte + bytes) * 8
    }

    private fun bit(): Int {
        if (bitPos >= bitEnd) { bitPos++; return 0 }
        val v = (buf[bitPos ushr 3].toInt() ushr (7 - (bitPos and 7))) and 1
        bitPos++
        return v
    }

    private fun bits(n: Int): Int { var v = 0; repeat(n) { v = (v shl 1) or bit() }; return v }
    private fun sbits(n: Int): Int { val v = bits(n); return (v shl (32 - n)) shr (32 - n) }
    private fun showBits(n: Int): Int { val p = bitPos; val v = bits(n); bitPos = p; return v }

    private fun vlc(table: Int): Int {
        // Canonical codes, short tables: walk them bit by bit.
        val t = VLC[table]
        var code = 0
        var len = 0
        while (len < 8) {
            code = (code shl 1) or bit(); len++
            val sym = t[len][code]
            if (sym != NONE) return sym
        }
        return 0
    }

    // ── state ────────────────────────────────────────────────────────
    private class Gain { var num = 0; val lev = IntArray(7); val loc = IntArray(7) }
    private class Tonal { var pos = 0; var num = 0; val coef = FloatArray(8) }

    private inner class Unit {
        var bandsCoded = 0
        var numComponents = 0
        val prevFrame = FloatArray(SAMPLES)
        var gcSwitch = 0
        val components = Array(64) { Tonal() }
        val gain = Array(2) { Array(4) { Gain() } }
        val spectrum = FloatArray(SAMPLES)
        val imdct = FloatArray(SAMPLES)
        val delay1 = FloatArray(46)
        val delay2 = FloatArray(46)
        val delay3 = FloatArray(46)
    }

    private val units = Array(channels) { Unit() }
    private val temp = FloatArray(1070)
    private val decodedBytes = ByteArray(blockAlign + 8)
    private val mcPrev = Array(4) { IntArray(4) { 3 } }
    private val mcNow = Array(4) { IntArray(4) { 3 } }
    private val mcNext = Array(4) { IntArray(4) { 3 } }
    private val weighting = Array(4) { intArrayOf(0, 7, 0, 7, 0, 7) }
    private val mantissas = IntArray(128)
    private val out = Array(channels) { FloatArray(SAMPLES) }

    /** Decode one frame of [blockAlign] bytes at [off]; returns per-channel 1024 samples, or
     *  null if the frame is broken (the caller plays silence for it). */
    fun decodeFrame(data: ByteArray, off: Int): Array<FloatArray>? {
        if (!decode(data, off)) return null
        return out
    }

    private fun decode(data: ByteArray, off: Int): Boolean {
        if (codingMode == JOINT_STEREO) {
            val jsAlign = (blockAlign / channels) * 2
            var ch = 0
            while (ch < channels) {
                val pair = ch / 2
                val base = off + pair * jsAlign
                initBits(data, base, jsAlign)
                if (!soundUnit(units[ch], out[ch], ch)) return false
                for (i in 0 until jsAlign) decodedBytes[i] = data[base + jsAlign - 1 - i]
                var p = 0
                var i = 4
                while ((decodedBytes[p].toInt() and 0xFF) == 0xF8) {
                    if (i >= jsAlign) return false
                    i++; p++
                }
                initBits(decodedBytes, p, jsAlign - p)
                val w = weighting[pair]
                System.arraycopy(w, 2, w, 0, 4)
                w[4] = bit(); w[5] = bits(3)
                for (k in 0 until 4) {
                    mcPrev[pair][k] = mcNow[pair][k]
                    mcNow[pair][k] = mcNext[pair][k]
                    mcNext[pair][k] = bits(2)
                }
                if (!soundUnit(units[ch + 1], out[ch + 1], ch + 1)) return false
                reverseMatrixing(out[ch], out[ch + 1], mcPrev[pair], mcNow[pair])
                channelWeighting(out[ch], out[ch + 1], w)
                ch += 2
            }
        } else {
            val per = blockAlign / channels
            for (i in 0 until channels) {
                initBits(data, off + i * per, per)
                if (!soundUnit(units[i], out[i], i)) return false
            }
        }
        for (i in 0 until channels) {
            val o = out[i]
            val u = units[i]
            iqmf(o, 0, o, 256, 256, o, 0, u.delay1)
            iqmf(o, 768, o, 512, 256, o, 512, u.delay2)
            iqmf(o, 0, o, 512, 512, o, 0, u.delay3)
        }
        return true
    }

    // ── sound unit ───────────────────────────────────────────────────
    private fun soundUnit(u: Unit, output: FloatArray, ch: Int): Boolean {
        val gain1 = u.gain[u.gcSwitch]
        val gain2 = u.gain[1 - u.gcSwitch]
        if (codingMode == JOINT_STEREO && ch % 2 == 1) {
            if (bits(2) != 3) return false
        } else if (bits(6) != 0x28) return false

        u.bandsCoded = bits(2)
        if (!gainControl(gain2, u.bandsCoded)) return false
        u.numComponents = tonalComponents(u.components, u.bandsCoded)
        if (u.numComponents < 0) return false
        val numSubbands = spectrum(u.spectrum)

        var lastTonal = -1
        for (i in 0 until u.numComponents) {
            val c = u.components[i]
            lastTonal = maxOf(c.pos + c.num, lastTonal)
            for (j in 0 until c.num) u.spectrum[c.pos + j] += c.coef[j]
        }
        var numBands = (SUBBAND[numSubbands + 1] - 1) shr 8
        if (lastTonal >= 0) numBands = maxOf((lastTonal + 256) shr 8, numBands)

        for (band in 0 until 4) {
            if (band <= numBands) imlt(u.spectrum, band * 256, u.imdct, band and 1 == 1)
            else u.imdct.fill(0f, 0, 512)
            gainCompensation(u.imdct, u.prevFrame, band * 256, gain1[band], gain2[band], 256,
                output, band * 256)
        }
        u.gcSwitch = u.gcSwitch xor 1
        return true
    }

    private fun gainControl(block: Array<Gain>, numBands: Int): Boolean {
        var b = 0
        while (b <= numBands) {
            val g = block[b]
            g.num = bits(3)
            for (j in 0 until g.num) {
                g.lev[j] = bits(4)
                g.loc[j] = bits(5)
                if (j > 0 && g.loc[j] <= g.loc[j - 1]) return false
            }
            b++
        }
        while (b < 4) { block[b].num = 0; b++ }
        return true
    }

    private fun tonalComponents(comps: Array<Tonal>, numBands: Int): Int {
        val nb = bits(5)
        if (nb == 0) return 0
        val selector = bits(2)
        if (selector == 2) return -1
        var codingMode = selector and 1
        val bandFlags = IntArray(4)
        val mant = IntArray(8)
        var count = 0
        for (i in 0 until nb) {
            for (b in 0..numBands) bandFlags[b] = bit()
            val perComponent = bits(3)
            val quantStep = bits(3)
            if (quantStep <= 1) return -1
            if (selector == 3) codingMode = bit()
            for (b in 0 until (numBands + 1) * 4) {
                if (bandFlags[b shr 2] == 0) continue
                val coded = bits(3)
                for (c in 0 until coded) {
                    val sf = bits(6)
                    if (count >= 64) return -1
                    val cmp = comps[count]
                    cmp.pos = b * 64 + bits(6)
                    val n = minOf(SAMPLES - cmp.pos, perComponent + 1)
                    val scale = SF_TABLE[sf] * INV_MAX_QUANT[quantStep]
                    quantSpectral(quantStep, codingMode, mant, n)
                    cmp.num = n
                    for (m in 0 until n) cmp.coef[m] = mant[m] * scale
                    count++
                }
            }
        }
        return count
    }

    private fun quantSpectral(selector: Int, clc: Int, out: IntArray, numCodes0: Int) {
        var numCodes = numCodes0
        if (selector == 1) numCodes /= 2
        if (clc != 0) {
            val nb = CLC_LENGTH[selector]
            if (selector > 1) {
                for (i in 0 until numCodes) out[i] = if (nb != 0) sbits(nb) else 0
            } else {
                for (i in 0 until numCodes) {
                    val code = if (nb != 0) bits(nb) else 0
                    out[i * 2] = MANT_CLC[code shr 2]
                    out[i * 2 + 1] = MANT_CLC[code and 3]
                }
            }
        } else {
            if (selector != 1) {
                for (i in 0 until numCodes) out[i] = vlc(selector - 1)
            } else {
                for (i in 0 until numCodes) {
                    val s = vlc(0)
                    out[i * 2] = MANT_VLC[s * 2]
                    out[i * 2 + 1] = MANT_VLC[s * 2 + 1]
                }
            }
        }
    }

    private fun spectrum(output: FloatArray): Int {
        val numSubbands = bits(5)
        val clc = bit()
        val vlcIndex = IntArray(32)
        val sfIndex = IntArray(32)
        for (i in 0..numSubbands) vlcIndex[i] = bits(3)
        for (i in 0..numSubbands) if (vlcIndex[i] != 0) sfIndex[i] = bits(6)
        var i = 0
        while (i <= numSubbands) {
            var first = SUBBAND[i]
            val last = SUBBAND[i + 1]
            if (vlcIndex[i] != 0) {
                quantSpectral(vlcIndex[i], clc, mantissas, last - first)
                val scale = SF_TABLE[sfIndex[i]] * INV_MAX_QUANT[vlcIndex[i]]
                var j = 0
                while (first < last) { output[first] = mantissas[j] * scale; first++; j++ }
            } else output.fill(0f, first, last)
            i++
        }
        output.fill(0f, SUBBAND[i], SAMPLES)
        return numSubbands
    }

    // ── joint stereo ─────────────────────────────────────────────────
    private fun interp(old: Float, new: Float, n: Int) = old + n * 0.125f * (new - old)

    private fun reverseMatrixing(su1: FloatArray, su2: FloatArray, prev: IntArray, cur: IntArray) {
        var band = 0
        var i = 0
        while (band < 1024) {
            val s1 = prev[i]
            val s2 = cur[i]
            var n = band
            if (s1 != s2) {
                val l1 = MATRIX[s1 * 2]; val r1 = MATRIX[s1 * 2 + 1]
                val l2 = MATRIX[s2 * 2]; val r2 = MATRIX[s2 * 2 + 1]
                while (n < band + 8) {
                    val c1 = su1[n]; var c2 = su2[n]
                    c2 = c1 * interp(l1, l2, n - band) + c2 * interp(r1, r2, n - band)
                    su1[n] = c2; su2[n] = c1 * 2f - c2
                    n++
                }
            }
            when (s2) {
                0 -> while (n < band + 256) { val c1 = su1[n]; val c2 = su2[n]; su1[n] = c2 * 2f; su2[n] = (c1 - c2) * 2f; n++ }
                1 -> while (n < band + 256) { val c1 = su1[n]; val c2 = su2[n]; su1[n] = (c1 + c2) * 2f; su2[n] = c2 * -2f; n++ }
                else -> while (n < band + 256) { val c1 = su1[n]; val c2 = su2[n]; su1[n] = c1 + c2; su2[n] = c1 - c2; n++ }
            }
            band += 256; i++
        }
    }

    private fun weights(index: Int, flag: Int): FloatArray {
        if (index == 7) return floatArrayOf(1f, 1f)
        val a = (index and 7) / 7f
        val b = sqrt(2 - a * a)
        return if (flag != 0) floatArrayOf(b, a) else floatArrayOf(a, b)
    }

    private fun channelWeighting(su1: FloatArray, su2: FloatArray, p3: IntArray) {
        if (p3[1] == 7 && p3[3] == 7) return
        val w0 = weights(p3[1], p3[0])
        val w1 = weights(p3[3], p3[2])
        var band = 256
        while (band < 1024) {
            var n = band
            while (n < band + 8) {
                su1[n] *= interp(w0[0], w0[1], n - band)
                su2[n] *= interp(w1[0], w1[1], n - band)
                n++
            }
            while (n < band + 256) { su1[n] *= w1[0]; su2[n] *= w1[1]; n++ }
            band += 256
        }
    }

    // ── transforms ───────────────────────────────────────────────────
    private val revBuf = FloatArray(256)

    /** 512-point IMDCT of 256 coefficients, windowed; odd bands arrive reversed. */
    private fun imlt(spec: FloatArray, off: Int, output: FloatArray, odd: Boolean) {
        for (i in 0 until 256) revBuf[i] = spec[off + i]
        if (odd) for (i in 0 until 128) { val t = revBuf[i]; revBuf[i] = revBuf[255 - i]; revBuf[255 - i] = t }
        Imdct.run(revBuf, output)
        for (i in 0 until 512) output[i] *= WINDOW[i]
    }

    private fun gainCompensation(inp: FloatArray, prev: FloatArray, prevOff: Int, now: Gain, next: Gain,
                                 n: Int, out: FloatArray, outOff: Int) {
        val gcScale = if (next.num != 0) GAIN_TAB1[next.lev[0]] else 1f
        if (now.num == 0) {
            for (p in 0 until n) out[outOff + p] = inp[p] * gcScale + prev[prevOff + p]
        } else {
            var pos = 0
            for (i in 0 until now.num) {
                val lastPos = now.loc[i] shl LOC_SCALE
                var lev = GAIN_TAB1[now.lev[i]]
                val nextLev = if (i + 1 < now.num) now.lev[i + 1] else ID2EXP
                val inc = GAIN_TAB2[nextLev - now.lev[i] + 15]
                while (pos < lastPos) { out[outOff + pos] = (inp[pos] * gcScale + prev[prevOff + pos]) * lev; pos++ }
                while (pos < lastPos + LOC_SIZE) {
                    out[outOff + pos] = (inp[pos] * gcScale + prev[prevOff + pos]) * lev
                    lev *= inc; pos++
                }
            }
            while (pos < n) { out[outOff + pos] = inp[pos] * gcScale + prev[prevOff + pos]; pos++ }
        }
        System.arraycopy(inp, n, prev, prevOff, n)
    }

    /** Inverse QMF: lo/hi bands -> 2*nIn samples. */
    private fun iqmf(lo: FloatArray, loOff: Int, hi: FloatArray, hiOff: Int, nIn: Int,
                     out: FloatArray, outOff: Int, delay: FloatArray) {
        System.arraycopy(delay, 0, temp, 0, 46)
        var i = 0
        while (i < nIn) {
            val p = 46 + 2 * i
            temp[p] = lo[loOff + i] + hi[hiOff + i]
            temp[p + 1] = lo[loOff + i] - hi[hiOff + i]
            temp[p + 2] = lo[loOff + i + 1] + hi[hiOff + i + 1]
            temp[p + 3] = lo[loOff + i + 1] - hi[hiOff + i + 1]
            i += 2
        }
        var p1 = 0
        var o = outOff
        for (j in 0 until nIn) {
            var s1 = 0f; var s2 = 0f
            var k = 0
            while (k < 48) { s1 += temp[p1 + k] * QMF[k]; s2 += temp[p1 + k + 1] * QMF[k + 1]; k += 2 }
            out[o] = s2; out[o + 1] = s1
            p1 += 2; o += 2
        }
        System.arraycopy(temp, nIn * 2, delay, 0, 46)
    }

    companion object {
        const val SAMPLES = 1024
        private const val JOINT_STEREO = 0x12
        private const val SINGLE = 0x2
        private const val NONE = Int.MIN_VALUE
        private const val ID2EXP = 4
        private const val LOC_SCALE = 3
        private const val LOC_SIZE = 1 shl LOC_SCALE

        private val CLC_LENGTH = intArrayOf(0, 4, 3, 3, 4, 4, 5, 6)
        private val MANT_CLC = intArrayOf(0, 1, -2, -1)
        private val MANT_VLC = intArrayOf(0, 0, 0, 1, 0, -1, 1, 0, -1, 0, 1, 1, 1, -1, -1, 1, -1, -1)
        private val INV_MAX_QUANT = floatArrayOf(0f, 1f / 1.5f, 1f / 2.5f, 1f / 3.5f, 1f / 4.5f,
            1f / 7.5f, 1f / 15.5f, 1f / 31.5f)
        private val SUBBAND = intArrayOf(0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144,
            160, 176, 192, 224, 256, 288, 320, 352, 384, 416, 448, 480, 512, 576, 640, 704, 768,
            896, 1024)
        private val MATRIX = floatArrayOf(0f, 2f, 2f, 2f, 0f, 0f, 1f, 1f)
        private val SF_TABLE = FloatArray(64) { 2.0.pow((it - 15) / 3.0).toFloat() }
        private val GAIN_TAB1 = FloatArray(16) { 2.0.pow((ID2EXP - it).toDouble()).toFloat() }
        private val GAIN_TAB2 = FloatArray(31) { 2.0.pow(-1.0 / LOC_SIZE * (it - 15)).toFloat() }

        private val QMF: FloatArray = run {
            val half = floatArrayOf(
                -0.00001461907f, -0.00009205479f, -0.000056157569f, 0.00030117269f,
                0.0002422519f, -0.00085293897f, -0.0005205574f, 0.0020340169f,
                0.00078333891f, -0.0042153862f, -0.00075614988f, 0.0078402944f,
                -0.000061169922f, -0.01344162f, 0.0024626821f, 0.021736089f,
                -0.007801671f, -0.034090221f, 0.01880949f, 0.054326009f,
                -0.043596379f, -0.099384367f, 0.13207909f, 0.46424159f)
            val w = FloatArray(48)
            for (i in 0 until 24) { val s = half[i] * 2f; w[i] = s; w[47 - i] = s }
            w
        }

        private val WINDOW: FloatArray = run {
            val w = FloatArray(512)
            var j = 255
            for (i in 0 until 128) {
                val wi = (sin(((i + 0.5) / 256.0 - 0.5) * PI) + 1.0).toFloat()
                val wj = (sin(((j + 0.5) / 256.0 - 0.5) * PI) + 1.0).toFloat()
                val ww = 0.5f * (wi * wi + wj * wj)
                w[i] = wi / ww; w[511 - i] = wi / ww
                w[j] = wj / ww; w[511 - j] = wj / ww
                j--
            }
            w
        }

        // Huffman tables: (symbol + 31, code length), in canonical order.
        private val HUFF = intArrayOf(
            31,1, 32,3, 33,3, 34,4, 35,4, 36,5, 37,5, 38,5, 39,5,
            31,1, 32,3, 30,3, 33,3, 29,3,
            31,1, 32,3, 30,3, 33,4, 29,4, 34,4, 28,4,
            31,1, 32,3, 30,3, 33,4, 29,4, 34,5, 28,5, 35,5, 27,5,
            31,2, 32,3, 30,3, 33,4, 29,4, 34,4, 28,4, 38,4, 24,4, 35,5, 27,5, 36,6, 26,6, 37,6, 25,6,
            31,3, 32,4, 30,4, 33,4, 29,4, 34,4, 28,4, 46,4, 16,4, 35,5, 27,5, 36,5, 26,5, 37,5, 25,5,
            38,6, 24,6, 39,6, 23,6, 40,6, 22,6, 41,6, 21,6, 42,7, 20,7, 43,7, 19,7, 44,7, 18,7, 45,7, 17,7,
            31,3, 62,4, 0,4, 32,5, 30,5, 33,5, 29,5, 34,5, 28,5, 35,5, 27,5, 36,5, 26,5, 37,6, 25,6,
            38,6, 24,6, 39,6, 23,6, 40,6, 22,6, 41,6, 21,6, 42,6, 20,6, 43,6, 19,6, 44,6, 18,6, 45,7,
            17,7, 46,7, 16,7, 47,7, 15,7, 48,7, 14,7, 49,7, 13,7, 50,7, 12,7, 51,7, 11,7, 52,8, 10,8,
            53,8, 9,8, 54,8, 8,8, 55,8, 7,8, 56,8, 6,8, 57,8, 5,8, 58,8, 4,8, 59,8, 3,8, 60,8, 2,8,
            61,8, 1,8)
        private val SIZES = intArrayOf(9, 5, 7, 9, 15, 31, 63)

        /** VLC[table][length][code] = symbol (or NONE). */
        private val VLC: Array<Array<IntArray>> = run {
            var at = 0
            Array(7) { t ->
                val byLen = Array(9) { l -> IntArray(1 shl l) { NONE } }
                var code = 0
                var prevLen = 0
                for (e in 0 until SIZES[t]) {
                    val sym = HUFF[(at + e) * 2] - 31
                    val len = HUFF[(at + e) * 2 + 1]
                    if (e == 0) code = 0 else code = (code + 1) shl (len - prevLen)
                    byLen[len][code] = sym
                    prevLen = len
                }
                at += SIZES[t]
                byLen
            }
        }
    }
}

/**
 * 512-point inverse MDCT of 256 coefficients, scaled as FFmpeg's (1/32768) so the decoder's
 * output lands in about -1..1:
 *     out[n] = sum_k in[k] * cos(2*pi/512 * (n + 1/2 + 128) * (k + 1/2)) / 32768
 * Computed as a 256-point DCT-IV (through a 128-point complex FFT) and unfolded by its
 * symmetries -- checked against the direct sum, and the whole decoder against vgmstream.
 */
internal object Imdct {
    private const val M = 256            // DCT-IV size
    private const val H = 128            // FFT size
    private val preRe = FloatArray(H)
    private val preIm = FloatArray(H)
    private val postRe = FloatArray(H)
    private val postIm = FloatArray(H)
    private val twRe = FloatArray(H / 2)
    private val twIm = FloatArray(H / 2)
    private val rev = IntArray(H)
    private val re = FloatArray(H)
    private val im = FloatArray(H)
    private val y = FloatArray(M)

    init {
        for (n in 0 until H) {
            val a = -PI * (4 * n + 1) / (4.0 * M)
            preRe[n] = cos(a).toFloat(); preIm[n] = sin(a).toFloat()
            val b = -PI * n / M
            // fold the 1/32768 output scale into the post-twiddle
            postRe[n] = (cos(b) / 32768.0).toFloat(); postIm[n] = (sin(b) / 32768.0).toFloat()
        }
        for (k in 0 until H / 2) {
            val a = -2 * PI * k / H
            twRe[k] = cos(a).toFloat(); twIm[k] = sin(a).toFloat()
        }
        for (i in 0 until H) {
            var r = 0; var x = i
            repeat(7) { r = (r shl 1) or (x and 1); x = x shr 1 }
            rev[i] = r
        }
    }

    @Synchronized
    fun run(input: FloatArray, output: FloatArray) {
        // pre-twiddle into bit-reversed order
        for (n in 0 until H) {
            val xr = input[2 * n]
            val xi = input[M - 1 - 2 * n]
            val r = rev[n]
            re[r] = xr * preRe[n] - xi * preIm[n]
            im[r] = xr * preIm[n] + xi * preRe[n]
        }
        // radix-2 FFT
        var len = 2
        while (len <= H) {
            val half = len shr 1
            val step = H / len
            var s = 0
            while (s < H) {
                var k = 0
                while (k < half) {
                    val wr = twRe[k * step]; val wi = twIm[k * step]
                    val a = s + k; val b = a + half
                    val tr = re[b] * wr - im[b] * wi
                    val ti = re[b] * wi + im[b] * wr
                    re[b] = re[a] - tr; im[b] = im[a] - ti
                    re[a] += tr; im[a] += ti
                    k++
                }
                s += len
            }
            len = len shl 1
        }
        // post-twiddle -> DCT-IV
        for (n in 0 until H) {
            val cr = re[n] * postRe[n] - im[n] * postIm[n]
            val ci = re[n] * postIm[n] + im[n] * postRe[n]
            y[2 * n] = cr
            y[M - 1 - 2 * n] = -ci
        }
        // unfold: out[n] = Y(n + 128), Y(m) = y[m] | -y[511-m] | -y[m-512]
        for (n in 0 until 512) {
            val m = n + 128
            output[n] = when {
                m < 256 -> y[m]
                m < 512 -> -y[511 - m]
                else -> -y[m - 512]
            }
        }
    }
}
