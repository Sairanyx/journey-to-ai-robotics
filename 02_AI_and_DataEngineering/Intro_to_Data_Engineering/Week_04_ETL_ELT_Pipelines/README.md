# 🗓️ **ETL and ELT Pipelines**

## ✅ **What is ETL?**

**ETL stands for:**

- **E = Extract**  
- **T = Transform**  
- **L = Load**

Raw data is essentially converted into analysis-ready data. Data is extracted from the source, then transformed to a format that works with the target system and loaded into the target system.

**Transformation means:**
- Clean, standardise, format the data  
- Removing duplicates  
- Filtering out data that we do not need  
- Enriching the data

---

## 🔁 **Approaches to ETL**

### **1. Batch Processing**
- Data moved in large chunks or batches at scheduled intervals. Instead of pulling the data continuously, it does it over time (daily, hourly etc.)  
- It can be cost effective, no constant resources needed to be available  
- Delay before the most recent data is available  
- **Examples:** Apache Spark, Blendo

### **2. Stream Processing**
- Extracts continuously and in real-time. The data is most of the time pulled as soon as it is created or available, and is processed while it is being transferred.  
- Full refresh sometimes is needed to erase contents of one or more tables and reload with fresh data  
- Immediate access to the latest data flows for quick decision making  
- Can be used to trigger actions based on specific data changes as they occur  
- There are plenty of verifications to be added also for batch processing  
- Frequent used word is **“on the fly”**  
- Higher cost as always requiring more computing resources  
- The complexity of setting up is higher  
- **Examples:** Apache Kafka, Apache Storm

---

## ✅ **What is ELT?**

- ELT is the process where data is first **extracted**, then **loaded into the target system**, and then **transformed while data is in the target system**  
- This approach uses scalability of modern cloud data platforms that can handle complex transformations on massive datasets efficiently  
- Useful in processing large sets of unstructured and non-relational data  
- Ideal for **data lakes**

---

## 💬 **Summary**

This week focused on how data moves from raw sources to usable formats. I learned the difference between ETL and ELT, when to use batch vs stream processing, and why modern systems often load data first (ELT) and transform later in the cloud. It helped me understand the beginning of data pipelines and how real-world companies automate data movement.