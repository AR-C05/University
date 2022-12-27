<?php
// gets list of doctors that work at hospital specified in POST message
$hoscode = $_POST["hospital"];
$query = "SELECT firstname, lastname FROM doctor WHERE hosworksat='$hoscode'";
$result = mysqli_query($connection, $query);

// failed query
if (!$result) {
    echo "<script>alert('Unable to retrieve information on doctors working at hospital with code: $hoscode')</script>";
}
// display all retrieved doctors' first and last names as table rows for each doc
while ($row = mysqli_fetch_assoc($result)) {
    $f = $row["firstname"];
    $l = $row["lastname"];
    echo "<tr>";
        echo "<td>$f</td>";
        echo "<td>$l</td>";
    echo "</tr>";
}
mysqli_free_result($result);
?>