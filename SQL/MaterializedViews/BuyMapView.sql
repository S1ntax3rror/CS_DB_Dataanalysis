CREATE MATERIALIZED VIEW BuyMapView AS
SELECT mapname, tbuytype, ctbuytype, winningside
FROM gamerounds gr
JOIN game g on gr.gameid = g.gameid;