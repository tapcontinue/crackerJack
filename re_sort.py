import re

# workThis = "apple orange"

# #* 01 - Basic python example to see differences in syntax
# x = re.findall(r'^(\S+)\s+(\S+)$', 'apple orange')
# z = re.sub(r'^(\S+)\s+(\S+)$', '\\2 \\1', 'apple orange')
# print(z)

# #* 02 - Building off previous example with external file and new syntax
workFile = open('workshop/test.html', 'rt') # open file
workFileContents = workFile.read() # read the entire file into a string
#
x = re.findall(r'^(\S+)\s+(\S+)$', workFileContents)
x = re.sub(r'^(\S+)\s+(\S+)$',r'\2 \1', workFileContents)
#
with open('./workshop/orange1.html', 'w') as file:
    file.write(x)


#* 03 - Using real data based off previous example
# workFile = open("workshop/index.html", "rt")
# workFileContents = workFile.read()

# a = re.findall(r"(<p class=\"subheading2\">.*$.<p class=\"subheading2\">{1,99}.*$)\n(<p class=\"figure-tall img-holder\">.*$){1,99}", workFileContents)
# a = re.sub(r"(<p class=\"subheading2\">.*$.<p class=\"subheading2\">{1,99}.*$)\n(<p class=\"figure-tall img-holder\">.*$){1,99}", r'\2 \1', workFileContents)

# print(a)

# with open('./workshop/sorted.html', 'w') as file:
#     file.write(a)
