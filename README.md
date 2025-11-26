# Smart University Resource Allocation & Scheduling System

A full end-to-end system that predicts university course demand, allocates classrooms optimally, and provides a professional dashboard for decision-makers. Designed using **Machine Learning**, **Optimization**, and **Business Analytics** principles.

---

## Project Summary

This project builds a complete **decision support system** for university administrators. It:

- Predicts course enrollment using Machine Learning  
- Allocates classrooms & timeslots using optimization  
- Calculates room utilization & scheduling efficiency  
- Presents insights on a professional Streamlit dashboard  

All data used is **synthetic**.

---

## Project Inputs (Synthetic Data)

- `data/synthetic/courses.csv` - course metadata  
- `data/synthetic/rooms.csv` - room capacities  
- `data/synthetic/historical_instances.csv` - historical enrollment for model training  

---

##  Project Outputs

- `models/rf_model.joblib` - trained demand prediction model  
- `data/synthetic/courses_with_predictions.csv` - predicted enrollment per course  
- `data/synthetic/assignments.csv` - optimized classroom assignment  
- Interactive dashboard (`streamlit_app.py`)  

---

##  What This Project Includes (Completed Work)

### **Data Engineering**
Synthetic timetable & enrollment generator  
Clean structured datasets  

### **Machine Learning - Course Demand Forecasting**
Feature engineering (`src/features.py`)  
RandomForest regression model (`src/model.py`)  
Training pipeline (`scripts/train_model.py`)  

### **Optimization - Room Allocation**
Greedy scheduling algorithm (`src/optimizer.py`)  
Room + timeslot assignment generation (`scripts/run_optimizer.py`)  

### **Dashboard - Streamlit UI**
Overview KPIs  
Course demand forecasting visualizations  
Room assignment viewer  
Utilization analytics (timeslot demand, room usage%)  
Clean, modern UI with navigation  

---

## How to Run the Project Locally

### Create & activate virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\Activate.ps1
pip install streamlit plotly pandas numpy scikit-learn joblib ortools statsmodels
python scripts/generate_data.py
python scripts/train_model.py
python scripts/run_optimizer.py
python -m streamlit run streamlit_app.py
