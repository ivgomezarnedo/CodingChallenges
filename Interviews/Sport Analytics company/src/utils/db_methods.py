import sqlite3
import logging
logging.basicConfig(level=logging.INFO)

connection = None


def get_sqlite_connection(db_location: str) -> sqlite3.Connection:
    """
    Singleton to return a SQLite connection or to declare it if there is none
    :param db_location: Location of the SQLite database
    :return: SQLite connection
    """
    global connection
    if connection is None:
        connection = sqlite3.connect(db_location)
        connection.row_factory = sqlite3.Row
    return connection


def close_sqlite_connection():
    """
    Close SQLite connection if there is one open and initialize to None the connection variable.
    :return:
    """
    global connection
    if connection is not None:
        connection.close()
    connection = None


def get_team_names(conn: sqlite3.Connection) -> dict:
    """
    Queries the DB and returns a dictionary with the team names and genders as keys and their ids as values
    :param conn: SQLite connection
    :return: dictionary
    """
    cur = conn.cursor()
    cur.execute("SELECT team_id, team_name, gender FROM Teams")
    return {(row[1], row[2]): row[0] for row in cur.fetchall()}


def get_player_names(conn: sqlite3.Connection) -> dict:
    """
    Queries the DB and returns a dictionary with the player names as keys and their ids as values
    :param conn: SQLite connection
    :return: dictionary
    """
    cur = conn.cursor()
    cur.execute("SELECT player_id, player_name FROM Players")
    return {row[1]: row[0] for row in cur.fetchall()}


def get_match_id(conn: sqlite3.Connection, team1_id: int, team2_id: int, match_date: str) -> int:
    """
    Queries the DB and returns a match id
    :param conn: SQLite connection
    :param team1_id: id of the first team
    :param team2_id: id of the second team
    :param match_date: date of the match
    :return: match id
    """
    cur = conn.cursor()
    cur.execute("SELECT match_id FROM Matches WHERE team1_id = ? AND team2_id = ? AND match_date = ?", (team1_id, team2_id, match_date))
    return cur.fetchone()[0]


def get_match_id(conn: sqlite3.Connection, team1_id: int, team2_id: int, match_date: str) -> int:
    """
    Queries the DB and returns a match id
    :param conn: SQLite connection
    :param team1_id: id of the first team
    :param team2_id: id of the second team
    :param match_date: date of the match
    :return: match id
    """
    cur = conn.cursor()
    cur.execute("SELECT match_id FROM Matches WHERE team1_id = ? AND team2_id = ? AND match_date = ?", (team1_id, team2_id, match_date))
    return cur.fetchone()[0]


def insert_team(conn: sqlite3.Connection, team_key: tuple) -> int:
    """
    Inserts a team into the DB and returns its id
    :param conn: SQLite connection
    :param team_key: team name and gender
    :return:
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO Teams (team_name, gender) VALUES (?, ?)", team_key)
    return cur.lastrowid


def insert_match_data(conn: sqlite3.Connection, team_1: int, team_2: int, match_date: str, match_type: str,
                      method: str, result: str, team_winner: int) -> int:
    """
    Inserts a match into the DB and returns its id. If the match already exists, returns its id.
    :param conn: SQLite connection
    :param team_1: id of the first team
    :param team_2: id of the second team
    :param match_date: date of the match
    :param match_type: type of match (ODI, T20...)
    :param method: method of victory (runs, wickets...)
    :param result: match result (win, tie...)
    :param team_winner: id of the winning team
    :return: match id
    """
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO Matches (team1_id, team2_id, match_date, match_type, method, result, winner_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (team_1, team_2, match_date, match_type, method, result, team_winner))
        match_id = cur.lastrowid
    except sqlite3.IntegrityError:
        logging.warning(f"Attempted to insert duplicate Match")
        match_id = get_match_id(conn, team_1, team_2, match_date)
    return match_id


def insert_player(conn: sqlite3.Connection, player_id: str, player_name: str):
    """
    Inserts a player into the DB
    :param conn: SQLite connection
    :param player_id: ID of a player
    :param player_name: Name of a player
    :return:
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Players (player_id, player_name) VALUES (?, ?)", (player_id, player_name))
    except sqlite3.IntegrityError:
        logging.warning(f"Attempted to insert duplicate Player_id: {player_id}")


def insert_match_player(conn: sqlite3.Connection, match_id: int, team_id: int, player_id: str):
    """
    Inserts a match player into the DB
    :param conn: SQLite connection
    :param match_id: id of the match
    :param team_id: id of the team
    :param player_id: id of the player
    :return:
    """
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Match_Players (match_id, team_id, player_id) VALUES (?, ?, ?)", (match_id, team_id, player_id))
    except sqlite3.IntegrityError:
        logging.warning(f"Attempted to insert duplicate row with Match_id {match_id} and Player_id: {player_id}")


def insert_innings(conn: sqlite3.Connection, match_id: int , team_id: int) -> int:
    """
    Inserts an innings into the DB and returns its id
    :param conn: SQLite connection
    :param match_id: id of the match
    :param team_id: id of the team
    :return: innings id
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO Innings (match_id, team_id) VALUES (?, ?)", (match_id, team_id))
    # No UNIQUE constraint on Innings, so no need to catch IntegrityError
    return cur.lastrowid


def insert_delivery(conn: sqlite3.Connection, innings_id: int, batter_id: str, bowler_id: str, non_striker_id: str, batter_runs: int, extras: int, total_runs: int):
    """
    Inserts a delivery into the DB
    :param conn: SQLite connection
    :param innings_id: id of the innings
    :param batter_id: Player id of the batter
    :param bowler_id: Player id of the bowler
    :param non_striker_id: Player id of the non-striker
    :param batter_runs: Runs scored by the batter
    :param extras: Extras scored
    :param total_runs: Total runs scored
    :return:
    """
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Deliveries (innings_id, batter_id, bowler_id, non_striker_id, batter_runs, extras, total_runs) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (innings_id, batter_id, bowler_id, non_striker_id, batter_runs, extras, total_runs)
    )
    # No UNIQUE constraint on Deliveries, so no need to catch IntegrityError


