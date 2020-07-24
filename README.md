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
- Re-sorts images based on the G3 requirement automatically (NEW!)
- Injects formatted HL digital number
- Extracts ePub names rather than ask for user input
- Finds extra music folder and moves content up a level


Full list:
https://github.com/tapcontinue/crackerJack/commits/master

**UPCOMING FEATURES:**

- Copyright extraction is based on single line, need to support multiple lines.
