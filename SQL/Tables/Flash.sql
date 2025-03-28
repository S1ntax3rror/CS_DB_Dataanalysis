CREATE TABLE IF NOT EXISTS Flash(
    -- Primary Key --
    flashID INT NOT NULL,

    -- Attributes --
    flashDuration REAL,

    -- Foreign Keys --
    attackerPlayerFrameID INT,
    playerFrameID INT,
    frameID INT
);