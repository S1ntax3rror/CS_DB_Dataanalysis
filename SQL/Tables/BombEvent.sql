CREATE TABLE IF NOT EXISTS BombEvent(
    -- Primary Key --
    bombEventID INT,

    -- Attributes --
    bombAction VARCHAR,
    bombSite VARCHAR(1),

    -- Foreign Keys --
    playerFrameID INT,
    frameID INT
);