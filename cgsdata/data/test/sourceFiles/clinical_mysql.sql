DROP DATABASE IF EXISTS `bridgeIris_clinical_db`;
CREATE DATABASE `bridgeIris_clinical_db`;

CREATE TABLE `sample` (
       `SAMPLE_ID` int(11) NOT NULL DEFAULT '0',
       `PATIENT_ID` int(11) NOT NULL,
       `DATE_OF_COLLECTION` timestamp NULL DEFAULT NULL,
       	PRIMARY KEY (`SAMPLE_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


