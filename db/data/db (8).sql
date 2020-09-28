-- Adminer 4.7.7 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `availability`;
CREATE TABLE `availability` (
  `node` int(11) NOT NULL,
  `value` int(11) DEFAULT NULL,
  PRIMARY KEY (`node`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `availability` (`node`, `value`) VALUES
(1,	97),
(2,	80),
(3,	85);

DROP TABLE IF EXISTS `computation_lock`;
CREATE TABLE `computation_lock` (
  `Locked` int(11) NOT NULL,
  PRIMARY KEY (`Locked`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `computation_lock` (`Locked`) VALUES
(0);

DROP TABLE IF EXISTS `events`;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_source` int(11) DEFAULT NULL,
  `action` int(11) DEFAULT NULL,
  `time_stamp` int(11) DEFAULT NULL,
  `feedback_1` double NOT NULL DEFAULT '0',
  `feedback_2` double DEFAULT '0',
  `feedback_3` double DEFAULT '0',
  `active` int(11) DEFAULT NULL,
  `controller_id` int(11) DEFAULT NULL,
  `random` int(11) DEFAULT '0',
  `sum_feedback` double NOT NULL DEFAULT '0',
  `action_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `file_table`;
CREATE TABLE `file_table` (
  `data_set` int(11) NOT NULL AUTO_INCREMENT,
  `node` int(11) DEFAULT NULL,
  PRIMARY KEY (`data_set`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `file_table` (`data_set`, `node`) VALUES
(1,	3);

DROP TABLE IF EXISTS `global_counter`;
CREATE TABLE `global_counter` (
  `action` varchar(10) NOT NULL,
  `id` int(11) NOT NULL,
  `value` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `latency`;
CREATE TABLE `latency` (
  `node_ID` int(11) DEFAULT NULL,
  `node` int(11) DEFAULT NULL,
  `value` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `latency` (`node_ID`, `node`, `value`, `id`) VALUES
(1,	1,	0,	1),
(1,	2,	1000,	2),
(1,	3,	1500,	3),
(2,	1,	1000,	10),
(2,	2,	0,	11),
(2,	3,	1200,	12),
(3,	1,	1500,	13),
(3,	2,	1200,	14),
(3,	3,	0,	15);

DROP TABLE IF EXISTS `nodes`;
CREATE TABLE `nodes` (
  `node_ID` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`node_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `nodes` (`node_ID`) VALUES
(1),
(2),
(3);

-- 2020-09-28 13:17:01
