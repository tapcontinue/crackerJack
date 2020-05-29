**CURRENT BUGS:**

Issue: Image sub-folder called "music" causes we'll have linking issues on the final HTML
Progress: Nearly solved, folder moves but need circumvent error when no dir exists.

**RESOLVED BUGS**

Issue: Copyright page is based on template and special text on title page is not being rolled into the final ePub.
Solution: I think the original html tag is unique and may be pulled in automatically in future builds.
Progress: Issue seems to be resolved. Took the same approach as the HLDB_ISBN injection to find the 
snippet of text toss it into a variables and place it into the template.

Issue: Closing HTML/body tags from each XHTML doc are being rolled into the final HTML doc.
Solution: Those will need to be deleted en mass and appended at the end of the document.
Progress: Issue seems to be resolved.
