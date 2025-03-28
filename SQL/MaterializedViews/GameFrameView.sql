CREATE MATERIALIZED VIEW MainWeapon AS
    SELECT
        PF.playerframeid,
        WMain.weaponname AS WeaponMain
    FROM
        playerframe PF  -- Ensure the correct base table is used
    JOIN
        inventory IMain ON PF.playerframeid = IMain.playerframeid
    JOIN
        weapon WMain ON IMain.weaponid = WMain.weaponid
    WHERE
        WMain.weaponclass NOT IN ('Pistols', 'Grenade', 'Melee', 'Equipment', '');

CREATE MATERIALIZED VIEW SideWeapon AS
    SELECT
        PF.playerframeid,
        WSide.weaponname AS WeaponSide
    FROM
        playerframe PF  -- Ensure the correct base table is used
    JOIN
        inventory ISide ON PF.playerframeid = ISide.playerframeid
    JOIN
        weapon WSide ON ISide.weaponid = WSide.weaponid
    WHERE
        WSide.weaponclass = 'Pistols';

CREATE MATERIALIZED VIEW GamePlayerFrameView AS
    SELECT
        GV.gameid,
        GV.mapname,
        GV.matchdate,
        GV.tbuytype,
        GV.ctbuytype,
        GV.roundendreason,
        GV.winningside,
        F.frameid,
        F.tick,
        F.clocktime,
        F.seconds,
        F.bombx AS BombX,
        F.bomby AS BombY,
        F.bombz AS BombZ,
        PF.playerframeid,
        PF.x AS PlayerX,
        PF.y AS PlayerY,
        PF.z AS PlayerZ,
        PF.viewx AS PlayerViewX,
        PF.viewy AS PlayerViewY,
        P.name,
        MainWeapon.WeaponMain,
        SideWeapon.WeaponSide,
        PF.armor,
        PF.hp,
        PF.isalive,
        ActiveWeapon.weaponname AS ActiveWeapon,
        TGS.side
    FROM
        GameView GV
    JOIN
        frame F ON GV.gameroundid = F.gameroundid
    JOIN
        playerframe PF ON F.frameid = PF.frameid
    JOIN
        playergameside PGS ON PF.playergamesideid = PGS.playergamesideid
    JOIN
        teamgameside TGS ON PGS.teamgamesideid = TGS.teamgamesideid
    JOIN
        player P ON PGS.playerid = P.playerid
    LEFT JOIN
        MainWeapon ON PF.playerframeid = MainWeapon.playerframeid
    LEFT JOIN
        SideWeapon ON PF.playerframeid = SideWeapon.playerframeid
    LEFT JOIN
        weapon ActiveWeapon ON PF.activeweaponid = ActiveWeapon.weaponid;
