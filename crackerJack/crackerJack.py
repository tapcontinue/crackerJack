import zipfile
import os
import shutil
import glob
import re

# * Get item/title from user
item_Number = input("What's the print item number: ")
item_Number_Padded = item_Number.zfill(8)

book_title = input("What's the title?: ")
clean_title = book_title.replace(" ", "_").replace("_-_", "_").replace(":", "_")
final_folder_title = f"{item_Number_Padded}_{clean_title}"

ePub_isbn = input("ePub ISBN?: ")
os.mkdir(f"{final_folder_title}")

# TODO: Ask for HLDB. Script will hyphenate and inject into copyright template.
# hldb_isbn = input("HLDB number: i.e. 9781705100219 ")


# **Crack open the ePub - mv content
with zipfile.ZipFile(f"input/{ePub_isbn}.epub", 'r') as zip_ref:
    zip_ref.extractall("./extracted_ePub_contents")

# * Extract images from ePub
image_extraction_source = "./extracted_ePub_contents/EPUB/image"
image_extraction_dest = (f"./{final_folder_title}")
dest = shutil.move(image_extraction_source, image_extraction_dest)

os.remove("./extracted_ePub_contents/EPUB/toc.xhtml")
os.remove("./extracted_ePub_contents/EPUB/tocinternal.xhtml")

# ** Merge/move all the XHTML into a single HTML - NOT SORTED!
body_files = sorted(glob.glob("./extracted_ePub_contents/EPUB/body*.xhtml"))
merged_body_files_path = f"{final_folder_title}/index.html"

with open(f'{final_folder_title}/index.html', 'w') as f:
    for file in body_files:
        with open(file) as infile:
            f.write(infile.read() + '\n')
shutil.rmtree('extracted_ePub_contents')

cracked_ePub = open(f"{final_folder_title}/index.html", 'r').read()

# !EXPERIMENTAL 01 - only removes single instance
# with fileinput.FileInput(merged_body_files_path, inplace=True, backup='.bak') as file:
#     for line in file:
#         print(line.replace("<section>", " "), end=''),

# !EXPERIMENTAL 02 - Re-jigger the previous script
text_to_search = cracked_ePub

replacement = [
    ("^", " "),
    ("<\?xml[\s\S]*?=|en-US\">", " "),
    ("<\?xml version=\"1.0\" encoding=\"utf-8\"\?>", " "),
    ("<!DOCTYPE html>", " "),
    (
    "<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\" xml:lang=\"en\" lang=\"en\">",
    ""),
    ("<style type=\"text/css\"> img { max-width: 100%; }</style>",
     "<link href=\"../temp.css\" type=\"text/css\" rel=\"stylesheet\" />"),
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
    ("   ", " "),
    ("<img src=\"./image/copyright.jpg\" alt=\"copyright.jpg\"/>",
     "<p class=\"figure\"><img src=\"./image/copyright.jpg\" alt=\"copyright.jpg\" /></p>"),
    ("/image/music/", "/image/"),
    ("<img src=\"./image/fcover.jpg\" alt=\"fcover.jpg\"/>",
     "<p class=\"figure cover\"><img src=\"./image/fcover.jpg\" alt=\"fcover.jpg\" /></p>"),
    ("<img src=\"./image/bcover.jpg\" alt=\"bcover.jpg\"/>",
     "<p class=\"figure backcover\"><img src=\"./image/bcover.jpg\" alt=\"bcover.jpg\" /></p>"),
    ("<div class=\"backcover\">", " "),
    ("id=\"toc_marker-\d\d\">", " "),
    ("<p class=\"chapter-heading\" >  ", "<p class=\"chapter-heading\">"),
    ("([ \t]*\n){2,}", "\n"),
    ("<img class=\"hallogo\" src=\"image/hallogo.png\" alt=\"hallogo.png\"/>",
     "<p class=\"figure\"><img class=\"hallogo\" src=\"./image/hallogo.png\" alt=\"hallogo.png\" /></p>"),
    ("	        <p class=\"figure-tall img-holder\"",
     "	    <p class=\"figure-tall img-holder\""),
    ("</p> ", "</p>"),
    ("<div class=\"break\">", " ")
]

for pat, repl in replacement:
    text_to_search = re.sub(pat, repl, text_to_search)

# ** SAVE-----------------------
saveFile = open('workshop/index.html', 'w')
saveFile.write(text_to_search)
saveFile.close()

# TODO - Remove duplicate header files
# TODO - Inject cover from template.
# TODO - Inject copyright from template
# TODO - move cover to top of the file
# TODO - move copyright to top of the file
