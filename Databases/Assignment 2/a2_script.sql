-- Script2 for Databases A2

USE assign2db;

-- Part 1 SQL Updates
-- all data in the hospital table before modification
SELECT * FROM hospital;
-- Dr. Shabado head of St. Joseph (December 19, 2010)
UPDATE hospital SET headdoc='SE66', headdocstartdate='2004-05-30' WHERE hoscode='ABC';
-- Dr. Spock head of Victoria in Victoria (June 1, 2001)
UPDATE hospital SET headdoc='GD56', headdocstartdate='2010-12-19' WHERE hoscode='BBC';
-- Dr. Aziz head of Victoria in London (May 30, 2004)
UPDATE hospital SET headdoc='YT67', headdocstartdate='2001-06-01' WHERE hoscode='DDE';
-- hospital table after modification
SELECT * FROM hospital;


-- Part 2 SQL Inserts
-- Insert a doctor of your choice who works at Victoria Hospital in London Ontario
INSERT INTO doctor VALUES ('AM14', 'Alyssa', 'Mendonsa', '2010-02-26', '1990-04-13', 'ABC', 'Neurologist');
-- Insert a patient whose name is your favourite actor or actress.  
INSERT INTO patient VALUES ('123908746','Tom','Cruise','1962-07-03');
-- Insert the data that will show that your new doctor treats your new patient
INSERT INTO looksafter VALUES ('AM14','123908746');
-- Insert a new hospital somewhere in Canada and have your new doctor be the head of your new hospital and they started sometime this month.
INSERT INTO hospital VALUES ('TRA','The Royal Alexandra', 'Edmonton', 'AB', 1900, 'AM14', '2022-10-02');
-- Write 4 statements that show all the data in the 4 tables to prove that your new rows were added.
SELECT * FROM doctor;
SELECT * FROM patient;
SELECT * FROM looksafter;
SELECT * FROM hospital;


-- Part 3 SQL Queries
-- Query 01 - Show the last names of all the patients
SELECT lastname FROM patient;

-- Query 02 - Show the last names of all the patients with no repeats
SELECT DISTINCT lastname FROM patient;

-- Query 03 - Show all the data in the Doctor table, in order of their last names
SELECT * FROM doctor ORDER BY lastname;

-- Query 04 - Show the name and id of all hospitals that have over 1500 beds
SELECT hosname, hoscode FROM hospital WHERE numofbed > 1500;

-- Query 05 - List the first name and last name of all the doctors who work at St. Joseph Hospital (look up by name)
SELECT firstname, lastname FROM doctor, hospital WHERE hosworksat=hoscode AND hosname="St. Joseph";

-- Query 06 - List the first name and last name of all patients whose last name begins with a "G"
SELECT firstname, lastname FROM patient WHERE lastname LIKE 'G%';

-- Query 07 - List the first name and last name of all patients who are treated by a doctor with the last name of Webster (look up by name)
SELECT p.firstname, p.lastname FROM patient p, looksafter l, doctor d WHERE d.lastname='Webster' AND l.licensenum=d.licensenum AND p.ohipnum=l.ohipnum;

-- Query 08 - List the hospital name, city and the last name of the head doctor of all the hospitals.
SELECT hosname, city, lastname FROM doctor, hospital WHERE headdoc=licensenum;

-- Query 09 - Find the total number of beds for all the hospitals
SELECT SUM(numofbed) FROM hospital;

-- Query 10 - List the first names and last name of the patient and the first name and last name of the doctor for all patients treated by a head doctor
SELECT p.firstname, p.lastname, d.firstname, d.lastname FROM patient p, doctor d, hospital h, looksafter l
    WHERE l.ohipnum=p.ohipnum AND l.licensenum=d.licensenum AND d.licensenum=h.headdoc;

-- Query 11 - Find all the surgeons (last name and first name) who work at a hospital called Victoria. Also list the hospital's province for each surgeon.
SELECT lastname, firstname, prov FROM doctor, hospital WHERE hosworksat=hoscode AND hosname='Victoria';

-- Query 12 - Find the first name of all doctors who don't treat anyone.
SELECT DISTINCT firstname FROM doctor, looksafter WHERE doctor.licensenum NOT IN (SELECT licensenum FROM looksafter);

-- Query 13 - Find all doctors (last name, first name, number of patients they treat, name of the hospital they work at) who treat MORE than one patient
SELECT firstname, lastname, COUNT(l.licensenum), hosname  FROM doctor, looksafter l, hospital h WHERE l.licensenum=doctor.licensenum AND hosworksat=hoscode
    GROUP BY l.licensenum HAVING COUNT(l.licensenum) > 1;

-- Query 14 - Find any doctor (first name and last name) who are the head of a hospital but work at a different hospital. 
--            Include both hospital names as well
--            write the query so that the titles of the columns are "Doctor First Name"  "Doctor Last Name" "Head of Hospital Name" "Works at Hospital Name" 
SELECT d.firstname AS "Doctor First Name", d.lastname AS "Doctor Last Name", h1.hosname AS "Head of Hospital Name", h2.hosname AS "Works at Hospital Name"
    FROM doctor d, hospital h1, hospital h2 WHERE d.licensenum=h1.headdoc AND d.hosworksat=h2.hoscode AND h1.hoscode<>h2.hoscode;

-- Query 15 - My Query - For all hospitals (name) in london, find all patients (last name, first name) for all doctors (lastname, firstname, licensenum)
--            Sort by hospital name, then by doc's lname, doc's fname, patient's lname (in that order of importance)
--            (i.e. if same hospital name, sort by doc last name; if that is same then sort by doc fname; if same doc, sort by patient lname)
SELECT h.hosname AS "Hospital Name", d.lastname AS "Doctor Last Name", d.firstname AS "Doctor First Name", p.firstname AS "Patient First Name", p.lastname AS "Patient Last Name"
    FROM doctor d, hospital h, patient p, looksafter l WHERE d.licensenum=l.licensenum AND p.ohipnum=l.ohipnum AND d.hosworksat=h.hoscode AND h.city="London"
    ORDER BY h.hosname, d.lastname, d.firstname, p.lastname;


-- Part 4 SQL Views/Deletes
-- Create a view that lists the first and last name and the birthday of each doctor and the first and last name and the birthday of each patients they are treating
--      NOTE: It will make the step below easier if you rename the columns to something like dfirst, dlast, dbirth, pfirst, plast, pbirth
CREATE VIEW docs_and_patients AS 
    SELECT d.firstname AS "dfirst", d.lastname AS "dlast", d.birthdate AS "dbirth", p.firstname AS "pfirst", p.lastname AS "plast", p.birthdate AS "pbirth"
    FROM doctor d, patient p, looksafter l WHERE d.licensenum=l.licensenum AND p.ohipnum=l.ohipnum;

-- Prove that it works by selecting all the rows from it
SELECT * FROM docs_and_patients;

-- Write a query to display the data just using your view, only show the last name and birthday of  the doctors and the last name and birthday of the patients
--    where the doctor is younger than the patient.
SELECT dlast, dbirth, plast, pbirth FROM docs_and_patients WHERE dbirth > pbirth;

-- Write a query to show all the patient information. 
SELECT * FROM patient;

-- Write a query to show all the looksafter information. 
SELECT * FROM looksafter;

-- Delete the patient you created by referencing the patient's first name and last name in the WHERE clause.
DELETE FROM patient WHERE firstname="Tom" AND lastname="Cruise";

-- Prove that the patient was deleted.
SELECT * FROM patient;

-- Prove that the patient was also deleted from the looksafter information. 
SELECT * FROM looksafter;

-- Show all the information from the doctor table.
SELECT * FROM doctor;

-- Delete the doctor with the firstname of Bernie
DELETE FROM doctor WHERE firstname="Bernie";

-- Prove that that doctor was deleted.
SELECT * FROM doctor;

-- Try to delete the doctor you created using their first and last name. It shouldn't delete,
--   put a comment at the very end of your script file right after this command to explain clearly why your new doctor cannot be deleted.
DELETE FROM doctor WHERE firstname="Alyssa" AND lastname="Mendonsa";
-- There is an existing reference to the doctor in the hospital table as the `headdoc` foreign key of the newly inserted hospital
--      Since no option was given for ON DELETE when creating the "doctor" table, mysql defaults to ON DELETE RESTRICT.
--      That is, it prevents the deletion and no action is taken


