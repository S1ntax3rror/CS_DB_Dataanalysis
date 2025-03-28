CREATE TABLE IF NOT EXISTS Price (
    -- Primary Key --
    priceID INT,

    -- Attributes --
    amountSold INT,
    date INT,
    price REAL,

    -- Foreign Key --
    CosmeticID INT
);