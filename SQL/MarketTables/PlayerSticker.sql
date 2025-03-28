CREATE TABLE IF NOT EXISTS PlayerSticker (
    -- Primary Key --
    playerStickerID INT,

    -- Attributes --
    condition VARCHAR,

    -- foreign keys --
    tournamentID INT,
    playerID Int,
    CosmeticID Int
);