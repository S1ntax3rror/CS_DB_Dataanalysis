CREATE INDEX game_index ON game (gameid);

CREATE INDEX gamerounds_index ON gamerounds (gameid, gameroundid);

CREATE INDEX frame_index ON frame (frameid);

CREATE INDEX playerframe_index ON playerframe (playerframeid);

CREATE INDEX inventory_index ON inventory (playerframeid);

CREATE INDEX weapon_index ON weapon (weaponid);