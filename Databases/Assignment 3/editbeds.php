<!DOCTYPE html>
<html>
<head>
    <title>Update Beds</title>
    <link rel="stylesheet" type="text/css" href="./styles.css">
    <!-- change bed count for selected hospital to amount specified by user -->
</head>
<body>
    <p><a href="index.html">Home</a></p>
    <?php
        include "connecttodb.php";
    ?>
    <h1>Update Bed Count</h1>
    <!-- get user to select hospital and ensure a valid bed count is entered -->
    <form action="" method="post">
        <!-- get list of hospitals -->
        Hospital: <select name="hospital">
            <?php include "getHospitalList.php" ?>
        </select><br/>
        New Bed Amount: <input type="text" name="beds" required pattern="[0-9]{1,6}" maxlength="6"
                oninvalid="this.setCustomValidity('Enter updated bed number')"
                oninput="this.setCustomValidity('')" placeholder="500"/> <br/>
        <br/>
        <input type="submit" value="Update"/>
    </form>
    <!-- try and update bed cound to specified amount for selected hospital -->
    <!-- inform user of success/failure -->
    <?php 
        if (isset($_POST["beds"])) {
            $beds = $_POST["beds"];
            $hospital = $_POST["hospital"];
            $query = "UPDATE hospital SET numofbed='$beds' WHERE hoscode='$hospital'";
            if (!mysqli_query($connection,$query) || mysqli_affected_rows($connection) == 0) {
                echo "<script>alert('Unable to update number of beds for hospital with code: $hospital')</script>";
            } else {
                echo "<script>alert('Number of beds updated')</script>";
            }
        }
    ?>
    <!-- disconnect from db -->
    <?php mysqli_close($connection) ?>
</body>
</html>