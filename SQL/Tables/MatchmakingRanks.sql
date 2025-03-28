CREATE TABLE IF NOT EXISTS MatchmakingRanks (
    -- Primary Key --
    matchMakingRanksID INT NOT NULL,

    -- Attributes
    rankOld VARCHAR,
    rankNew VARCHAR,
    rankChange INT,
    winCount INT,

    -- Foreign Keys --
    playerID INT NOT NULL,
    gameID INT NOT NULL
);