-- ============================================
-- PRODUCT OPERATIONS & PERFORMANCE DASHBOARD
-- SQL Analysis Queries
-- ============================================

-- Select database
USE product_operation;


-- 1. View all employees
SELECT *
FROM employees;


-- 2. View all projects
SELECT *
FROM projects;


-- 3. View all tasks
SELECT *
FROM tasks;


-- 4. Count total number of tasks
SELECT COUNT(*) AS total_tasks
FROM tasks;


-- 5. Count tasks by status
SELECT
    status,
    COUNT(*) AS task_count
FROM tasks
GROUP BY status
ORDER BY task_count DESC;


-- 6. Count tasks by priority
SELECT
    priority,
    COUNT(*) AS task_count
FROM tasks
GROUP BY priority
ORDER BY task_count DESC;


-- 7. Employee workload
SELECT
    employee_id,
    COUNT(*) AS total_tasks
FROM tasks
GROUP BY employee_id
ORDER BY total_tasks DESC;


-- 8. Completed tasks by employee
SELECT
    employee_id,
    COUNT(*) AS completed_tasks
FROM tasks
WHERE status = 'Completed'
GROUP BY employee_id
ORDER BY completed_tasks DESC;


-- 9. Project-wise total tasks
SELECT
    project_id,
    COUNT(*) AS total_tasks
FROM tasks
GROUP BY project_id
ORDER BY total_tasks DESC;


-- 10. Project-wise completed tasks
SELECT
    project_id,
    COUNT(*) AS completed_tasks
FROM tasks
WHERE status = 'Completed'
GROUP BY project_id
ORDER BY completed_tasks DESC;


-- 11. Find delayed tasks
SELECT *
FROM tasks
WHERE status = 'Delayed';


-- 12. Find high-priority delayed tasks
SELECT *
FROM tasks
WHERE priority = 'High'
  AND status = 'Delayed';


-- 13. Find tasks currently in progress
SELECT *
FROM tasks
WHERE status = 'In Progress';

-- ============================================
-- JOIN-BASED BUSINESS ANALYSIS
-- ============================================

-- 14. Tasks with employee names
SELECT
    t.task_id,
    t.task_name,
    e.employee_name,
    e.department,
    t.priority,
    t.status
FROM tasks t
JOIN employees e
    ON t.employee_id = e.employee_id;


-- 15. Tasks with project names
SELECT
    t.task_id,
    t.task_name,
    p.project_name,
    p.client,
    t.priority,
    t.status
FROM tasks t
JOIN projects p
    ON t.project_id = p.project_id;


-- 16. Complete task information
SELECT
    t.task_id,
    t.task_name,
    p.project_name,
    e.employee_name,
    e.department,
    t.priority,
    t.start_date,
    t.due_date,
    t.status
FROM tasks t
JOIN employees e
    ON t.employee_id = e.employee_id
JOIN projects p
    ON t.project_id = p.project_id;


-- 17. Employee-wise workload with employee names
SELECT
    e.employee_id,
    e.employee_name,
    e.department,
    COUNT(t.task_id) AS total_tasks
FROM employees e
LEFT JOIN tasks t
    ON e.employee_id = t.employee_id
GROUP BY
    e.employee_id,
    e.employee_name,
    e.department
ORDER BY total_tasks DESC;


-- 18. Project-wise task status
SELECT
    p.project_name,
    t.status,
    COUNT(*) AS task_count
FROM projects p
JOIN tasks t
    ON p.project_id = t.project_id
GROUP BY
    p.project_name,
    t.status
ORDER BY
    p.project_name,
    task_count DESC;