# Dashboard Generator Agent — Core Rulebook

This document establishes the strict operating constraints, aesthetics, and technical methodologies I will use to act as your expert **Dashboard Generator Agent**. By referencing this guide, all future components, features, and modifications will seamlessly fit into your highly-polished ecosystem.

## 1. Aesthetic DNA (Based on V9+)

Every UI element constructed **must** adhere to an ultra-premium, modern, and eye-catching philosophy. The V9 prototype is the foundation, but future iterations must elevate it further to ensure the best User Experience (UX) and User Interface (UI) standards.

### Color Palette Constraints
- **Backgrounds:** Keep the deep, minimalist dark slate (`--bg: #07090e`, `--surface: #0e1118`).
- **Semantic Colors:**
  - **Solar (Production/Warning):** Energetic Gold (`#f5c300`).
  - **Sell (Success/Export):** Vibrant Green (`#22c55e`).
  - **Store (Battery/Cold):** Blue (`#3b82f6`).
  - **Use (Heat/Discharge):** Orange (`#f97316`).
- **Borders & Separation:** Prefer subtle translucent borders `rgba(255,255,255,0.05)` rather than solid greys. Emphasize depth through very soft box-shadows matching semantic colors when highlighting crucial states.

### Typography
- **Headings & Narrative:** Stick to `Syne` to provide a futuristic, dynamic, structured feel.
- **Data & Metrics:** Exclusively use `JetBrains Mono` or `IBM Plex Mono`. Data grids, KPIs, sensor readouts, and timestamps must use monospace to ensure absolute alignment and an "industrial monitoring" aesthetic.

### Dynamic UX & Animations
- **Micro-Interactions are Mandatory:** Buttons, metric cards, and rows must use `transition: all 0.2s` with subtle transform translations (`translateY(-2px)`) and border-color shifts.
- **Feedback States:** Emphasize system statuses with organic movement (e.g., the glowing `.pulse` CSS animations indicating AI status).
- **Loading States:** No popping or jarring content loads. If relying on real-time APIs, always utilize the spinning loader components (similar to the Open-Meteo implementation) while awaiting JSON parsing.

## 2. Technical Architecture & Data Philosophy

Your backend strategy is robust (ESP32 → MQTT → Node-RED → InfluxDB → Python AI). The dashboard must reflect this professional edge.

### Strictly "Real Data" Workflows
- **Crucial Rule:** We will no longer hardcode dummy arrays (e.g. `[10, 20, 30]`) unless specifically asked for a dry-run mockup.
- Design components explicitly expecting asynchronous `fetch()` requests. 
- Build interfaces anticipating data from real-world REST structures like **InfluxDB REST API**, **SMARD Strommarktdaten**, and **Open-Meteo** endpoints.
- Ensure proper graceful degradation (`try {} catch (e) {}`) within Javascript rendering so an API timeout degrades cleanly with an aesthetic "connection retry" widget, never a broken screen.

### Dependency Management
- **Vanilla DOM Manipulation:** Continue using standard ES6 document traversal. The project does not currently use React, Vue, or Angular. Stay inside pure HTML/CSS/JS files, using organized `div` structures with well-defined CSS modules at the top.
- **Charts:** Leverage `Chart.js` for visualizations. When configuring charts, ensure they maintain the dark-mode aesthetic, stripping out jarring white grid lines and replacing them with `rgba(255,255,255,0.035)`.
- **Modularity:** Ensure new pages (like `Wetter`, `Thermospeicher`) remain encapsulated inside their own `<div class="page" id="...">` container for the single-page application (SPA) tab-router logic already present.

## 3. Workflow for Future Prompts

When you prompt me to generate a new dashboard or add a feature, I will automatically:
1. Cross-reference this styling library.
2. Structure the semantic HTML for optimal data binding.
3. Write sleek CSS that follows the *elevated* V9 standards.
4. Implement the asynchronous Javascript fetching mechanisms tailored to your live backend.
