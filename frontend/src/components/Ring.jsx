export default function Ring({ value = 0, size = 132, stroke = 10, label, sub, accent = '#5fd6a0' }) {
  const r = (size - stroke) / 2
  const c = 2 * Math.PI * r
  const dash = (Math.min(100, Math.max(0, value)) / 100) * c
  return (
    <div className="ring" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,.08)" strokeWidth={stroke} />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={accent}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${dash} ${c - dash}`}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          style={{ transition: 'stroke-dasharray .5s ease' }}
        />
      </svg>
      <div className="ring-center">
        <strong style={{ color: accent }}>{label ?? `${value}%`}</strong>
        {sub && <span>{sub}</span>}
      </div>
    </div>
  )
}
