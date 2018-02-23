<?php
switch ($_SERVER['SERVER_NAME']) {
case 'tomasz-cichocki.pl':
case 'tomaszcichocki.online':
	header("Location: /t");
	break;
case 'klepadlo.pl':
	header("Location: /k");
	break;
case 'grievous.pl':
	header("Location: /g");
	break;
case 'c3po.pl':
	header("Location: /c");
	break;
case 'dooku.pl':
	header("Location: /d");
	break;
case 'zamiana.online':
	header("Location: /z");
	break;
}
die();
?>
