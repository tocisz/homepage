import os
from pathlib import Path
import re
import codecs
import markdown

INPUT = "t/posts_source"
OUTPUT = "t/posts"
HEAD = "t/layouts/header.php"
FOOT = "t/layouts/footer.php"

def process(input, outdir):
    print(input)
    fout = re.sub(r'.md$','.html', input.name)
    title = re.sub(r'.md$','', input.name).replace("-", " ")
    input_file = input.open(mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text, output_format="html5")
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
    output_file.write("""    </div>
    <div class="col-12 col-md-9 pull-md-3 bd-content">
""")
    output_file.write(html)
    output_file.write("""    </div>
  </div>
</div>
""")
    output_file.write(codecs.open(FOOT, mode="r", encoding="utf-8").read())

# for f in os.listdir(INPUT):
for f in Path(INPUT).glob("*.md"):
    #if f.endswith(".md"):
    process(f, OUTPUT)
