import zipfile
import os
import shutil
import glob
import re

#* Get item/title from user
item_Number = input("What's the item number: ")
item_Number_Padded = item_Number.zfill(8)

book_title = input("What's the title?: ")
clean_title = book_title.replace(" ", "_").replace("_-_", "_").replace(":", "_")
final_folder_title = (f"{item_Number_Padded}_{clean_title}")

os.mkdir(f"{final_folder_title}")

#**Crack open the ePub - mv content
with zipfile.ZipFile("./9781540080639.epub", 'r') as zip_ref:
    zip_ref.extractall("./extracted_ePub_contents")

image_extraction_source = "./extracted_ePub_contents/EPUB/image"
image_extraction_dest = (f"./{final_folder_title}")
dest = shutil.move(image_extraction_source, image_extraction_dest)

os.remove("./extracted_ePub_contents/EPUB/toc.xhtml")
os.remove("./extracted_ePub_contents/EPUB/tocinternal.xhtml")

#* Merge/move all the XHTML into a single HTML
body_files = glob.glob("./extracted_ePub_contents/EPUB/*.xhtml")

with open(f'{dest}.html', 'w') as f:
    for file in body_files:
        with open(file) as infile:
            f.write(infile.read()+'\n')
shutil.rmtree('extracted_ePub_contents')
