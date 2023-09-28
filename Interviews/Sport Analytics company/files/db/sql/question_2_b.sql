--QUESTION 2: b) 
-- Which male and female teams had the highest win percentages in 2019?
-- NOTE: It uses the view created in question 2: a)

SELECT gender, team_name, win_percentage
FROM (
    SELECT 
        gender, 
        team_name, 
        win_percentage, 
        ROW_NUMBER() OVER (PARTITION BY gender ORDER BY win_percentage DESC) as rank
    FROM 
        team_year_win_percentage_view
    WHERE 
        year = '2019'
) as teams_ranked
WHERE rank = 1;

