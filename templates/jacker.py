import cracker
import re
import fileinput

text_to_search = (f"{cracker.image_extraction_dest}.image.html")

# print(text_to_search)

#* REPLACE
replacement = [
    ("<\?xml version=\"1.0\" encoding=\"utf-8\"\?>", " "),
    ("<!DOCTYPE html>", " "),
    ("<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\" xml:lang=\"en\" lang=\"en\">", ""),
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

#** SAVE
saveFile = open(f"{cracker.image_extraction_dest}index.html", "w")
saveFile.write(text_to_search)
saveFile.close()
