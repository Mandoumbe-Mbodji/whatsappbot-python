<?php
// Vos informations de connexion à la base de données
$servername = "localhost";
$username = "dacey";
$password = "dacey";
$dbname = "assurebase";

// Créer une connexion à la base de données
$conn = new mysqli($servername, $username, $password, $dbname);

// Vérifier la connexion
if ($conn->connect_error) {
    die("La connexion à la base de données a échoué : " . $conn->connect_error);
}

// Récupérer les données du formulaire
$username = $_POST['username'];
$email = $_POST['email'];
$password = password_hash($_POST['password'], PASSWORD_DEFAULT);

// Préparer et exécuter la requête SQL
$sql = "INSERT INTO utilisateurs (username, email, password) VALUES ('$username', '$email', '$password')";

if ($conn->query($sql) === TRUE) {
    echo "Inscription réussie!";
} else {
    echo "Erreur lors de l'inscription : " . $conn->error;
}

// Fermer la connexion à la base de données
$conn->close();
?>
