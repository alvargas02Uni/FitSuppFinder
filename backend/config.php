<?php
    $hostname = 'rafadgvc.mysql.database.azure.com';  
    $dbname = 'FitSuppFinder';  
    $admin_username = 'rafadgvc';  
    $admin_password = 'FitSuppFinder1';  

    $conn =new PDO("mysql:host=$hostname;dbname=$dbname", $admin_username, $admin_password);

    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if ($conn->connect_error) { 
        die("Conexión fallida: " . $conn->connect_error);
    }
?>