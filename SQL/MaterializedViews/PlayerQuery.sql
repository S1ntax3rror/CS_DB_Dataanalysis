CREATE MATERIALIZED VIEW player_query AS
    SELECT GRS.gameroundid, F.frameid, PGS.playergamesideid, P.playerid, PF.playerframeid FROM gamerounds GRS
                        JOIN frame F ON GRS.gameroundid = F.gameroundid
                        JOIN playerframe PF ON F.frameid = PF.frameid
                        JOIN playergameside PGS ON PF.playergamesideid = PGS.playergamesideid
                        JOIN player P ON PGS.playerid = P.playerid