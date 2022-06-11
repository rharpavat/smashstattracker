CREATE TABLE IF NOT EXISTS MatchDataTest (
   MatchID int NOT NULL,
   PlayerID varchar(20) NOT NULL,
   PlayedCharacter varchar(20),
   PlayerRank int,
   Kills int,
   Deaths int,
   SelfDestructs int,
   DamageGiven int,
   DamageTaken int,
   StageName varchar(50),
   MatchDate DATE   
);

SELECT 
   table_name, 
   column_name, 
   data_type 
FROM 
   information_schema.columns
WHERE 
   table_name = 'matchdata';