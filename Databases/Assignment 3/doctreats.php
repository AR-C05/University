<!DOCTYPE html>
<html>
<head>
    <title>Doctors and Patients</title>
    <link rel="stylesheet" type="text/css" href="./styles.css">
    <!-- lists all patients for selected doctor -->
</head>
<body>
    <p><a href="index.html">Home</a></p>
    <?php
        include "connecttodb.php";
    ?>
    <h1>Doctors and their Patients</h1>
    <!-- get user to select a doc -->
    <form action="" method="post">
        Doctor: <select name="doctor">
            <!-- get list of docs -->
            <?php include "getDoctorList.php" ?>
        </select>
        <br/><br/>
        <input type="submit" value="Get Patients">
        <br/>
    </form>
    <!-- display patient info once doc is selected -->
    <?php 
        if (isset($_POST["doctor"])) {
            echo "<table>";
            echo "<tr>";
                echo "<th>OHIP Number</th>";
                echo "<th>First Name</th>";
                echo "<th>Last Name</th>";
            echo "</tr>";
            include "getPatientsOfDoc.php";
            echo "</table>";
        }
    ?>
    <!-- close db connection -->
    <?php mysqli_close($connection) ?>
</body>
</html>