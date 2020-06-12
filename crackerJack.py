import zipfile
import os
import shutil
import glob
import re
import isbn_hyphenate
import fileinput

while True:
    # * Get item# from user
    item_Number = input("What's the print item number: ")
    item_Number_Padded = item_Number.zfill(8)

    # * Get title from user
    book_title = input("What's the title?: ")
    clean_title = book_title.replace(" ", "_").replace("_-_", "_").replace(":", "_").replace("__", "_")
    final_folder_title = f"{item_Number_Padded}_{clean_title}"

    # * Extract ePub_isbn based on file in input remove .DS_Store pulled from server
    path = "./input"
    if ".DS_Store" in path:
        os.remove(path + ".DS_Store")

    dir_list = os.listdir(path)
    ePub_isbn = str([i for i in dir_list if i.startswith('978')])
    ePub_isbn = ePub_isbn[2:15]

    os.mkdir(f"{final_folder_title}")

    # * Crack open the ePub - mv content
    with zipfile.ZipFile(f"input/{ePub_isbn}.epub", 'r') as zip_ref:
        zip_ref.extractall("./extracted_ePub_contents")

    # * Extract images from ePub
    image_extraction_source = "./extracted_ePub_contents/EPUB/image"
    image_extraction_dest = f"./{final_folder_title}"
    dest = shutil.move(image_extraction_source, image_extraction_dest)

    os.remove("./extracted_ePub_contents/EPUB/toc.xhtml")
    os.remove("./extracted_ePub_contents/EPUB/tocinternal.xhtml")

    # ! - Still experimental: Extract the photo rights from the copyright.xhtml
    answer = input("Photo rights on title page? Yes/No: ")
    if answer == "no":
        photo_rights = "none"
        print('Skipping photo rights')
    if answer == "yes":
        copyright_file = "./extracted_ePub_contents/EPUB/copyright.xhtml"

        with open(copyright_file, 'r') as search_list, \
                open(copyright_file, 'r', encoding="utf8") as source_file:

            for line in source_file:
                if "photorights" in line:
                    photo_rights = (line[26:-5])  # Assuming the tag hasn't changed.

    # * Merge/move all the XHTML into a single HTML - NOT SORTED!
    body_files = sorted(glob.glob("./extracted_ePub_contents/EPUB/body*.xhtml"))
    merged_body_files_path = f"{final_folder_title}/index.html"

    with open(f'{final_folder_title}/index.html', 'w') as f:
        for file in body_files:
            with open(file) as infile:
                f.write(infile.read() + '\n')
    shutil.rmtree('extracted_ePub_contents')

    cracked_ePub = open(f"{final_folder_title}/index.html", 'r').read()

    # * Replace old HL tags with G3 tags
    text_to_search = cracked_ePub

    replacement = [
        ("<\?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"\?>", " "),
        ("<!DOCTYPE html>", " "),
        ("<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:epub=\"http://www.idpf.org/2007/ops\"", " "),
        ("xmlns:ibooks=\"http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0\"", " "),
        (
        "epub:prefix=\"ibooks: http://vocabulary.itunes.apple.com/rdf/ibooks/vocabulary-extensions-1.0\" xml:lang=\"en\"",
        " "),
        ("lang=\"en\">", " "),
        ("<head>", " "),
        ("<link href=\"css/main.css\" rel=\"stylesheet\" type=\"text/css\" media=\"screen, projection\" />", " "),
        ("<!-- Extra Meta Tag - Viewport Element -->", " "),
        ("<meta name=\"viewport\" content=\"width=device-width,minimum-scale=1.0,maximum-scale=1.0\" />", " "),
        ("</head>", " "),
        ("<title>body\d\d</title>", " "),
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
        ("\"photorights\"", "\"copyright\""),
        ("<div class=\"group.\">", " "),
        ("<br />", " "),
        ("<br/>", " "),
        ("<section class=\"break\"> ", " "),
        ("<div class=\"copyrightart\">", " "),
        ("\"png\"/>", "\"png\"/></p>"),
        ("<div class=\"music{001,099}\">", "<p class=\"figure-tall img-holder\">"),
        ("<div class=\"music{01,99}\">", "<p class=\"figure-tall img-holder\">"),
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
        ("<p class=\"chapter-heading\" > id\"=toc_marker-\d\d\">",
         "<p class=\"chapter-heading\">"),
        ("</body> </html>", " "),
        ("<body id=\"body\d\d\" xml:lang=\"en-US\">", " "),
        ("music.png\" />", "music.png\"/></p>"),
        ("<div class=\"backcover\">", " "),
        ("<img src=\"./image/bcover.jpg\" alt=\"bcover.jpg\" />",
         "<p class=\"figure backcover\"><img src=\"./image/bcover.jpg\" alt=\"bcover.jpg\" /></p>"),
        ("<p class=\"chapter-heading\">", "\n<p class=\"chapter-heading\">"),
        ("<div class=\"music\d\d\">", "<p class=\"figure-tall img-holder\">"),
        ("png\"/>", "png\"/></p>"),
        ("png\" />", "png\"/>"),
        (".png\"/>", ".png\"/></p>"),
        ("alt=\"image/music/", "alt=\"./image/"),
        ("</body>", " "),
        ("</html>", " "),
        ("	{1,5}<p class", "<p class"),
        ("		  <p class", "<p class"),
        ("<div class=\"musicfirst\">", "<p class=\"figure-tall img-holder\">"),
        ("</p></p></p>", "</p>"),
        ("</p></p>", "</p>"),
        ("<div class=\"musicfirst\">", "<p class=\"figure-tall img-holder\">"),
        ("  xml:lang=\"en\"", " "),
        ("<link href=\"css/main.css\" rel=\"stylesheet\" type=\"text/css\" media=\"screen, projection\"/>", ""),
        ("					<img", "<p class=\"figure-tall img-holder\"><img"),
        ("				<p class=\"figure-tall img-holder\">\$", ""),
        ("<p class=\"figure-tall img-holder\">$\n", ""),
        ("\n\n<p ", "<p "),
        ("", ""),
    ]

    for pat, repl in replacement:
        text_to_search = re.sub(pat, repl, text_to_search)

    # * SAVE
    saveFile = open('workshop/index.html', 'w')
    saveFile.write(text_to_search)
    saveFile.close()

    # * Get HLDB from user to inject into a generic copyright page
    get_hldb_isbn = input("HLDB number: i.e. 9781705100219 ")
    HLDB_ISBN = isbn_hyphenate.hyphenate(get_hldb_isbn)

    # * Merge templates to index
    templates = ['templates/body01.xhtml', 'templates/body02.xhtml', 'workshop/index.html', 'templates/body03.xhtml']

    with open('./workshop/output.xhtml', 'w') as outfile:
        for template in templates:
            with open(template) as infile:
                outfile.write(infile.read())
                outfile.write("\n")

    # * Clear out temp files move into final resting place
    os.remove("./workshop/index.html")
    os.remove(final_folder_title + "/index.html")
    os.rename("./workshop/output.xhtml", "./workshop/index.html")
    shutil.move("./workshop/index.html", final_folder_title + "/index.html")

    # * INJECT HLDB ISBN into final html file
    final_resting_spot = (final_folder_title + "/index.html")

    with fileinput.FileInput(final_resting_spot, inplace=True, ) as file:
        for line in file:
            print(line.replace("{HLDB_ISBN}", HLDB_ISBN), end='')

    # * Remove music dir and move files up a level
    extra_music_dir_path = (final_folder_title + "/image/music/")
    new_music_path = (final_folder_title + "/image")

    if os.path.exists(extra_music_dir_path):
        files = os.listdir(extra_music_dir_path)
        for f in files:
            shutil.move(extra_music_dir_path + f, new_music_path)
        else:
            pass

    # * Remove the now empty music dir
    if os.path.exists(extra_music_dir_path):
        shutil.rmtree(extra_music_dir_path)

    # * EXPERIMENTAL - INJECT photo rights into final html file
    with fileinput.FileInput(final_resting_spot, inplace=True, ) as file:
        for line in file:
            print(line.replace("{photo_rights}", photo_rights), end='')
