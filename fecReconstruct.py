import zlib
import zfec

#function to determine if some of our data is in error AND if we have enough correct blocks to fix it(b/c maybe some of the parity blocks have been corrupted as well)
def there_is_an_error_in_first_NUMBLOCKS_AND_theres_numblock_correct_blocks(list_of_data,list_of_checksum,NUMBLOCKS,NUMPARITYBLOCKS):
    error_in_first_num_blocks = False
    for j in range(0, NUMBLOCKS):    
        if(list_of_checksum[j] != str(zlib.adler32(list_of_data[j]))):
        	error_in_first_num_blocks = True
    
    total_correct = 0
    if error_in_first_num_blocks:
        for j in range(0, NUMBLOCKS+NUMPARITYBLOCKS):
            if (list_of_checksum[j] == str(zlib.adler32(list_of_data[j]))):     
                total_correct+=1

    if (total_correct >= NUMBLOCKS): 
        return True
    return False

# The return of this function will be the first argument to the decode function
def get_list_of_NUMBLOCKS_correct_blocks(list_of_data,list_of_checksum,NUMBLOCKS,NUMPARITYBLOCKS):
    List = [ ] 
    for j in range(0,NUMBLOCKS+NUMPARITYBLOCKS):
        if(list_of_checksum[j] == str(zlib.adler32(list_of_data[j]))):	
            List.append(list_of_data[j])

    List = List[:NUMBLOCKS]
    return List

# The return of this function will be the second argument to the decode function
def get_list_of_indexes_which_are_correct(list_of_data,list_of_checksum,NUMBLOCKS,NUMPARITYBLOCKS):
    List = [ ]
    for j in range(0,NUMBLOCKS+NUMPARITYBLOCKS):
        if(list_of_checksum[j] == str(zlib.adler32(list_of_data[j]))):	
            List.append(j)

    List = List[:NUMBLOCKS]
    return List


f_in = open('testfecoutput','rb')
f_out = open('hopefullyoriginal','wb')

#Extract header information
wholefile = f_in.read()
list_of_groupofblocks = wholefile.split('FGF')
header = list_of_groupofblocks.pop(0)
totalpadded = int(header.split('AAA')[1])
BLOCKSIZE = int(header.split('AAA')[2])
NUMBLOCKS = int(header.split('AAA')[3])
NUMPARITYBLOCKS = int(header.split('AAA')[4])

#Extract groups of blocks
list_of_blocks = [ ] 
i=0
for line in list_of_groupofblocks:
    list_of_blocks.append(line.split('ZEZ'))

#Extract the original data and checksum into two seperate lists
tmp_data = [ ]
tmp_checksum = [ ]
list_of_orig_data = [ ]
list_of_checksum = [ ]
for i in range(0,len(list_of_blocks)):
    for j in range(0,len(list_of_blocks[i])):
        tmp_data.append(list_of_blocks[i][j].split('BCB')[0])
        tmp_checksum.append(list_of_blocks[i][j].split('BCB')[1])
    list_of_orig_data.append(tmp_data)
    list_of_checksum.append(tmp_checksum)
    tmp_data = [ ]
    tmp_checksum = [ ] 

#Create decoder object
decoder =  zfec.Decoder(NUMBLOCKS, NUMBLOCKS+NUMPARITYBLOCKS)

#Decode, correct errors, concatenate result
final_output = ''
for i in range(0,len(list_of_orig_data)):
    #Fix the errors
    print i
    print list_of_orig_data[i]
    if there_is_an_error_in_first_NUMBLOCKS_AND_theres_numblock_correct_blocks(list_of_orig_data[i],list_of_checksum[i],NUMBLOCKS,NUMPARITYBLOCKS):
        list_of_NUMBLOCKS_correct_blocks = get_list_of_NUMBLOCKS_correct_blocks(list_of_orig_data[i],list_of_checksum[i],NUMBLOCKS,NUMPARITYBLOCKS)
        list_of_indexes_which_are_correct = get_list_of_indexes_which_are_correct(list_of_orig_data[i],list_of_checksum[i],NUMBLOCKS,NUMPARITYBLOCKS)
        decoded_blocks = decoder.decode(list_of_NUMBLOCKS_correct_blocks,list_of_indexes_which_are_correct)
        list_of_orig_data.pop(i)
        list_of_orig_data.insert(i,decoded_blocks)
      
    #Note if the error is not fixable we will print out the error as is
    #Concatenate the current NUMBLOCKS of blocks
    final_output+= ''.join(list_of_orig_data[i][:NUMBLOCKS])
    
#Remove padding
final_output = final_output[:(-1)*totalpadded]

#Write result to file
f_out.write(final_output)