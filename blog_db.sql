-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: contacts
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `bcontact`
--

DROP TABLE IF EXISTS `bcontact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bcontact` (
  `sl_no` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `ph_num` varchar(45) NOT NULL,
  `msg` varchar(100) NOT NULL,
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bcontact`
--

LOCK TABLES `bcontact` WRITE;
/*!40000 ALTER TABLE `bcontact` DISABLE KEYS */;
INSERT INTO `bcontact` VALUES (1,'sonu','sonu@gmail.com','234576789','first'),(2,'soumya ranjan khuntia','soumyaranjankhuntia82@gmail.com','6372501139','please work'),(3,'Harry','codewithharry@gmail.com','9854638296','Thank you harry bahi for this amazing flask tutorial'),(4,'Harry','codewithharry@gmail.com','9854638296','Thank you harry bahi for this amazing flask tutorial'),(5,'codebasics','codebasics@gmail.com','9867964538','this is codebasics'),(6,'unknown','jhshfjahwuhja@gmail.com','8475843748','sadhfjhukbjvhgsuafdjhfbdujhfb'),(7,'unknown','jhshfjahwuhja@gmail.com','8475843748','sadhfjhukbjvhgsuafdjhfbdujhfb'),(8,'hvhghbv','hggyggyguguy@gmail.com','767456746','hdttertsghfvgftertghytrg'),(9,'SRK','fayssghs@gmail.com','9854638296','what happens'),(10,'harry','harry@gmail.com','9365372627','is it works');
/*!40000 ALTER TABLE `bcontact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blogins`
--

DROP TABLE IF EXISTS `blogins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blogins` (
  `lid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`lid`),
  KEY `idx_bname_id` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blogins`
--

LOCK TABLES `blogins` WRITE;
/*!40000 ALTER TABLE `blogins` DISABLE KEYS */;
INSERT INTO `blogins` VALUES (1,'sonu','1234','soumyaranjankhuntia82@gmail.com'),(13,'chinu','5678',NULL);
/*!40000 ALTER TABLE `blogins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bpost`
--

DROP TABLE IF EXISTS `bpost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bpost` (
  `slno` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  `sub_title` varchar(100) DEFAULT NULL,
  `slug` varchar(45) NOT NULL,
  `content` varchar(200) NOT NULL,
  `img_file` varchar(30) DEFAULT NULL,
  `date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `lname` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`slno`),
  KEY `fk_idx` (`lname`),
  CONSTRAINT `fk` FOREIGN KEY (`lname`) REFERENCES `blogins` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bpost`
--

LOCK TABLES `bpost` WRITE;
/*!40000 ALTER TABLE `bpost` DISABLE KEYS */;
INSERT INTO `bpost` VALUES (1,'Soumya','This is first post','first','my first post uploaded successfully',NULL,'2024-01-14 11:57:25',NULL),(2,'gunul','He is my school friend','second','soumya ranjan khuntia',NULL,'2024-01-14 11:57:25',NULL),(3,'chinu','He is my yonger brother','third','chittaranjan Khuntia',NULL,'2024-01-14 11:57:25',NULL),(4,'munu','he is my senior friend','four','soumya prakash ojha',NULL,'2024-01-14 11:57:25',NULL),(5,'Ojha','one of coluge','five','he is a good boy',NULL,'2024-01-14 11:57:25',NULL),(6,'samarjit','study at driems','five-1','he is a good student and topper',NULL,'2024-01-14 11:57:25',NULL),(7,'sagarika','DRIEMS','six','she studied at DRIEMS and she is extovert and chilled girl',NULL,'2024-01-14 11:57:25',NULL),(10,'Harry','Youtuber','eight','He is a very good youtuber and i started my virtual technology journy from him.',NULL,'2024-01-14 11:57:25',NULL),(11,'Krish naik','Generative AI,ML','eleven','He is very good ML enginner and generative ai specialist',NULL,'2024-01-14 12:04:11',NULL),(12,'codebasics','ML,AI,GenAI','twelve','he is teaching different subdomains of python and they are also very important',NULL,'2024-01-15 13:50:42',NULL);
/*!40000 ALTER TABLE `bpost` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact`
--

DROP TABLE IF EXISTS `contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact` (
  `sl_no` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `ph_no` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `sub` varchar(100) NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`sl_no`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact`
--

LOCK TABLES `contact` WRITE;
/*!40000 ALTER TABLE `contact` DISABLE KEYS */;
INSERT INTO `contact` VALUES (1,'sonu','6372501139','soumyaranjankhuntia82@gmail.com','first commit','9999-12-31 23:59:59'),(2,'soumya ranjan khuntia','9763456285','soumyaranjankhuntia63@gmail.com','please work','2024-01-12 13:14:15'),(3,'sagarika','1234422','sagarika@gmail.com','Database works clearly and finely','2024-01-12 13:29:24');
/*!40000 ALTER TABLE `contact` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-16  8:13:11
