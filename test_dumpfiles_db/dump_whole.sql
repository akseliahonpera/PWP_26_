CREATE DATABASE  IF NOT EXISTS `pwp26` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pwp26`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: pwp26
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `userID` int NOT NULL,
  `jobDescription` varchar(255) NOT NULL,
  `timetable` varchar(63) DEFAULT NULL,
  `location` varchar(63) NOT NULL,
  `created` datetime NOT NULL,
  `opening_hours` varchar(63) NOT NULL,
  `category` varchar(31) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `userID` (`userID`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,23,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(2,22,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(3,4,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(4,12,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(5,17,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(6,5,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(7,2,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(8,21,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(9,23,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(10,14,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(11,10,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(12,16,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(13,15,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(14,7,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(15,2,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(16,19,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(17,19,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(18,18,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(19,5,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(20,9,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(21,10,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(22,17,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(23,4,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(24,6,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality'),(25,10,'Looking for a part-time barista for weekend shifts','Weekends 8am–2pm','Downtown Cafe, Springfield','2026-02-09 00:00:00','08:00-14:00','Hospitality');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `email` varchar(63) NOT NULL,
  `address` varchar(63) NOT NULL,
  `phoneNumber` varchar(31) NOT NULL,
  `description` varchar(255) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'testuser\": \"+0','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(2,'testuser\": \"+1','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(3,'testuser\": \"+2','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(4,'testuser\": \"+3','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(5,'testuser\": \"+4','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(6,'testuser\": \"+5','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(7,'testuser\": \"+6','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(8,'testuser\": \"+7','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(9,'testuser\": \"+8','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(10,'testuser\": \"+9','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(11,'testuser\": \"+10','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(12,'testuser\": \"+11','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(13,'testuser\": \"+12','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(14,'testuser\": \"+13','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(15,'testuser\": \"+14','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(16,'testuser\": \"+15','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(17,'testuser\": \"+16','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(18,'testuser\": \"+17','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(19,'testuser\": \"+18','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(20,'testuser\": \"+19','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(21,'testuser\": \"+20','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(22,'testuser\": \"+21','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:51'),(23,'testuser\": \"+22','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(24,'testuser\": \"+23','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(25,'testuser\": \"+24','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(26,'testuser\": \"+25','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(27,'testuser\": \"+26','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(28,'testuser\": \"+27','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(29,'testuser\": \"+28','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(30,'testuser\": \"+29','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(31,'testuser\": \"+30','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(32,'testuser\": \"+31','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(33,'testuser\": \"+32','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(34,'testuser\": \"+33','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(35,'testuser\": \"+34','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(36,'testuser\": \"+35','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(37,'testuser\": \"+36','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(38,'testuser\": \"+37','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(39,'testuser\": \"+38','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(40,'testuser\": \"+39','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(41,'testuser\": \"+40','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(42,'testuser\": \"+41','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(43,'testuser\": \"+42','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(44,'testuser\": \"+43','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(45,'testuser\": \"+44','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(46,'testuser\": \"+45','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(47,'testuser\": \"+46','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(48,'testuser\": \"+47','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(49,'testuser\": \"+48','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52'),(50,'testuser\": \"+49','securepassword123','testuser@example.com','123 Main Street, Springfield','555-123-4567','Test user account for database insertion','2026-02-10 04:03:52');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-10 13:15:38
