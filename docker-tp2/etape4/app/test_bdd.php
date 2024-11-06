<?php
$servername = "data"; // Nom du service dans docker-compose
$username = "user";
$password = "userpassword";
$dbname = "mydb";

// Création de la connexion
$conn = new mysqli($servername, $username, $password, $dbname);

// Vérification de la connexion
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Création de la table si elle n'existe pas
$sql_create_table = "CREATE TABLE IF NOT EXISTS test_table (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
)";
$conn->query($sql_create_table);

// Vérification si la table est vide et insertion d'une donnée si c'est le cas
$sql_check_empty = "SELECT COUNT(*) as count FROM test_table";
$result_check = $conn->query($sql_check_empty);
$row_check = $result_check->fetch_assoc();

if ($row_check['count'] == 0) {
    $sql_insert = "INSERT INTO test_table (name) VALUES ('test')";
    $conn->query($sql_insert);
}

// Lecture (SELECT)
$sql_select = "SELECT * FROM test_table";
$result = $conn->query($sql_select);

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"]. " - Name: " . $row["name"]. "<br>";
    }
} else {
    echo "0 results";
}

$conn->close();
?>
