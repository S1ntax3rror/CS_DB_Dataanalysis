CREATE TABLE IF NOT EXISTS Game (
    -- Primary Key --
    gameID INT,

    -- Attributes --
    matchId VARCHAR,
    matchName VARCHAR,
    hltvUrl VARCHAR,
    clientName VARCHAR,
    mapName VARCHAR,
    demoID VARCHAR,
    matchDate INT,
    playbackFramesCount INT,
    playbackTicks INT,
    parsedToFrameIdx INT,
    tickRate INT,


    -- Foreign Keys --
    serverVarID INT NOT NULL,
    tournamentID INT
);