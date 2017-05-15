-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--
-- Delete database tournament if exist

DROP DATABASE IF EXISTS tournament;

-- Create database name tournament
CREATE DATABASE tournament;

-- Connect to database
\c tournament;

-- Create table name player
CREATE TABLE players(
    id serial,
    name text
    );

-- Create table name matchese
CREATE TABLE matches(
    id serial,
    winner integer,
    loser integer
    );

-- Create view to select how many win a player has
create view view_wins as
select players.id, count(matches.id) as wins
from players left outer join matches
    on players.id = matches.winner
group by players.id;

-- Create view to select how many plays a player has
create view view_played as
select players.id, count(matches.id) as played
from players left outer join matches
    on players.id = matches.winner or players.id = matches.loser
group by players.id;
