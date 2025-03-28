CREATE TABLE IF NOT EXISTS Kill(
    -- Primary Key --
    killID INT NOT NULL,

    -- Foreign Keys --
    attackerPlayerFrameID INT,
    victimPlayerFrameID INT,
    assisterPlayerFrameID INT,
    tradedPlayerFrameID INT,
    flashThrowerPlayerFrameID INT,
    weaponID INT,
    frameID INT,

    -- Attributes --
    penetratedObjects INT,
    isSuicide BOOLEAN,
    attackerBlinded BOOLEAN,
    victimBlinded BOOLEAN,
    thruSmoke BOOLEAN,
    isTrade BOOLEAN,
    isHeadshot BOOLEAN,
    isFirstKill BOOLEAN,
    isTeamKill BOOLEAN
);