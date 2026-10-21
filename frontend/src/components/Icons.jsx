// Inline SVG icons — no external font or emoji needed, so rendering is
// identical in every browser (emoji fonts are missing on many Linux setups).
const base = { width: 16, height: 16, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2, strokeLinecap: 'round', strokeLinejoin: 'round' }

export const Flame = (p) => (
  <svg {...base} {...p}>
    <path d="M12 3c2 3.5 4.5 5 4.5 8.5A4.5 4.5 0 0 1 12 16a4.5 4.5 0 0 1-4.5-4.5C7.5 8 10 6.5 12 3Z" />
    <path d="M12 21c3.3 0 6-2.2 6-5.5 0-1.6-.6-2.9-1.5-4" />
    <path d="M12 21c-3.3 0-6-2.2-6-5.5 0-1.6.6-2.9 1.5-4" />
  </svg>
)

export const Speaker = ({ muted, ...p }) => (
  <svg {...base} {...p}>
    <path d="M4 10v4h3l4 3V7l-4 3H4Z" />
    {!muted && <path d="M15.5 8.5a5 5 0 0 1 0 7" />}
    {!muted && <path d="M18 6a8.5 8.5 0 0 1 0 12" />}
    {muted && <path d="m16 9 5 6M21 9l-5 6" />}
  </svg>
)

export const Clock = (p) => (
  <svg {...base} {...p}>
    <circle cx="12" cy="12" r="8.5" />
    <path d="M12 7.5V12l3 2" />
  </svg>
)

export const Bulb = (p) => (
  <svg {...base} {...p}>
    <path d="M9 18h6M10 21h4" />
    <path d="M12 3a6 6 0 0 0-3.5 10.9V16h7v-2.1A6 6 0 0 0 12 3Z" />
  </svg>
)

export const Target = (p) => (
  <svg {...base} {...p}>
    <circle cx="12" cy="12" r="8.5" />
    <circle cx="12" cy="12" r="4" />
  </svg>
)

export const Bolt = (p) => (
  <svg {...base} {...p}>
    <path d="M13 3 5 14h5l-1 7 8-11h-5l1-7Z" />
  </svg>
)

export const Check = (p) => (
  <svg {...base} {...p}>
    <path d="m5 13 4 4L19 7" />
  </svg>
)

export const Star = (p) => (
  <svg {...base} {...p}>
    <path d="m12 4 2.4 5 5.6.8-4 4 .9 5.7L12 16.8 7.1 19.5 8 13.8l-4-4L9.6 9 12 4Z" />
  </svg>
)

export const Play = (p) => (
  <svg {...base} {...p}>
    <path d="M7 4.5v15l13-7.5-13-7.5Z" />
  </svg>
)

export const Warn = (p) => (
  <svg {...base} {...p}>
    <path d="M12 4.5 3 20h18L12 4.5Z" />
    <path d="M12 10v4.5M12 17.2v.3" />
  </svg>
)

export const Info = (p) => (
  <svg {...base} {...p}>
    <circle cx="12" cy="12" r="8.5" />
    <path d="M12 11v5.5M12 7.8v.4" />
  </svg>
)

export const Book = (p) => (
  <svg {...base} {...p}>
    <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15.5H6.5A2.5 2.5 0 0 0 4 21V5.5Z" />
    <path d="M4 18.5h16" />
  </svg>
)
