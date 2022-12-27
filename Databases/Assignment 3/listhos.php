<!DOCTYPE html>
<html>
<head>
    <title>Hospital Information</title>
    <link rel="stylesheet" type="text/css" href="./styles.css">
    <!-- list hospital information for selected hospital -->
</head>
<body>
    <p><a href="index.html">Home</a></p>
    <?php
        include "connecttodb.php";
    ?>
    <!-- get hospital selection -->
    <h1>Hospitals</h1>
    <form action="" method="post">
        Hospital: <select name="hospital">
            <?php include "getHospitalList.php" ?>
        </select>
        <br/><br/>
        <input type="submit" value="Get Hospital Information"/>
    </form>

    <!-- once hospital is selected, display its information, and all docs that work there -->
    <?php 
        if (isset($_POST["hospital"])) {
            echo "<hr/>";
            echo "<hr/>";
            echo "<h2>Hospital</h2>";
            echo "<table>";
            echo "<tr>";
                echo "<th>Hospital</th>";
                echo "<th>City</th>";
                echo "<th>Province</th>";
                echo "<th># Beds</th>";
                echo "<th>Head Doctor</th>";
            echo "</tr>";
            include "getFullHospitalList.php";
            echo "</table>";

            echo "<hr/>";
            echo "<hr/>";
            echo "<h3>Doctors Working Here</h3>";
            echo "<table>";
            echo "<tr>";
                echo "<th>First Name</th>";
                echo "<th>Last Name</th>";
            echo "</tr>";
            include "getDocNamesList.php";
            echo "</table>";
        } 
    ?>
    <!-- disconnect from db -->
    <?php mysqli_close($connection) ?>
</body>
</html>