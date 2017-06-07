'''
Write a short Python script that reads in a file, 
divides it into blocks of a fixed size, 
appends a checksum 
(and possibly other header information as needed) to each block, 
applies forward error correction to each block, 
and then concatenates all the blocks (including headers) and writes the whole thing to a file.
Create a corrupted version of the file: open it and change some bytes. 
(You can write a Python script to read in a file, 
    change N individual bytes randomly distributed throughout the file, and write the result to a new file.) 
Write a short Python script that reads in the corrupted file. 
Can you recover the original data? Verify your data for each block using the checksum.
Try running your code with different block sizes, code rates, and byte error rates. 
Explain (using data from your experiments) how these are related.
'''

import zlib
import zfec


#Output of this file will be in this format assuming for example the encoding is (3,5)
'''
AAA<totalPadded>AAA<BLOCKSIZE>AAA<NUMBLOCKS>AAA<NUMPARITYBLOCKS>                                                  ...[all on same line]
FGF<DATAofsizeBLOCKSIZE>BCB<Checksum>ZEZ<DATAofsizeBLOCKSIZE>BCB<Checksum>ZEZ<DATAofsizeBLOCKSIZE>BCB<Checksum>   ...[all on same line]
   <ParityDATAofsizeBLOCKSIZE>BCB<Checksum>ZEZ<ParityDATAofsizeBLOCKSIZE>BCB<Checksum>                            ...[all on same line]
FGF<DATAofsizeBLOCKSIZE>BCB<Checksum>ZEZ<DATAofsizeBLOCKSIZE>BCB<Checksum>ZEZ<DATAofsizeBLOCKSIZE>BCB<Checksum>   ...[all on same line]
   <ParityATAofsizeBLOCKSIZE>BCB<Checksum>ZEZ<ParityDATAofsizeBLOCKSIZE>BCB<Checksum>                            ...[all on same line]
FGF<DATAofsizeBLOCKSIZE>BCB<Checksum>ZEZ<DATAofsizeBLOCKSIZE>BCB<Checksum>ZEZ<DATAofsizeBLOCKSIZE>BCB<Checksum>   ...[all on same line]
   <ParityDATAofsizeBLOCKSIZE>BCB<Checksum>ZEZ<ParityDATAofsizeBLOCKSIZE>BCB<Checksum>                            ...[all on same line]

-data and checksum seperated by BCB
-every group of 5 blocks seperated by FGF (if the coding is 3,5)
-every block within a encoding group seperated by ZEZ
'''

f_in = open('test1.txt', 'rb')
fout_tmp = open('tmpfec','wb')
f_out = open('testfecoutput', 'wb')
BLOCKSIZE = 200
NUMBLOCKS = 3  #NUMBLOCKS per fec thing (i.e. 3 if the arguments are (3,5) to the encoder)
NUMPARITYBLOCKS = 3 # total will be numblo
numYs = 0
numXs = 0

#Pre-Processing to get the file in the format that fits the Blocksize 
#and the number of blocks per fec thing
wholefile = f_in.read()
len_whole_file = len(wholefile)

if len_whole_file % BLOCKSIZE != 0:
    wholefile = wholefile + 'Y' * (BLOCKSIZE - (len_whole_file % BLOCKSIZE)) 
    numYs = (BLOCKSIZE - (len_whole_file % BLOCKSIZE))

len_whole_file = len(wholefile)
num_total_blocks = len_whole_file / BLOCKSIZE

if (num_total_blocks % NUMBLOCKS != 0): 
    wholefile = wholefile + 'X'*(BLOCKSIZE*(NUMBLOCKS-(num_total_blocks%NUMBLOCKS) ))
    numXs = (BLOCKSIZE*(NUMBLOCKS-(num_total_blocks%NUMBLOCKS)))

totalpadded = numXs+numYs

#rewrite original data with padded X's and Y's
fout_tmp.write(wholefile)
fout_tmp.close()
fin_tmp = open('tmpfec','rb')

#reread from file
array = [ ]
line = fin_tmp.read(BLOCKSIZE)
while (line!=''):
    array.append(line)
    line = fin_tmp.read(BLOCKSIZE)

#Encode and concatenate all together
c=0
array2 = [ ]
miniarray= [ ]
final_output = ''
encoder = zfec.Encoder(NUMBLOCKS, NUMBLOCKS+NUMPARITYBLOCKS)#(3,5)

for i in range(0,(len(array)/NUMBLOCKS)):#(0,1,2--->(9/3) = 3
    for j in range(0,NUMBLOCKS): #(0,1,2)
        #print str(i)+' '+str(j)
        miniarray.append(array[c+j])

    encoded_blocks = encoder.encode(miniarray)
    #print encoded_blocks
    encoded_blocks_with_checksum = [line+'BCB'+ str(zlib.adler32(line)) for line in encoded_blocks]
    #print encoded_blocks_with_checksum
    final_output = final_output + ('FGF' + 'ZEZ'.join(encoded_blocks_with_checksum) )
    #print final_output
    miniarray = [ ]
    array2.append(encoded_blocks_with_checksum)
    c = c + NUMBLOCKS


#Make a header with (total padded)(BLOCKSIZE)(NUMBLOCKS)(NUMPARITYBLOCKS)
final_output ='AAA' + str(totalpadded) + 'AAA' + str(BLOCKSIZE) + 'AAA'+str(NUMBLOCKS)+'AAA'+str(NUMPARITYBLOCKS) +'AAA'+ final_output 

#Write to file
f_out.write(final_output)


'''
sources
http://stackoverflow.com/questions/12453580/concatenate-item-in-list-to-strings-python

'''




