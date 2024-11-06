<?php
$servername = "data";
$username = "root";
$password = "rootpassword";
$dbname = "testdb";

try {
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $conn->exec("CREATE TABLE IF NOT EXISTS visitors (id INT AUTO_INCREMENT PRIMARY KEY, visit_time TIMESTAMP)");
    $conn->exec("INSERT INTO visitors (visit_time) VALUES (NOW())");

    $stmt = $conn->prepare("SELECT * FROM visitors ORDER BY visit_time DESC LIMIT 5");
    $stmt->execute();

    $results = $stmt->fetchAll();
    echo "<h1>Dernières visites :</h1>";
    foreach ($results as $row) {
        echo "Visite ID: " . $row['id'] . " - Temps de visite: " . $row['visit_time'] . "<br>";
    }

} catch(PDOException $e) {
    echo "Erreur: " . $e->getMessage();
}

$conn = null;
?>
