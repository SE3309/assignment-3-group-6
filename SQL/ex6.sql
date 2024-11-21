UPDATE BRATmusic.ListeningStats
SET duration = 300
WHERE
userID = 'blairbilly@example.com' AND mediaID = '40';
UPDATE BRATmusic.ListeningStats
SET duration = duration + 50
WHERE duration IS NOT NULL;
UPDATE BRATmusic. ListeningStats
SET
duration = NULL
WHERE
mediaID = '40' ;