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

INSERT INTO `events` (`id`, `data_source`, `action`, `time_stamp`, `feedback_1`, `feedback_2`, `feedback_3`, `active`, `controller_id`, `random`, `sum_feedback`, `action_type`) VALUES
(17,	1,	1,	1601115411,	0,	0.6476190476190475,	0,	0,	1,	0,	0.6476190476190475,	'move'),
(18,	1,	0,	1601115485,	0.780952380952381,	0,	0.1333333333333333,	0,	2,	0,	0.9142857142857143,	'move'),
(19,	1,	1,	1601115531,	0,	0.6142857142857143,	0.35238095238095235,	0,	1,	0,	0.9666666666666667,	'move'),
(20,	1,	0,	1601115612,	0.7571428571428571,	0,	0.7380952380952381,	0,	2,	0,	1.4952380952380953,	'move'),
(21,	1,	7,	1601115663,	0,	0.6285714285714286,	0.9809523809523809,	0,	1,	0,	1.6095238095238096,	'copy'),
(22,	1,	2,	1601115667,	0,	0.6476190476190475,	0,	0,	3,	0,	0.6476190476190475,	'move'),
(23,	1,	13,	1601116168,	0,	0,	0,	0,	2,	0,	0,	'change reference copy'),
(24,	5,	6,	1601116213,	0,	0,	0,	0,	2,	0,	0,	'copy');

DROP TABLE IF EXISTS `file_table`;
CREATE TABLE `file_table` (
  `data_set` int(11) NOT NULL AUTO_INCREMENT,
  `node` int(11) DEFAULT NULL,
  PRIMARY KEY (`data_set`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `file_table` (`data_set`, `node`) VALUES
(1,	3),
(5,	1),
(6,	2);

DROP TABLE IF EXISTS `global_counter`;
CREATE TABLE `global_counter` (
  `action` varchar(10) NOT NULL,
  `id` int(11) NOT NULL,
  `value` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `global_counter` (`action`, `id`, `value`) VALUES
('M12',	0,	2),
('M21',	1,	2),
('M13 ',	2,	1),
('M31',	3,	0),
('M32',	4,	0),
('M23',	5,	0),
('C12',	6,	0),
('C21',	7,	1),
('C13',	8,	0),
('C31',	9,	0),
('C32',	10,	0),
('C23',	11,	0),
('NA',	12,	0),
('CR1',	13,	0),
('CR2',	14,	0),
('CR3',	15,	0);

DROP TABLE IF EXISTS `latency`;
CREATE TABLE `latency` (
  `c_id` int(11) DEFAULT NULL,
  `node` int(11) DEFAULT NULL,
  `value` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `latency` (`c_id`, `node`, `value`, `id`) VALUES
(1,	1,	0,	1),
(1,	2,	1000,	2),
(1,	3,	1500,	3),
(2,	1,	1000,	10),
(2,	2,	0,	11),
(2,	3,	1200,	12),
(3,	1,	1500,	13),
(3,	2,	1200,	14),
(3,	3,	0,	15);

-- 2020-09-26 10:56:46
