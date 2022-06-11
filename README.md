# smashstattracker

### Requirements
1. As a user, I want to store the stat results of my Smash matches.
2. As a user, I want to obtain long-running metrics over the stored data.
3. As a user, I want a friendly way to view statistics from matches over time.

### Architecture
#### Database
- SQL DB to store match data, allowing complex joins/queries.
- Cannot use NoSQL db here as document store is not optimized for this data structure

1 table per player
    - Automatically created?
    - Named after player
Match ID primary key
    - Links match records across tables
    - Is this necessary?

**MatchData**: 
    MatchID (int, required)
    PlayerID (string, required)
    Character (string, optional)
    Rank (int, optional)
    Kills (int, optional)
    Deaths (int, optional)
    SelfDestructs (int, optional)
    DamageGiven (number, optional)
    DamageTaken (number, optional)
    StageName (string, optional)
    Date (mm/dd/yyyy)

**KillData**: MOVE THIS TO MONGODB
    MatchID (int, required)
    Killer (string, required) -> PlayerID
    Killee (string, required) -> PlayerID OR "AT"
    KillCount (int, required)

**PlayerStatsOverTime**:
    PlayerID (string, pkey)
    Date (mm/dd/yyyy)
    TotalKills (int)
    AvgKills (double)
    TotalDeaths (int)
    AvgDeaths (double)
    TotalSDs (int)
    AvgSDs (double)
    TotalWins (int)
    KDRatio (double)
    AvgRank (double)

#### Lambda Processor: DataUploader
- Executes every day (?)
- Checks if source Google Sheet has changed
- If not changed, skip run
- Else,
    > Parse + insert new data from Sheets into DB
    > Do we want to support past data checking/updating?
        -> not for mvp probably

#### Lambda Processor: DataAnalyzer
- Executes every day (?)
- Run analytics queries on data, save to DB

#### Web Interface
- Updates every day (?)
- Pulls data from DB and visualizes it
    > Do we need caching of some sort? 
    > If data is only being updated once a day, no need to query the DB for every request. Query once and cache.
