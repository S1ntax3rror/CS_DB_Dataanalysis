CREATE TABLE IF NOT EXISTS Inventory (
    -- Primary Keys && Foreign Keys --
    playerFrameID INT,
    weaponID INT,

    -- Attributes --
    ammoInReserve SMALLINT,
    ammoInMagazine SMALLINT
);