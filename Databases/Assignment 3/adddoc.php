<!DOCTYPE html>
<html>
<head>
    <title>Add a Doctor</title>
    <!-- adds a new doc to the db -->
</head>
<body>
    <p><a href="index.html">Home</a></p>
    <?php
        include "connecttodb.php";
    ?>
    <h1>Add a New Doctor</h1>
    <!-- get the data for new doc; ensure non-null input and correct format (i.e. number/date etc) -->
    <form action="" method="post">

        First Name: <input type="text" name="first" maxlength="20" required 
            oninvalid="this.setCustomValidity('First name cannot be empty')"
            oninput="this.setCustomValidity('')"/> <br/>
            
        Last Name: <input type="text" name="last" maxlength="20" required 
            oninvalid="this.setCustomValidity('Last name cannot be empty')"
            oninput="this.setCustomValidity('')"/> <br/>

        Birthdate: <input type="date" name="bdate" required 
            oninvalid="this.setCustomValidity('Must enter the birthdate')"
            oninput="this.setCustomValidity('')"/> <br/>

        Specialization: <input type="text" name="specialization"/> <br/>
        
        License Number: <input type="text" name="license" minlength="4" maxlength="4" required 
            oninvalid="this.setCustomValidity('Enter 4 character license number')"
            oninput="this.setCustomValidity('')" placeholder="XXXX"/> <br/>

        License date: <input type="date" name="ldate" required 
            oninvalid="this.setCustomValidity('Must enter license date')"
            oninput="this.setCustomValidity('')"> <br/>

        Hospital: <select name="hospital">
            <!-- get list of selectable hospitals from the php file -->
            <?php include "getHospitalList.php" ?>
        </select>
        <br/><br/>
        <input type="submit" value="Add New Doctor"/>

    </form>

    <!-- once the user submits, try and add the new doc -->
    <?php
        if (isset($_POST["first"])) {
            include "addDocToDB.php";
        }
    ?>
    <!-- close the db connection -->
    <?php mysqli_close($connection) ?>
</body>
</html>