import zlib

final_output_string = ''

f_in = open('compressed_test1_withchecksum', 'r')
f_out = open('decompressed_test1', 'w')

whole_compressed_file = f_in.read()
#print whole_compressed_file[:20]

headerandfile = whole_compressed_file.split('BBBBB')
#print whole_compressed_file[0]
BLOCKSIZE = int(headerandfile[0])

list_of_compressed_lines = headerandfile[1].split("EEAEE")

# get rid of first element b/c doesnt hold anything (symtom of split function)
list_of_compressed_lines.pop(0)

list_of_compressed_lines_without_checksum = [line.split("AAWAA")[0] for line in list_of_compressed_lines]

list_of_checksums = [line.split("AAWAA")[1] for line in list_of_compressed_lines]

list_of_decompressed_lines = [zlib.decompress(line) for line in list_of_compressed_lines_without_checksum]

index = 0

for line in list_of_decompressed_lines:
    newCheckSum = zlib.adler32(line)
    #print 'new: ' + str(newCheckSum)
    #print 'old: ' + str(list_of_checksums[index])
    #
    #
    if str(list_of_checksums[index])!=str(newCheckSum):
        print 'error in packet' + str(index)
    index=index+1

final_output_string = ''.join(list_of_decompressed_lines)
#print final_output_string

f_out.write(final_output_string)


''' 
Sources

slicing in Python
http://stackoverflow.com/questions/663171/is-there-a-way-to-substring-a-string-in-python

splitting in Python
https://docs.python.org/2/library/stdtypes.html

get rid of first element
http://stackoverflow.com/questions/4426663/how-do-i-remove-the-first-item-from-a-python-list
'''

