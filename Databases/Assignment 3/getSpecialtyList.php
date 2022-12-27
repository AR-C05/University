<?php
// getmuseum.php from flip4 adapted for hospital
// simply gets a list of all specialities as a dropdown menu

$query = "SELECT DISTINCT speciality FROM doctor;";
$result = mysqli_query($connection, $query);
if (!result) {
    die ("Databases query failed.");
}
while ($row = mysqli_fetch_assoc($result)) {
    echo "<option value='" . $row["speciality"] . "'>" . $row["speciality"] . "</option>";
}
mysqli_free_result($result);
?>