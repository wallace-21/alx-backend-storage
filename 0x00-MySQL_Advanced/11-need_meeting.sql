-- Script that creates a view

CREATE VIEW need_meeting AS
SELECT name FROM students
WHERE score < 80 AND last_meeting is NULL OR (CURDATE() - last_meeting) > 30;
