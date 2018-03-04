<?php
$directory = POSTS_DIR . '/';
if (glob($directory . '*.md') != FALSE)
{
    $file_count = count(glob($directory . '*.md'));
    $files = array_reverse(glob($directory . '*.md'));
    echo '<ul>';
    foreach ($files as $file)
    {
        echo '<li><a href="posts' . $post->path_to_post($file) . '">' . $post->format_blog_title($file) . '</a></li>';
    }
    echo '</ul>';
}
?>
