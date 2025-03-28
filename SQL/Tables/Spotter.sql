CREATE TABLE IF NOT EXISTS Spotter(
    -- Primary Key --
    spotterID INT,

    -- Foreign Keys --
    playerID INT,
    playerFrameID INT
);