# 🛡️ AI Disaster Command Center

> **Enterprise-Grade Multi-Agent AI System for Natural Disaster Response & Emergency Orchestration**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Developer Portfolio](https://img.shields.io/badge/Developer_Portfolio-Kanhaiya_Patel-7C3AED?style=for-the-badge)](https://portfolio-kanhaiya-patel.vercel.app/)

---

## 📌 Project Overview

**AI Disaster Command Center** is an intelligent multi-agent emergency management platform built to assist first responders, municipal command centers, and rescue teams during natural disasters (floods, landslides, earthquakes, and severe storms).

By orchestrating **6 specialized AI agents** through a centralized Commander Agent built with **LangGraph**, the system continuously monitors environmental telemetry, assesses flood damage from aerial CCTV/drone imagery, predicts casualty risks, plans optimal rescue deployment routes, and generates automated incident reports.

---

## 🤖 6 Specialized AI Agents

<div align="center">

| Agent | Responsibility | Core Tools & Frameworks |
| :--- | :--- | :--- |
| **🌦 Weather Intelligence Agent** | Fetches live meteorological data, radar updates, and rainfall telemetry. | OpenWeather API, Python async |
| **📷 Disaster Detection Agent** | Analyzes drone & CCTV feeds for flood severity, stranded victims, and infrastructure damage. | OpenCV, Groq Vision API |
| **📈 Risk Prediction Agent** | Calculates inundation rates, casualty risk scores, and evacuation timelines. | XGBoost, Scikit-Learn |
| **🚑 Rescue Planning Agent** | Computes optimal dispatch routes for ambulances, boats, and rescue teams. | Leaflet GIS, Routing Machine |
| **📦 Resource Allocation Agent** | Tracks shelter capacities, food/water rations, and medical supply levels. | MongoDB Aggregations |
| **📢 Communication Agent** | Synthesizes multi-agent telemetry into executive incident reports & emergency SMS alerts. | Groq Llama 3 API |

</div>

---

## 💡 Key Features

- **🤖 Autonomous Agent Orchestration**: Powered by **LangGraph StateGraph** — agents collaborate dynamically, sharing context through a centralized blackboard state.
- **🗺️ Interactive Spatial Command Map**: Built with **Leaflet GIS**, featuring live heatmaps, drone detection markers, shelter zones, and rescue routes.
- **📊 Real-Time Telemetry Dashboard**: Dark glassmorphic interface with interactive metric cards, live execution animations, and incident history timeline.
- **📄 Executive Report Generation**: Auto-generates multi-channel emergency briefings (PDF, SMS, Control Room broadcast) with action checklists for incident commanders.

---

## 🛠️ Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, Framer Motion, Leaflet GIS, Recharts
- **Backend API**: FastAPI (Python 3.11), Uvicorn, Pydantic v2
- **AI & Agentic Workflows**: LangGraph, LangChain, Groq API (Llama 3 70B), OpenCV
- **Database & Storage**: MongoDB (Motor async driver)

---

## 🚀 Getting Started

### Backend Setup (FastAPI & AI Agents)

1. **Navigate to the backend folder**:
   ```bash
   cd backend
   ```
2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Environment Variables**:
   Create a `.env` file inside `backend/`:
   ```env
   GROQ_API_KEY=your_groq_api_key
   MONGO_URI=mongodb://localhost:27017/disaster_db
   ```
5. **Launch FastAPI server**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup (React Dashboard)

1. **Navigate to the frontend folder**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Open `http://localhost:5173` to access the Command Center interface.

---

## 📬 Contact & Developer Info

- **Developer**: Kanhaiya Patel
- **Portfolio**: [portfolio-kanhaiya-patel.vercel.app](https://portfolio-kanhaiya-patel.vercel.app/)
- **LinkedIn**: [kanhaiya-patel](https://www.linkedin.com/in/kanhaiya-patel-1490b6324/)
- **GitHub**: [@kanhaiyapatel59](https://github.com/kanhaiyapatel59)