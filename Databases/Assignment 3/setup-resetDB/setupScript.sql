-- basically the script provided for a2 setup with some modifications

-- ---------------------------------
-- SCRIPT 1

-- Set up the database

SHOW DATABASES;
DROP DATABASE IF EXISTS a3hospitals;
CREATE DATABASE a3hospitals;
USE a3hospitals; 


-- Create the tables for the database

SHOW TABLES;

CREATE TABLE doctor(licensenum CHAR(4) NOT NULL, firstname VARCHAR(20) NOT NULL, lastname VARCHAR(20) NOT NULL, licensedate DATE NOT NULL, birthdate DATE NOT NULL, hosworksat CHAR(3), speciality VARCHAR(30), PRIMARY KEY(licensenum));

CREATE TABLE patient (ohipnum CHAR(9) NOT NULL,firstname VARCHAR(20) NOT NULL, lastname VARCHAR(20) NOT NULL,birthdate DATE NOT NULL, PRIMARY KEY(ohipnum));

CREATE TABLE hospital (hoscode CHAR(3) NOT NULL, hosname VARCHAR(30) NOT NULL, city VARCHAR (20) NOT NULL, prov CHAR(2) NOT NULL, numofbed SMALLINT NOT NULL, headdoc CHAR(4),headdocstartdate DATE,  PRIMARY KEY (hoscode),   FOREIGN KEY (headdoc) REFERENCES doctor(licensenum));

-- add the foreign key
ALTER TABLE doctor ADD CONSTRAINT fk_worksat FOREIGN KEY (hosworksat) REFERENCES hospital(hoscode);

CREATE TABLE looksafter(licensenum CHAR(4) NOT NULL, ohipnum CHAR(9) NOT NULL, PRIMARY KEY (licensenum, ohipnum), FOREIGN KEY(licensenum) REFERENCES doctor(licensenum) ON DELETE RESTRICT, FOREIGN KEY (ohipnum) REFERENCES patient(ohipnum) ON DELETE CASCADE);

SHOW TABLES;

-- ------------------------------------
-- insert some data

-- insert into the Patients Table
SELECT * FROM patient;
INSERT INTO patient VALUES ('110112113','Monica','Geller','1964-05-12');
INSERT INTO patient VALUES ('444555666','Ross','Geller','1967-08-12');
INSERT INTO patient VALUES ('111222333','Rachel','Green','1962-09-17');
INSERT INTO patient VALUES ('333444555','Chandler','Geller','1970-06-11');
INSERT INTO patient VALUES ('667766777','Joey','Bing','1971-06-20');
INSERT INTO patient VALUES ('111222111','Phoebe','Bing','1959-12-24');
SELECT * FROM patient;

-- insert into the Hospital Table
SELECT * FROM hospital;
INSERT INTO hospital VALUES ('BBC','St. Joseph', 'London', 'ON', 1000, NULL, NULL);
INSERT INTO hospital VALUES ('ABC','Victoria', 'London', 'ON', 1600, NULL, NULL);
INSERT INTO hospital VALUES ('DDE','Victoria', 'Victoria', 'BC', 1200, NULL, NULL);
SELECT * FROM hospital;

-- insert into the Doctor Table
SELECT * FROM doctor;
INSERT INTO doctor VALUES ('RD34','Bernie', 'Kavorikian','1980-09-09', '1930-06-11','BBC','Urologist');
INSERT INTO doctor VALUES ('GD56','Joey', 'Shabado','1960-06-24', '1969-06-24','BBC','Podiatrist');
INSERT INTO doctor VALUES ('HT45','Ross', 'Clooney','1987-06-20', '1940-06-22','DDE','Surgeon');
INSERT INTO doctor VALUES ('YT67','Ben', 'Spock','1955-02-20', '1930-06-11','DDE','Urologist');
INSERT INTO doctor VALUES ('JK78','Mandy', 'Webster','1990-09-08', '1969-10-11','BBC','Surgeon');
INSERT INTO doctor VALUES ('SE66','Colleen', 'Aziz','1989-08-24', '1999-01-26','ABC','Surgeon');
SELECT * FROM doctor;

-- insert into the looksafter Table
SELECT * FROM looksafter;
INSERT INTO looksafter VALUES ('GD56','110112113');
INSERT INTO looksafter VALUES ('GD56','333444555');
INSERT INTO looksafter VALUES ('GD56','667766777');
INSERT INTO looksafter VALUES ('HT45','444555666');
INSERT INTO looksafter VALUES ('JK78','667766777');
INSERT INTO looksafter VALUES ('JK78','111222333');
INSERT INTO looksafter VALUES ('SE66','111222333');
INSERT INTO looksafter VALUES ('YT67','111222333');
INSERT INTO looksafter VALUES ('YT67','111222111');
SELECT * FROM looksafter;



-- now for the modifications (basically additional data)
UPDATE hospital SET headdoc='SE66', headdocstartdate='2004-05-30' WHERE hoscode='ABC';
UPDATE hospital SET headdoc='GD56', headdocstartdate='2010-12-19' WHERE hoscode='BBC';
UPDATE hospital SET headdoc='YT67', headdocstartdate='2001-06-01' WHERE hoscode='DDE';

INSERT INTO doctor VALUES ('AM14', 'Alyssa', 'Mendonsa', '2010-02-26', '1990-04-13', 'ABC', 'Neurologist');
INSERT INTO patient VALUES ('123908746','Tom','Cruise','1962-07-03');
INSERT INTO looksafter VALUES ('AM14','123908746');
INSERT INTO hospital VALUES ('TRA','The Royal Alexandra', 'Edmonton', 'AB', 1900, 'AM14', '2022-10-02');

INSERT INTO hospital VALUES ('QEH','Queen Elizabeth Hospital', 'Charlottetown', 'PE', 1000, NULL, NULL);
INSERT INTO hospital VALUES ('ERH','Edmundston Regional Hospital', 'Edmundston', 'NB', 500, NULL, NULL);
INSERT INTO hospital VALUES ('ASS','All Saints Springhill Hospital', 'Springhill', 'NS', 1200, NULL, NULL);
INSERT INTO hospital VALUES ('LMH','Lorne Memorial Hospital', 'Swan Lake', 'MB', 1400, NULL, NULL);

INSERT INTO doctor VALUES ('AJ13', 'Anuv', 'Jain', '2015-02-26', '1995-03-11', 'QEH', 'Psychologist');
INSERT INTO doctor VALUES ('KC47', 'Kim', 'Campbell', '1990-02-23', '1947-03-10', 'ERH', 'Surgeon');
INSERT INTO doctor VALUES ('JA80', 'Jacinda', 'Ardern', '2008-11-08', '1980-06-26', 'ASS', 'Optometrist');
INSERT INTO doctor VALUES ('AM89', 'Alex', 'Morgan', '2011-07-13', '1989-07-02', 'LMH', 'Geriatrician');
INSERT INTO doctor VALUES ('EP90', 'Ellyse', 'Perry', '2012-10-05', '1990-11-03', 'TRA', 'Physiotherapist');

INSERT INTO patient VALUES ('987601230', 'Elon', 'Musk', '1971-06-28');
INSERT INTO patient VALUES ('782164982', 'Angela', 'Merkel', '1954-07-17');
INSERT INTO patient VALUES ('187865182', 'Jimmy', 'Carter', '1924-10-01');
INSERT INTO patient VALUES ('382164982', 'Winifer', 'Fernandez', '1995-01-06');
INSERT INTO patient VALUES ('992164982', 'Emma', 'Raducanu', '2002-11-13');


INSERT INTO looksafter VALUES ('AJ13', '987601230');
INSERT INTO looksafter VALUES ('AM89', '187865182');
INSERT INTO looksafter VALUES ('JA80', '187865182');
INSERT INTO looksafter VALUES ('KC47', '782164982');
INSERT INTO looksafter VALUES ('EP90', '382164982');
INSERT INTO looksafter VALUES ('EP90', '992164982');


UPDATE hospital SET headdoc='AJ13', headdocstartdate='2019-05-30' WHERE hoscode='QEH';
UPDATE hospital SET headdoc='KC47', headdocstartdate='1993-06-13' WHERE hoscode='ERH';
UPDATE hospital SET headdoc='JA80', headdocstartdate='2017-10-26' WHERE hoscode='ASS';
UPDATE hospital SET headdoc='AM89', headdocstartdate='2016-02-11' WHERE hoscode='LMH';