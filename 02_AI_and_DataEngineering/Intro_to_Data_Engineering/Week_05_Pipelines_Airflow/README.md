# Week 5 – Data Pipelines and Apache Airflow

### Data Pipeline

Example from class: “Data Pipeline is no different from our water pipelines.”

- A way to automatically move data from point A to point B with some steps in between (C, D, E)

---

### Automation vs Orchestration

**Automation:**  
- Running individual blocks/tasks at a certain time and speed  
- Focus is on a single task

**Orchestration:**  
- Running multiple blocks together in the right order to get a full pipeline  
- Bigger picture, not just one task

---

### Directed Acyclic Graph (DAG)

- Set of nodes connected with directed edges  
- No cycles (you don’t visit the same node again)  
- Used in Airflow to represent workflows

---

### Apache Airflow

- Workflow scheduler written in Python (created by Airbnb)  
- DAGs are written as Python code

**Some components:**
- `BashOperator` – run a bash command  
- `datetime` – work with dates and times  
- `timedelta` – used for setting time intervals (like schedule)

---

### DAG Basics

**Default arguments (at the top):**
- `owner`  
- `start_date = datetime(...)`  
- `depends_on_past = False`  
- `retries = ...`  
- `retry_delay = timedelta(minutes=5)`

**DAG definition:**
- It’s a class  
- Give it a name: `dag_id='...'`  
- Add `default_args=default_args`  
- Set `schedule_interval = timedelta(days=1)`

---

### Tasks

- Define tasks using `BashOperator`  
- Example:  
  - `task_id = 'task1'`  
  - `bash_command = 'echo Hello'`  
  - `dag = dag` (connects it to the DAG)

**Task dependencies:**
- Example: Task 2 runs after Task 1  
- task1 >> task2

### Airflow Architecture (simple breakdown)

| Component | Description |
|-----------|-------------|
| Web Server | Web UI to see DAGs, logs, run tasks manually |
| Scheduler | Decides when tasks should run and in what order |
| Executor | Runs the tasks (different types like LocalExecutor, CeleryExecutor) |
| Metadata Database | Stores DAGs, task status, logs, configurations |
| Worker | Executes the tasks given by the scheduler |
