---
version: 1.0.0
name: Captain's Prestige (Atmospheric Glass)
author: Antigravity
colors:
  primary: "#0A192F"      # Deep Navy (Background)
  secondary: "#112240"    # Dark Teal (Surfaces)
  accent: "#64FFDA"       # Aquamarine (Primary Action)
  highlight: "#FBD38D"    # Muted Gold (Secondary/Status)
  surface: "rgba(17, 34, 64, 0.7)"
  border: "rgba(100, 255, 218, 0.1)"
  text:
    main: "#CCD6F6"
    muted: "#8892B0"
    heading: "#E6F1FF"
typography:
  fontFamily: "'Inter', system-ui, sans-serif"
  monoFamily: "'JetBrains Mono', monospace"
  baseSize: "16px"
  headingWeight: 700
spacing:
  base: "8px"
  container: "1200px"
effects:
  blur: "20px"
  shadow: "0 20px 50px rgba(2, 12, 27, 0.7)"
  transition: "all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1)"
---

# Captain ETA Design System

## 🌊 Overview
Captain ETA is a professional maritime navigation tool. The design should evoke a sense of **command, precision, and high-tech instrumentation**. We use a "Dark Bridge" aesthetic—mimicking the atmosphere of a modern ship's bridge at night.

## 🎨 Visual Language
- **Atmospheric Glass**: UI components use glassmorphism (transparency + backdrop-blur) to simulate high-end glass displays.
- **Micro-interactions**: Every button and input should feel "alive" with subtle glows and transitions.
- **Typography**: Headers are bold and clean (`Inter`). Technical data and results use `JetBrains Mono` for a "digital instrument" feel.

## 🧱 Components

### Glass Panels
- **Background**: `rgba(17, 34, 64, 0.7)`
- **Blur**: `backdrop-filter: blur(20px)`
- **Border**: `1px solid rgba(100, 255, 218, 0.1)`
- **Shadow**: Deep, soft shadows to create floating depth.

### Buttons (Command Actions)
- **Primary**: Gradient of Aquamarine (`#64FFDA`). High contrast against navy.
- **Secondary**: Outlined with `accent` color.
- **Hover**: Subtle outer glow (box-shadow).

### Inputs (Telemetry)
- Dark backgrounds with high-contrast text.
- Focus state: `1px solid var(--accent)` with a subtle shadow glow.

## 🚦 Status Indicators
- **Safe/Active**: `#64FFDA` (Aquamarine)
- **Warning/Critical**: `#F56565` (Maritime Red)
- **Neutral/Secondary**: `#FBD38D` (Gold)

## 📐 Layout
- Centralized dashboard with a fixed sidebar or top-nav.
- Information density should be balanced: high enough for professionals, but clean enough to avoid clutter.
