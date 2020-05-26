# crackerJack

crackerJack is a series of modifications to a ePub to match the G3 spec.

USAGE:
Place a epub into the input and run the crackerJack.py script.

It will ask for a item/title go ahead and provide that.
When it asks for ePub ISBN you'll have to match the ePub in the input folder. I.e. 9781540080639

I'll make it more dynamic in a bit, the script will read the file name.

Once the script is done everything is be in a new folder based on your input for item#/title which matches the G3 spec.


COMPLETED FEATURES:
- Cracks open a ePub
- Merges body files
- Swaps old HL HTML tags for G3 tags
- Replace XHTML headers
- Reorders structure
- Injects prebody files (copyright page / css / fcover)
- Injects formatted HL digital number

NEXT UP…
- Re-sort images/
