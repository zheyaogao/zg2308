use lahman2017;
SELECT playerID, nameLast, nameFirst FROM People where exists (select * from appearances where appearances.playerID = people.playerID and yearID >= 2017);
alter table appearances modify column playerid varchar(30);
use similarity;
select * from similarity;
select hex(11);

select nameLast, birthCity from people where playerID='willite01';

select * from hottest;

select * from similarity where song_id= 'SOTZJGF12A58A78BEA';

select * from hottest where song = "a'b";

select * from recommendation; 

select c.*,
    (select nameLast from lahman2017.people where lahman2017.people.playerID=c.playerID) as last_name,
    (select nameFirst from lahman2017.people where lahman2017.people.playerID=c.playerID) as last_name,
    d.avg_salary, d.salary_seasons, c.batting_average/d.avg_salary*1000 as ba_dollar from 
    (select a.*, b.total_hits, b.total_abs, b.batting_average from 
    (
        SELECT playerID, sum(InnOuts) as total_outs, sum(gs) as total_gs,
        sum(g) as games, round(sum(InnOuts)/27) as computed_games FROM lahman2017.Fielding 
        where pos='C' and yearID >= 1950 
        group by playerID 
        having computed_games >162 
    ) as a 
    join 
        (SELECT playerID, sum(h) as total_hits, sum(ab) as total_abs, round(sum(h)/sum(ab),3) 
        as batting_average from lahman2017.Batting 
        where yearID >= 1950 and ab > 0 group by playerID) as b 
    on 
        a.playerID = b.playerID) as c 
    join 
        (select playerID, round(avg(salary)) as avg_salary, count(*) as salary_seasons from 
		lahman2017.salaries group by playerID having salary_seasons >=3 and avg_salary >0) as d
    on
        c.playerID = d.playerID
    order by batting_average desc;
    
    
select if('bcd'>1,1,2);
select cast('b' as decimal);

use classiccars;
select distinct orderLineNumber from orderdetails;
select distinct orderNumber from orderdetails;
select distinct productScale from products;

create database w4111final;
use w4111final;


CREATE TABLE `person` (
  `uni` varchar(12) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  PRIMARY KEY (`uni`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `student` (
  `uni` varchar(12) NOT NULL,
  `major` varchar(12) NOT NULL,
  `advisor` varchar(12) NOT NULL,
  PRIMARY KEY (`uni`),
  KEY `student_faculty_idx` (`advisor`),
  CONSTRAINT `student_faculty` FOREIGN KEY (`advisor`) REFERENCES `faculty` (`uni`) 
      ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `student_person` FOREIGN KEY (`uni`) REFERENCES `person` (`uni`) 
      ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `faculty` (
  `uni` varchar(12) NOT NULL,
  `title` varchar(45) NOT NULL,
  PRIMARY KEY (`uni`),
  CONSTRAINT `faculty_person` FOREIGN KEY (`uni`) REFERENCES `person` (`uni`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

delete from person where last_name = 'Wizard';

drop table `person`;

use w4111final;

CREATE TABLE `banking_account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `balance` double NOT NULL,
  `version` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

use sakila;
create table facts as
select rental.rental_id, rental.rental_date,
rental.inventory_id, rental.customer_id,
rental.staff_id, payment.payment_id, payment.amount
from rental join payment
on rental.rental_id = payment.rental_id ;

create table date_dimension as 
select
 rental_date,
 year(rental_date) as year,
 ceil(month(rental_date)/4) as quarter,
 month(rental_date) as month,
 dayofmonth(rental_date) as day_of_month 
from rental
union
select
 payment_date, 
 year(payment_date) as year,
 ceil(month(payment_date)/4) as quarter,
 month(payment_date) as month,
 dayofmonth(payment_date) as day_of_month
from payment;

create temporary table tmp1 as 
 select 
	address_id,
    city_id,
    (select city from city where city.city_id=address.city_id) as city,
    district,
    (select country_id from city where city.city_id=address.city_id) as country_id
from address;


create table address_hierarchy as 
  select 
	address_id,
    city_id,
    (select city from city where city.city_id=address.city_id) as city,
    district,
    (select country_id from city where city.city_id=address.city_id) as country_id
from address;

ALTER TABLE `data_dimension` 
CHANGE COLUMN `date` `date` DATE NOT NULL ,
ADD PRIMARY KEY (`date`);

drop table date_dimension;