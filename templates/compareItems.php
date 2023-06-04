<?php
include '../backend/config.php';

$query = $_POST['query'];


// Consulta en la tabla productsHSN
$hsnQuery = $conn->prepare("SELECT * FROM productsHSN WHERE name LIKE ?");
$hsnQuery->execute(["%$query%"]);

// Consulta en la tabla productsMyProtein
$myProteinQuery = $conn->prepare("SELECT * FROM productsMyProtein WHERE name LIKE ?");
$myProteinQuery->execute(["%$query%"]);

// Consulta en la tabla productsMyProtein
$AmazonQuery = $conn->prepare("SELECT * FROM productsAmazon WHERE name LIKE ?");
$AmazonQuery->execute(["%$query%"]);

// Comparación y determinación de los mejores productos
$productsHSN = array();
$productsMP = array();
$productsAmazon = array();
$products = array();

while ($row = $hsnQuery->fetch()) {
    $productsHSN[] = $row;
    $products[] = $row;
}

while ($row = $myProteinQuery->fetch()) {
    $productsMP[] = $row;
    $products[] = $row;
}

while ($row = $AmazonQuery->fetch()) {
    $productsAmazon[] = $row;
    $products[] = $row;
}

sortProducts($productsHSN);
sortProducts($productsMP);
sortProducts($productsAmazon);
sortProducts($products);

// Mostrar los resultados en la página HTML
echo '<!DOCTYPE html>';
echo '<html>';
echo '<head>';
echo '  <meta charset="UTF-8">';
echo '  <title>FitSuppFinder - Resultados de Búsqueda</title>';
echo '  <link rel="stylesheet" type="text/css" href="../static/home_style.css">';
echo '</head>';
echo '<body>';
echo '<main>';
echo '  <h1>FitSuppFinder - Resultados de Búsqueda</h1>';

if (!empty($productsHSN) || !empty($productsMP)) {
    echo '  <table>';
    echo '    <tr>';
    echo '      <th>Origen</th>';
    echo '      <th>Marca</th>';
    echo '      <th>Nombre</th>';
    echo '      <th>Precio</th>';
    echo '      <th>Cantidad</th>';
    echo '      <th>url</th>';
    echo '    </tr>';
    if (!empty($productsHSN)) {
        //foreach ($productsHSN as $product){
        $product = $productsHSN[0];
            echo '    <tr>';
            echo '      <td>HSN</td>';
            echo '      <td>' . $product['brand'] . '</td>';
            echo '      <td>' . $product['name'] . '</td>';
            echo '      <td>' . $product['price'] . '</td>';
            echo '      <td>' . $product['quantity'] . ' ' . $product['measure'] . '</td>';
            echo '      <td><a href="'.$product['url'].'">Enlace a pantalla de compra</td>';
            echo '    </tr>';
        //}
    }else{
        echo '<p>No se encontraron resultados para HSN</p>';
    }
    if (!empty($productsMP)) {
        $product = $productsMP[0];
            echo '    <tr>';
            echo '      <td>MyProtein</td>';
            echo '      <td>' . $product['brand'] . '</td>';
            echo '      <td>' . $product['name'] . '</td>';
            echo '      <td>' . $product['price'] . '</td>';
            echo '      <td>' . $product['quantity'] . ' ' . $product['measure'] . '</td>';
            echo '      <td><a href="'.$product['url'].'">Enlace a pantalla de compra</td>';
            echo '    </tr>';
    }
    else{
        echo '<p>No se encontraron resultados para MyProtein</p>';
    }
    if (!empty($productsAmazon)) {
        $product = $productsAmazon[0];
            echo '    <tr>';
            echo '      <td>Amazon</td>';
            echo '      <td>' . $product['brand'] . '</td>';
            echo '      <td>' . $product['name'] . '</td>';
            echo '      <td>' . $product['price'] . '</td>';
            echo '      <td>' . $product['quantity'] . ' ' . $product['measure'] . '</td>';
            echo '      <td><a href="'.$product['url'].'">Enlace a pantalla de compra</td>';
            echo '    </tr>';
    }
    else{
        echo '<p>No se encontraron resultados para Amazon</p>';
    }
    //foreach ($products as $product){
    $product = $products[0];
        echo '    <tr id="best">';
        echo '      <td>Mejor de todos</td>';
        echo '      <td>' . $product['brand'] . '</td>';
        echo '      <td>' . $product['name'] . '</td>';
        echo '      <td>' . $product['price'] . '</td>';
        echo '      <td>' . $product['quantity'] . ' ' . $product['measure'] . '</td>';
        echo '      <td><a href="'.$product['url'].'">Enlace a pantalla de compra</td>';
        echo '    </tr>';
    //}
    echo '  </table>';
} else {
    echo '  <p>No se encontraron resultados.</p>';
}
echo '<a class="submit" href="../templates/index.html" >Volver al buscador</a>';
echo '</main>';
echo '</body>';
echo '</html>';

function sortProducts(&$products){
    usort($products, function ($a, $b) {
        $aQuantity = $a['quantity'] * getQuantityMultiplier($a['measure']);
        $bQuantity = $b['quantity'] * getQuantityMultiplier($b['measure']);
    
        $aRatio = $a['price'] / $aQuantity ;
        $bRatio = $b['price'] / $bQuantity;
    
        if ($aRatio == $bRatio) {
            return 0;
        }

        return ($aRatio < $bRatio) ? -1 : 1;
    });
}

function getQuantityMultiplier($measure)
{
    switch ($measure) {
        case 'g':
            return 1;
        case 'mg':
            return 0.001;
        case 'kg':
            return 1000;
        case 'oz':
            return 28.3495;
        case 'lb':
            return 453.592;
        default:
            return 1;
    }
}
?>
