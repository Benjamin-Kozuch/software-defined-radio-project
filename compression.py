import zlib

BLOCKSIZE = 500

array = [ ]

f_in = open('145px-Solid_blue.svg.png', 'r')

line = f_in.read(BLOCKSIZE)

length_of_file = len(line)

while (line!=''):

    checksum = zlib.adler32(line) & 0xffffffff 

    #line_with_checksum = line + 'AAAAAWXYZAAAAA' +`checksum` #(same as str(checksum))

    compressed_line = zlib.compress(line)

    array.append(compressed_line + 'AAWAA' +`checksum`)

    line = f_in.read(BLOCKSIZE)			

    length_of_file += len(line)



concatenated_compressed_lines_withtheir_checksums = ''

for i in array:
    concatenated_compressed_lines_withtheir_checksums +=("EEAEE"+i)
    

'''
print 'the length of  original  file is: ' + str(length_of_file) 
print 'the length of compressed file is: ' + str(len(concatenated_compressed_lines_withtheir_checksums))
print 'the BLOCKSIZE is                : ' + str(BLOCKSIZE)
print 'the CR is                       : ' + str(float(length_of_file)/(len(concatenated_compressed_lines_withtheir_checksums)))
'''

f_out = open('compressed_test1_withchecksum', 'w')
header = str(BLOCKSIZE) +'BBBBB'
final_output = header + concatenated_compressed_lines_withtheir_checksums
#print 'finaloutput'+ final_output #[:20]
f_out.write(final_output)
f_out.close()




'''
Sources

-HOW TO CONCATENATE INT TO STRING
http://stackoverflow.com/questions/2847386/python-string-and-integer-concatenation

-adler32
https://docs.python.org/2/library/zlib.html
'''


