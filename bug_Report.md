**CURRENT BUGS:**

Issue: Image sub-folder called "music" causes we'll have linking issues on the final HTML
Progress: Nearly solved, folder moves but need circumvent error when no dir exists.

**RESOLVED BUGS**

Issue: Script breaks randomly when picking up the ePub ePub ISBN from file name.
Solution: 1st attempt to pick up this content lead to an issue with .DS_Store files being brought in from the server.
Depending on creation date/user the .DS_Store may exist and cause an issue. 
Modifications were made to be more specific to target files that start with 978. If it continue to
be an issue could also target the ePub extension.

Issue: Copyright page is based on template and special text on title page is not being rolled into the final ePub.
Solution: I think the original html tag is unique and may be pulled in automatically in future builds.
Progress: Issue seems to be resolved. Took the same approach as the HLDB_ISBN injection to find the 
snippet of text toss it into a variables and place it into the template.

Issue: Closing HTML/body tags from each XHTML doc are being rolled into the final HTML doc.
Solution: Those will need to be deleted en mass and appended at the end of the document.
Progress: Issue seems to be resolved.
