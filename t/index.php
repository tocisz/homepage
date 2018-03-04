<?php
// Include global config
include_once 'config/config.php';

// Display the header files
$title = 'The blog archive';
require 'layouts/header.php';
?>
<div class="container-fluid">
<?php
echo "<h1>$title</h1>";
include_once 'index_raw.php';
?>
</div>
<?php
require 'layouts/footer.php';
?>
