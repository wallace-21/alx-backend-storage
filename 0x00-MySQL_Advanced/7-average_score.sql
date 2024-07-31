-- creates a stored procedure

DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    SELECT AVG(score) INTO @average_score FROM corrections WHERE corrections.user_id = user_id;
    UPDATE users SET average_score = @average_score WHERE id = user_id;
END;$$
DELIMITER ;
