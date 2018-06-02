<?php

$lat = htmlspecialchars($_GET['lat']); 
$lon = htmlspecialchars($_GET['lon']); 
$key = 'key=AIzaSyB_QwA_ogbw1uvOOazfbE0JqI_aoRpWQD0';
$center = "&" . "q=" . $lat . ',' . $lon;
$zoom  = "&zoom=16";
    
?>

<?php

$servername = "localhost";
$username = "webApp";
$password = "password";
$dbname = "tracking";

// Create connection
$conn = new mysqli($servername, $username, $password,$dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
echo "Connected successfully";
    
$sql = "INSERT INTO ben (lat, lon) VALUES ($lat,$lon)";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}


?>

<?php