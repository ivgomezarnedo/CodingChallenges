--QUESTION 2: c) 
-- Which players had the highest strike rate as batsmen in 2019? (Note to receive full credit, you
-- need to account for handling extras properly.)


SELECT batter_id, player_name, ROUND(CAST(batter_runs AS REAL) / CAST(total_balls AS REAL) * 100,2) as strike_rate
FROM (
    SELECT 
        d.batter_id,
        p.player_name,
        SUM(d.batter_runs) as batter_runs, -- Only 'batter_runs' are taken into account.
        COUNT(*) as total_balls
    FROM Deliveries d
    JOIN Innings i ON i.innings_id = d.innings_id
    JOIN Matches m ON m.match_id = i.match_id
    JOIN Players p ON p.player_id = d.batter_id
    WHERE strftime('%Y', m.match_date) = '2019'
    GROUP BY d.batter_id, p.player_name
) 
WHERE total_balls > 0
ORDER BY strike_rate DESC
LIMIT 10;

