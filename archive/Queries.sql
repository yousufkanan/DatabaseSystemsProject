Use finalProject;


DROP TABLE if exists fighterNum;
DROP TABLE if exists fighterDen;
DROP TABLE if exists WomenFighters;



/* How many fights per weightclass. */
Select WeighClass, Count(*) as Fightcount
	 From Events
	 Group by WeighClass
	 Order by Fightcount;



/*Who has the highest win rate (out of min amount of fights) */

SELECT firstName, lastName, wins , losses, draws
FROM fighter
WHERE (wins + losses + draws) > 8
ORDER BY 
    CASE 
        WHEN (losses + draws) = 0 THEN wins / 0.00000001 -- handling division by almost zero
        ELSE wins / (losses + draws) 
    END DESC
LIMIT 50;

/*using the regression coeffecient rormula we can do this
-- get average reach of the fighters
-- get average wins of the fighters */
CREATE TABLE fighterNum AS(
SELECT 
    SUM((reach - (SELECT AVG(reach) FROM fighter)) 
    * (wins - (SELECT AVG(wins) FROM fighter))) as numerator
FROM 
    fighter);

Create Table fighterDen AS(
SELECT
    POW(SUM(POW(reach - (SELECT AVG(reach) FROM fighter), 2)),0.5) 
    * POW(SUM(POW(wins - (SELECT AVG(wins) FROM fighter), 2)),0.5) as denominator
FROM fighter);


SELECT POW(numerator / denominator,2) as "R-Squared"
FROM fighterNum, fighterDen;

DROP TABLE fighterNum;
DROP TABLE fighterDen;





/* how many fighters are in each weight class */  
Select WeighClass, count(*) as count
from Events
group by WeighClass
order by count desc;


/* what is the average win/loss of 50 fighters. */
SELECT firstName, lastName, wins , losses, draws
FROM fighter
WHERE (wins + losses + draws) > 8
ORDER BY
	CASE
    	WHEN (losses + draws) = 0 THEN wins / 0.00000001 -- handling division by almost zero
    	ELSE wins / (losses + draws)
	END DESC
LIMIT 50;

/*how many fights per weight class */
Select WeighClass, count(*) as count
from Events
group by WeighClass
order by count desc;

/* average number of takedowns per fight sorted by weightclass */ 
SELECT events.WeighClass, AVG(events.Takedowns1 + events.Takedowns2) AS AverageTakedownsPerFight
FROM events
GROUP BY events.WeighClass;

/* create a seperate table for women fighters */ 
CREATE TABLE WomenFighters AS
SELECT DISTINCT Fighter1 AS FighterName
FROM events
WHERE WeighClass LIKE '%women%'
UNION
SELECT DISTINCT Fighter2 AS FighterName
FROM events
WHERE WeighClass LIKE '%women%';

