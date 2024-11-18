SELECT * FROM BRATmusic.ListeningStats;

SELECT userID, mediaID FROM BRATmusic.ListeningStats;

SELECT * FROM BRATmusic.ListeningStats WHERE duration > 100;

SELECT COUNT(*) AS total_entries FROM BRATmusic.ListeningStats;

SELECT DISTINCT userID FROM BRATmusic.ListeningStats;

SELECT MAX(duration) AS max_duration FROM BRATmusic.ListeningStats;

SELECT userID, SUM(duration) AS total_duration
FROM BRATmusic.ListeningStats
GROUP BY userID;

SELECT * FROM BRATmusic.ListeningStats WHERE userID LIKE '%example.com%';
