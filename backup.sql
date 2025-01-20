-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: registration
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `appointment_logs`
--

DROP TABLE IF EXISTS `appointment_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointment_logs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `appointment_id` int NOT NULL,
  `log_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `log_description` text NOT NULL,
  PRIMARY KEY (`log_id`),
  KEY `appointment_logs_ibfk_1` (`appointment_id`),
  CONSTRAINT `appointment_logs_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointment_logs`
--

LOCK TABLES `appointment_logs` WRITE;
/*!40000 ALTER TABLE `appointment_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `appointment_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `reason` text,
  `status` enum('pending','confirmed','canceled','completed') DEFAULT 'pending',
  PRIMARY KEY (`appointment_id`),
  UNIQUE KEY `unique_appointment` (`doctor_id`,`appointment_date`,`appointment_time`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,1,1,'2023-12-22','09:00:00','Routine check-up','confirmed'),(2,2,1,'2023-12-23','11:00:00','Cardiology follow-up','pending'),(3,1,1,'2023-12-22','10:00:00','Routine check-up','pending');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branches`
--

DROP TABLE IF EXISTS `branches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branches` (
  `branch_id` int NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(255) NOT NULL,
  PRIMARY KEY (`branch_id`),
  UNIQUE KEY `branch_name` (`branch_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branches`
--

LOCK TABLES `branches` WRITE;
/*!40000 ALTER TABLE `branches` DISABLE KEYS */;
INSERT INTO `branches` VALUES (1,'Cardiology'),(2,'Dentist');
/*!40000 ALTER TABLE `branches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `id` int NOT NULL,
  `department_name` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`department_id`),
  KEY `id` (`id`),
  CONSTRAINT `departments_ibfk_1` FOREIGN KEY (`id`) REFERENCES `employees` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor_availability`
--

DROP TABLE IF EXISTS `doctor_availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_availability` (
  `availability_id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `available_date` date NOT NULL,
  `available_time` time NOT NULL,
  `is_available` tinyint(1) DEFAULT '1',
  `available_start_time` time NOT NULL,
  `available_end_time` time NOT NULL,
  PRIMARY KEY (`availability_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `doctor_availability_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_availability`
--

LOCK TABLES `doctor_availability` WRITE;
/*!40000 ALTER TABLE `doctor_availability` DISABLE KEYS */;
INSERT INTO `doctor_availability` VALUES (1,1,'2023-12-22','09:00:00',0,'00:00:00','00:00:00'),(2,1,'2023-12-22','10:00:00',0,'00:00:00','00:00:00'),(3,1,'2023-12-23','11:00:00',1,'00:00:00','00:00:00'),(4,3,'2023-12-23','10:00:00',0,'00:00:00','00:00:00');
/*!40000 ALTER TABLE `doctor_availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `degree` varchar(255) NOT NULL,
  `specialization` varchar(255) NOT NULL,
  `Employee_password` text,
  `employee_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `doctors_ibfk_1` (`employee_id`),
  CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,'MD','Cardiology',NULL,8),(2,'MD','Cardiology',NULL,10),(9,'MD','Cardiologist',NULL,13);
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Employee_name` varchar(255) NOT NULL,
  `surname` varchar(255) NOT NULL,
  `role` enum('doctor','nurse','admin','receptionist','lab_staff') NOT NULL,
  `email` varchar(255) NOT NULL,
  `gender` enum('female','male','other') NOT NULL,
  `contacts` bigint DEFAULT NULL,
  `department` enum('dentist','Cardiology') DEFAULT NULL,
  `Employee_password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'John','Doe','doctor','john.doe@example.com','male',123456789,'Cardiology','$2b$12$LBifi.ZSBgYtE6eVSJM.9OLda5A3TDO2xVQjWb05VorDFE8dF4/oi'),(2,'Jane','Smith','receptionist','jane.smith@example.com','female',987654321,NULL,'$2b$12$cfrq1mu8ktfWparR9115sujAefA83hiDCHGKyDSGxs/dHl0bexIWW'),(3,'Admin','User','admin','admin@example.com','other',NULL,NULL,'$2b$12$IIbq.NcyCyyVJw9Rtinlm.x7gT1NpHy1RSxbZ0cHnbrQr4dTFb8Le'),(8,'Zeki','Türk','doctor','zeki.turk@example.com','male',NULL,NULL,'$2b$12$BnbtAqmV1HLk3IU4Iyt1j.51he5brhKG73.2aOiM1kO/.fyH3pB1K'),(9,'Livan','Türk','doctor','livan.turk@example.com','male',NULL,NULL,'$2b$12$vbWMbwwnuCVYsslizog8/ukNOTkpJuo/4DOYR9DrPwJWBNvnRqTOG'),(10,'Elif Naz','Türk','doctor','elifnaz.turk@example.com','female',13435353466,NULL,'$2b$12$GgPPNInjB69jtW3RQdvH6OkzwxnXGcVStxdEjWQzbYHyqnrgnk8Ju'),(11,'Ayşe','Yılmaz','receptionist','ayse.yilmaz@example.com','female',NULL,NULL,'$2b$12$5O7W/L9pzAg9tQ3hxgdPv.I6E.RimvvAq4OjK5/FjqmfYZiaZcGMG'),(12,'Admina','User','admin','admin2@example.com','other',2335465764,NULL,'$2b$12$OgQRNwgpFCLeDIKNP3QXW.ZIIsiYmTqsZJJ/LcW6Jfn9OXMiYm1G.'),(13,'Ahmet','Koray','doctor','ahmet.koray@example.com','male',123456731212,'Cardiology','$2b$12$POpYRfDdoRc7yIiu7j.6Bee.GBzBpCM7wJOesqhuXMDkEgUo2k3V6'),(15,'Ahmet','Koray','doctor','ahmet.koray2@example.com','male',123456731212,'Cardiology','$2b$12$XApKOuE6/5t8TiRS4ZdP0O2rAUglaj7FMapG5XTnG2wVYKnl5aVMm');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lab_tests`
--

DROP TABLE IF EXISTS `lab_tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lab_tests` (
  `test_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL,
  `test_name` varchar(255) NOT NULL,
  `priority` enum('low','medium','high') NOT NULL,
  `test_reason` text,
  `requested_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` enum('pending','in_progress','completed','cancelled') DEFAULT 'pending',
  `result` text,
  `completed_at` datetime DEFAULT NULL,
  `assigned_staff_id` int DEFAULT NULL,
  `assigned_at` datetime DEFAULT NULL,
  `appointment_id` int DEFAULT NULL,
  PRIMARY KEY (`test_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `lab_tests_ibfk_3` (`assigned_staff_id`),
  KEY `lab_tests_ibfk_appointment` (`appointment_id`),
  CONSTRAINT `lab_tests_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  CONSTRAINT `lab_tests_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `employees` (`id`),
  CONSTRAINT `lab_tests_ibfk_3` FOREIGN KEY (`assigned_staff_id`) REFERENCES `employees` (`id`),
  CONSTRAINT `lab_tests_ibfk_appointment` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lab_tests`
--

LOCK TABLES `lab_tests` WRITE;
/*!40000 ALTER TABLE `lab_tests` DISABLE KEYS */;
/*!40000 ALTER TABLE `lab_tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification_log`
--

DROP TABLE IF EXISTS `notification_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification_log` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `to_email` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `status` enum('sent','failed') NOT NULL,
  `sent_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification_log`
--

LOCK TABLES `notification_log` WRITE;
/*!40000 ALTER TABLE `notification_log` DISABLE KEYS */;
INSERT INTO `notification_log` VALUES (1,'webprojectutaa@gmail.com','Test Notification','This is a test notification from the Notification Service.','sent','2024-12-23 22:07:56');
/*!40000 ALTER TABLE `notification_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nurse_patient_assignments`
--

DROP TABLE IF EXISTS `nurse_patient_assignments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nurse_patient_assignments` (
  `assignment_id` int NOT NULL AUTO_INCREMENT,
  `nurse_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `assigned_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`assignment_id`),
  KEY `nurse_id` (`nurse_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `nurse_patient_assignments_ibfk_1` FOREIGN KEY (`nurse_id`) REFERENCES `employees` (`id`),
  CONSTRAINT `nurse_patient_assignments_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nurse_patient_assignments`
--

LOCK TABLES `nurse_patient_assignments` WRITE;
/*!40000 ALTER TABLE `nurse_patient_assignments` DISABLE KEYS */;
/*!40000 ALTER TABLE `nurse_patient_assignments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nurses`
--

DROP TABLE IF EXISTS `nurses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nurses` (
  `id` int NOT NULL,
  `degree` varchar(255) NOT NULL,
  `Employee_password` text,
  PRIMARY KEY (`id`),
  CONSTRAINT `nurses_ibfk_1` FOREIGN KEY (`id`) REFERENCES `employees` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nurses`
--

LOCK TABLES `nurses` WRITE;
/*!40000 ALTER TABLE `nurses` DISABLE KEYS */;
/*!40000 ALTER TABLE `nurses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_records`
--

DROP TABLE IF EXISTS `patient_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_records` (
  `record_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `id` int NOT NULL,
  `department_id` int NOT NULL,
  `patient_status` enum('improving','No change','dismissed') DEFAULT NULL,
  `doctor_note` text NOT NULL,
  `visit_reason` text,
  `visit_date` date DEFAULT NULL,
  `prescription` text,
  `additional_notes` text,
  `nurse_note` text,
  PRIMARY KEY (`record_id`),
  KEY `patient_id` (`patient_id`),
  KEY `id` (`id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `patient_records_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  CONSTRAINT `patient_records_ibfk_2` FOREIGN KEY (`id`) REFERENCES `employees` (`id`),
  CONSTRAINT `patient_records_ibfk_3` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_records`
--

LOCK TABLES `patient_records` WRITE;
/*!40000 ALTER TABLE `patient_records` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient_records` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `set_visit_date` BEFORE INSERT ON `patient_records` FOR EACH ROW BEGIN

    IF NEW.visit_date IS NULL THEN

        SET NEW.visit_date = CURRENT_DATE;

    END IF;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `patient_name` varchar(30) NOT NULL,
  `patient_surname` varchar(30) DEFAULT NULL,
  `patient_age` int NOT NULL,
  `patient_blood_group` enum('A+','A-','B+','B-','O+','O-','AB+','AB-') DEFAULT NULL,
  `gender` enum('female','male') NOT NULL,
  `contacts` bigint NOT NULL,
  `next_of_keen_contacts` bigint NOT NULL,
  `insurance` text NOT NULL,
  `patient_email` varchar(30) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `last_updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`patient_id`),
  CONSTRAINT `patients_chk_1` CHECK ((`patient_age` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'Alice','Brown',30,'O+','female',123456789,987654321,'Premium Health','alice.brown@example.com','$2b$12$XtSvoMjElWyus2kLQZTuA.15yqr2wB031tHVkE/0pUTCmZ5pW5EIm','2024-12-29 17:06:33'),(2,'Bob','Green',40,'A-','male',555555555,666666666,'Basic Health','bob.green@example.com','$2b$12$1qXChkQAK6/iIch9N5Ims.Egkqe34h1Fw4VNn4GUKA5Ffsnq5k5li','2024-12-29 17:06:33'),(3,'Web','Project',25,'A+','female',123456789,987654321,'Basic Plan','webprojectutaa@gmail.com','$2b$12$xFuZUghhRM4dv1WaJZgR7.byUbJtEFC5P.XQrBHy5biQ0KklsNnlq','2024-12-29 17:06:33'),(4,'Ahmet','Kara',45,'A+','male',5551234567,5559876543,'Public Health','ahmet.kara@example.com','$2b$12$YCL8f/S/yL7uWDwZw/sUt.xN99oe74l1N46i3/dtOyP2m58DPkh8u','2024-12-29 17:06:33'),(5,'Emin','Aslan',25,'O+','male',123456789021,98762154321,'Premium Health','emin.aslan@gmail.com','$2b$12$jlowSffRqPh4KNS6awFfIe3PJYDOk2jTKsnvMZRTOWzw8FZYo6B2q','2024-12-30 14:31:06');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescriptions`
--

DROP TABLE IF EXISTS `prescriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescriptions` (
  `prescription_id` int NOT NULL AUTO_INCREMENT,
  `doctor_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `prescription_date` date DEFAULT NULL,
  `medication_details` text NOT NULL,
  PRIMARY KEY (`prescription_id`),
  KEY `prescriptions_ibfk_1` (`doctor_id`),
  KEY `prescriptions_ibfk_2` (`patient_id`),
  CONSTRAINT `prescriptions_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`),
  CONSTRAINT `prescriptions_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescriptions`
--

LOCK TABLES `prescriptions` WRITE;
/*!40000 ALTER TABLE `prescriptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `prescriptions` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `set_prescription_date` BEFORE INSERT ON `prescriptions` FOR EACH ROW BEGIN

    IF NEW.prescription_date IS NULL THEN

        SET NEW.prescription_date = CURRENT_DATE;

    END IF;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-20 18:43:45
