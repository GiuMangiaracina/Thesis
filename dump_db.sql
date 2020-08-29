-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `availability`
--

DROP TABLE IF EXISTS `availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `availability` (
  `node` int(11) NOT NULL,
  `value` int(11) DEFAULT NULL,
  PRIMARY KEY (`node`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `availability`
--

LOCK TABLES `availability` WRITE;
/*!40000 ALTER TABLE `availability` DISABLE KEYS */;
INSERT INTO `availability` VALUES (1,97),(2,80),(3,85);
/*!40000 ALTER TABLE `availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `computation_lock`
--

DROP TABLE IF EXISTS `computation_lock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `computation_lock` (
  `Locked` int(11) NOT NULL,
  PRIMARY KEY (`Locked`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `computation_lock`
--

LOCK TABLES `computation_lock` WRITE;
/*!40000 ALTER TABLE `computation_lock` DISABLE KEYS */;
INSERT INTO `computation_lock` VALUES (0);
/*!40000 ALTER TABLE `computation_lock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_source` int(11) DEFAULT NULL,
  `action` int(11) DEFAULT NULL,
  `time_stamp` int(11) DEFAULT NULL,
  `feedback_1` double DEFAULT NULL,
  `feedback_2` double DEFAULT NULL,
  `feedback_3` double DEFAULT NULL,
  `active` int(11) DEFAULT NULL,
  `controller_id` int(11) DEFAULT NULL,
  `random` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1946 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_table`
--

DROP TABLE IF EXISTS `file_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_table` (
  `data_set` int(11) NOT NULL AUTO_INCREMENT,
  `node` int(11) DEFAULT NULL,
  PRIMARY KEY (`data_set`)
) ENGINE=InnoDB AUTO_INCREMENT=190 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_table`
--

LOCK TABLES `file_table` WRITE;
/*!40000 ALTER TABLE `file_table` DISABLE KEYS */;
INSERT INTO `file_table` VALUES (1,1);
/*!40000 ALTER TABLE `file_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `global_counter`
--

DROP TABLE IF EXISTS `global_counter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `global_counter` (
  `action` varchar(10) NOT NULL,
  `id` int(11) NOT NULL,
  `value` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `global_counter`
--

LOCK TABLES `global_counter` WRITE;
/*!40000 ALTER TABLE `global_counter` DISABLE KEYS */;
INSERT INTO `global_counter` VALUES ('M12',0,0),('M21',1,0),('M13 ',2,0),('M31',3,0),('M32',4,0),('M23',5,0),('C12',6,0),('C21',7,0),('C13',8,0),('C31',9,0),('C32',10,0),('C23',11,0),('NA',12,0),('CR1',13,0),('CR2',14,0),('CR3',15,0);
/*!40000 ALTER TABLE `global_counter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `latency`
--

DROP TABLE IF EXISTS `latency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `latency` (
  `c_id` int(11) DEFAULT NULL,
  `node` int(11) DEFAULT NULL,
  `value` int(11) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `latency`
--

LOCK TABLES `latency` WRITE;
/*!40000 ALTER TABLE `latency` DISABLE KEYS */;
INSERT INTO `latency` VALUES (1,1,0,1),(1,2,1000,2),(1,3,1500,3),(2,1,1000,10),(2,2,0,11),(2,3,1200,12),(3,1,1500,13),(3,2,1200,14),(3,3,0,15);
/*!40000 ALTER TABLE `latency` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-29 11:46:59
