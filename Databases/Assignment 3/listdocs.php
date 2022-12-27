<!DOCTYPE html>
<html>
<head>
    <title>Doctor Information</title>
    <link rel="stylesheet" type="text/css" href="./styles.css">
    <!-- lists all docs; filtered and sorted as specified -->
</head>
<body>
    <p><a href="index.html">Home</a></p>
    <?php
        include "connecttodb.php";
    ?>
    <h1>Doctors</h1>
    <!-- get user's filtering/sorting preferences -->
    <form action="" method="post">
        <table>
            <tr>
                <th>Filter By:</th>
                <th><p class="radioTitle">Sort By&nbsp</p>(optional):</th>
                <th><p class="radioTitle">Order By&nbsp</p>(optional): <br></th>
            </tr>
            <tr>
                <td>
                    <!-- get list of specialities -->
                    <select name="speciality">
                        <option value="None">None</option>
                        <?php include "getSpecialtyList.php"; ?>
                    </select>
                </td>
                <td>
                    <input type="radio" name="sortBy" value="lastname">Last Name <br>
                    <input type="radio" name="sortBy" value="birthdate">Birthdate <br>
                </td>
                <td>
                    <input type="radio" name="order" value="ASC">Ascending <br>
                    <input type="radio" name="order" value="DESC">Descending <br>
                </td>
            </tr>
        </table>
        <br><br>
        <input type="submit" value="Show Doctors">
    </form>
    <table>
        <tr>
            <th>Licence</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>License Date</th>
            <th>Birthdate</th>
            <th>Works At</th>
            <th>Speciality</th>
        </tr>
        <!-- display list of docs after applying user's preferences -->
        <?php
            include "getFullDocList.php";
        ?>
    </table>
    <?php mysqli_close($connection) ?>
</body>
</html>