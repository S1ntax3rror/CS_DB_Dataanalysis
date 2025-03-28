CREATE MATERIALIZED VIEW GamePlayerViewWithPlant AS
SELECT
    GPV.gameid,
    GR.gameroundid,
    GPV.mapname,
    GPV.matchdate,
    GPV.tbuytype,
    GPV.ctbuytype,
    GPV.roundendreason,
    GPV.winningside,
    GPV.frameid,
    GPV.tick,
    GPV.clocktime,
    GPV.seconds,
    GPV.bombx,
    GPV.bomby,
    GPV.bombz,
    GPV.playerframeid,
    GPV.PlayerX,
    GPV.PlayerY,
    GPV.PlayerZ,
    GPV.PlayerViewX,
    GPV.PlayerViewY,
    GPV.armor,
    GPV.hp,
    GPV.isalive,
    GPV.name,
    GPV.side,
    GPV.WeaponMain,
    GPV.WeaponSide,
    GPV.ActiveWeapon,
    CASE
        WHEN F.tick > GR.bombplanttick THEN 1
        ELSE 0
    END AS bombIsPlanted
FROM gameplayerframeview GPV
JOIN frame F ON F.frameid = GPV.frameid
JOIN gamerounds GR ON F.gameroundid = GR.gameroundid;