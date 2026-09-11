SELECT building, COUNT(*) AS complaint_count
FROM complaints
GROUP BY building
ORDER BY complaint_count DESC;

SELECT department, COUNT(*) AS unresolved_count
FROM complaints
WHERE status <> 'Resolved'
GROUP BY department
ORDER BY unresolved_count DESC;

SELECT category, ROUND(AVG(resolution_days), 2) AS avg_resolution_days
FROM complaints
WHERE resolution_days IS NOT NULL
GROUP BY category
ORDER BY avg_resolution_days DESC;
