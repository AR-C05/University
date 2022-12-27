<?php
// modified 'addthework.php' from flipped4
// get the data to insert from POST and attempt insert to db

$license = $_POST["license"];
$fname = $_POST["first"];
$lname = $_POST["last"];
$licdate = $_POST["ldate"];
$bdate = $_POST["bdate"];
$hos = $_POST["hospital"];
$spec = $_POST["specialization"];

$query = 'INSERT INTO doctor (licensenum, firstname, lastname, licensedate, birthdate, hosworksat, speciality)
          VALUES ("' . $license . '", "' . $fname . '", "' . $lname . '", "' . $licdate . '", "' . $bdate . '", "' . $hos . '", "' . $spec . '");';

// inform if insert failed or succeeded
if (!mysqli_query($connection,$query) || mysqli_affected_rows($connection) == 0) {
    echo "<script>alert('A doctor with that license number already exists!')</script>";
} else {
    echo "<script>alert('Doctor added')</script>";
}
?>