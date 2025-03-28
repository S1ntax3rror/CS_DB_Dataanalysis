ALTER TABLE AnnouncementFinalRound
ADD CONSTRAINT pk_announcementfinalround PRIMARY KEY (tick, gameID);

ALTER TABLE AnnouncementLastRoundHalf
ADD CONSTRAINT pk_announcementlastroundhalf PRIMARY KEY (tick, gameID);

ALTER TABLE AnnouncementMatchStarted
ADD CONSTRAINT pk_announcementmatchstarted PRIMARY KEY (tick, gameID);

ALTER TABLE BombEvent
ADD CONSTRAINT pk_bombevent PRIMARY KEY (bombEventID);

ALTER TABLE Damage
ADD CONSTRAINT pk_damage PRIMARY KEY (damageID);

ALTER TABLE Fire
ADD CONSTRAINT pk_fire PRIMARY KEY (uniqueID, frameID);

ALTER TABLE Flash
ADD CONSTRAINT pk_flash PRIMARY KEY (flashID);

ALTER TABLE Frame
ADD CONSTRAINT pk_frame PRIMARY KEY (frameID);

ALTER TABLE Game
ADD CONSTRAINT pk_game PRIMARY KEY (gameID);

ALTER TABLE GameHalfEnded
ADD CONSTRAINT pk_gamehalfended PRIMARY KEY (tick, gameID);

ALTER TABLE GameRounds
ADD CONSTRAINT pk_gamerounds PRIMARY KEY (gameRoundID);

ALTER TABLE Grenade
ADD CONSTRAINT pk_grenade PRIMARY KEY (grenadeID);

ALTER TABLE Inventory
ADD CONSTRAINT pk_inventory PRIMARY KEY (playerFrameID, weaponID);

ALTER TABLE Kill
ADD CONSTRAINT pk_kill PRIMARY KEY (killID);

ALTER TABLE MatchmakingRanks
ADD CONSTRAINT pk_matchmakingranks PRIMARY KEY (matchMakingRanksID);

ALTER TABLE MatchStart
ADD CONSTRAINT pk_matchstart PRIMARY KEY (tick, gameID);

ALTER TABLE MatchStartedChanged
ADD CONSTRAINT pk_matchstartedchanged PRIMARY KEY (tick, gameID);

ALTER TABLE Player
ADD CONSTRAINT pk_player PRIMARY KEY (playerID);

ALTER TABLE PlayerFrame
ADD CONSTRAINT pk_playerframe PRIMARY KEY (playerFrameID);

ALTER TABLE Projectile
ADD CONSTRAINT pk_projectile PRIMARY KEY (projectileID);

ALTER TABLE PlayerGameSide
ADD CONSTRAINT pk_playergameside PRIMARY KEY (playerGameSideID);

ALTER TABLE ServerVar
ADD CONSTRAINT pk_servervar PRIMARY KEY (serverVarID);

ALTER TABLE Smoke
ADD CONSTRAINT pk_smoke PRIMARY KEY (grenadeEntityID, frameid);

ALTER TABLE Spotter
ADD CONSTRAINT pk_spotter PRIMARY KEY (spotterID);

ALTER TABLE Team
ADD CONSTRAINT pk_team PRIMARY KEY (teamID);

ALTER TABLE TeamGameSide
ADD CONSTRAINT pk_teamgameside PRIMARY KEY (teamGameSideID);

ALTER TABLE TeamSwitch
ADD CONSTRAINT pk_teamswitch PRIMARY KEY (tick, gameID);

ALTER TABLE Tournament
ADD CONSTRAINT pk_tournament PRIMARY KEY (tournamentID);

ALTER TABLE WarmupChanged
ADD CONSTRAINT pk_warmupchanged PRIMARY KEY (tick, gameID);

ALTER TABLE Weapon
ADD CONSTRAINT pk_weapon PRIMARY KEY (weaponID);

ALTER TABLE WeaponFire
ADD CONSTRAINT pk_weaponfire PRIMARY KEY (weaponFireID);