# define list of places
places = ['Berlin', 'Cape Town', 'Sydney', 'Moscow']

# Write files to disk.  Creates listfile.txt if it doesn't already exist
with open('listfile.txt', 'w') as filehandle:
    for listitem in places:
        filehandle.write('%s\n' % listitem)

# Read files from disk
# define an empty list
places = []

# open file and read the content in a list
with open('listfile.txt', 'r') as filehandle:
    for line in filehandle:
        # remove linebreak which is the last character of the string
        currentPlace = line[:-1]

        # add item to the list
        places.append(currentPlace)

print (str(places))
