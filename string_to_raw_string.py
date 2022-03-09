#
# convert a string to a raw string
# BUT, doesn't work overly well when  copying and pasting
# MS Windows paths.
#


# 'string' to r'string'
# this works since nothing could be intrepret as an escape char
d = 'D:\Projects\Miscellaneous\Testing'
mydir = r'{}'.format(d)    #convert to a raw string
print(mydir)


# 'string' to r'string' but with replacement since the directory that
# starts with a 0. Replace needed since \0 is intrepreted as an escape char.
# Note, other replacements would be needed for other escape code.
# For example if folder starts with a t, you'd have \t that is Interrupted
# as an escape code for a tab
d = 'D:\Projects\Miscellaneous\0-testing'
d = d.replace('\0','\\0')   # convert files
mydir = r'{}'.format(d)    #convert to a raw string
print(mydir)



# you have no issues if you just use a raw string from the get go
d = r'D:\Projects\Miscellaneous\testing'
print(d)
d = r'D:\Projects\Miscellaneous\0-testing'
print(d)
