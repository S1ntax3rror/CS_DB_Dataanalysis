ALTER TABLE PlayerSticker
DROP CONSTRAINT fk_tournament;

ALTER TABLE PlayerSticker
DROP CONSTRAINT fk_player;

ALTER TABLE PlayerSticker
DROP CONSTRAINT fk_Cosmetic;

ALTER TABLE TeamSticker
DROP CONSTRAINT fk_tournament;

ALTER TABLE TeamSticker
DROP CONSTRAINT fk_team;

ALTER TABLE TeamSticker
DROP CONSTRAINT fk_Cosmetic;

ALTER TABLE Price
DROP CONSTRAINT fk_Cosmetic;

ALTER TABLE WeaponSkin
DROP CONSTRAINT fk_weapon;

ALTER TABLE WeaponSkin
DROP CONSTRAINT fk_Cosmetic;


ALTER TABLE Cosmetic
DROP CONSTRAINT pk_Cosmetic;

ALTER TABLE PlayerSticker
DROP CONSTRAINT pk_playerSticker;

ALTER TABLE Price
DROP CONSTRAINT pk_price;

ALTER TABLE TeamSticker
DROP CONSTRAINT pk_teamSticker;

ALTER TABLE WeaponSkin
DROP CONSTRAINT pk_weaponSkin;