# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()

    cursor.execute('UPDATE standings SET wins = 0, matches = 0')
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()

    cursor.execute('DELETE FROM standings')
    cursor.execute('DELETE FROM players')
    db.commit()
    db.close()
    


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()

    cursor.execute('SELECT COUNT(*) FROM players')
    
    #Fetch the executed query and store the first value of the tuple returned
    total = cursor.fetchone()
    total = total[0]

    return total

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()

    cursor.execute('INSERT INTO players (name) VALUES (%s)', (name,))
    cursor.execute('INSERT INTO standings VALUES ((SELECT id FROM players WHERE name = %s), 0, 0)', (name,))
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
    cursor = db.cursor()
    cursor.execute('SELECT id, name, wins, matches FROM players JOIN standings ON players.id = standings.player_id ORDER BY wins DESC')
    standings_list = cursor.fetchall()
    db.close()
    
    return standings_list

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute('UPDATE standings SET wins = wins + 1 WHERE player_id = %s', (winner,))
    cursor.execute('UPDATE standings SET matches = matches + 1 WHERE player_id = %s', (winner,))
    cursor.execute('UPDATE standings SET matches = matches + 1 WHERE player_id = %s', (loser,))
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
    db = connect()
    cursor = db.cursor()
    cursor.execute('SELECT count(*) FROM standings')
    result = cursor.fetchall()
    
    standings = playerStandings()

    list_tuples = [i[0:2] for i in standings]

    index = 0
    pairings = []

    for row in result:
        while (index < row[0]):
            pair = list_tuples[index] + list_tuples[index + 1]
            pairings.append(pair)
            index = index + 2
    return pairings


if __name__ == '__main__':
    standings = swissPairings()
    print standings
    


