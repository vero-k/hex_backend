
DROP TABLE IF EXISTS playergame;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS player;


CREATE TABLE player(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);


CREATE TABLE game(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  level INTEGER,
  difficulty TEXT,
  width INTEGER, 
  height INTEGER, 
  hex_nr_width INTEGER,
  hex_nr_height INTEGER,
  belongs_to_player_id INTEGER,
  FOREIGN KEY (belongs_to_player_id) REFERENCES player (id)
);

CREATE TABLE playergame (
    player_id INTEGER,
    game_id INTEGER,
    FOREIGN KEY(player_id) REFERENCES player(id),
    FOREIGN KEY(game_id) REFERENCES game(id),
    PRIMARY KEY (player_id, game_id)
);


CREATE INDEX idx_games_belongs_to ON game (belongs_to_player_id);

INSERT INTO player (name) VALUES ('admin');