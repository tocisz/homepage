<?php
$directory = POSTS_DIR . '/';
echo "<p>";
if (glob($directory . '*.md') != FALSE)
{
    $file_count = count(glob($directory . '*.md'));
    $files = array_reverse(glob($directory . '*.md'));
    echo '<ul>';
    foreach ($files as $file)
    {
        echo '<li><a href="' . $path_prefix . $post->path_to_post($file) . '">' . $post->format_blog_title($file) . '</a></li>';
    }
    echo '</ul>';
}
echo "</p>";
?>
