use lahman2017raw;
ALTER TABLE appearances ADD PRIMARY KEY (`yearID`,`teamID`,`playerID`);
ALTER TABLE appearances ADD CONSTRAINT `apptopeople` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`);
ALTER TABLE appearances ADD CONSTRAINT `apptoteam` FOREIGN KEY (`yearID`,`teamID`) REFERENCES `Teams` (`yearID`,`teamID`)

ALTER TABLE batting ADD PRIMARY KEY (`playerID`,`yearID`,`stint`,`teamID`);
ALTER TABLE batting ADD CONSTRAINT `battingtopeople` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`);
ALTER TABLE batting ADD CONSTRAINT `battingtoteam` FOREIGN KEY (`yearID`,`teamID`) REFERENCES `Teams` (`yearID`,`teamID`);

ALTER TABLE fielding ADD PRIMARY KEY (`playerID`,`yearID`,`stint`,`teamID`,`POS`,`InnOuts`,`PO`,`E`);
ALTER TABLE fielding ADD CONSTRAINT `fieldingtopeople` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`);
ALTER TABLE fielding ADD CONSTRAINT `fieldingtoteam` FOREIGN KEY (`yearID`,`teamID`) REFERENCES `Teams` (`yearID`,`teamID`);

ALTER TABLE Managers ADD PRIMARY KEY (`playerID`,`yearID`,`teamID`,`inseason`);
ALTER TABLE Managers ADD CONSTRAINT `managertopeople` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`);
ALTER TABLE Managers ADD CONSTRAINT `managertoteam` FOREIGN KEY (`yearID`,`teamID`) REFERENCES `Teams` (`yearID`,`teamID`);

ALTER TABLE people ADD PRIMARY KEY (`playerID`);

ALTER TABLE teams ADD PRIMARY KEY (`yearID`,`teamID`);

