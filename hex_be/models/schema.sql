DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS game;

CREATE TABLE player(
  player_id INTEGER PRIMARY KEY,
  player_name TEXT NOT NULL
);


CREATE TABLE game(
  game_id INTEGER PRIMARY KEY,
  belongs_to_player_id INTEGER,
  levl INTEGER,
  difficulty TEXT,
  width INTEGER, 
  height INTEGER, 
  hex_nr_width INTEGER,
  hex_nr_height INTEGER,
  FOREIGN KEY (belongs_to_player_id) REFERENCES player (player_id)
);

CREATE INDEX idx_games_belongs_to ON game (belongs_to_player_id);