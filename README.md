# ♿ Philippine Regional Disability Analysis Dashboard  

## 🌏 Live Application  
🔗 **View the Dashboard:**  
https://jkianboringot-functional-disability.streamlit.app/

📓 **View the Development Process (Notebook):**  
https://nbviewer.org/github/Jkianboringot/new-functional-disability/blob/main/keep/main.ipynb  

---

## 📌 About the Project  

This web application provides an interactive choropleth map visualization of functional difficulty data across the Philippines.

It analyzes the Household Population Five Years Old and Over (2020 Census) and transforms raw statistical tables into an accessible, map-based dashboard.

The goal is to convert complex census data into clear, actionable regional insights that support data-driven planning and decision-making.

---

## 📚 Legal & Policy Foundation  

### Republic Act No. 7277 (Magna Carta for Disabled Persons) – 1992  
Enacted on March 24, 1992, this law promotes the rehabilitation, self-development, and integration of persons with disabilities (PWDs) into mainstream society. It guarantees equal access to education, employment, healthcare services, and social participation.

### Republic Act No. 10754 – 2016  
Expands the benefits and privileges of PWDs, strengthening the government's commitment to inclusion and welfare.

---

## 📊 Data Sources  

• Philippine Statistics Authority (PSA) – Functional Difficulty (2020 Census)  
https://psa.gov.ph/content/functional-difficulty-philippines-household-population-five-years-old-and-over-2020-census  

• Humanitarian Data Exchange (HDX) – Functional Difficulty Dataset  
https://data.humdata.org/dataset/philippines-functional-difficulty-census-2020  

• HDX – Population Projection (2020–2025, Admin 3 Level)  
https://data.humdata.org/dataset/philippines-population-projection-2020-2025-admin3  

• GeoJSON Map Source – Philippines Administrative Boundaries  
https://github.com/faeldon/philippines-json-maps  

---

## 🔎 The Problem  

Before this dashboard:

- Disability data was primarily available in spreadsheets and reports  
- Regional comparison required manual analysis  
- Identifying high-need areas was time-consuming  
- Funding and intervention decisions were slower and less informed  

---

## 💡 The Solution  

An interactive, map-based dashboard that allows users to:

- 🗺️ Select specific Philippine regions  
- ♿ Filter by type of functional difficulty  
- 🎨 View severity through color-coded choropleth visualization  
- 📈 Instantly analyze distribution patterns and population counts  

This supports:

- Evidence-based resource allocation  
- Faster regional comparison  
- Improved transparency in decision-making  
- Stronger support planning for NGOs, researchers, and government agencies  

---

## 🧠 Technical Architecture  

```mermaid
flowchart LR

A[Raw Data Sources<br/>CSV • Excel • Government Reports]
--> B[Data Cleaning<br/>Pandas • NumPy]

B --> C[Data Analysis<br/>Aggregation • Statistics]
C --> D[Visualization Layer<br/>Matplotlib • Plotly]

D --> E[Streamlit Dashboard<br/>Interactive UI]

E --> F[Users<br/>NGOs • Government • Researchers]
