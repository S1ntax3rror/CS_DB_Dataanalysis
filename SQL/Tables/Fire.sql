CREATE TABLE IF NOT EXISTS Fire(
    -- Primary Key --
    uniqueID BIGINT,

    -- Attributes --
    x REAL,
    y REAL,
    z REAL,

    -- Foreign Keys --
    frameID INT
);