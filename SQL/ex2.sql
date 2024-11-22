CREATE TABLE SubscriptionTiers (
   TierName VARCHAR(255) NOT NULL,
   Price DECIMAL(10, 2),
   Duration INT, -- Duration in months
   PRIMARY KEY (TierName)
);


-- Insert data into SubscriptionTiers
INSERT INTO SubscriptionTiers (TierName, Price, Duration)
VALUES
   ('Premium', 19.99, 12), -- Premium subscription: $19.99/year
   ('Free', 0.00, NULL);   -- Free subscription: No cost, no duration


-- Create the UserPlaylistLibrary table
CREATE TABLE UserPlaylistLibrary (
   LibraryID INT NOT NULL AUTO_INCREMENT,
   PlaylistID INT,
   PRIMARY KEY (LibraryID)
);


-- Create the Users table (base table)
CREATE TABLE User (
   UserID VARCHAR(255) NOT NULL,
   DisplayName VARCHAR(255),
   StartDateOfSubscription DATE,
   Password VARCHAR(255),
   SubscriptionType VARCHAR(255),
   PlaylistLibraryID INT,
   PRIMARY KEY (UserID)
);


-- Create the Playlist table
CREATE TABLE Playlist (
   PlaylistID INT NOT NULL,
   MediaID INT NOT NULL,
   DateAdded DATE,
   Description TEXT,
   Creator VARCHAR(255),
   PRIMARY KEY (PlaylistID, MediaID),
   UNIQUE (PlaylistID) -- Add a UNIQUE constraint for PlaylistID
);


-- Add foreign keys for User
ALTER TABLE User
ADD CONSTRAINT FK_SubscriptionType FOREIGN KEY (SubscriptionType) REFERENCES SubscriptionTiers(TierName),
ADD CONSTRAINT FK_PlaylistLibraryID FOREIGN KEY (PlaylistLibraryID) REFERENCES UserPlaylistLibrary(LibraryID);


-- Add foreign keys for Playlist
ALTER TABLE Playlist
ADD CONSTRAINT FK_Creator FOREIGN KEY (Creator) REFERENCES User(UserID);


ALTER TABLE UserPlaylistLibrary
ADD CONSTRAINT FK_PlaylistID FOREIGN KEY (PlaylistID) REFERENCES Playlist(PlaylistID);


-- Add table for Premium Users
CREATE TABLE PremiumUser (
   UserID VARCHAR(255) NOT NULL,
   PremiumFeature VARCHAR(255), -- Example premium feature
   PRIMARY KEY (UserID),
   FOREIGN KEY (UserID) REFERENCES User(UserID)
);


-- Add table for Free Users
CREATE TABLE FreeUser (
   UserID VARCHAR(255) NOT NULL,
   AdPreference VARCHAR(255), -- Example field for free users
   PRIMARY KEY (UserID),
   FOREIGN KEY (UserID) REFERENCES User(UserID)
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
mediaID INT(20) PRIMARY KEY AUTO_INCREMENT, 
mediaName VARCHAR(200), 
mediaFile longblob,
totalDurationListenedTo INT, 
mediaRanking INT, 
dateCreated DATE, 
lengthOfMedia INT, 
albumID VARCHAR(20), 
artistName VARCHAR(50)
/*no foreign keys yet until al tgthr
FOREIGN KEY (albumID) REFERENCES Album (albumID), 
FOREIGN KEY (artistName) REFERENCES Artist (artistName)*/
);

CREATE TABLE ListeningStats (
userID VARCHAR(10),
mediaID VARCHAR(20),
duration INT,
PRIMARY KEY (userID, mediaID)
);

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