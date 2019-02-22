use lahman2017;



alter table people modify column playerID varchar(32);


select nameLast,nameFirst,playerID,
(select category from halloffame where halloffame.playerID = people.playerID) as category
from people where 
not exists(select * from managers where managers.playerID = people.playerID) and
not exists(select * from appearances where appearances.playerID = people.playerID)
limit 10;


SELECT 
batting.playerID, 
sum(h)/sum(ab) as career_average, 
sum(h) as total_hits, 
sum(ab) as total_at_bats, 
sum(HR) as home_runs 
from batting group by playerID ;

select 
playerID, nameLast, nameFirst, total_hits, total_abs, career_average, total_hrs, total_wins
from 
(select * from 
(select playerID as batting_player, 
sum(h)/sum(ab) as career_average, 
sum(h) as total_hits, 
sum(ab) as total_abs, 
sum(HR) as total_hrs
from batting
group by playerID
having career_average > 0.34 and total_hrs > 500) as a
right join people
on a.batting_player = people.playerID) as b
left join
(select playerID as pitching_player,
sum(W) as total_wins
from pitching
group by playerID
having total_wins > 350) as c
on b.playerID = c.pitching_player
where career_average > 0.34 and total_hrs > 500 or total_wins > 350;

select * from batting limit 1;


select a.playerID, teamid, yearid, nameLast,nameFirst, 'N/A' as inseason, 'player' as role, games, g_batting, g_fielding, g_p from
(select playerID, teamid, yearid, g_all+0 as games, g_batting, g_defense as g_fielding, g_p from appearances where yearID = '1961' and teamID = 'CHN') as a
join people on a.playerID = people.playerID
union
select b.playerID, 'CHN' as teamid, '1961' as yearid, nameLast, nameFirst, inseason, 'manager' as role, games, 'N/A' as g_batting, 'N/A' as g_fielding, 'N/A' as g_p from
(select inseason, playerID, g+0 as games from managers where yearID = '1961' and teamID = 'CHN') as b
join people
on b.playerID=people.playerID
order by role desc, games desc;

select a.playerID, teamid, yearid, nameLast,nameFirst, 'N/A' as inseason, 'player' as role, games, g_batting, g_fielding, g_p from
(select playerID, teamid, yearid, g_all+0 as games, g_batting, g_defense as g_fielding, g_p from appearances where yearID = '1961' and teamID = 'CHN') as a
join people on a.playerID = people.playerID order by games;


CREATE TABLE `AllStarFullFixed` (
  `playerID` varchar(12) NOT NULL,
  `yearID` char(4) NOT NULL,
  `gameNum` int(11) DEFAULT NULL,
  `gameID` varchar(32) NOT NULL,
  `teamID` varchar(4) NOT NULL,
  `lgID` enum('NL','AL') NOT NULL,
  `GP` varchar(4) DEFAULT NULL,
  `startingPos` varchar(4) DEFAULT NULL,
  PRIMARY KEY (`playerID`,`gameID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



drop trigger insert_before_AllStarFullFixed;


select playerID from batting join people limit 1;

DELIMITER // 
CREATE  PROCEDURE update_batting_h_ab (playerid1 varchar(12), teamid1 varchar(3), yearid1 varchar(4), stint1 char(2), h1 int(5),ab1 int(5))
BEGIN


update batting SET h = h1,ab = ab1 where playerid = playerid1 abattingnd teamid = teamid1 and yearid = yearid1 and stint = stint1;
Update copy_tables_are_awesome  SET  total_hits = total_hits+h1,total_abs = total_abs +ab1
where playerid = playerid1 and teamid = teamid1 and yearid = yearid1;



END
//
DELIMITER ;

select playerid
 from appearances limit 10;
