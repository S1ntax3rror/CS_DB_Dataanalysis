CREATE TABLE IF NOT EXISTS Grenade(
    -- Primary Key --
    grenadeID INT,

    -- Attributes --
    grenadeX REAL,
    grenadeY REAL,
    grenadeZ REAL,
    grenadeType VARCHAR,
    entityID BIGINT,

    -- Foreign Keys --
    throwFrameID INT,
    destroyFrameID INT,
    throwerPlayerFrameID INT
);