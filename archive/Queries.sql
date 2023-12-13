Use finalProject;


DROP TABLE if exists fighterNum;
DROP TABLE if exists fighterDen;



--How many fights per weightclass.

--What is the average age of fighters


--Who has the highest win rate (out of min amount of fights)

SELECT firstName, lastName, wins , losses, draws
FROM fighter
WHERE (wins + losses + draws) > 8
ORDER BY 
    CASE 
        WHEN (losses + draws) = 0 THEN wins / 0.00000001 -- handling division by almost zero
        ELSE wins / (losses + draws) 
    END DESC
LIMIT 50;


--What effect does reach have on wins
-- using the regression coeffecient rormula we can do this
-- get average reach of the fighters
-- get average wins of the fighters
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





--how many fighters are in each weight class 
Select weight_class, count(*) as count
from weightClass
group by weight_class
order by count desc;


--who has the fastest average fight time (out of min amount of fights)
