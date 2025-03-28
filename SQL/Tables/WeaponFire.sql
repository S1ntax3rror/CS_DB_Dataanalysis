CREATE TABLE IF NOT EXISTS WeaponFire(
    -- Primary Key --
    weaponFireID INT,

    -- Foreign Keys --
    playerFrameID INT,
    weaponID INT,
    frameID INT,

    -- Attributes --
    playerStrafe BOOLEAN
);