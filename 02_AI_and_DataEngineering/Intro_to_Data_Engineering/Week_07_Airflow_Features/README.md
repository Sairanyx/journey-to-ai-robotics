# Week 5 - XCom, Task Instance (ti) and **context in Airflow

## What is XCom?

- XCom (Cross-Communication) lets tasks in Airflow send **small data** to each other.  
- Used for things like messages, file paths, simple status values.  
- Values are stored in Airflow’s **metadata database**, so only small amounts of data should be used.

---

## What is a Task Instance (ti)?

- A **Task Instance (ti)** is one specific run of a task inside a DAG.
- I can access it inside a Python task with `context['ti']`.
- I use `ti` to:
  - Push data to XCom → `ti.xcom_push()`
  - Pull data from XCom → `ti.xcom_pull()`
  - Check info like execution date, state, retries

---

## What is **context?

- In Python, `**` collects keyword arguments into a dictionary.
- In Airflow, when I write `def task(**context):`, Airflow passes a dictionary called **context**.
- This dictionary includes things like:
  - `ti` (task instance)
  - `execution_date`
  - `task_id`, `dag_id`, `run_id`

So:
- `**context` = Python way to receive Airflow's metadata
- `context['ti']` = how I access XCom inside that function

---

## When should I use XCom?

**Use XCom for:**
- Small values like `"done"`, `"failed"`, `"cleaned"`
- File paths like `"/tmp/weather.csv"`
- Passing task results or signals

**Do NOT use XCom for:**
- CSV files  
- Pandas DataFrames  
- Large data

Instead → save data to a file or database, and only push the **file path** via XCom.

---

## Summary

- XCom is for sending **small data between tasks**.
- `ti` is the **task instance** for the current run; I use it for `xcom_push()` and `xcom_pull()`.
- `**context` gives me access to `ti` and other task information.
- XCom should only be used for small info, not full datasets.

