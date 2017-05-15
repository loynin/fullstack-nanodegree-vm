#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches;")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players;")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM players;")
    results = c.fetchone()
    db.close()
    return results[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name.
    """
    db = connect()
    c = db.cursor()
    sqlstr = "INSERT INTO players(name) VALUES(%s);"
    c.execute(sqlstr,(name,))
    db.commit()
    db.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played

    """
    db = connect()
    c = db.cursor()
    
    players = """SELECT players.id, players.name, view_wins.wins, view_played.played 
                  FROM players INNER JOIN view_wins on players.id = view_wins.id 
                  INNER JOIN view_played on players.id = view_played.id 
                  ORDER BY view_wins.wins;"""

    c.execute(players)
   
    ranks = []
    for row in c.fetchall():
        ranks.append(row)

    db.close()
    return ranks


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    match = ("INSERT INTO matches (winner,loser) VALUES (%s,%s);")
    c.execute(match,(winner,loser,))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    ranks = playerStandings()
    pairs = []

    totalPlayers = countPlayers()

    while len(ranks) >1:
        validMatch = checkPairs(ranks,0,1)
        player1 = ranks.pop(0)
        player2 = ranks.pop(validMatch-1)
        pairs.append((player1[0],player1[1],player2[0],player2[1]))

    return pairs


def checkPairs(ranks, id1, id2):
    """Checks if two players have already had a match against each other.
    If they have, recursively checks through the list until a valid match is
    found.
    Args:

        ranks: list of current ranks from swissPairings()
        id1: player needing a match
        id2: potential matched player
    Returns id of matched player or original match if none are found.
    """
    if id2 >= len(ranks):
        return id1 + 1
    elif validPair(ranks[id1][0], ranks[id2][0]):
        return id2
    else:
        return checkPairs(ranks, id1, (id2 + 1))


def validPair(player1, player2):
    """Checks if two players have already played against each other
    Args:
        player1: the id number of first player to check
        player2: the id number of potentail paired player
        
    Return true if valid pair, false if not
    """
    db = connect()
    c = db.cursor()
    sql = """SELECT winner, loser
             FROM matches
             WHERE ((winner = %s AND loser = %s)
                    OR (winner = %s AND loser = %s))"""
    c.execute(sql, (player1, player2, player2, player1))
    matches = c.rowcount
    db.close()
    if matches > 0:
        return False
    return True


