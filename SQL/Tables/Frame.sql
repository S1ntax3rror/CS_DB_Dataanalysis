CREATE TABLE IF NOT EXISTS Frame (
    -- Primary Key --
    frameID INT,

    -- Attributes --
    clockTime VARCHAR(5),
    seconds REAL,
    bombX REAL,
    bombY REAL,
    bombZ REAL,
    tick INT,

    -- Foreign Keys --
    gameRoundID INT
);