-- ==========================================
-- PRODUCT OPERATIONS SQL ANALYSIS
-- Author: Priyanshu Prajapati
-- ==========================================

USE product_operation;

-- 1. View all tasks
SELECT * FROM tasks;

-- 2. Total number of tasks
SELECT COUNT(*) AS total_tasks
FROM tasks;

-- 3. Task status summary
SELECT status, COUNT(*) AS task_count
FROM tasks
GROUP BY status;

-- 4. Completed task percentage
SELECT
    COUNT(*) AS total_tasks,
    SUM(status = 'Completed') AS completed_tasks,
    ROUND(SUM(status='Completed')*100/COUNT(*),2) AS completion_rate
FROM tasks;

-- 5. Delayed tasks
SELECT * FROM tasks
WHERE status = 'Delayed';

-- 6. Employee workload
SELECT
    e.employee_name,
    COUNT(t.task_id) AS total_tasks
FROM employees e
JOIN tasks t
ON e.employee_id = t.employee_id
GROUP BY e.employee_name
ORDER BY total_tasks DESC;

-- 7. Project performance
SELECT
    p.project_name,
    COUNT(t.task_id) AS total_tasks,
    SUM(t.status='Completed') AS completed_tasks,
    ROUND(SUM(t.status='Completed')*100/COUNT(*),2) AS completion_rate
FROM projects p
JOIN tasks t
ON p.project_id = t.project_id
GROUP BY p.project_name
ORDER BY completion_rate DESC;

-- 8. High priority pending work
SELECT task_name, priority, status
FROM tasks
WHERE priority='High'
AND status!='Completed';
