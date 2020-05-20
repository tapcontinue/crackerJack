import zipfile
import os
import shutil
import glob
import re
import isbn_hyphenate

# * Get item/title from user
item_Number = input("What's the print item number: ")
item_Number_Padded = item_Number.zfill(8)

book_title = input("What's the title?: ")
clean_title = book_title.replace(" ", "_").replace("_-_", "_").replace(":", "_")
final_folder_title = f"{item_Number_Padded}_{clean_title}"

ePub_isbn = input("ePub ISBN?: ")
os.mkdir(f"{final_folder_title}")

#* Crack open the ePub - mv content
with zipfile.ZipFile(f"input/{ePub_isbn}.epub", 'r') as zip_ref:
# with zipfile.ZipFile(glob.glob(f"input/*.epub", 'r')) as zip_ref:
    zip_ref.extractall("./extracted_ePub_contents")

#* Extract images from ePub
image_extraction_source = "./extracted_ePub_contents/EPUB/image"
image_extraction_dest = (f"./{final_folder_title}")
dest = shutil.move(image_extraction_source, image_extraction_dest)

os.remove("./extracted_ePub_contents/EPUB/toc.xhtml")
os.remove("./extracted_ePub_contents/EPUB/tocinternal.xhtml")

#* Merge/move all the XHTML into a single HTML - NOT SORTED!
body_files = sorted(glob.glob("./extracted_ePub_contents/EPUB/body*.xhtml"))
merged_body_files_path = f"{final_folder_title}/index.html"

with open(f'{final_folder_title}/index.html', 'w') as f:
    for file in body_files:
        with open(file) as infile:
            f.write(infile.read() + '\n')
shutil.rmtree('extracted_ePub_contents')

cracked_ePub = open(f"{final_folder_title}/index.html", 'r').read()

#* Replace old HL tags with G3 tags
text_to_search = cracked_ePub

replacement = [
    ("<\?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"\?>", " "),
    ("<!DOCTYPE html>", " "),
    ("<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\"", " "),
	("xmlns:ibooks=\"http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0\"", " "),
	("epub:prefix=\"ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0\" xml:lang=\"en\"", " "),
	("lang=\"en\">", " "),
    ("<head>", " "),
   	("<link href=\"css/main.css\" rel=\"stylesheet\" type=\"text/css\" media=\"screen, projection\" />", " "),
	("<!-- Extra Meta Tag - Viewport Element -->", " "),
	("<meta name=\"viewport\" content=\"width=device-width,minimum-scale=1.0,maximum-scale=1.0\" />", " "),
    ("</head>", " "),
    ("<title>body\d\d</title>"," "),
    ("\'>", "\">"),
    ("class=\'", "class=\""),
    ("=\'", "\"="),
    ("\' id\"", "\" id\""),
    ("\’", "'"),
    ("\“", "\""),
    ("\”", "\""),
    ("<section>", " "),
    ("</section>", " "),
    ("</article>", " "),
    ("<article>", " "),
    ("<h3 class=\"songpretitle\">", "<p class=\"subheading1\">"),
    ("hladdress", "copyright"),
    ("<p class=\"website\">", "<p class=\"copyright\">"),
    ("<div class=\"header-container\">", " "),
    ("<div class=\"music1\">", "<section class=\"music\">"),
    ("<h4 class=\"credit\">", "<p class=\"credit\">"),
    ("</h4>", "</p>"),
    ("<h1 class=\"songtitle\"", "<p class=\"chapter-heading\" >"),
    ("<div style=\"text-align:center;\">", " "),
    ("</h1>", "</p>"),
    ("\"credit\"", "\"subheading2\""),
    ("\"</h4>", "</p>"),
    ("<section class=\"song-start\">", " "),
    ("<div class=\"credit-container\">", " "),
    ("<div>", " "),
    ("</div>", " "),
    ("<div class=\"footer-container\">", " "),
    ("<div class=\"location\">", " "),
    ("class=\"rights\"", "class=\"subheading2\""),
    ("class=\"songsubtitle\"", "class=\"subheading1\""),
    ("<h3 class", "<p class"),
    ("</h3>", "</p>"),
    ("\n{2}", " "),
    ("	         ", " "),
    ("class=\"isbn\">Print", "class=\"copyright print\">Print"),
    ("class=\"isbn\">ePub", "class=\"copyright epub\">ePub"),
    ("class=\"isbn\">Kindle", "class=\"copyright kindle\">Kindle"),
    ("<section class=\"music\">", "<p class=\"figure-tall img-holder\">"),
    ("class=\"address\"", "class=\"copyright\""),
    ("<section class=\"address-container\">", " "),
    (">Email\"", " target=\"_blank\">Email"),
    ("<p class=\"website\"><a href=\"http://www.halleonard.com\">www.halleonard.com</a></p>",
     "<p class=\"copyright\"><a href=\"http://www.halleonard.com\" target=\"_blank\">www.halleonard.com</a></p>"),
    ("img src=\"image/", "img src=\"./image/"),
    ("src=\"images\"", "src=\"./image"),
    ("png\"/>", "png\"/></p>"),
    ("\"photorights\"", "\"copyright\""),
    ("<div class=\"group.\">", " "),
    ("<br />", " "),
    ("<br/>", " "),
    ("<section class=\"break\"> ", " "),
    ("<div class=\"copyrightart\">", " "),
    ("\"png\"/>", "\"png\"/></p>"),
    ("<div class=\"music{079,099}\">", "<p class=\"figure-tall img-holder\">"),
    ("<div class=\"music{79,99}\">", "<p class=\"figure-tall img-holder\">"),
    ("<div class=\"music\">", "<p class=\"figure-tall img-holder\">"),
    ("   ", " "),
    ("<img src=\"./image/copyright.jpg\" alt=\"copyright.jpg\"/>",
     "<p class=\"figure\"><img src=\"./image/copyright.jpg\" alt=\"copyright.jpg\" /></p>"),
    ("/image/music/", "/image/"),
    ("<img src=\"./image/fcover.jpg\" alt=\"fcover.jpg\"/>",
     "<p class=\"figure cover\"><img src=\"./image/fcover.jpg\" alt=\"fcover.jpg\" /></p>"),
    ("<div class=\"backcover\">", " "),
    ("id=\"toc_marker-\d\d\">", " "),
    ("<p class=\"chapter-heading\" >  ", "<p class=\"chapter-heading\">"),
    ("([ \t]*\n){2,}", "\n"),
    ("<img class=\"hallogo\" src=\"image/hallogo.png\" alt=\"hallogo.png\"/>",
     "<p class=\"figure\"><img class=\"hallogo\" src=\"./image/hallogo.png\" alt=\"hallogo.png\" /></p>"),
    ("	        <p class=\"figure-tall img-holder\"",
     "	    <p class=\"figure-tall img-holder\""),
    ("</p> ", "</p>"),
    ("<div class=\"break\">", " "),
    ("<p class=\"chapter-heading\" > id\"=toc_marker-\d\d\">","<p class=\"chapter-heading\">"),
    ("</body> </html>", " "),
    ("<body id=\"body\d\d\" xml:lang=\"en-US\">", " "),
    ("music.png\" />","music.png\"/></p>"),
    ("<div class=\"backcover\">"," "),
   	("<img src=\"./image/bcover.jpg\" alt=\"bcover.jpg\" />", "<p class=\"figure backcover\"><img src=\"./image/bcover.jpg\" alt=\"bcover.jpg\" /></p>"),
    ("<p class=\"chapter-heading\">", "\n<p class=\"chapter-heading\">")
]

for pat, repl in replacement:
    text_to_search = re.sub(pat, repl, text_to_search)

#* SAVE
saveFile = open('workshop/index.html', 'w')
saveFile.write(text_to_search)
saveFile.close()

#* Get HLDB from user to inject into a generic copyright page
get_hldb_isbn = input("HLDB number: i.e. 9781705100219 ")
HLDB_ISBN = isbn_hyphenate.hyphenate(get_hldb_isbn)

copyright_1 = """
<head>
	<title>CoverImage</title>
	<link href="../temp.css" type="text/css" rel="stylesheet" />
</head>

<body>
	<p class="figure cover"><img src="./images/fcover.jpg" alt="fcover.jpg" /></p>
	<p class="figure img"><img src="./images/copyright.jpg" alt="copyright.jpg" /></p>
    <p class="copyright HL Digital">HL Digital: {HLDB_ISBN}</p>
"""

copyright_2 = """
	<p class="figure img"><img class="hallogo" src="./image/hallogo.png" alt="hallogo.png" /></p>
	<p class="copyright">For all works contained herein:</p>
	<p class="copyright">Unauthorized copying, arranging, adapting, recording, Internet posting, public performance,</p>
	<p class="copyright">or other distribution of music in this publication is an infringement of copyright.</p>
	<p class="copyright">Infringers are liable under the law.</p>
	<p class="copyright">Visit Hal Leonard Online at</p>
	<p class="website"><a href="http://www.halleonard.com" target="_blank">www.halleonard.com</a></p>

	<p class="copyright">Contact us:</p>
	<p class="copyright"><span class="bold">Hal Leonard</span></p>
	<p class="copyright">7777 W. Bluemound Rd.</p>
	<p class="copyright">Milwaukee, WI 53213</p>
	<p class="copyright"><a href="mailto:info@halleonard.com" target="_blank">Email: info@halleonard.com</a></p>

    <p class="copyright">In Europe, contact:</p>
	<p class="copyright"><span class="bold">Hal Leonard Europe Limited</span></p>
	<p class="copyright">42 Wigmore Street</p>
	<p class="copyright">Marylebone, London, W1U 2RN</p>
	<p class="copyright"><a href="mailto:info@halleonardeurope.com" target="_blank">Email: info@halleonardeurope.com</a></p>

    <p class="copyright">In Australia, contact:</p>
	<p class="copyright"><span class="bold">Hal Leonard Australia Pty. Ltd.</span></p>
	<p class="copyright">4 Lentara Court</p>
	<p class="copyright">Cheltenham, Victoria, 3192 Australia</p>
	<p class="copyright"><a href="mailto:ausadmin@halleonard.com.au" target="_blank">Email: ausadmin@halleonard.com.au</a></p>
"""

preBodyFiles = copyright + copyright_2

# TODO: Inject HLDB/cover & copyright into the HTML file

# <head>
# 	<title>CoverImage</title>
# 	<link href="../temp.css" type="text/css" rel="stylesheet" />
# </head>
# <body>
# 	<p class="figure cover"><img src="./image/fcover.jpg" alt="fcover.jpg" /></p>
# 	<p class="figure img"><img src="./image/copyright.jpg" alt="copyright.jpg" /></p>

# TODO - move cover to top of the file
# TODO - move copyright to top of the file
