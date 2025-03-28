ALTER TABLE AnnouncementFinalRound
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE AnnouncementLastRoundHalf
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE AnnouncementMatchStarted
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE BombEvent
ADD CONSTRAINT fk_playerframe FOREIGN KEY (playerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE BombEvent
ADD CONSTRAINT fk_frame FOREIGN KEY (frameID) REFERENCES Frame(frameID);

ALTER TABLE Damage
ADD CONSTRAINT fk_attackerplayerframe FOREIGN KEY (attackerPlayerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Damage
ADD CONSTRAINT fk_victimplayerframe FOREIGN KEY (victimPlayerFrameID) REFERENCES PlayerFrame(playerframeid);

ALTER TABLE Damage
ADD CONSTRAINT fk_weapon FOREIGN KEY (weaponID) REFERENCES Weapon(weaponID);

ALTER TABLE Damage
ADD CONSTRAINT fk_frame FOREIGN KEY (frameID) REFERENCES Frame(frameID);

ALTER TABLE Fire
ADD CONSTRAINT fk_frame FOREIGN KEY (frameID) REFERENCES Frame(frameID);

ALTER TABLE Flash
ADD CONSTRAINT fk_attackerplayerframe FOREIGN KEY (attackerPlayerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Flash
ADD CONSTRAINT fk_playerframe FOREIGN KEY (playerframeid) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Flash
ADD CONSTRAINT fk_frame FOREIGN KEY (frameID) REFERENCES Frame(frameID);

ALTER TABLE Frame
ADD CONSTRAINT fk_gameround FOREIGN KEY (gameRoundID) REFERENCES GameRounds(gameRoundID);

ALTER TABLE Game
ADD CONSTRAINT fk_servervar FOREIGN KEY (serverVarID) REFERENCES ServerVar(serverVarID);

ALTER TABLE Game
ADD CONSTRAINT fk_tournament FOREIGN KEY (tournamentID) REFERENCES Tournament(tournamentID);

ALTER TABLE GameHalfEnded
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE GameRounds
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE Grenade
ADD CONSTRAINT fk_throwframe FOREIGN KEY (throwFrameID) REFERENCES Frame(frameID);

ALTER TABLE Grenade
ADD CONSTRAINT fk_destroyframe FOREIGN KEY (destroyFrameID) REFERENCES Frame(frameID);

ALTER TABLE Grenade
ADD CONSTRAINT fk_playerframe FOREIGN KEY (throwerPlayerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Inventory
ADD CONSTRAINT fk_playerframe FOREIGN KEY (playerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Inventory
ADD CONSTRAINT fk_weapon FOREIGN KEY (weaponID) REFERENCES Weapon(weaponID);

ALTER TABLE Kill
ADD CONSTRAINT fk_attackerplayerframe FOREIGN KEY (attackerPlayerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Kill
ADD CONSTRAINT fk_victimplayerframe FOREIGN KEY (victimPlayerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Kill
ADD CONSTRAINT fk_assisterplayerframe FOREIGN KEY (assisterPlayerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Kill
ADD CONSTRAINT fk_tradedplayerframe FOREIGN KEY (tradedPlayerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Kill
ADD CONSTRAINT fk_flashthrowerplayerframe FOREIGN KEY (flashThrowerPlayerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE Kill
ADD CONSTRAINT fk_weapon FOREIGN KEY (weaponID) REFERENCES Weapon(weaponID);

ALTER TABLE Kill
ADD CONSTRAINT fk_frame FOREIGN KEY (frameID) REFERENCES Frame(frameID);

ALTER TABLE MatchmakingRanks
ADD CONSTRAINT fk_playerID FOREIGN KEY (playerID) REFERENCES Player(playerID);

ALTER TABLE MatchmakingRanks
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE MatchStart
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE MatchStartedChanged
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE PlayerFrame
ADD CONSTRAINT fk_playergameside FOREIGN KEY (playerGameSideID) REFERENCES PlayerGameSide(playerGameSideID);

ALTER TABLE PlayerFrame
ADD CONSTRAINT fk_frame FOREIGN KEY (frameID) REFERENCES Frame(frameID);

ALTER TABLE PlayerFrame
ADD CONSTRAINT fk_activeweapon FOREIGN KEY (activeWeaponID) REFERENCES Weapon(weaponID);

ALTER TABLE Projectile
ADD CONSTRAINT fk_frame FOREIGN KEY (frameID) REFERENCES Frame(frameID);

ALTER TABLE PlayerGameSide
ADD CONSTRAINT fk_player FOREIGN KEY (playerID) REFERENCES Player(playerID);

ALTER TABLE PlayerGameSide
ADD CONSTRAINT fk_teamGameSide FOREIGN KEY (teamGameSideID) REFERENCES TeamGameSide(teamGameSideID);

ALTER TABLE Smoke
ADD CONSTRAINT fk_frame FOREIGN KEY (frameID) REFERENCES Frame(frameID);

ALTER TABLE Spotter
ADD CONSTRAINT fk_player FOREIGN KEY (playerID) REFERENCES Player(playerID);

ALTER TABLE Spotter
ADD CONSTRAINT fk_playerframe FOREIGN KEY (playerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE TeamGameSide
ADD CONSTRAINT fk_team FOREIGN KEY (teamID) REFERENCES Team(teamID);

ALTER TABLE TeamGameSide
ADD CONSTRAINT fk_gameround FOREIGN KEY (gameRoundID) REFERENCES GameRounds(gameRoundID);

ALTER TABLE TeamSwitch
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE WarmupChanged
ADD CONSTRAINT fk_game FOREIGN KEY (gameID) REFERENCES Game(gameID);

ALTER TABLE WeaponFire
ADD CONSTRAINT fk_playerframe FOREIGN KEY (playerFrameID) REFERENCES PlayerFrame(playerFrameID);

ALTER TABLE WeaponFire
ADD CONSTRAINT fk_weapon FOREIGN KEY (weaponID) REFERENCES Weapon(weaponID);

ALTER TABLE WeaponFire
ADD CONSTRAINT fk_frame FOREIGN KEY (frameID) REFERENCES Frame(frameID);