---
name: sci-fi-ui-design
description: Design futuristic sci-fi style user interfaces with neon colors, glowing effects, grid layouts, and cyberpunk aesthetics. Use when creating UI components, dashboards, or applications with sci-fi, cyberpunk, futuristic, or neon visual themes.
---

# Sci-Fi UI Design

## Core Design Principles

### Color Palette

**Primary Neon Colors:**
- Cyan: `#00f0ff` - Main accent, highlights
- Magenta: `#ff00ff` - Secondary accent, warnings
- Electric Blue: `#0080ff` - Interactive elements
- Hot Pink: `#ff0080` - Alerts, important states

**Background Colors:**
- Deep Space: `#0a0a0f` - Primary background
- Dark Void: `#12121a` - Card/panel backgrounds
- Midnight: `#1a1a2e` - Elevated surfaces

**Text Colors:**
- Bright White: `#ffffff` - Primary text
- Soft Glow: `#e0e0ff` - Secondary text
- Dimmed: `#8080a0` - Disabled/muted text

### Visual Effects

**Glow Effects:**
```css
/* Neon glow */
.neon-glow {
  box-shadow: 
    0 0 5px #00f0ff,
    0 0 10px #00f0ff,
    0 0 20px #00f0ff,
    0 0 40px #00f0ff;
}

/* Text glow */
.text-glow {
  text-shadow: 
    0 0 5px currentColor,
    0 0 10px currentColor;
}
```

**Grid Background:**
```css
.grid-bg {
  background-image: 
    linear-gradient(rgba(0, 240, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 240, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
}
```

**Scanline Effect:**
```css
.scanlines::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0, 0, 0, 0.3) 2px,
    rgba(0, 0, 0, 0.3) 4px
  );
  pointer-events: none;
}
```

### Typography

**Font Families:**
- Primary: `'Orbitron', 'Rajdhani', sans-serif` - Headers, titles
- Secondary: `'Share Tech Mono', monospace` - Data, code
- Body: `'Exo 2', 'Titillium Web', sans-serif` - Regular text

**Text Styles:**
- Headers: Uppercase, letter-spacing 2-4px
- Labels: Uppercase, letter-spacing 1px, smaller size
- Data: Monospace, tabular numbers

### Component Patterns

**Sci-Fi Button:**
```css
.sf-button {
  background: transparent;
  border: 2px solid #00f0ff;
  color: #00f0ff;
  padding: 12px 24px;
  font-family: 'Orbitron', sans-serif;
  text-transform: uppercase;
  letter-spacing: 2px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.sf-button:hover {
  background: rgba(0, 240, 255, 0.2);
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.5);
}

.sf-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(0, 240, 255, 0.4),
    transparent
  );
  transition: left 0.5s;
}

.sf-button:hover::before {
  left: 100%;
}
```

**Sci-Fi Card/Panel:**
```css
.sf-panel {
  background: rgba(18, 18, 26, 0.9);
  border: 1px solid rgba(0, 240, 255, 0.3);
  border-radius: 4px;
  position: relative;
  backdrop-filter: blur(10px);
}

.sf-panel::before {
  content: '';
  position: absolute;
  top: -1px;
  left: -1px;
  right: -1px;
  bottom: -1px;
  background: linear-gradient(
    135deg,
    rgba(0, 240, 255, 0.5) 0%,
    transparent 30%,
    transparent 70%,
    rgba(255, 0, 255, 0.5) 100%
  );
  border-radius: 4px;
  z-index: -1;
}

/* Corner accents */
.sf-panel::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 20px;
  height: 20px;
  border-top: 2px solid #00f0ff;
  border-left: 2px solid #00f0ff;
}
```

**Sci-Fi Input:**
```css
.sf-input {
  background: rgba(10, 10, 15, 0.8);
  border: 1px solid rgba(0, 240, 255, 0.3);
  color: #e0e0ff;
  padding: 12px 16px;
  font-family: 'Share Tech Mono', monospace;
  transition: all 0.3s;
}

.sf-input:focus {
  outline: none;
  border-color: #00f0ff;
  box-shadow: 
    0 0 10px rgba(0, 240, 255, 0.3),
    inset 0 0 10px rgba(0, 240, 255, 0.1);
}
```

### Layout Patterns

**Dashboard Grid:**
```css
.sf-dashboard {
  display: grid;
  grid-template-columns: 250px 1fr 300px;
  grid-template-rows: 60px 1fr;
  gap: 20px;
  min-height: 100vh;
  background: #0a0a0f;
  padding: 20px;
}

.sf-header {
  grid-column: 1 / -1;
  border-bottom: 1px solid rgba(0, 240, 255, 0.3);
}

.sf-sidebar {
  border-right: 1px solid rgba(0, 240, 255, 0.2);
}

.sf-main {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}
```

**Hexagon Grid:**
```css
.hex-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hex-item {
  width: 100px;
  height: 115px;
  background: rgba(0, 240, 255, 0.1);
  clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(0, 240, 255, 0.3);
}
```

### Animation Patterns

**Pulse Animation:**
```css
@keyframes pulse-glow {
  0%, 100% { 
    box-shadow: 0 0 5px #00f0ff, 0 0 10px #00f0ff;
  }
  50% { 
    box-shadow: 0 0 20px #00f0ff, 0 0 40px #00f0ff;
  }
}

.pulse {
  animation: pulse-glow 2s ease-in-out infinite;
}
```

**Glitch Effect:**
```css
@keyframes glitch {
  0% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
  100% { transform: translate(0); }
}

.glitch:hover {
  animation: glitch 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}
```

**Data Stream:**
```css
@keyframes data-stream {
  0% { background-position: 0 0; }
  100% { background-position: 0 20px; }
}

.data-stream {
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 10px,
    rgba(0, 240, 255, 0.1) 10px,
    rgba(0, 240, 255, 0.1) 20px
  );
  animation: data-stream 1s linear infinite;
}
```

### Data Visualization

**Progress Bar:**
```css
.sf-progress {
  height: 8px;
  background: rgba(0, 240, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.sf-progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #00f0ff, #ff00ff);
  box-shadow: 0 0 10px #00f0ff;
  transition: width 0.5s ease;
}
```

**Status Indicators:**
```css
.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.status-online {
  background: #00ff88;
  box-shadow: 0 0 10px #00ff88;
}

.status-warning {
  background: #ffaa00;
  box-shadow: 0 0 10px #ffaa00;
}

.status-danger {
  background: #ff0044;
  box-shadow: 0 0 10px #ff0044;
}
```

## Framework-Specific Patterns

### Vue 3 + Element Plus

Override Element Plus variables:
```javascript
// main.js
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(ElementPlus, {
  zIndex: 3000,
  size: 'default',
  button: {
    color: '#00f0ff'
  }
})
```

Custom theme SCSS:
```scss
// styles/element-override.scss
:root {
  --el-color-primary: #00f0ff;
  --el-color-primary-light-3: #40f3ff;
  --el-color-primary-light-5: #80f7ff;
  --el-color-primary-light-7: #c0fbff;
  --el-color-primary-light-8: #d0fcff;
  --el-color-primary-light-9: #e0fdff;
  --el-color-primary-dark-2: #00c0cc;
  
  --el-bg-color: #0a0a0f;
  --el-bg-color-page: #12121a;
  --el-bg-color-overlay: #1a1a2e;
  
  --el-text-color-primary: #ffffff;
  --el-text-color-regular: #e0e0ff;
  --el-text-color-secondary: #8080a0;
  
  --el-border-color: rgba(0, 240, 255, 0.3);
  --el-border-color-light: rgba(0, 240, 255, 0.2);
  --el-border-color-lighter: rgba(0, 240, 255, 0.1);
}
```

### React + Tailwind CSS

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'neon-cyan': '#00f0ff',
        'neon-magenta': '#ff00ff',
        'neon-blue': '#0080ff',
        'deep-space': '#0a0a0f',
        'dark-void': '#12121a',
        'midnight': '#1a1a2e',
      },
      fontFamily: {
        'orbitron': ['Orbitron', 'sans-serif'],
        'tech-mono': ['Share Tech Mono', 'monospace'],
        'exo': ['Exo 2', 'sans-serif'],
      },
      boxShadow: {
        'neon': '0 0 5px #00f0ff, 0 0 10px #00f0ff, 0 0 20px #00f0ff',
        'neon-lg': '0 0 10px #00f0ff, 0 0 20px #00f0ff, 0 0 40px #00f0ff',
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'glitch': 'glitch 0.3s ease-in-out',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 5px #00f0ff, 0 0 10px #00f0ff' },
          '50%': { boxShadow: '0 0 20px #00f0ff, 0 0 40px #00f0ff' },
        },
      },
    },
  },
}
```

## Design Checklist

When creating sci-fi UI components:

- [ ] Use dark backgrounds (#0a0a0f, #12121a)
- [ ] Apply neon accent colors (#00f0ff, #ff00ff)
- [ ] Add glow effects to interactive elements
- [ ] Use futuristic fonts (Orbitron, Share Tech Mono)
- [ ] Include grid or scanline background patterns
- [ ] Add corner accents or borders with gradients
- [ ] Apply subtle animations (pulse, glitch, data stream)
- [ ] Ensure sufficient contrast for readability
- [ ] Use uppercase text with letter-spacing for headers
- [ ] Include status indicators with appropriate colors
