CREATE TABLE IF NOT EXISTS TeamGameSide(
    -- Primary Keys --
    teamGameSideID INT NOT NULL,

    -- Attributes --
    side VARCHAR(2),

    -- Foreign Keys --
    teamID INT NOT NULL,
    gameRoundID INT NOT NULL
);