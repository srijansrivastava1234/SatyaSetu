# Hackathon Rulebook & Stage Compliance Checklist (Member 5)
*Rules Enforcement: Rule 02 (MPH Hall Presentation Rules), Rule 04 (5-Minute Hard Cutoff)*

---

## 1. Pre-Stage Readiness Checklist (15 Minutes Before Call)
- [ ] **Laptops Status**:
  - Laptop 1 (Backend - Member 1): Running `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
  - Laptop 3 (Stage Display - Member 3): Connected to local mobile hotspot / loopback; Tab 1 (Slides) and Tab 2 (SatyaSetu App) open.
  - Laptop 4 (Extension - Member 4): Loaded in Chrome Developer Mode.
- [ ] **Acoustics & Microphones**:
  - Test lapel or hand mics in MPH hall.
  - Establish speaking distance (2 inches from mouth) to prevent echo in large halls.
- [ ] **Timekeeper Stopwatch**:
  - Member 5 or designated timekeeper has phone stopwatch running with silent vibration at:
    - `3:00` (120 seconds left)
    - `4:30` (30 seconds warning to wrap up)
    - `5:00` (Hard stop - thank judges immediately).

---

## 2. Emergency Contingency Matrix

| Failure Point | Real-Time Mitigation |
| :--- | :--- |
| **Auditorium Wi-Fi drops completely** | Laptop 3 is already bound to local loopback `127.0.0.1:8000` with pre-warmed canonical cache. Zero network dependency. |
| **Projector fails to mirror display** | Switch immediately from "Extend" to "Duplicate" (`Win + P`). Have backup PDF slides on USB flash drive. |
| **Judge interrupts during demo** | Member 5 answers the interruption in 1 sentence, and Member 3 maintains the demo flow silently on screen. |
| **Speaker B fumbles input text** | Member 3 clicks the pre-configured quick scenario buttons on the UI rather than manual keyboard typing. |
