CREATE TABLE Teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL, -- Not sure if the name should be unique.
   	gender TEXT
);

CREATE TABLE Players (
    player_id TEXT PRIMARY KEY,
    player_name TEXT
);

CREATE TABLE Matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    match_type TEXT,
    match_date TEXT NOT NULL,
    method TEXT,
    result TEXT,
    winner_id INTEGER,
    UNIQUE(team1_id, team2_id, match_date),
    FOREIGN KEY(team1_id) REFERENCES Teams(team_id),
    FOREIGN KEY(team2_id) REFERENCES Teams(team_id),
    FOREIGN KEY(winner_id) REFERENCES Teams(team_id)
);


CREATE TABLE Match_Players (
    match_player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    player_id TEXT NOT NULL,
    UNIQUE(match_id, player_id),
    FOREIGN KEY(match_id) REFERENCES Matches(match_id),
    FOREIGN KEY(team_id) REFERENCES Teams(team_id),
    FOREIGN KEY(player_id) REFERENCES Players(player_id)
);

CREATE TABLE Innings (
    innings_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    FOREIGN KEY(match_id) REFERENCES Matches(match_id),
    FOREIGN KEY(team_id) REFERENCES Teams(team_id)
);

CREATE TABLE Deliveries (
    delivery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    innings_id INTEGER NOT NULL,
    batter_id TEXT NOT NULL,
    bowler_id TEXT NOT NULL,
    non_striker_id TEXT NOT NULL,
    batter_runs INTEGER NOT NULL,
    extras INTEGER NOT NULL,
    total_runs INTEGER NOT NULL,
    FOREIGN KEY(innings_id) REFERENCES Innings(innings_id),
    FOREIGN KEY(batter_id) REFERENCES Players(player_id),
    FOREIGN KEY(bowler_id) REFERENCES Players(player_id),
    FOREIGN KEY(non_striker_id) REFERENCES Players(player_id)
);
