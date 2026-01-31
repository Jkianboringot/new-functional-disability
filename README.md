# ♿ Philippine Regional Disability Analysis Dashboard

## About the Project
Access to proper support and funding for persons with disabilities often depends on **knowing where help is needed most**.  
However, raw government data can be difficult to interpret and analyze quickly.

This project is an **interactive data visualization dashboard** that analyzes and displays **regional disability patterns across the Philippines**, helping organizations and decision-makers allocate resources more effectively.

It transforms complex datasets into **clear, visual insights** that anyone can understand.

---

## 🔹 The Problem
Before this tool:
- 📊 Disability data existed mostly in spreadsheets and reports.
- ❌ Hard to compare regions quickly.
- ❌ Difficult for organizations to identify which areas need urgent support.
- ❌ Slower and less informed funding decisions.

---

## 🔹 Solution
An **interactive map-based dashboard** where users can:

- 🗺️ Select a specific region in the Philippines  
- ♿ Filter by type of disability  
- 🎨 View severity using color-coded visualization  
- 📈 Instantly see counts and distribution  

This makes patterns obvious and supports **data-driven decisions**.

---

## 🔹 Architecture Diagram

```mermaid
flowchart LR

A[Raw Data Sources<br/>CSV • Excel • Government Reports]
--> B[Data Cleaning<br/>Pandas • NumPy]

B --> C[Data Analysis<br/>Aggregation • Statistics]
C --> D[Visualization Layer<br/>Matplotlib • Plotly]

D --> E[Streamlit Dashboard<br/>Interactive UI]

E --> F[Users<br/>NGOs • Government • Researchers]
