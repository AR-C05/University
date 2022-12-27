<!DOCTYPE html>
<html>
<head>
    <title>Hospital Information</title>
    <link rel="stylesheet" type="text/css" href="./styles.css">
    <!-- remove doc (if possible) with specified license number -->
</head>
<body>
    <p><a href="index.html">Home</a></p>
    <?php
        include "connecttodb.php";
    ?>
    <!-- get a valid license num; confirm if they want to delete -->
    <h1>Remove a  Doctor</h1>
    <form action="" method="post" onsubmit="return confirm('Are you sure about deleting this doctor?');">
        <p>To remove a doctor, enter their license number</p>
        <input type="text" name="licensenum" id="licensenum" minlength="4" maxlength="4" required 
            oninvalid="this.setCustomValidity('Enter 4 character license number')"
            oninput="this.setCustomValidity('')" placeholder="XXXX"/>
        <br/><br/>
        <input type="submit" class="delBtn" value="Remove Doctor"/>
    </form>
    <!-- attempt deletion once user confirms intention; inform of success/failure -->
    <?php 
        if (isset($_POST["licensenum"])) {
            $license = $_POST["licensenum"];
            $query = "DELETE FROM doctor WHERE licensenum='$license';";
            if (!mysqli_query($connection,$query) || mysqli_affected_rows($connection) == 0) {
                echo "<script>alert('A doctor with license number: $license could not be deleted. Either it is an invalid license number, the doctor is treating some patient(s), or the doctor is head of a hospital')</script>";
            } else {
                echo "<script>alert('The doctor with license $license has been deleted')</script>";
            }
        }
    ?>
    <!-- disconnect from db -->
    <?php mysqli_close($connection) ?>
</body>
</html>