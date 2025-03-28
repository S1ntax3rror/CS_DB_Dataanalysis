ALTER TABLE PlayerFrame
ALTER COLUMN playergamesideid SET NOT NULL;

ALTER TABLE PlayerFrame
ALTER COLUMN frameid SET NOT NULL;

ALTER TABLE PlayerFrame
ADD CONSTRAINT frame_player_unique UNIQUE (frameid, playergamesideid);