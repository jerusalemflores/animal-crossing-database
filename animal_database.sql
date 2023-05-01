CREATE TABLE villager (
    villagerID INT PRIMARY KEY, 
    name VARCHAR(50), 
    species VARCHAR(50), 
    strengths VARCHAR(255), 
    weaknesses VARCHAR(255), 
    specialMoves VARCHAR(255), 
    category VARCHAR(50), 
    record VARCHAR(50), 
    boxingGear VARCHAR(50)
    );
CREATE TABLE matches ( 
    matchID INT PRIMARY KEY, 
    location VARCHAR(50), 
    winner VARCHAR(50), 
    loser VARCHAR(50),  
    prize VARCHAR(50) 
    );
CREATE TABLE category3 ( 
    categoryID INT PRIMARY KEY, 
    category VARCHAR(50), 
    minimumWeight DECIMAL(10, 2),
    maximumWeight DECIMAL(10,2), 
    rules VARCHAR(255)
    );
CREATE TABLE boxingGear ( 
    gearID INT PRIMARY KEY, 
    name VARCHAR(50), 
    description VARCHAR(255) 
    );
CREATE TABLE villagerScores3( 
    villagerID INT PRIMARY KEY,
    name VARCHAR(50), 
    strength1Score INT, 
    strength2Score INT, 
    strength3Score INT, 
    strength4Score INT, 
    weakness1Score INT, 
    weakness2Score INT, 
    weakness3Score INT, 
    weakness4Score INT, 
    totalScore INT, 
    FOREIGN KEY (villagerID) REFERENCES villager(villagerID) 
    );
