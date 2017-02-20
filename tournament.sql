-- Table definitions for the tournament.
--

CREATE TABLE players ( id SERIAL PRIMARY KEY NOT NULL, 
	                  name TEXT NOT NULL );

CREATE TABLE standings ( player_id INTEGER NOT NULL, 
	                    wins INTEGER, 
	                    matches INTEGER,
	                    FOREIGN KEY (player_id) REFERENCES players(id) );


