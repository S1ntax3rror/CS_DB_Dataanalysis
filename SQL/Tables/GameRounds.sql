CREATE TABLE IF NOT EXISTS GameRounds(
    -- Primary Key --
    gameRoundID INT NOT NULL,

    -- Attributes --
    tBuyType VARCHAR,
    winningSide VARCHAR,
    ctBuyType VARCHAR,
    roundEndReason VARCHAR,
    roundNum INT,
    startTick INT,
    endTick INT,
    bombPlantTick INT, -- ?
    endOfficialTick INT,
    ctRoundStartEqVal INT,
    tScore INT,
    endCTScore INT,
    ctScore INT,
    tRoundSpendMoney INT,
    tFreezeTimeEndEqVal INT,
    ctRoundSpendMoney INT,
    tRoundStartEqVal INT,
    ctFreezeTimeEndEqVal INT,
    endTScore INT,
    freezeTimeEndTick INT,
    isWarmup BOOLEAN,


    -- Foreign Key --
    gameID INT NOT NULL
);