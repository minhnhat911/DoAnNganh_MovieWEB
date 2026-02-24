USE movieweb_db;

DELIMITER //

CREATE PROCEDURE get_top_10_movies_by_views (
    IN time_period VARCHAR(10),   
    IN p_month INT,            
    IN p_year  INT              
)
BEGIN
    -- daily: giữ nguyên - theo ngày hiện tại
    IF time_period = 'daily' THEN
        SELECT m.title, SUM(e.views) AS total_views
        FROM movies m
        JOIN episodes e ON m.id = e.movie_id
        WHERE DATE(m.created_at) = CURDATE()
        GROUP BY m.id
        ORDER BY total_views DESC
        LIMIT 10;

    -- weekly: giữ nguyên - theo tuần hiện tại (ISO, mode 1)
    ELSEIF time_period = 'weekly' THEN
        SELECT m.title, SUM(e.views) AS total_views
        FROM movies m
        JOIN episodes e ON m.id = e.movie_id
        WHERE YEARWEEK(m.created_at, 1) = YEARWEEK(CURDATE(), 1)
        GROUP BY m.id
        ORDER BY total_views DESC
        LIMIT 10;

    -- monthly: dùng tháng/năm người dùng, NULL thì mặc định tháng/năm hiện tại
    ELSEIF time_period = 'monthly' THEN
        SELECT m.title, SUM(e.views) AS total_views
        FROM movies m
        JOIN episodes e ON m.id = e.movie_id
        WHERE YEAR(m.created_at)  = COALESCE(p_year,  YEAR(CURDATE()))
          AND MONTH(m.created_at) = COALESCE(p_month, MONTH(CURDATE()))
        GROUP BY m.id
        ORDER BY total_views DESC
        LIMIT 10;

    -- yearly: dùng năm người dùng, NULL thì mặc định năm hiện tại
    ELSEIF time_period = 'yearly' THEN
        SELECT m.title, SUM(e.views) AS total_views
        FROM movies m
        JOIN episodes e ON m.id = e.movie_id
        WHERE YEAR(m.created_at) = COALESCE(p_year, YEAR(CURDATE()))
        GROUP BY m.id
        ORDER BY total_views DESC
        LIMIT 10;

    -- mặc định: toàn thời gian
    ELSE
        SELECT m.title, SUM(e.views) AS total_views
        FROM movies m
        JOIN episodes e ON m.id = e.movie_id
        GROUP BY m.id
        ORDER BY total_views DESC
        LIMIT 10;
    END IF;
END //

DELIMITER ;


CALL get_top_10_movies_by_views('all', NULL, NULL);