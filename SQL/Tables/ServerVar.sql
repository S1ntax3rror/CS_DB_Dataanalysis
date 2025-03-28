CREATE TABLE IF NOT EXISTS ServerVar(
    serverVarID SERIAL,
    cashBombPlanted INT,
    cashBombDefused INT,
    bombTimer INT,
    buyTime INT,
    freezeTime INT,
    roundRestartDelay INT,
    roundTimeDefuse INT,
    roundTime INT,
    cashTeamLoserBonusConsecutive INT,
    maxRounds INT,
    timeoutsAllowed INT,
    cashTeamTWinBomb INT,
    coachingAllowed INT,
    cashWinElimination INT,
    cashWinTimeRunOut INT,
    cashWinDefuse INT,
    cashPlayerKilledDefault INT,
    cashTeamLoserBonus INT,

    CONSTRAINT RowUniqueness UNIQUE (
        cashBombPlanted, cashBombDefused, bombTimer, buyTime, freezeTime, roundRestartDelay,
        roundTimeDefuse, roundTime, cashTeamLoserBonusConsecutive, maxRounds, timeoutsAllowed,
        cashTeamTWinBomb, coachingAllowed, cashWinElimination, cashWinTimeRunOut, cashWinDefuse,
        cashPlayerKilledDefault, cashTeamLoserBonus
    )
);