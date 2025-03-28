CREATE TABLE IF NOT EXISTS WeaponSkin (
    -- Primary Key --
    weaponSkinID INT,

    -- Attributes --
    condition VARCHAR,
    StatTrak BOOLEAN,

    -- foreign keys --
    CosmeticID Int,
    game_weaponID INT
);