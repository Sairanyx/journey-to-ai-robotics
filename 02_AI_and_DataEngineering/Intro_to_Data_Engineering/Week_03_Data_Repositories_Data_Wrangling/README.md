## 🗓️ **Week 3 Summary -** Data Repositories and Data Wrangling

---

### ℹ️ Intro to skills and technologies used

- Introduced just by concept to some technical skills and technologies Data Engineers work with:
    - RDMS : MySQL, Oracle Database, PostgreSQL, IBM DB2
    - NoSQL: Redis, MongoDB, Cassandra, Neo4j
    - Data Warehouses: Amazon Redshift, Oracle Exadata, Google BigQuery, IBM Db2 Warehouse
    - Data Pipelines: Apache Bearn, Airflow, Dataflow
- More info on tools and languages we will learn during the program and uses
- Short info on data transformation in batches and streams
- Importance of soft skills in workplace/start-up or group projects

---

### 📝 Data Repositories

- Data Repositorie refers to collected, organised and isolated data ready to be used. Choice or repo is based on the system used:
    - OLTP, online transactional processing for high volume of small  fast operations (online banking)
    - OLAP, online analytical processing for complex queries and data analysis, so smaller volume but bigger operations (Finance analytics)
- Categories of date repos:
    - Database
        - For input, storage, search, retrieve and modify data
        - Managed by DBMS, program for maintaining, controlling storage, modifying and querying data
        - Factors influencing choice:
            - Data type and structure
            - Quering mechanisms
            - Latency requirements
            - Transaction speeds
            - Intented use of data
        - Raltional DB
            - Organised data, well defined structure and schema, optimised for operations and querying (PostgreSQL, Access, Oracle, MySQL)
        - Non-Relational DB
            - Usually unstructured and semi-structured data than can be in schema-less format (MongoDB, HBase, Bigtable)
            - Build for speed, flexibility, scaling
            - Types: Key-Value, Column-Family, Graph, Document
    - Data Warehouse
        - Centralised repository for structured data mainly used for storing large amount if it coming from multiple sources.
        - Includes ETL/ELT pipelines, data modeling layers, query engines, and metadata management
        - Optimises for OLAP and not OLTP
        - Designed for analysis and reporting
        - Data is integrated from various sources
    - Data Marts
        - Subset of Data Warehouses, for specific departments like for finance, business functions
        - Derived from Data Warehouses, so structured data, useful for smaller queries so the entire data warehouse data is not always quered as its of course slower
    - Data lake
        - Stores raw, unstructured, semi-structured and structured data. Centralised repo for all types of data in native form
        - For Big Data, ML, Exploration, can also be ETL/ELT later for Data Warehouses
        - Minimal processing before storage, data stored raw form and transormed when needed
    - Data Spaces
        - Federated data ecosystem where multiple organisations share data in a controlled, standardised and interoperable way
        - Not a single repo used, all about collaboration and trust with common rules like GaiaX
- Info on European Strategy of Data, bigger picture and involvement, usage and aspirations for the future

---

### 🔄 **Data Wrangling**

- Data Wrangling, from raw to structured:
    - Cleaning
    - Transforming
    - Organising
- Examples used: Missing Values, encoding features - One Hot and Label and differences, how to use and when
- Examples of Data Scaling briefly and how they will be used in the future for ML and Data Analysis

---

### 🛠 **Tools used this week**

- Jupyter Notebook
- Python (Pandas)

---

### 💬  Summary

This week focused on understanding where data is stored, why different storage systems exist, and how raw data begins its journey into usable form. I also saw how Data Engineers support machine learning workflows by enabling clean, structured, and accessible data. Also, practised Data Wrangling concepts.