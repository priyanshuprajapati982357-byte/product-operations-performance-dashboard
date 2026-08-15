import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. DATABASE CONNECTION
# ============================================================

password = os.getenv("MYSQL_PASSWORD")

if not password:
    raise ValueError(
        "MYSQL_PASSWORD environment variable is not set."
    )

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="product_operation",
    use_pure=True
)

print("Database connected successfully!")


# ============================================================
# 2. LOAD DATA FROM MYSQL
# ============================================================

tasks = pd.read_sql(
    "SELECT * FROM tasks",
    connection
)

employees = pd.read_sql(
    "SELECT * FROM employees",
    connection
)

projects = pd.read_sql(
    "SELECT * FROM projects",
    connection
)


# ============================================================
# 3. DATA QUALITY CHECKS
# ============================================================

print("\n----- DATASET SHAPE -----")
print(tasks.shape)

print("\n----- COLUMN NAMES -----")
print(tasks.columns.tolist())

print("\n----- DATA TYPES -----")
print(tasks.dtypes)

print("\n----- MISSING VALUES -----")
print(tasks.isnull().sum())

print("\n----- DUPLICATE ROWS -----")
print(tasks.duplicated().sum())


# ============================================================
# 4. DATA CLEANING
# ============================================================

tasks["start_date"] = pd.to_datetime(
    tasks["start_date"]
)

tasks["due_date"] = pd.to_datetime(
    tasks["due_date"]
)

print("\n----- DATA TYPES AFTER CLEANING -----")
print(tasks.dtypes)

print("\n----- INVALID DATE VALUES -----")

print(
    "Invalid start dates:",
    tasks["start_date"].isna().sum()
)

print(
    "Invalid due dates:",
    tasks["due_date"].isna().sum()
)

print("\n----- DUPLICATE TASK IDs -----")

print(
    tasks["task_id"].duplicated().sum()
)


# ============================================================
# 5. TASK STATUS ANALYSIS
# ============================================================

status_analysis = tasks["status"].value_counts()

print("\n----- TASK STATUS VALUES -----")
print(status_analysis)


# ============================================================
# 6. KEY PERFORMANCE INDICATORS
# ============================================================

total_tasks = len(tasks)

completed_tasks = (
    tasks["status"] == "Completed"
).sum()

delayed_tasks = (
    tasks["status"] == "Delayed"
).sum()

completion_rate = (
    completed_tasks / total_tasks
) * 100


print("\n----- COMPLETION KPI -----")

print("Total Tasks:", total_tasks)

print("Completed Tasks:", completed_tasks)

print(
    "Completion Rate:",
    round(completion_rate, 2),
    "%"
)


print("\n----- DELAY KPI -----")

print("Delayed Tasks:", delayed_tasks)


# ============================================================
# 7. EMPLOYEE WORKLOAD ANALYSIS
# ============================================================

employee_workload = (
    tasks
    .groupby("employee_id")
    .size()
    .reset_index(name="total_tasks")
)

employee_workload = employee_workload.merge(
    employees[
        [
            "employee_id",
            "employee_name",
            "department",
            "role"
        ]
    ],
    on="employee_id",
    how="left"
)

employee_workload = employee_workload.sort_values(
    "total_tasks",
    ascending=False
)

print("\n----- EMPLOYEE WORKLOAD -----")

print(employee_workload)


# ============================================================
# 8. PROJECT PERFORMANCE ANALYSIS
# ============================================================

project_performance = (
    tasks
    .groupby("project_id")
    .agg(
        total_tasks=("task_id", "count"),

        completed_tasks=(
            "status",
            lambda x: (
                x == "Completed"
            ).sum()
        ),

        delayed_tasks=(
            "status",
            lambda x: (
                x == "Delayed"
            ).sum()
        )
    )
    .reset_index()
)


# Calculate completion rate

project_performance["completion_rate"] = (
    project_performance["completed_tasks"]
    / project_performance["total_tasks"]
    * 100
).round(2)


# Add project information

project_performance = project_performance.merge(
    projects[
        [
            "project_id",
            "project_name",
            "client"
        ]
    ],
    on="project_id",
    how="left"
)


# Arrange columns

project_performance = project_performance[
    [
        "project_id",
        "project_name",
        "client",
        "total_tasks",
        "completed_tasks",
        "delayed_tasks",
        "completion_rate"
    ]
]


# Sort by completion rate

project_performance = project_performance.sort_values(
    "completion_rate",
    ascending=False
)


print("\n----- PROJECT PERFORMANCE -----")

print(project_performance)


# ============================================================
# 9. TASK STATUS VISUALIZATION
# ============================================================

status_counts = tasks["status"].value_counts()

plt.figure(figsize=(8, 5))

status_counts.plot(kind="bar")

plt.title("Task Status Distribution")

plt.xlabel("Task Status")

plt.ylabel("Number of Tasks")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    "task_status_distribution.png",
    dpi=300
)

plt.show()


# ============================================================
# 10. EMPLOYEE WORKLOAD VISUALIZATION
# ============================================================

workload_chart = employee_workload.sort_values(
    "total_tasks",
    ascending=True
)

plt.figure(figsize=(9, 5))

plt.barh(
    workload_chart["employee_name"],
    workload_chart["total_tasks"]
)

plt.title("Employee Workload")

plt.xlabel("Number of Tasks")

plt.ylabel("Employee")

plt.tight_layout()

plt.savefig(
    "employee_workload.png",
    dpi=300
)

plt.show()


# ============================================================
# 11. PROJECT COMPLETION VISUALIZATION
# ============================================================

project_chart = project_performance.sort_values(
    "completion_rate",
    ascending=True
)

plt.figure(figsize=(9, 5))

plt.barh(
    project_chart["project_name"],
    project_chart["completion_rate"]
)

plt.title("Project Completion Rate")

plt.xlabel("Completion Rate (%)")

plt.ylabel("Project")

plt.xlim(0, 100)

plt.tight_layout()

plt.savefig(
    "project_completion_rate.png",
    dpi=300
)

plt.show()


# ============================================================
# 12. EXPORT ANALYSIS DATA TO EXCEL
# ============================================================

output_file = "Product_Operations_Dashboard.xlsx"

with pd.ExcelWriter(
    output_file,
    engine="openpyxl"
) as writer:

    tasks.to_excel(
        writer,
        sheet_name="Tasks",
        index=False
    )

    employees.to_excel(
        writer,
        sheet_name="Employees",
        index=False
    )

    projects.to_excel(
        writer,
        sheet_name="Projects",
        index=False
    )

    employee_workload.to_excel(
        writer,
        sheet_name="Employee Workload",
        index=False
    )

    project_performance.to_excel(
        writer,
        sheet_name="Project Performance",
        index=False
    )


print("\n----- EXCEL EXPORT -----")

print(
    "Excel analysis file created successfully:",
    output_file
)


# ============================================================
# 13. CLOSE DATABASE CONNECTION
# ============================================================

connection.close()

print("\nDatabase connection closed.")

print("Analysis completed successfully!")