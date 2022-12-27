<?php
// getmuseum.php from flip4 adapted for hospital
// simply gets a list of all doctors (all information) as rows of a table

if (isset($_POST["sortBy"])) {
    $sort = $_POST["sortBy"];
} else {
    $sort = "licensenum";
}
if (isset($_POST["order"])) {
    $order = $_POST["order"];
} else {
    $order = "ASC";
}

if (isset($_POST["speciality"])) {
    if ($_POST["speciality"] == "None") {
        $query = "SELECT * FROM doctor ORDER BY $sort $order;";
        $result = mysqli_query($connection, $query);
    } else {
        $filter = $_POST["speciality"];
        $query = "SELECT * FROM doctor WHERE speciality='$filter' ORDER BY $sort $order;";
        $result = mysqli_query($connection, $query);
    }    
} else {
    $query = "SELECT * FROM doctor ORDER BY $sort $order";
    $result = mysqli_query($connection, $query);
}

if (!$result) {
    die ("Databases query failed.");
}
while ($row = mysqli_fetch_assoc($result)) {
    echo "<tr> <td>" . $row["licensenum"] . "</td>"
         . "<td>" . $row["firstname"] . "</td>"
         . "<td>" . $row["lastname"] . "</td>"
         . "<td>" . $row["licensedate"] . "</td>"
         . "<td>" . $row["birthdate"] . "</td>"
         . "<td>" . $row["hosworksat"] . "</td>"
         . "<td>" . $row["speciality"] . "</td> </tr>";
}
mysqli_free_result($result);
?>