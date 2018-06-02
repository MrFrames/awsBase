<?php

// db connection perameters:
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
echo "Connected successfully to database";

// Selects last item from table 'ben':
$sql_get_id = "SELECT * FROM ben ORDER BY id DESC LIMIT 1";
$result = $conn->query($sql_get_id);

// Iterates across result (likely a better way to do this):
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        //echo "id: " . $row["id"]. " - lon,lat: " . $row["lon"]. "," . $row["lat"];
        $lat = $row['lat']; 
        $lon = $row['lon'];
    }
} else {
    echo "0 results";
}

$conn->close();

// Defines perameters for map:

$key = 'key=AIzaSyB_QwA_ogbw1uvOOazfbE0JqI_aoRpWQD0';
$center = "&" . "q=" . $lat . ',' . $lon;
$zoom  = "&zoom=16";

?>

<!DOCTYPE html>

<head> 
    <link href="{% static '../static/style.css'%}" type="text/css" rel="stylesheet">
</head>

<body>
    <div class="heading">
        <h1>where is ben?</h1>
    </div>
    
    <div class="map">
        <iframe
                width="600"
                height="450"
                frameborder="0" style="border:0"
                src="https://www.google.com/maps/embed/v1/place?<?php echo "$key$center$zoom" ?>" allowfullscreen>
        </iframe>
    </div>
</body>