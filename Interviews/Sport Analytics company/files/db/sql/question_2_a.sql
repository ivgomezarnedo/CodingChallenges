
--QUESTION 2: a) 
--The win records (percentage win and total wins) for each team by year and gender, excluding ties,
--matches with no result, and matches decided by the DLS method in the event that, for whatever
-- reason, the planned innings can’t be completed.

CREATE VIEW IF NOT EXISTS team_year_win_percentage_view as
   SELECT total.*, COALESCE(wins.total_wins,0) as total_wins, ROUND((CAST(COALESCE(wins.total_wins,0) AS REAL)/ CAST(total.total_matches AS REAL))*100,2) as win_percentage
   FROM (
	   select team_id, team_name, gender, strftime('%Y', match_date) as year, count(distinct match_id) as total_matches
	   from Teams t join Matches m on t.team_id=m.team1_id or t.team_id =m.team2_id 
	   group by team_id, team_name, strftime('%Y', match_date)
   ) AS total 
   LEFT JOIN (
      select winner_id, strftime('%Y', match_date) as year, count(*) as total_wins
	   from Matches
	where result='win' and (method is null or method!='DLS')
	group by winner_id, strftime('%Y', match_date)
   ) as wins on total.team_id=wins.winner_id and total.year=wins.year;
  
  
 select *
 from team_year_win_percentage_view
 order by team_id, year asc;




SELECT batter_id, player_name, ROUND(CAST(total_runs AS REAL) / CAST(total_balls AS REAL) * 100,2) as strike_rate
FROM (
    SELECT 
        d.batter_id,
        p.player_name,
        SUM(d.total_runs) as total_runs,
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


