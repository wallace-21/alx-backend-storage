-- script that creates a stored procedure

DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    SELECT SUM(score * weight) / SUM(weight) INTO @average_weighted_score FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
    UPDATE users SET average_score = @average_weighted_score WHERE id = user_id;
END;$$
DELIMITER ;
