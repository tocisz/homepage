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
$directory = POSTS_DIR . '/';

// Ensure the directory isn't empty
if (glob($directory . '*.md') != FALSE)
{
    $file_count = count(glob($directory . '*.md'));
    $files = glob($directory . '*.md', GLOB_NOSORT);
    array_multisort(array_map('filemtime', $files), SORT_NUMERIC, SORT_DESC, $files);
    echo '<ul>';
    foreach ($files as $file)
    {
        echo '<li><a href="posts' . $post->path_to_post($file) . '">' . $post->format_blog_title($file) . '</a></li>';
    }
    echo '</ul>';
}
?>
</div>
<?php
require 'layouts/footer.php';
?>
