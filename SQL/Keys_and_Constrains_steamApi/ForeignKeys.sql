ALTER TABLE PlayerSticker
ADD CONSTRAINT fk_tournament FOREIGN KEY (tournamentID) REFERENCES Tournament(tournamentID);

ALTER TABLE PlayerSticker
ADD CONSTRAINT fk_player FOREIGN KEY (playerID) REFERENCES Player(playerID);

ALTER TABLE PlayerSticker
ADD CONSTRAINT fk_Cosmetic FOREIGN KEY (CosmeticID) REFERENCES Cosmetic(CosmeticID);

ALTER TABLE TeamSticker
ADD CONSTRAINT fk_tournament FOREIGN KEY (tournamentID) REFERENCES Tournament(tournamentID);

ALTER TABLE TeamSticker
ADD CONSTRAINT fk_team FOREIGN KEY (teamID) REFERENCES Team(teamID);

ALTER TABLE TeamSticker
ADD CONSTRAINT fk_Cosmetic FOREIGN KEY (CosmeticID) REFERENCES Cosmetic(CosmeticID);

ALTER TABLE Price
ADD CONSTRAINT fk_Cosmetic FOREIGN KEY (CosmeticID) REFERENCES Cosmetic(CosmeticID);

ALTER TABLE WeaponSkin
ADD CONSTRAINT fk_weapon FOREIGN KEY (game_weaponID) REFERENCES Weapon(weaponID);

ALTER TABLE WeaponSkin
ADD CONSTRAINT fk_Cosmetic FOREIGN KEY (CosmeticID) REFERENCES Cosmetic(CosmeticID);