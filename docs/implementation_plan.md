# UX/UI Audit & Enhancement Proposals

Based on a thorough review of the current dashboard mechanics (from the perspective of a daily operator or manager), I have identified key areas that could transform the app from a "functional prototype" into a "commercial-grade product". 

## 1. Identified UX Frictions

*   **Information Overload:** Currently, the dashboard presents a massive amount of dense, technical data (lux measurements, thermal gradients, spot prices) simultaneously. Without an "Insights" summary panel, a non-engineer might find it hard to know if the system is performing *well* at a glance.
*   **Static Scalability:** While the daily chart now fetches live APIs, the "30 Tage" and "12 Monate" buttons still rely on simulated arrays. Clicking those feels disjointed because the data suddenly jumps back to static mockups.
*   **Notification Cramping:** The red danger modal works beautifully, but the standard drop-down for the Notification Bell can feel cramped when displaying full news headlines, leading to text cutoffs.
*   **Translation Feedback:** The translation switcher works perfectly now, but because it happens instantly across the DOM, there's no visual "loading" indicator. Users might miss that text changed if they aren't looking at the right spot.

---

## 2. Proposals for Increased User Comfort

To make a user feel entirely comfortable and in total control of the system, I propose adding the following features:

### A. "Info Mode" (Contextual Help)
By clicking a universal `[ ? ]` button in the header, the dashboard enters an "overlay mode". Hovering over any chart, KPI, or sensor fades everything else out and displays a tooltip precisely explaining what that metric means (e.g., "This shows the day-ahead electricity auction price from the Bundesnetzagentur"). This significantly lowers the learning curve.

### B. Actionable "Insights" Widget
Instead of just displaying the chart, we should add a small `AI Insights` natural-language widget right on the "Übersicht" homepage. It will synthesize the data into plain German/English: 
> *"Prices are incredibly low tonight (€0.14). The system is scheduled to fully charge the thermal storage using the grid before sunrise."*

### C. True Data Portability (Export Button)
Commercial operators want to manipulate their data in Excel. We should add a seamless `[ Daten Exportieren (CSV) ]` button below the charts allowing them to instantly download the fetched InfluxDB/API arrays into a usable `.csv` file.

## User Review Required

> [!IMPORTANT]
> Because there are several directions we can take here, I need to know which features you want to prioritize for execution.

## Open Questions

1. Do you want me to prioritize building the **Info Mode (Tooltips)**, the **Actionable Insights Widget**, or the **Data Export** functionality first?
2. Are you experiencing the dashboard primarily on a **Desktop Monitor** or a **Mobile Device/Tablet**? (This tells me if I need to focus on Responsive CSS grid redesigns).

## Verification Plan

### Automated Tests
- I will execute structural DOM tests to verify CSV generation triggers correctly via JavaScript blobs without needing a server.
- I will review the UI spacing additions via code inspection.

### Manual Verification
- You will refresh the dashboard and use the new features introduced based on your choices.
