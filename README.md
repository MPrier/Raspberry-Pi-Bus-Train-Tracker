# Lowell Transit Tracker

A live **bus and commuter rail departure board** built for the **Lowell Regional Transit Authority (LRTA)** and **MBTA Lowell Line**.  
Runs on a **Raspberry Pi** connected to a small display, showing upcoming bus and train times in a clean, station-style interface.

---

## 🚉 Features

- Displays **real-time MBTA commuter rail departures** from Lowell Station  
- Shows **daily LRTA bus schedules** with automatic updates throughout the day  
- Highlights **bus–train connection opportunities** using color-coded indicators  
  - 🟩 Green → departures < 40 minutes apart  
  - 🟨 Yellow → departures between 40–60 minutes  
- Automatic **refresh countdown** and dynamic updates  
- Designed for **Raspberry Pi 3B or later** running in fullscreen mode

---

## 🖥️ UI Overview

The screen is divided into three sections:
- **Top:** Next possible bus–train connections  
- **Left:** LRTA bus schedule  
- **Right:** MBTA commuter rail schedule  

Built using **Tkinter** for a lightweight graphical interface optimized for small monitors.

---

## 🧠 Technologies Used

- **Python 3**
- **Tkinter** (UI)
- **Requests** (API calls)
- **pytz / datetime** (time zone handling)
- **MBTA v3 API**
- **LRTA SWIV API**

---


