SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;

CREATE TABLE `vast`.`instance` (
 `id` int NOT NULL AUTO_INCREMENT,
 `time` int DEFAULT NULL,
 `machine_id` int DEFAULT NULL,
 `instance_id` int NOT NULL,
 `earning` float DEFAULT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `vast`.`hardware` (
  `id` int NOT NULL AUTO_INCREMENT,
  `time` int DEFAULT NULL,
  `machine_id` int DEFAULT NULL,
  `component` varchar(45) DEFAULT NULL,
  `hw_id` varchar(45) DEFAULT NULL,
  `utilisation` double DEFAULT NULL,
  `temperature` int DEFAULT NULL,
  `power_consumption` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `vast`.`machine` (
  `id` int NOT NULL AUTO_INCREMENT,
  `time` int DEFAULT NULL,
  `machine_id` int DEFAULT NULL,
  `account_credit` float DEFAULT NULL,
  `reliability` float DEFAULT NULL,
  `rentals_stored` int DEFAULT NULL,
  `rentals_on_demand` int DEFAULT NULL,
  `rentals_bid` int DEFAULT NULL,
  `earn_hour` float DEFAULT NULL,
  `hostname` varchar(45) DEFAULT NULL,
  `earn_day` float DEFAULT NULL,
  `verification` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `vast`.`event` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `time` INT NULL,
  `machine_id` int DEFAULT NULL,
  `name` VARCHAR(45) NULL,
  `val1` VARCHAR(45) NULL,
  `val2` VARCHAR(45) NULL,
  `val3` VARCHAR(45) NULL,
  `val4` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));
