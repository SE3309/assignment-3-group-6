USE BRATmusic;
-- Create Advertiser Table
CREATE TABLE Advertiser (
    company VARCHAR(255) PRIMARY KEY -- Primary key for the advertiser's name (up to 255 characters)
);

-- Create Advertisement Table
CREATE TABLE Advertisement (
    AdId INT AUTO_INCREMENT PRIMARY KEY, -- Auto-incrementing unique identifier for advertisements
    costOfAd DECIMAL(10, 2) NOT NULL, -- Cost of the advertisement (monetary value with 2 decimal places)
    company VARCHAR(255), -- Foreign key linking to the Advertiser table
    adFile LONGBLOB, -- Stores the advertisement file (e.g., MP3 file)
    FOREIGN KEY (company) REFERENCES Advertiser(company) -- Ensures referential integrity with Advertiser
        ON DELETE CASCADE -- Deletes advertisements if the associated advertiser is deleted
        ON UPDATE CASCADE -- Updates advertisements if the associated advertiser is updated
);

CREATE TABLE Artist (
    artistName VARCHAR(500) PRIMARY KEY,
    totalDurationListenedTo INT NOT NULL,
    revenueGenerated DECIMAL(10, 2) NOT NULL,
    email VARCHAR(500) NOT NULL UNIQUE,
    password VARCHAR(500) NOT NULL
);

CREATE TABLE Album (
    albumID INT AUTO_INCREMENT PRIMARY KEY,
    dateCreated DATE NOT NULL,
    artistName VARCHAR(255) NOT NULL,
    FOREIGN KEY (artistName) REFERENCES Artist(artistName)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE EventCalendar (
    eventID INT AUTO_INCREMENT PRIMARY KEY,
    eventDate DATE NOT NULL,
    eventTime TIME NOT NULL,
    location VARCHAR(255) NOT NULL,
    artistName VARCHAR(255) NOT NULL,
    revenueGenerated DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (artistName) REFERENCES Artist(artistName)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


SET GLOBAL max_allowed_packet = 256 * 1024 * 1024;  -- 64MB
SHOW VARIABLES LIKE 'max_allowed_packet';

SET GLOBAL net_read_timeout = 60;
SET GLOBAL net_write_timeout = 60;

CREATE TABLE Media (
    mediaID INT PRIMARY KEY AUTO_INCREMENT, 
    mediaName VARCHAR(200), 
    mediaFile LONGBLOB,
    totalDurationListenedTo INT, 
    mediaRanking INT, 
    dateCreated DATE, 
    lengthOfMedia INT, 
    albumID VARCHAR(20), 
    artistName VARCHAR(50)
    /* Foreign keys will be added later when the referenced tables are created
    FOREIGN KEY (albumID) REFERENCES Album (albumID), 
    FOREIGN KEY (artistName) REFERENCES Artist (artistName) */
);

CREATE TABLE ListeningStats (
    userID VARCHAR(10),
    mediaID INT,  -- Match the data type of mediaID in Media table
    duration INT,
    PRIMARY KEY (userID, mediaID),
    FOREIGN KEY (mediaID) REFERENCES Media(mediaID)  -- References Media table
);
