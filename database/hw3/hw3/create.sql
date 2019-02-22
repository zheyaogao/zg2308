create database hw3;
use hw3;

CREATE TABLE `table_definitions` (
  `name` varchar(12) NOT NULL,
  `file` varchar(32) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `column_definitions` (
  `column_name` varchar(12) NOT NULL,
  `column_type` varchar(12) NOT NULL,
  `not_null`  varchar(12) default NULL,
  `table_name`  varchar(12) NOT NULL,
  PRIMARY KEY (`column_name`,`table_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `index_definitions` (
  `index_name` varchar(32) NOT NULL,
  `index_type` varchar(12) NOT NULL,
  `column`  varchar(12) NOT NULL,
  `table_name`  varchar(12) NOT NULL,
  PRIMARY KEY (`index_name`,`table_name`,`column`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

