<?php
$host = 'data_container';
$db = 'testdb';
$user = 'testuser';
$pass = 'testpass';

$conn = new PDO("mysql:host=$host;dbname=$db", $user, $pass);

// Exemple d'opération de lecture
$query = $conn->query("SELECT * FROM example_table LIMIT 1");
$row = $query->fetch(PDO::FETCH_ASSOC);

if ($row) {
    echo "Données lues : " . $row['data_column'];
} else {
    echo "Aucune donnée trouvée.";
}

// Exemple d'opération d'écriture
$conn->exec("INSERT INTO example_table (data_column) VALUES ('Donnée de test')");

$conn = null;
?>

