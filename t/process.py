import os
import shutil
from pathlib import Path
import re
import codecs
import markdown

INPUT = "posts_source"
OUTPUT = "posts"
HEAD = "layouts/header.php"
FOOT = "layouts/footer.php"

def title_from_path(input):
    return re.sub(r'.md$','', input.name).replace("-", " ")

def short_article_path(input):
    return re.sub(r'.md$','.html', input.name)

def process(input, index, outdir):
    fout = short_article_path(input)
    title = title_from_path(input)
    input_file = input.open(mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text, extensions = ['extra','meta'], output_format="html5")
    output_file = codecs.open(os.path.join(outdir,fout), "w",
                          encoding="utf-8",
                          errors="xmlcharrefreplace"
                          )
    # print(codecs.open(HEAD, mode="r", encoding="utf-8").read())
    # print(html)
    # print(codecs.open(FOOT, mode="r", encoding="utf-8").read())
    output_file.write(codecs.open(HEAD, mode="r", encoding="utf-8").read().replace("<?php echo $title ?>",title))
    output_file.write("""<div class="container-fluid">
  <div class="row">
    <div class="col-12 col-md-3 push-md-9 bd-sidebar">
""")
    output_file.write(index)
    output_file.write("""    </div>
    <div class="col-12 col-md-9 pull-md-3 bd-content">
""")
    output_file.write(html)
    output_file.write("""    </div>
  </div>
</div>
""")
    output_file.write(codecs.open(FOOT, mode="r", encoding="utf-8").read())

def generate_index(posts):
    output = "<p>"
    if len(posts) > 0:
        output += "<ul>"
    for f in posts:
        output += "<li><a href=\"{path}\">{title}</a></li>".format(
                        path = short_article_path(f), title = title_from_path(f)
                )
    if len(posts) > 0:
        output += "</ul>"
    output += "</p>"
    return output

posts = [p for p in Path(INPUT).glob("*.md")]
index = generate_index(posts)

for f in Path(INPUT).glob("*"):
    if f.suffix == '.md':
        print("Processing {}".format(f.name))
        process(f, index, OUTPUT)
    elif f.is_file():
        print("Copying {}".format(f.name))
        shutil.copy(f, os.path.join(OUTPUT,f.name))
