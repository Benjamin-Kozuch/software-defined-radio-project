import random
f_in = open('testfecoutput','rb')
wholefile = f_in.read()

#This random or not random number will decide how many chars get destroyed all together
Number_of_destroyed = 5
'''
#This will give random 
#range = 100
#Number_of_destroyed = int((random.random())*range)
'''

for i in range(0,Number_of_destroyed):
    randomnumber = random.random()
    
    #This random number will decide which char in the file will become corrup
    random_btw_zero_and_len_of_file = int(randomnumber * len(wholefile))
    
    wholefile = wholefile[0:random_btw_zero_and_len_of_file-1]+'a'+wholefile[random_btw_zero_and_len_of_file:len(wholefile)]

    print str(i)+': '+str(random_btw_zero_and_len_of_file)

    print wholefile[random_btw_zero_and_len_of_file-5:random_btw_zero_and_len_of_file+5]    



f_out = open('testfecoutput','wb')
f_out.write(wholefile)

#line 9356
#1115

