<?php
// connects to the hospital data database
// code from flipped classroom 4, simply changed $dbname
$dbhost = "localhost";
$dbuser = "root";
$dbpass = "cs3319";
$dbname = "a3hospitals";

$connection = mysqli_connect($dbhost, $dbuser,$dbpass,$dbname);
if (mysqli_connect_errno()) {
    die("Database connection failed :" .
        mysqli_connect_error() . " (" . mysqli_connect_errno() . ")" );
}
?>