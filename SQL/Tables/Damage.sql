CREATE TABLE IF NOT EXISTS Damage(
    -- Primary Key --
    damageID INT NOT NULL,

    -- Foreign Keys --
    attackerPlayerFrameID INT,
    victimPlayerFrameID INT,
    weaponID INT,
    frameID INT,

    -- Attributes --
    hitGroup VARCHAR,
    armorDamageTaken SMALLINT,
    armorDamage SMALLINT,
    hpDamageTaken SMALLINT,
    hpDamage SMALLINT,
    isFriendlyFire BOOLEAN,
    attackerStrafe BOOLEAN
);