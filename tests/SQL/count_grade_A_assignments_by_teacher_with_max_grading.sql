-- Write query to find the number of grade A's given by the teacher who has graded the most assignments


SELECT COUNT(*) AS num_grade_a_assignments
FROM assignments a
INNER JOIN (
  SELECT teacher_id, COUNT(*) AS num_graded_assignments
  FROM assignments
  WHERE grade IS NOT NULL
  GROUP BY teacher_id
  ORDER BY num_graded_assignments DESC
  LIMIT 1
) g ON a.teacher_id = g.teacher_id
WHERE a.grade = 'A';
