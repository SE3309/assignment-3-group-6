USE BRATmusic;

-- 1. Create the SubscriptionTiers table (referenced by the User table)
CREATE TABLE SubscriptionTiers (
    TierName VARCHAR(255) NOT NULL,
    Price DECIMAL(10, 2),
    Duration INT, -- Duration in months
    PRIMARY KEY (TierName)
);

-- 2. Create the UserPlaylistLibrary table (referenced by the User table)
CREATE TABLE UserPlaylistLibrary (
   LibraryID INT NOT NULL,
   PlaylistID INT UNIQUE NOT NULL,
   PRIMARY KEY (PlaylistID)
);

-- 3. Create the User table (references SubscriptionTiers and UserPlaylistLibrary)
CREATE TABLE User (
    email VARCHAR(255) PRIMARY KEY, -- email is the primary key and serves as the user ID
    display_name VARCHAR(255) NOT NULL,
    start_date_of_subscription DATE NOT NULL,
    password VARCHAR(255) NOT NULL,
    subscription_type_id VARCHAR(255), -- Foreign key referencing SubscriptionTiers (matches TierName data type)
    playlist_library_id INT, -- Foreign key referencing UserPlaylistLibrary

    -- Adding foreign key constraints
    CONSTRAINT fk_subscription_type FOREIGN KEY (subscription_type_id) REFERENCES SubscriptionTiers(TierName),
    CONSTRAINT fk_playlist_library FOREIGN KEY (playlist_library_id) REFERENCES UserPlaylistLibrary(LibraryID)
);

-- 4. Create the Playlist table
CREATE TABLE Playlist (
   PlaylistID INT NOT NULL,
   MediaID INT NOT NULL,
   DateAdded DATE,
   Description TEXT,
   Creator VARCHAR(255),
   PRIMARY KEY (PlaylistID, MediaID),
   UNIQUE (PlaylistID) -- Add a UNIQUE constraint for PlaylistID
);

-- 5. Create the PremiumUser table (references the User table)
CREATE TABLE PremiumUser (
   UserID VARCHAR(255) NOT NULL,
   PremiumFeature VARCHAR(255), -- Example premium feature
   PRIMARY KEY (UserID),
   FOREIGN KEY (UserID) REFERENCES User(email) -- Corrected to reference User.email (primary key in User table)
);

-- 6. Create the FreeUser table (references the User table)
CREATE TABLE FreeUser (
   UserID VARCHAR(255) NOT NULL,
   AdPreference VARCHAR(255), -- Example field for free users
   PRIMARY KEY (UserID),
   FOREIGN KEY (UserID) REFERENCES User(email) -- Corrected to reference User.email (primary key in User table)
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

CREATE TABLE Artist (
    artistName VARCHAR(500) PRIMARY KEY,
    totalDurationListenedTo INT NOT NULL,
    revenueGenerated DECIMAL(10, 2) NOT NULL,
    email VARCHAR(500) NOT NULL UNIQUE,
    password VARCHAR(500) NOT NULL
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

