# crackerJack

**What is it?:**

crackerJack convert a ePub to a G3 HTML document.

**HOW TO USE:**

Place an epub into the input and run the crackerJack.py script.

It will ask for a item/title go ahead and provide that.
When it asks for ePub ISBN you'll have to match the ePub in the input folder. I.e. 9781540080639
I'll make it more dynamic in a bit, the script will read the file name.

Once the script is done everything is be in a new folder based on your input for item#/title which matches the G3 spec.


**COMPLETED FEATURES:**

- Cracks open a ePub
- Merges body files
- Swaps old HL HTML tags for G3 tags
- Replaces XHTML headers
- Reorders structure
- Injects pre-body files (copyright page / css / fcover)
- Injects formatted HL digital number

**UPCOMING FEATURES:**

- Re-sort images
G3 requires image to be kept together. This is easily done in regEx but I want to do it with Python.

**CURRENT BUGS:**

Issue: Image sub-folder called "music" causes we'll have linking issues on the final HTML
Solution #1: Manually move the contents up a level.
Solution #2: Find instances of this structure programmatically and move contents out of folder
Progress: Investigating.



**RESOLVED BUGS**

Issue: Copyright page is based on template and special text on title page is not being rolled into the final ePub.
Solution: I think the original html tag is unique and may be pulled in automatically in future builds.
Progress: Issue seems to be resolved. Took the same approach as the HLDB_ISBN injection to find the 
snippet of text toss it into a variables and place it into the template.

Issue: Closing HTML/body tags from each XHTML doc are being rolled into the final HTML doc.
Solution: Those will need to be deleted en mass and appended at the end of the document.
Progress: Issue seems to be resolved.
