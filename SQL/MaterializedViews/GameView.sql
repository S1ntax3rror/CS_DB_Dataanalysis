CREATE MATERIALIZED VIEW IF NOT EXISTS GameView AS
    SELECT
        G.gameid,
        G.matchname,
        G.matchdate,
        G.hltvurl,
        G.mapname,
        GR.gameroundid,
        GR.starttick,
        GR.endtick,
        GR.tBuyType,
        GR.ctBuyType,
        GR.winningSide,
        GR.roundEndReason,
        GR.roundNum,
        GR.tScore,
        GR.ctScore,
        TOUR.tournamentname,
        T_team.teamname AS T_team,
        CT_team.teamname AS CT_team
    FROM
        game G
    JOIN
        tournament TOUR ON G.tournamentid = TOUR.tournamentid
    JOIN
        gamerounds GR ON G.gameid = GR.gameid
    JOIN
        teamgameside TGS_T ON GR.gameroundid = TGS_T.gameroundid AND TGS_T.side = 'T'
    JOIN
        team T_team ON TGS_T.teamid = T_team.teamid
    JOIN
        teamgameside TGS_CT ON GR.gameroundid = TGS_CT.gameroundid AND TGS_CT.side = 'CT'
    JOIN
        team CT_team ON TGS_CT.teamid = CT_team.teamid;