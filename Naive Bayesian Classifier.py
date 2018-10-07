
# coding: utf-8

# In[ ]:


FILE = 'INPUT.txt'


# In[ ]:


### Change attributes as per question given
class OBSERVATIONS:
    def __init__(self,obsNo,outlook,temp,humidity,wind,playTennis="NO"):
        self.obsNo = obsNo
        self.OUTLOOK = outlook
        self.TEMP = temp
        self.HUMIDITY = humidity
        self.WIND = wind
        self.PLAYTENNIS = playTennis


# In[ ]:


## READING DATA
input_data = open(FILE)
data = input_data.read().splitlines()
print("----- DATA FROM INPUT FILE-----")
data


# In[ ]:


### Loading Data and Storing Observations

No_of_Ob = int(data[0])
No_of_Attr = int(data[1])+1

listOfTitles = []
listOfObs = []

j = 0
for i in data[2].split(" "):
    if j==0 or j==5:
        j=j+1
        continue
    listOfTitles.append(i)
    j=j+1
    

print("Attributes observed: \n\n",listOfTitles)

index = 3

while index < len(data)-1:  ### -1 because last touple is out test data
    line = data[index].split(" ")
    obsNo = ''.join(line[0])
    outlook = line[1]
    temp = line[2]    ### Change values as per given question
    humidity = line[3]
    wind = line[4]
    playTennis = line[5]
    
    
    tempOb = OBSERVATIONS(obsNo,outlook,temp,humidity,wind,playTennis) ### Change calling parameters
    listOfObs.append(tempOb)
    index=index+1


# In[ ]:


## FINDING COUNT OF OUTPUT (Y)

count_OP = {}

for obsn in listOfObs:
        key = str(obsn.PLAYTENNIS) ### Change
        
        if key in count_OP:
            count_OP[key] = count_OP[key] +1;
            
        else:
            count_OP[key] = 1;
        
            
total= No_of_Ob
        
print("TOTAL COUNT OF Classifications : \n")
for x,y in count_OP.items():
    print(x,y,sep=' : ')


# In[ ]:


### FINDING PROBABILITY OF OUTPUT COLUMN P(N) = No(N)/No(TOTAL)
prob_OP = {}

for key in count_OP.keys():
    prob_OP[key] = count_OP[key]/total

print("PROBABILITY OF OUTPUT FIELD : \n")
for x,y in prob_OP.items():
    print(x,y,sep=' : ')


# In[ ]:


### FINDING THE CONDITIONAL PROBABILITIES of Rest of Attributes

listOfProbabilities = []

for title in listOfTitles:
    
    tempMap = {}
    
    for obsn in listOfObs:
        value = getattr(obsn,title)
        opvalue = getattr(obsn,'PLAYTENNIS')   ### Change as per given question
        
        key = str(value)+"|"+str(opvalue)  ### Change as per given question
        
        if key in tempMap:
            tempMap[key] = tempMap[key]+ (1/count_OP[str(opvalue)])
        else:
            tempMap[key] = 1/count_OP[str(opvalue)]
            
    listOfProbabilities.append(tempMap);

listOfProbabilities.append(prob_OP)


# In[ ]:


print("Conditional Probabilities of Attributes : \n")
for i in listOfProbabilities:
    
    for x,y in i.items():
        print(x,y,sep=" : ")
    print()


# In[ ]:


### GETTING TEST DATA

line = data[len(data)-1].split(" ")
test = OBSERVATIONS(No_of_Ob+1,line[0],line[1],line[2],line[3])

print("Test Data : \n",line)


# In[ ]:


### STEP 1 : Find the Probability of given touple with every class attribute

tempMap = {}

for x in count_OP.keys():
    
    temp=1
    
    for y,z in zip(listOfTitles,listOfProbabilities):
        
        key = getattr(test,str(y))+"|"+str(x)    ### Change as per question
        ###print(key)
        if key in z:
            ###print("inside if")
            temp = temp * z[key]
        else:
            ###print("inside else")
            temp = temp*0
    
    tempMap[x] = temp
    
    
print("Probability of T = { test_dat} with YES and NO \n\n")    
for x,y in tempMap.items():
    print(x,y)
        
        
### ALL respective probabilites are in tempMap


# In[ ]:


### NOW WE CALCULATE LIKELIHOOD for YES and NO
### WE REPLACE VALUES IN tempMap with value(tempMap)*P(either YES OR NO)

for x in tempMap:
    tempMap[x] = tempMap[x]*prob_OP[x]

print("Likelihood for Yes and No : \n")
for x,y in tempMap.items():
    print(x,y)


# In[ ]:


### NOW we calculate ESTIMATED VALUE i.e. P(T)

estVal = 0
for x in tempMap:
    estVal = tempMap[x]+estVal
    
print("Estimated value P(T) = \n ",estVal)


# In[ ]:


### Calculating actual probability
finalProb = {}

max = float('-inf')
ans = ''
for x in tempMap:
    finalProb[x] = tempMap[x]/estVal
    ###print(finalProb[x],max)
    if finalProb[x] > max:    ### Comapring for the highest probability and marking the output in ans.
        max = finalProb[x]
        ans = x
        
print("PLAY TENNIS = "+str(ans))
    

