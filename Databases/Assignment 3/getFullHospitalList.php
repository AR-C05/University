<?php
// gets all information for hospital specified in POST message; head doc's first and last name is retrieved and displayed

$hoscode = $_POST["hospital"];
$query = "SELECT hosname, city, prov, numofbed, headdoc FROM hospital WHERE hoscode='$hoscode'";
$result = mysqli_query($connection, $query);

if (!$result) {
    echo "<script>alert('Unable to retrieve information on hospital with code: $hoscode')</script>";
}
while ($row = mysqli_fetch_assoc($result)) {
    $name = $row["hosname"];
    $city = $row["city"];
    $prov = $row["prov"];
    $beds = $row["numofbed"];
    $head = $row["headdoc"];
    echo "<tr>";
        echo "<td>$name</td>";
        echo "<td>$city</td>";
        echo "<td>$prov</td>";
        echo "<td>$beds</td>";
    $qHead = "SELECT firstname, lastname FROM doctor WHERE licensenum='$head'";
    $rHead = mysqli_query($connection, $qHead);
    if (!$rHead) {
        echo "<script>alert('Unable to retrieve information on head doctor with license: $head')</script>";
    }
    while ($rowH = mysqli_fetch_assoc($rHead)) {
        $f = $rowH["firstname"];
        $l = $rowH["lastname"];
        echo "<td>$f $l</td>";
    }
    echo "</tr>";
}
mysqli_free_result($result);
?>