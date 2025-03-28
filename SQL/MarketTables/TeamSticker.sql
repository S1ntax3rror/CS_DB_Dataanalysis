CREATE TABLE IF NOT EXISTS TeamSticker (
    -- Primary Key --
    teamStickerID INT,

    -- Attributes --
    condition VARCHAR,

    -- foreign keys --
    tournamentID INT,
    teamID Int,
    CosmeticID Int
);