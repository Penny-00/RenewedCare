


# 🏥 RenewedCare — Predictive Intelligence for Primary Health Centers

>AI-driven solution to strengthen primary health care in Africa. 

>Combines data analytics, predictive modeling, and a clinician-friendly dashboard to enhance diagnosis, triage, and decision support in under-resourced communities. Built for the DataFest Hackathon.

---

## 🚀 Project Overview
**PHCare AI** leverages open health data, machine learning, and intelligent dashboards to:
- Identify gaps in primary healthcare coverage
- Predict risks like **drug stockouts**, **patient overload**, and **outbreaks**
- Support **data-driven allocation** of staff, equipment, and medicine
- Provide **interactive tools** (dashboards, chatbots) for health workers and policymakers

---

## 🧩 System Architecture
```mermaid
flowchart TD
    A["Data Sources: WHO, DHIS2, OpenAfrica"] --> B["ETL & Data Warehouse (PostgreSQL)"]
    B --> C["AI Models: Forecasting, NLP, Optimization"]
    C --> D["Streamlit Dashboard / React App"]
    D --> E["End Users: PHC Managers, Health Workers, Policymakers"]

