<?php
// simply gets a list of all patients (ohip, fname, lname) of a doc as rows of a table

$lic = $_POST["doctor"];
$query = "SELECT * FROM vPatientsOfDoc WHERE licensenum='$lic';";
$result = mysqli_query($connection, $query);

if (!$result) {
    die ("Databases query failed.");
}
while ($row = mysqli_fetch_assoc($result)) {
    $ohip = $row["ohipnum"];
    $first = $row["firstname"];
    $last = $row["lastname"];
    echo "<tr>";
        echo "<td>$ohip</td>";
        echo "<td>$first</td>";
        echo "<td>$last</td>";
    echo "</tr>";
}
mysqli_free_result($result);
?>