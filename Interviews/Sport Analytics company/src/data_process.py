from utils import db_methods
import logging
import sqlite3


def _insert_teams(conn: sqlite3.Connection, teams: list, gender: str) -> dict:
    """
    This function is used to insert teams into a database if they are not already present.
    :param conn: SQLite connection
    :param teams: List of teams
    :param gender: Gender of the teams
    :return: A dictionary (teams_match) where the key is a tuple of team name and gender, and the value is the team's id in the database.
    """
    teams_db = db_methods.get_team_names(conn)
    teams_match = {}
    for team in teams:
        team_key = (team, gender)  # The team's unique key is (name, gender)
        if team_key not in list(teams_db.keys()):  # If the team is not in the database, insert it
            team_id = db_methods.insert_team(conn, (team, gender))
            teams_match[team_key] = team_id
        else:
            teams_match[team_key] = teams_db.get(team_key)
    return teams_match


def _insert_match_data(conn: sqlite3.Connection, match_date: str, match_type: str, outcome: dict, teams_match: dict, gender: str):
    """
    Extracts information from the match and inserts it into the database.
    :param conn: SQLite connection
    :param match_date: The date when the match took place
    :param match_type: The type of the match (e.g., 'ODI', 'Test').
    :param outcome: A dictionary containing information about the match outcome
    :param teams_match: A dictionary where the key is a tuple of team name and gender, and the value is the team's id in the database.
    :param gender: A string indicating the gender of the teams involved in the match.
    :return: The id of the match inserted into the database.
    """
    method = outcome.get('method')
    winner = outcome.get('winner')
    result = outcome.get('result') if outcome.get('result') else 'win'
    team_1 = list(teams_match.values())[0]
    team_2 = list(teams_match.values())[1]
    team_winner = teams_match.get((winner, gender))  # The winner team is always going to be one of the teams in the match

    return db_methods.insert_match_data(conn, team_1, team_2, match_date, match_type, method, result, team_winner)


def _insert_players(conn: sqlite3.Connection, match_id: int, players_match: dict, teams_match: dict, players_by_teams: dict):
    """
    Extracts all the players from each team in a match and inserts them into the database.
    :param conn: SQLite connection
    :param match_id: The id of the match in the database
    :param players_match: A dictionary where the key is a player's name and the value is the player's id
    :param teams_match: A dictionary where the key is a tuple of team name and gender, and the value is the team's id in the database.
    :param players_by_teams: A dictionary where the key is a team name and the value is a list of players in that team.
    :return: None. This function operates by side effects, inserting data into the database.
    """
    for team_key in teams_match.keys():
        team_name = team_key[0]
        for player in players_by_teams[team_name]:
            player_id = players_match[player]
            try:
                players_db = db_methods.get_player_names(conn)  # Recheck the database immediately before insertion. TODO: This is inefficient. Fix it.
                if player_id not in list(players_db.values()):  # Player_id not in the DB
                    db_methods.insert_player(conn, player_id, player)
            except sqlite3.IntegrityError:
                logging.warning(f"Attempted to insert duplicate player ID {player_id}")
            db_methods.insert_match_player(conn, match_id, teams_match[team_key], player_id)


def _get_innings_by_team(match, teams_match: dict) -> dict:
    """
    This function organizes innings data by the team name. Each team's innings is a list of deliveries.
    :param match: A dictionary containing match data
    :param teams_match: A dictionary where the key is a tuple of team name and gender, and the value is the team's id in the database.
    :return: A dictionary where the key is a team name and the value is a list of deliveries for that team.
    """
    innings_by_team = {}
    for team_key in teams_match.keys():
        team_name = team_key[0]
        innings_by_team[team_name] = []
    for innings in match['innings']:
        for over in innings['overs']:
            innings_by_team[innings['team']].extend(over['deliveries'])
    return innings_by_team


def _insert_deliveries(conn: sqlite3.Connection, deliveries, innings_id, players_match):
    """
    This function is used to insert deliveries into the database.
    :param conn: SQLite connection
    :param deliveries: A list of deliveries.
    :param innings_id: The id of the innings.
    :param players_match: A dictionary mapping player names to their IDs.
    :return: None. This function operates by side effects, inserting data into the database.
    """
    for delivery_info in deliveries:
        batter = players_match.get(delivery_info['batter'])
        bowler = delivery_info['bowler']
        non_striker = delivery_info['non_striker']
        batter_runs = delivery_info['runs']['batter']
        extras = delivery_info['runs']['extras']
        total_runs = delivery_info['runs']['total']
        db_methods.insert_delivery(conn, innings_id, batter, bowler, non_striker, batter_runs, extras, total_runs)


def _insert_innings_and_deliveries(conn: sqlite3.Connection, innings_by_team: dict, teams_match: dict, match_id: int, gender: str, players_match: dict):
    """
    This function is used to insert innings and deliveries into the database.
    :param conn: SQLite connection
    :param innings_by_team: A dictionary where the key is a team name and the value is a list of deliveries for that team.
    :param teams_match: A dictionary where the key is a tuple of team name and gender, and the value is the team's id in the database.
    :param match_id: The id of the match in the database
    :param gender: A string indicating the gender of the teams involved in the match.
    :param players_match: A dictionary mapping player names to their IDs.
    :return: None. This function operates by side effects, inserting data into the database.
    """
    for team, deliveries in innings_by_team.items():
        innings_id = db_methods.insert_innings(conn, match_id, teams_match.get((team, gender)))
        _insert_deliveries(conn, deliveries, innings_id, players_match)


def insert_match(conn: sqlite3.Connection, match: dict):
    """
    Main of the execution. Given a match, this function process the data and inserts it into the database.
    :param conn: SQLite connection
    :param match: A dictionary containing match data
    :return: None. This function operates by side effects, inserting data into the database.
    """
    # Parsing the data and inserting into the tables
    info = match['info']
    players = info['registry']['people']
    players_by_team = info['players']
    gender = info['gender']
    match_date = info['dates'][0]
    match_type = info['match_type']
    outcome = match['info']['outcome']

    if match_type != 'ODI':
        logging.info("Match is not an ODI")
        return

    # Inserting teams
    teams_match = _insert_teams(conn, info['teams'], gender)
    # Inserting match
    match_id = _insert_match_data(conn, match_date, match_type, outcome, teams_match, gender)
    # Inserting players
    _insert_players(conn, match_id, players, teams_match, players_by_team)

    innings_by_team = _get_innings_by_team(match, teams_match)
    # Inserting innings and deliveries
    _insert_innings_and_deliveries(conn, innings_by_team, teams_match, match_id, gender, players)

    conn.commit()  # Committing the changes to the database. Avoid committing after each insertion and only commits when all the data of a match has been inserted.
    logging.info(f"Inserted match {match_id} data into the database")


