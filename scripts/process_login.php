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
$password = $_POST['password'];

// Préparer et exécuter la requête SQL
$sql = "SELECT * FROM utilisateurs WHERE username='$username'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Utilisateur trouvé, vérifier le mot de passe
    $row = $result->fetch_assoc();
    if (password_verify($password, $row['password'])) {
        echo "Connexion réussie!";
    } else {
        echo "Mot de passe incorrect!";
    }
} else {
    echo "Utilisateur non trouvé!";
}

// Fermer la connexion à la base de données
$conn->close();
?>
