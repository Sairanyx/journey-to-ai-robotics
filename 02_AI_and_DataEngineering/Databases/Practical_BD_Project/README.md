# 🤖 Robotics Experiments & Benchmark Tracker Database  
**Status:** In Progress - Part 1: Database Design Phase

---

## 🔷 1. Project Context & Purpose

This database is part of the course **TE00CS89-3003 - Databases**, but it is also designed with long-term robotics research goals in mind. It will be the foundation for tracking experiments in **simulated and real environments**, supporting reproducibility and optimisation of robotic systems.

### 🎯 Purpose
- Track robotics projects and their versions
- Store hyperparameter configurations
- Record simulation and real robot runs
- Compare performance metrics
- Define benchmarks to evaluate success

### 🌍 Why this matters
Robotics systems rely on continuous experimentation and tuning. This database enables:
- Better reproducibility  
- Clear experiment tracking  
- Comparison across versions and robots  
- Alignment with embodied AI and robotics research fields  

---

## 🔷 2. Current Progress (Design Phase)

| Component                     | Status     |
|------------------------------|------------|
| Topic selection              | ✅ Complete |
| ER model (8 entities)        | ✅ Complete |
| Relational schema (3NF)      | ✅ Complete |
| SQL implementation           | 🔄 Pending |
| Data insertion & queries     | 🔄 Pending |
| Future ETL/Robotics linkage  | 🔲 Planned |

> This repository will be continuously updated as I move into implementation.

---

## 🔷 3. Database Entities Overview

| Entity         | Purpose |
|----------------|--------|
| **Project**    | Represents a robotics project |
| **Version**    | A specific configuration or code snapshot |
| **Hyperparameter** | Configuration parameter (weak entity) |
| **Run**        | Execution of a version (simulation or physical) |
| **Robot**      | Hardware used in physical runs |
| **Task**       | Defines what is being tested (e.g., navigation) |
| **Metric**     | Performance result of a run |
| **Benchmark**  | Target values to evaluate performance |

All entities and relationships are normalized to **Third Normal Form (3NF)**.

---

## 🔷 4. Long-Term Vision

This database is designed to evolve into a full **Robotics Experiment Management Platform**, potentially linked with:

- ROS / Gazebo simulation logs  
- Apache Airflow ETL pipelines  
- Performance dashboards  
- Real robot execution tracking  

This will directly support my future goals in **embodied AI, humanoid robotics, and Aalto University research pathways**.

---

## 🔷 5. Use of AI (Transparency)

AI tools were used only for:
- Brainstorming database ideas  
- Understanding robotics and database concepts  
- Structuring content and improving clarity 
- For this README.md file, restructing sentences, adding more information and creating the overall structure of the document with some artistic flair

**No AI was used to automatically generate the documentation or SQL code. All final content was written by me.**
**However, AI was used for the generation of the structure of this document**

---


