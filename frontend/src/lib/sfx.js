// Tiny WebAudio sound engine — no external assets, works offline.
let ctx = null

function ac() {
  if (typeof window === 'undefined') return null
  if (!ctx) {
    const Ctor = window.AudioContext || window.webkitAudioContext
    if (!Ctor) return null
    ctx = new Ctor()
  }
  if (ctx.state === 'suspended') ctx.resume()
  return ctx
}

function tone({ freq = 440, dur = 0.08, type = 'sine', gain = 0.06, slide = 0, delay = 0 }) {
  const a = ac()
  if (!a) return
  const t0 = a.currentTime + delay
  const osc = a.createOscillator()
  const g = a.createGain()
  osc.type = type
  osc.frequency.setValueAtTime(freq, t0)
  if (slide) osc.frequency.exponentialRampToValueAtTime(Math.max(40, freq + slide), t0 + dur)
  g.gain.setValueAtTime(0.0001, t0)
  g.gain.exponentialRampToValueAtTime(gain, t0 + 0.008)
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur)
  osc.connect(g).connect(a.destination)
  osc.start(t0)
  osc.stop(t0 + dur + 0.02)
}

export const sfx = {
  key() {
    tone({ freq: 520 + Math.random() * 120, dur: 0.025, type: 'square', gain: 0.012 })
  },
  error() {
    tone({ freq: 180, dur: 0.18, type: 'sawtooth', gain: 0.05, slide: -90 })
    tone({ freq: 120, dur: 0.22, type: 'square', gain: 0.03, delay: 0.02 })
  },
  runComplete() {
    tone({ freq: 660, dur: 0.09, type: 'triangle', gain: 0.05 })
    tone({ freq: 990, dur: 0.12, type: 'triangle', gain: 0.045, delay: 0.08 })
  },
  typingMastered() {
    ;[523, 659, 784, 1047].forEach((f, i) =>
      tone({ freq: f, dur: 0.16, type: 'triangle', gain: 0.05, delay: i * 0.075 }),
    )
  },
  recallPass() {
    ;[784, 988, 1319].forEach((f, i) => tone({ freq: f, dur: 0.2, type: 'sine', gain: 0.055, delay: i * 0.09 }))
  },
  recallFail() {
    ;[330, 262, 196].forEach((f, i) => tone({ freq: f, dur: 0.18, type: 'sawtooth', gain: 0.04, delay: i * 0.1 }))
  },
  levelUp() {
    ;[523, 659, 784, 1047, 1319].forEach((f, i) =>
      tone({ freq: f, dur: 0.22, type: 'sine', gain: 0.05, delay: i * 0.08 }),
    )
  },
}

export function speak(text, enabled) {
  if (!enabled || typeof window === 'undefined' || !window.speechSynthesis) return
  try {
    window.speechSynthesis.cancel()
    const u = new SpeechSynthesisUtterance(text)
    u.rate = 1.02
    u.pitch = 1
    window.speechSynthesis.speak(u)
  } catch (_) {}
}

export function haptic(ms = 12) {
  if (typeof navigator !== 'undefined' && navigator.vibrate) {
    try {
      navigator.vibrate(ms)
    } catch (_) {}
  }
}
