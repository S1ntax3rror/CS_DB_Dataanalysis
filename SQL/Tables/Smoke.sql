CREATE TABLE IF NOT EXISTS Smoke (
    -- Primary Key --
    grenadeEntityID BIGINT,

    -- Attributes --
    x REAL,
    y REAL,
    z REAL,
    startTick INT,

    -- Foreign Keys --
    frameID INT
);