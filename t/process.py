import os
import shutil
from pathlib import Path
import re
import codecs
import markdown
from io import StringIO
import hashlib
from base64 import b64decode, b64encode

import json
import boto3
import botocore

INPUT = "posts_source"
OUTPUT = "posts"
HEAD = "layouts/header.php"
FOOT = "layouts/footer.php"

with open('config.json', 'r') as cf:
    config = json.load(cf)
s3 = boto3.client('s3', config['region'], aws_access_key_id=config['key'], aws_secret_access_key=config['secret'])
#site = s3.Bucket(config['bucket'])

def title_from_path(input):
    return re.sub(r'.md$','', input.name).replace("-", " ")

def short_article_path(input):
    return re.sub(r'.md$','', input.name)

def s3_etag(key):
    try:
        return s3.head_object(
            Bucket = config['bucket'],
            Key = key
        )['ETag'][1:-1]
    except botocore.exceptions.ClientError:
        return None

# Max size in bytes before uploading in parts.
AWS_UPLOAD_MAX_SIZE = 20 * 1024 * 1024
# Size of parts when uploading in parts
AWS_UPLOAD_PART_SIZE = 6 * 1024 * 1024

# Purpose : Get the md5 hash of a file stored in S3
# Returns : Returns the md5 hash that will match the ETag in S3
def local_etag(sourcePath):
    filesize = os.path.getsize(sourcePath)
    hash = hashlib.md5()

    if filesize > AWS_UPLOAD_MAX_SIZE:

        block_count = 0
        md5string = ""
        with open(sourcePath, "rb") as f:
            for block in iter(lambda: f.read(AWS_UPLOAD_PART_SIZE), ""):
                hash = hashlib.md5()
                hash.update(block)
                md5string = md5string + hash.digest()
                block_count += 1

        hash = hashlib.md5()
        hash.update(md5string)
        return hash.hexdigest() + "-" + str(block_count)

    else:
        with open(sourcePath, "rb") as f:
            for block in iter(lambda: f.read(AWS_UPLOAD_PART_SIZE), b""):
                hash.update(block)
        return hash.hexdigest()

def upload_text(key, body):
    md5 = hashlib.md5(body.encode('utf-8')).hexdigest()
    etag = s3_etag(key)
    if md5 != etag:
        print("MD5: {}".format(md5))
        print("etag: {}".format(etag))
        s3.put_object(
            Bucket = config['bucket'],
            Key = key,
            Body = body,
            ACL = 'public-read',
            ContentType = 'text/html',
            # ContentMD5 = md5
        )
        s3.put_object(
            Bucket = config['bucket'],
            Key = 't/' + key,
            ACL = 'public-read',
            WebsiteRedirectLocation = '/'+ key
        )
    else:
        print("Checksums match. Not uploading.")

def process(input, index, outdir):
    fout = short_article_path(input)
    title = title_from_path(input)
    input_file = input.open(mode="r", encoding="utf-8")
    text = input_file.read()
    html = markdown.markdown(text, extensions = ['extra','meta'], output_format="html5")
    output = StringIO()
    output.write(codecs.open(HEAD, mode="r", encoding="utf-8").read().replace("<?php echo $title ?>",title))
    output.write("""<div class="container-fluid">
  <div class="row">
    <div class="col-12 col-md-3 push-md-9 bd-sidebar">
""")
    output.write(index)
    output.write("""    </div>
    <div class="col-12 col-md-9 pull-md-3 bd-content">
""")
    output.write(html)
    output.write("""    </div>
  </div>
</div>
""")
    output.write(codecs.open(FOOT, mode="r", encoding="utf-8").read())
    # output_file = codecs.open(os.path.join(outdir,fout), "w",
    #                       encoding="utf-8",
    #                       errors="xmlcharrefreplace"
    #                       )
    # output_file.write(output.getvalue())

    key = outdir + '/' + fout
    body = output.getvalue()
    output.close()
    upload_text(key, body)

def upload_file(f):
    md5 = local_etag(f)
    etag = s3_etag(OUTPUT + '/' + f.name)
    if md5 != etag:
        print("MD5: {}".format(md5))
        print("etag: {}".format(etag))
        if f.suffix in config['suffix_to_type']:
            ct = config['suffix_to_type'][f.suffix]
        else:
            ct = 'application/octet-stream'
        print("Uploading as {}".format(ct))
        with f.open('rb') as fo:
            s3.put_object(
                Bucket = config['bucket'],
                Key = OUTPUT + '/' + f.name,
                Body = fo,
                ACL = 'public-read',
                ContentType = ct
            )
    else:
        print("Checksums match. Not uploading.")
    # shutil.copy(f, os.path.join(OUTPUT,f.name))

def generate_index(posts, path_prefix=""):
    output = "<p>"
    if len(posts) > 0:
        output += "<ul>"
    for f in posts:
        output += "<li><a href=\"{path}\">{title}</a></li>".format(
                        path = path_prefix+short_article_path(f), title = title_from_path(f)
                )
    if len(posts) > 0:
        output += "</ul>"
    output += "</p>"
    return output

def generate_frontpage(posts):
    title = 'The blog archive';
    output = StringIO()
    output.write(codecs.open(HEAD, mode="r", encoding="utf-8").read().replace("<?php echo $title ?>",title))
    output.write("""<div class="container-fluid">
<h1>{}</h1>""".format(title))
    output.write(generate_index(posts, OUTPUT+"/"))
    output.write("</div>")
    output.write(codecs.open(FOOT, mode="r", encoding="utf-8").read())
    return output.getvalue()

posts = [p for p in Path(INPUT).glob("*.md")]
posts.reverse()
index = generate_index(posts)

print("Processing index.html")
front = generate_frontpage(posts)
upload_text("index.html", front)

for f in Path(INPUT).glob("*"):
    if f.suffix == '.md':
        print("Processing {}".format(f.name))
        process(f, index, OUTPUT)
    elif f.is_file():
        print("Uploading {}".format(f.name))
        upload_file(f)
