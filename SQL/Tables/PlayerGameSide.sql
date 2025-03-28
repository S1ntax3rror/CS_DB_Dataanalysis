CREATE TABLE IF NOT EXISTS PlayerGameSide(
    -- Primary Keys
    playerGameSideID INT NOT NULL,

    -- Foreign Keys --
    teamGameSideID INT NOT NULL,
    playerID INT NOT NULL
);