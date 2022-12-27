<?php
// getHospitalList.php modified for doctor
// simply gets a list of all doctors (license, name) as a dropdown menu

$query = "SELECT * FROM doctor;";
$result = mysqli_query($connection, $query);
if (!$result) {
    die ("Databases query failed.");
}
while ($row = mysqli_fetch_assoc($result)) {
    $lic = $row["licensenum"];
    $first = $row["firstname"];
    $last = $row["lastname"];
    echo "<option value='$lic'> $lic: $first $last</option>";
}
mysqli_free_result($result);
?>