create database FootBallDB_24
use FootballDB_24
select * from epl_match_24

select a.HomeTeam,
		COUNT(CASE WHEN a.FullTimeResult = 'A' THEN 1 END) AS Total_A,
        COUNT(CASE WHEN a.FullTimeResult = 'D' THEN 1 END) AS Total_D,
        COUNT(CASE WHEN a.FullTimeResult = 'H' THEN 1 END) AS Total_H,
        count(a.FullTimeResult) as Total,
        Format((COUNT(CASE WHEN a.FullTimeResult = 'H' THEN 1 END)*1.0 / count(a.FullTimeResult)), 'P2') as aver
from epl_match_24 as a
group by a.HomeTeam
order by Total_A desc,Total_D desc,Total_H desc

select a.*
from epl_match_24 a
where MONTH(a.MatchDate) = '01' and YEAR(a.MatchDate) = '2025'

EXEC sp_help 'epl_match_24'
alter table epl_match_24
alter column MatchDate Datetime
--1. Tổng số bàn thắng của mỗi đội trong một mùa giải
--Mục đích: Đánh giá sức mạnh tấn công của các đội.
    select a.Season, a.Team, sum(sum_goal) sum_goal
    from 
    (Select a.Season, a.HomeTeam as Team, sum(a.FullTimeHomeGoals) sum_goal
    from epl_match_24 a
    group by a.Season, a.HomeTeam
    Union
    select a.Season, a.AwayTeam as Team, sum(a.FullTimeAwayGoals) sum_goal
    from epl_match_24 a
    group by a.Season, a.AwayTeam) a
    group by a.Season, a.Team
    order by sum(a.sum_goal) desc

    select a.Season, a.Team, sum(sum_goal) sum_goal
    from 
    (Select a.Season, a.HomeTeam as Team, a.FullTimeHomeGoals sum_goal
    from epl_match_24 a
    Union all
    select a.Season, a.AwayTeam as Team, a.FullTimeAwayGoals sum_goal
    from epl_match_24 a
   ) a
    group by a.Season, a.Team
    order by sum(a.sum_goal) desc

--3. Tổng số điểm của mỗi đội trong mùa giải
--Mục đích: Xác định đội mạnh nhất (thay vì chỉ nhìn bàn thắng)
select a.Season, a.Team, sum(a.point) as point       
from (
        select a.Season, a.HomeTeam Team, (COUNT(CASE WHEN a.FullTimeResult = 'H' THEN 1 END)*3 +COUNT(CASE WHEN a.FullTimeResult = 'D' THEN 1 END)) as point
        from epl_match_24 a
        group by a.Season, a.HomeTeam
        union all
        select a.Season, a.AwayTeam Team, (COUNT(CASE WHEN a.FullTimeResult = 'A' THEN 1 END)*3 +COUNT(CASE WHEN a.FullTimeResult = 'D' THEN 1 END)) as point
        from epl_match_24 a
        group by a.Season, a.AwayTeam) a
group by a.Season, a.Team
order by sum(a.point) desc

--4. Trung bình số bàn thắng mỗi trận theo mùa
--Mục đích: Đánh giá xu hướng tấn công của giải đấu qua các năm.
select a.Season, a.HomeTeam,a.AwayTeam,AVG(a.FullTimeHomeGoals*1.0+a.FulltimeAwayGoals) as avg_goal
from epl_match_24 a
group by a.Season, a.HomeTeam,a.AwayTeam
order by a.HomeTeam asc, a.AwayTeam asc

--5. Hiệu suất sút trúng đích của đội chủ nhà và đội khách
--Mục đích: Đánh giá hiệu quả dứt điểm.
select a.Season, Format(sum(a.HomeShotsOnTarget)*1.0/sum(a.HomeShots), 'P2') as Performance, (sum(a.AwayShotsOnTarget)*1.0/sum(a.AwayShots)) as Away_Performance
from epl_match_24 a
group by a.Season

---6. Trung bình số thẻ vàng và đỏ mỗi đội
---Mục đích: Đánh giá tính kỷ luật của đội.
select a.Team, avg(a.red*1.0), avg(yellow*1.0)            
     from(       select a.Hometeam Team, a.HomeRedCards red,a.HomeYellowCards yellow
            from epl_match_24 a
            union all
            select a.AwayTeam Team, a.AwayRedCards red,a.AwayYellowCards yellow
            from epl_match_24 a) a
group by a.Team
---7. Tỉ lệ thắng sân nhà và sân khách của từng đội
---Mục đích: Phân tích phong độ sân nhà/sân khách.
with 
homestats as(
select a.HomeTeam Team, (count(case when a.FullTimeResult = 'H' then 1 end)*1.0 / count(a.FullTimeResult)) as per
from epl_match_24 a
group by a.HomeTeam),
awaystats as(
select a.AwayTeam Team, (count(case when a.FullTimeResult = 'A' then 1 end)*1.0 / count(a.FullTimeResult)) as per
from epl_match_24 a
group by a.AwayTeam)
select h.Team, format((h.per),'P2') as home, format((a.per),'P2') as away 
from homestats h join awaystats a on h.Team = a.Team 


--8. Trung bình số cú sút của đội thắng vs đội thua
--Mục đích: So sánh chiến thuật – liệu nhiều sút có dẫn đến thắng?
select a.Win_team, avg(a.win_shot) win_shot, avg(a.lose_shot) lose_shot  
from ( 
        select a.HomeTeam Win_team, avg(a.HomeShots*1.0) win_shot, avg(a.AwayShots) lose_shot
        from epl_match_24 a
        where a.FullTimeResult = 'H'
        group by a.HomeTeam
        Union
        select a.AwayTeam Win_team, avg(a.AwayShots) win_shot, avg(a.HomeShots) lose_shot
        from epl_match_24 a
        where a.FullTimeResult = 'A'
        group by a.AwayTeam) a
group by a.Win_team

SELECT
  AVG(
    CASE 
      WHEN FullTimeResult = 'H' THEN HomeShots
      WHEN FullTimeResult = 'A' THEN AwayShots
      else 0
    END
  ) * 1.0 AS avg_shots_winner,
  AVG(
    CASE 
      WHEN FullTimeResult = 'H' THEN AwayShots
      WHEN FullTimeResult = 'A' THEN HomeShots
      else 0
    END
  ) * 1.0 AS avg_shots_loser,
  SUM(CASE WHEN FullTimeResult IN ('H','A') THEN 1 ELSE 0 END) AS matches_count
FROM epl_match_24
WHERE FullTimeResult IN ('H','A')
  AND HomeShots IS NOT NULL
  AND AwayShots IS NOT NULL;


---9. Đội có số trận hòa nhiều nhất trong mùa
---Mục đích: Xác định đội "an toàn" nhất (ít thắng, ít thua)
select a.Season, b.Team, a.draw
from(        
       select a.Season, max(a.draw) draw
        from
                (select a.Season, a.Team, sum(a.draw) draw
                from (
                select a.Season, a.HomeTeam Team, sum(case when a.FullTimeResult = 'D' then 1 else 0 end) draw
                from epl_match_24 a
                group by a.Season, a.HomeTeam
                union all
                select a.Season, a.AwayTeam Team, sum(case when a.FullTimeResult = 'D' then 1 else 0 end) draw
                from epl_match_24 a
                group by a.Season, a.AwayTeam)  a
                group by a.Season, a.Team) a
                group by a.Season) a inner join (select a.Season, a.Team, sum(a.draw) draw
                from (
                select a.Season, a.HomeTeam Team, sum(case when a.FullTimeResult = 'D' then 1 else 0 end) draw
                from epl_match_24 a
                group by a.Season, a.HomeTeam
                union all
                select a.Season, a.AwayTeam Team, sum(case when a.FullTimeResult = 'D' then 1 else 0 end) draw
                from epl_match_24 a
                group by a.Season, a.AwayTeam)  a
                group by a.Season, a.Team) b on a.Season = b.Season and a.draw = b.draw
                order by a.draw asc
        
--10. Hiệu số bàn thắng (Goal Difference) của từng đội
--Mục đích: Chỉ số quan trọng phản ánh sức mạnh toàn diện.
select a.Team, format((sum(goal)*1.0/sum(a.total_shot)), 'P2') aver    
from       (select a.HomeTeam Team, a.FullTimeHomeGoals goal,a.HomeShots total_shot
        from epl_match_24 a
        union
        select a.AwayTeam Team, a.FullTimeAwayGoals goal,a.AwayShots total_shot
        from epl_match_24 a
        ) a
group by a.Team
