<!DOCTYPE html>
<html>
<head>
    <title>Assign a Doctor</title>
    <!-- assigns doc to patient (i.e. creates a looksafter relation) -->
</head>
<body>
    <p><a href="index.html">Home</a></p>
    <?php
        include "connecttodb.php";
    ?>
    <h1>Assign a doctor to a patient</h1>
    <!-- get license and ohip nums; ensure correct format and non-null -->
    <form action="" method="post">
        <p>Enter Doctor's License Number and Patient's OHIP number to assign the doctor to a patient</p>

        License Number: <input type="text" name="license" minlength="4" maxlength="4" required 
                oninvalid="this.setCustomValidity('Enter 4 character license number')"
                oninput="this.setCustomValidity('')" placeholder="XXXX"/> <br/>

        OHIP Number: <input type="text" name="ohip" required pattern="[0-9]{9}" maxlength="9"
                oninvalid="this.setCustomValidity('Enter 9 digit OHIP number')"
                oninput="this.setCustomValidity('')" placeholder="000000000"/> <br/>
        <br/>
        <input type="submit" value="Assign Doc">
    </form>

    <!-- once user submits, create and insert the relation, alert user if unsuccessful -->
    <?php
        if (isset($_POST["ohip"])) {
            $license = $_POST["license"];
            $ohip = $_POST["ohip"];
            $query = "INSERT INTO looksafter VALUES ('$license', '$ohip')";
            if (!mysqli_query($connection,$query) || mysqli_affected_rows($connection) == 0) {
                echo "<script>
                        alert('Doctor $license could not be assigned to patient $ohip.\\nEnsure valid License and OHIP numbers. \\nEnsure that the assignment does not already exist.')
                    </script>";
            }
        }
    ?>
    <!-- disconnect from db -->
    <?php mysqli_close($connection) ?>
</body>
</html>