<?php
// getmuseum.php from flip4 adapted for hospital
// simply gets a list of all hospitals as a dropdown menu

$query = "SELECT * FROM hospital;";
$result = mysqli_query($connection, $query);
if (!$result) {
    die ("Databases query failed.");
}
while ($row = mysqli_fetch_assoc($result)) {
    echo "<option value='" . $row["hoscode"] . "'>" . $row["hoscode"] . ": " . $row["hosname"] . "</option>";
}
mysqli_free_result($result);
?>