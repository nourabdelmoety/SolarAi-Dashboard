# ☀ SolarAI — Advanced Energy Management Dashboard (V9)

[![Status](https://img.shields.io/badge/Status-Commercial%20Prototype-gold?style=for-the-badge)](https://github.com/your-username/repo-name)
[![Stack](https://img.shields.io/badge/Stack-Vanilla%20JS--HTML--CSS-blue?style=for-the-badge)](https://github.com/your-username/repo-name)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**SolarAI** is a high-performance, zero-dependency energy management platform designed to bridge the gap between residential solar production and smart thermal storage. This dashboard serves as the central control hub for a multi-sensor solar ecosystem, utilizing AI to optimize energy usage, storage, and grid export.

---

## 🚀 Key Features

### 🧠 AI-Driven Insights & Automation
Real-time advice engine that analyzes live spot prices and solar forecasts to provide actionable energy strategies (e.g., "SELL now", "STORE for tonight").

### 🌡 Thermal Storage Visualizer
A high-fidelity simulation of an 800-liter buffer tank. includes real-time heat capacity calculations and loss-rate analysis based on high-precision DS18B20 sensor data.

### 🌤 Intelligent Weather Integration
Deep integration with **Open-Meteo (DWD ICON model)** for Bavaria. Features dynamic solar yield estimations based on hourly cloud cover and sunrise/sunset trajectories.

### 🌍 Multilingual (DE/EN) & Offline-Resilient
Full translation coverage with a smart DOM-injection engine. The "Offline Mode" ensures data persistence and visual integrity even without an internet connection using local simulation fallbacks.

---

## 🛠 Technical Architecture

- **Frontend**: Vanilla HTML5, CSS3 (Glassmorphism), and ES6+ JavaScript.
- **Charts**: Interactive timeline visualizations via **Chart.js**.
- **Data Layers**:
  - **Live Weather**: Open-Meteo REST API.
  - **Energy Markets**: Energy-Charts Spot Price API.
  - **Sensors**: Architected for MQTT/InfluxDB integration (ESP32 backend).
- **Design**: Premium "Commercial Grade" aesthetic with responsive grid layouts and context-aware tooltips.

---

## 📁 Project Structure

```bash
├── src/
│   └── solar_dashboard_v9.html  # Main Application Core
├── scripts/
│   ├── inject_ux.py            # UX Enhancement Pipeline
│   └── extract_data.py         # Telemetry extraction scripts
├── docs/
│   ├── build_guide.md          # Technical documentation
│   └── architecture_map.png    # System flow diagram
└── README.md                   # You are here
```

---

## 🔧 Installation & Usage

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/repo-name.git
   ```
2. **Launch**:
   Open `src/solar_dashboard_v9.html` in any modern web browser.
3. **Admin Mode**:
   Click the **"KI: MODE"** badge in the header and enter the default password `admin` to access manual override controls.

---

## 👔 Contact & Development
**Project Goal**: Transitioning German residential solar systems to proactive, AI-managed smart homes.

*Developed as a high-impact prototype for [Professor Name/University Name].*
