<?php

// Include the class and simple configuration file
include_once 'config/config.php';

require 'vendor/autoload.php';
use Michelf\MarkdownExtra;

$requested_post = htmlspecialchars(trim(stripslashes($_GET['name'])));
$posts_url = POSTS_DIR . DIRECTORY_SEPARATOR . $requested_post . '.md';

if (file_exists($posts_url) && preg_match('/[^a-z_\-0-9]/i', $posts_url))
{
    // Split the file into slugs and the post
    $file_pieces = $post->split_file(file_get_contents($posts_url));
    $post_data = $file_pieces[1];
    $post_content = $file_pieces[2];

    $metadata = $post->slugify($post_data);

    // Parse it!
    $output = MarkdownExtra::defaultTransform($post_content);

    // Make it pretty
    $title = $post->format_blog_title($requested_post);
    require 'layouts/header.php';
?>
<div class="container-fluid">
  <div class="row">
    <div class="col-12 col-md-3 push-md-9 bd-sidebar">
      <?php include_once 'index_raw.php'; ?>
    </div>
    <div class="col-12 col-md-9 pull-md-3 bd-content">
      <?php echo $output; ?>
    </div>
  </div>
</div>
<?php
    require 'layouts/footer.php';
}
else
{
    header('Location: /t/404');
}
