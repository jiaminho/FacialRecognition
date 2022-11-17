# CITS 1401 - Project 1
# Name: Jia Min Ho
# Student ID: 23337561
# September 2022


### Main ###

def main(csvfile, adultID, Option):
    main_dict = prepareDict(csvfile)
    
    if Option == "stats":
        return getStats(main_dict, adultID)
    
    elif Option == "FR":
        return getFR(main_dict, adultID)


### Prepare Dictionary ###
    
def prepareDict(csvfile):
    
    header_index = {}
    main_dict = {}
    
    # open and read file 
    with open(csvfile, "r") as filein:
        
        # prepare header
        header = filein.readline() # read first line
        header  = header.strip()
        header = header.replace('\n', '')
        header_list = header.split(",")
        
        # get index of each header column in a dict (in case columns are not in the same sequence as sample file)
        for index, header_element in enumerate(header_list):
            header_index[header_element] = index
            
        # prepare main dict
        for line in filein:
            line = line.strip()
            line.replace('\n', '')
            linelist = line.split(",")
            
            ID = linelist[header_index['ID']]            
            Expression = linelist[header_index['Expression']]            
            Distance = int(linelist[header_index['Distance']])
            Gdis = float(linelist[header_index['Gdis']])
            Ldis = float(linelist[header_index['Ldis']])
            
            if Gdis <= 0:
                Gdis = 50
            if Ldis <= 0:
                Ldis = 50
            
            distance = {
                'Gdis' : Gdis,
                'Ldis' : Ldis
                }
            
            if ID not in main_dict:
                main_dict[ID] = {}
                
            if Expression not in main_dict[ID]:
                main_dict[ID][Expression] = {}
                
            main_dict[ID][Expression][Distance] = distance
    
    return main_dict
        
        
        
### STATS ###

### OP1 to OP4 ###

def getStats(main_dict, adultID):
    
    OP1 = getOP1(main_dict, adultID)
    OP2 = getOP2(main_dict, adultID)
    OP3 = getOP3(main_dict, adultID)
    OP4 = getOP4(main_dict, adultID)
    
    return OP1, OP2, OP3, OP4


# Get Min & Max of Ldis & Gdis
def getOP1(main_dict, adultID):
    
    adultID_dict = main_dict[adultID]
    OP1 = []
    
    # loop from 1 to 8
    for i in range(1,9):
        
        minG = min(adultID_dict['Neutral'][i]['Gdis'], 
                  adultID_dict['Angry'][i]['Gdis'], 
                  adultID_dict['Disgust'][i]['Gdis'], 
                  adultID_dict['Happy'][i]['Gdis'])
        
        maxG = max(adultID_dict['Neutral'][i]['Gdis'], 
                  adultID_dict['Angry'][i]['Gdis'], 
                  adultID_dict['Disgust'][i]['Gdis'], 
                  adultID_dict['Happy'][i]['Gdis'])
        
        minL = min(adultID_dict['Neutral'][i]['Ldis'], 
                  adultID_dict['Angry'][i]['Ldis'], 
                  adultID_dict['Disgust'][i]['Ldis'], 
                  adultID_dict['Happy'][i]['Ldis'])
        
        maxL = max(adultID_dict['Neutral'][i]['Ldis'], 
                  adultID_dict['Angry'][i]['Ldis'], 
                  adultID_dict['Disgust'][i]['Ldis'], 
                  adultID_dict['Happy'][i]['Ldis'])
        
        OP1.append([round(minG, 4), round(maxG, 4), round(minL, 4), round(maxL, 4)])
        
    return OP1


# get Difference of Distances
def getOP2(main_dict, adultID):
    
    adultID_dict = main_dict[adultID]
    OP2 = []
    exps = ['Neutral','Angry','Disgust','Happy']
    
    # loop through 4 expression
    for exp in exps:
        
        sub_OP2 = []
        
        # loop from 1 to 8
        for i in range(1,9):
            
            difference = adultID_dict[exp][i]['Gdis'] - adultID_dict[exp][i]['Ldis']
            sub_OP2.append(round(difference, 4))
            
        OP2.append(sub_OP2)
    
    return OP2


# get average from list
def avrg(values):
    return sum(values)/len(values)


# Get average of Gdis
def getOP3(main_dict, adultID):

    adultID_dict = main_dict[adultID]
    OP3 = []
    
    # loop from 1 to 8
    for i in range(1,9):

        average = avrg([
            adultID_dict['Neutral'][i]['Gdis'],
            adultID_dict['Angry'][i]['Gdis'],
            adultID_dict['Disgust'][i]['Gdis'],
            adultID_dict['Happy'][i]['Gdis']
        ])
        
        OP3.append(round(average, 4))

    return OP3


# get standard deviation from list
def std_dv(values): 
    mean = avrg(values) # mean
    var  = sum((x-mean)**2 for x in values) / len(values)  # variance
    std  = var**0.5  # standard deviation
    
    return std


# get standard deviation of Ldis
def getOP4(main_dict, adultID):

    adultID_dict = main_dict[adultID]
    OP4 = []
    
    # loop from 1 to 8
    for i in range(1,9):

        standard_deviation = std_dv([
            adultID_dict['Neutral'][i]['Ldis'],
            adultID_dict['Angry'][i]['Ldis'],
            adultID_dict['Disgust'][i]['Ldis'],
            adultID_dict['Happy'][i]['Ldis']
        ])
        
        OP4.append(round(standard_deviation, 4))

    return OP4



### FR ###

# function to calculate cosine similarity score
def cos_sim_score(listA, listB):
    
    dotAB = sum(listA[i] * listB[i] for i in range(len(listA)))
    normA = sum(a**2 for a in listA)**0.5
    normB = sum(b**2 for b in listB)**0.5
    cos_sim = dotAB / (normA * normB)
    
    return cos_sim


## compare different expressions of the same adult
def part1FR(main_dict, adultID):
    
    adultID_dict = main_dict[adultID]
    
    Neutral = []
    Angry = []
    Disgust = []
    Happy = []
    
    cos_sim_list = []
    
    # put dictionary back into list
    for i in range(1,9):
        Neutral.append(adultID_dict['Neutral'][i]['Gdis'])
        Angry.append(adultID_dict['Angry'][i]['Gdis'])
        Disgust.append(adultID_dict['Disgust'][i]['Gdis'])
        Happy.append(adultID_dict['Happy'][i]['Gdis'])
    
    cos_sim_list = [
        cos_sim_score(Neutral, Angry),
        cos_sim_score(Neutral, Disgust),
        cos_sim_score(Neutral, Happy)
    ]
    
    return max(cos_sim_list)


## compare neutral expressions of this adultID to all other adults
def part2FR(main_dict, adultID):
    
    adultList = list(main_dict.keys())
    adultDistanceDict = {adult: [] for adult in adultList}
    adultCosSimDict = {adult: [] for adult in adultList}
    
    cos_sim_list = []
    
    # put list of neutral distance of each adult into dict
    for adult in adultList:
        Neutral = []
        
        # get list from dictionary
        for i in range(1,9):
            Neutral.append(main_dict[adult]['Neutral'][i]['Gdis'])
        
        adultDistanceDict[adult] = Neutral
    
    # calculate cosine similarity score between adult1 vs every adult
    for adult in adultList:
        adultCosSimDict[adult] = cos_sim_score(adultDistanceDict[adultID], adultDistanceDict[adult])
    
    return adultCosSimDict
    
    
# get max cossim between Gdis
def getFR(main_dict, adultID):
    
    # compare different expressions of same adult and get max cossim
    maxcossim1 = part1FR(main_dict, adultID)
    
    # comapre neutral expressions of all adults
    adultCosSimDict = part2FR(main_dict, adultID)
    
    ## find max cos sim across all adults
    adultCosSimDict[adultID] = maxcossim1
    max_cossim_ID = max(adultCosSimDict, key=adultCosSimDict.get)
    max_cossim = round(adultCosSimDict[max_cossim_ID],4)
    
    return max_cossim_ID, max_cossim
    
    
