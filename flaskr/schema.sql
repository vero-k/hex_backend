DROP TABLE IF EXISTS player;

CREATE TABLE player(
  id INTEGER PRIMARY KEY,
  user_id TEXT NOT NULL,
  levl INTEGER,
  difficulty TEXT,
  width INTEGER, 
  height INTEGER, 
  hex_nr_width INTEGER,
  hex_nr_height INTEGER);