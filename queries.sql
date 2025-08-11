-- List of rooms and the number of students in each.
SELECT
    r.id,
    r.name,
    COUNT(s.id) AS student_count
FROM rooms r
LEFT JOIN students s ON s.room_id = r.id
GROUP BY r.id, r.name
ORDER BY r.id;

-- Top 5 rooms with the smallest average student age
SELECT
    r.id,
    r.name,
    AVG(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS avg_age
FROM rooms r
JOIN students s ON s.room_id = r.id
GROUP BY r.id, r.name
ORDER BY avg_age ASC
LIMIT 5;


-- Top 5 rooms with the largest age difference among students
SELECT
    r.id,
    r.name,
    MAX(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) - MIN(TIMESTAMPDIFF(YEAR, s.birthday, CURDATE())) AS age_diff
FROM rooms r
JOIN students s ON s.room_id = r.id
GROUP BY r.id, r.name
ORDER BY age_diff DESC
LIMIT 5;


-- List of rooms where students of different sexes live together
SELECT
    r.id,
    r.name
FROM rooms r
JOIN students s ON s.room_id = r.id
GROUP BY r.id, r.name
HAVING COUNT(DISTINCT s.sex) > 1;