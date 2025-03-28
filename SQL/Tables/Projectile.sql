CREATE TABLE IF NOT EXISTS Projectile(
    -- Primary Key --
    projectileID BIGINT,

    -- Attributes --
    x REAL,
    y REAL,
    z REAL,
    projectileType VARCHAR,

    -- Foreign Keys --
    frameID INT
);