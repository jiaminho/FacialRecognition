# CITS 1401 - Project 2
# Name: Jia Min Ho
# Student ID: 23337561
# Semester 2, 2022



### Main ###

def main(csvfile, SubjIDs):
    
    # catch incorrect inputs and terminate gracefully
    
    if not isinstance(SubjIDs, list):
        print("SubjIDs provided is not a list. Please provide correct input")
        return [None, None, None, None] 
    if len(SubjIDs) != 2:
        print("SubjIDs provided is not a list of 2 elements. Please provide correct input")
        return [None, None, None, None] 
    if not isinstance(SubjIDs[0], str):
        print("SubjIDs provided is not a list of strings. Please provide correct input")
        return [None, None, None, None] 
    if not isinstance(SubjIDs[1], str):
        print("SubjIDs provided is not a list of strings. Please provide correct input")
        return [None, None, None, None] 
    if (SubjIDs[0]) == "":
        print("SubjIDs provided is an empty string. Please provide correct input")
        return [None, None, None, None] 
    if (SubjIDs[1]) == "":
        print("SubjIDs provided is an empty string. Please provide correct input")
        return [None, None, None, None]
    if not isinstance(csvfile, str):
        print("Input file provided is not a string. Please provide correct input")
          
    # make SubjIDs case insensitive
    SubjIDs = [x.upper() for x in SubjIDs]
    
    # run the main function to prepare dictionary and outputs OP1, OP2, OP3, OP4 if input provided are correct
    try:
        main_dict = prepareDict(csvfile)
    
        OP1 = getOP1(main_dict, SubjIDs)
        OP2 = getOP2(main_dict, SubjIDs)
        OP3 = getOP3(main_dict, SubjIDs)
        OP4 = getOP4(main_dict, SubjIDs)
    
        return OP1, OP2, OP3, OP4
    
    
    # Terminate gracefully if there is an error
    
    except KeyError:
        print("The SubjIDs/input provided is wrong. Please provide correct input")
        return [None, None, None, None]
    
    except NameError:
        print("There is a NameError in the input!")
        return [None, None, None, None]
           
    except FileNotFoundError: # terminate gracefully if the file cannot be found or opened 
        print("The provided filename is not found. Please provide correct filename.")
        return [None, None, None, None]  
    
    except PermissionError:
        print("Insufficient permission to read this file")
        return [None, None, None, None] 
    
    except IsADirectoryError:
        print("The provided filename is a directory!")
        return [None, None, None, None]
    
    except NameError:
        print("There is a name error in the input file")
        return [None, None, None, None]
    
    except TypeError:
        print("There is a TypeError in the input file")
        return [None, None, None, None]
    
    except UnicodeDecodeError:
        print("There is a UnicodeDecodeError in the input file")
        return [None, None, None, None]
        


# Function to create a dictionary

def create_dictionary(keys,values):
    result = {}
    for key, value in zip(keys, values):
        result[key] = value
    return result



### Prepare Dictionary ###

def prepareDict(csvfile):
    header_index = {}
    main_dict = {}
    
    with open(csvfile, "r") as filein:
        
        # prepare header
        header = filein.readline()
        header = header.strip()
        header = header.replace('\n', '')
        header_list = header.split(",")
        header_list = map(lambda x: x.upper(), header_list) # make header all upper case
        
        # get index of each header column in a dict (in case column are not in sequence as sample file)
        for index, header_element in enumerate(header_list):
            header_index[header_element] = index
            
        # prepare main dict
        for line in filein:
            line = line.strip()
            line.replace('\n','')
            linelist = line.split(",")
            
            SubjID = linelist[header_index['SUBJID']].upper() # make SubjID uppercase (case insensitive)
            Landmark = linelist[header_index['LANDMARK']].upper() # make Landmark uppercase (case insensitive)
            
            
            # location keys
            location_key = ['OX','OY','OZ','MX','MY','MZ']
            location_value = []
            
            # location values 
            for i in location_key:
                loc_val = linelist[header_index[i]]
                if loc_val != "":
                    if -200 <= float(loc_val) <= 200:
                        location_value.append(float(loc_val))
                    else:
                        location_value.append(None) # out of bound data = None
                else:
                    location_value.append(None) # missing data = None
                    
            location = create_dictionary(location_key,location_value)
            
            
            if SubjID not in main_dict:
                main_dict[SubjID] = {}
                
            if Landmark not in main_dict[SubjID]:
                main_dict[SubjID][Landmark] = {}
                
            main_dict[SubjID][Landmark] = location
            
                  
    return main_dict
        


# function to calculate 3D Asymmetry and 3D Euclidean Distance

def formula(listA, listB):
    ans = 0
    for i in range(len(listA)):
        A = (listB[i] - listA[i])**2
        ans = ans + A
        
    return (ans**0.5)



# function to calcute the facial asymmetries for each subject in the csv file

def all_facial_asymmetry(main_dict, SubjIDs):
       
    final_output = []
    
    # get all subject ID
    all_IDs = list(main_dict.keys())
    ID_total_asym = [] # empty list for total asymmetry values for each subject
    
    location_keys = ['OX','OY','OZ','MX','MY','MZ']
    asym_output = []
    
    for i in all_IDs:
        
        asym_values = []
        
        # get 7 landmarks of subject
        landmark_keys = list(main_dict[i].keys())
    
        # get 3D location values of each landmark
        for landmark_key in landmark_keys:
            loc_val = []

            # get location values from main dict
            for location_key in location_keys:
                
                ans = main_dict[i][landmark_key][location_key]
                loc_val.append(ans)

            # check if there is none in the list, if yes, then append none
            if any(elem is None for elem in loc_val):
                asym_values.append(None)
            else:
                # list of 3D asymmetry values
                listA = loc_val[:3]
                listB = loc_val[-3:]
                ans = formula(listA, listB)
                asym_values.append(ans)
 
        # create dictionary to find out which is nosetip 'prn'
        dict_output = create_dictionary(landmark_keys,asym_values)    
        
        # if no. of landmark of subject != 7 or none in assym values, then none
        if len(landmark_keys) != 7 or any(elem is None for elem in asym_values) or dict_output.get('PRN') != 0:
            asym_output.append(None)
        else:
            asym_output.append(dict_output)
        
    # dictionary of total asymmetry values for each subject ID
    ID_asym_dict = create_dictionary(all_IDs, asym_output)
    
    # remove None values
    new_dict = {key: value for key, value in ID_asym_dict.items() if value is not None}
    
    return new_dict



### OP1 ###

# get 3D asymmetry of landmarks for F1 and F2
def getOP1(main_dict, SubjIDs):
    
    OP1 = []
    F1 = SubjIDs[0]
    F2 = SubjIDs[1]
    subjects = [F1,F2]
    
    # get facial asymmetry values from all_facial_asymmetry function
    facial_asymmetry = all_facial_asymmetry(main_dict, SubjIDs)
    keysList = list(facial_asymmetry.keys())
    
    for subject in subjects:
        if subject in keysList:
            OP1_dict = facial_asymmetry[subject]
            del OP1_dict['PRN']
            OP1_dict = {key : round(OP1_dict[key], 4) for key in OP1_dict}
            OP1.append(OP1_dict)
        else:
            OP1.append(None)
            
    return OP1



### OP2 ### 

# get 3D Euclidean distance of facial distances for F1 and F2
def getOP2(main_dict, SubjIDs):
    
    OP2 = []
    location_keys = ['OX','OY','OZ']
    
    # create subject list for iteration
    F1 = SubjIDs[0]
    F2 = SubjIDs[1]
    subjects = [F1,F2]
    

    for subject in subjects:
        
        location_values = []
        
        # get 7 landmarks of subject
        landmark_keys = list(main_dict[subject].keys())

        # get 3D location values of each landmark
        for landmark_key in landmark_keys:
            loc_val = []
            
            # get location values
            for location_key in location_keys:
                ans = main_dict[subject][landmark_key][location_key]
                if ans != None:
                    loc_val.append(ans)
                else:
                    loc_val.append(None) # if empty or out of bound, append none

            location_values.append(loc_val)


        # create dictionary of ('OX','OY','OZ') for each landmark
        landmark_values = create_dictionary(landmark_keys, location_values)
        
        
        # check requirements. Return none if invalid input or data
        facial_asymmetry_dict = all_facial_asymmetry(main_dict, SubjIDs) # get facial asymmetry values from all_facial_asymmetry function
        facial_asymmetry = facial_asymmetry_dict.get(subject)  
        
        if len(landmark_keys) != 7 or any(elem is None for elem in location_values) or facial_asymmetry == None:
            output_dict = None
            
        else:
            # calculate facial distance
            A1 = landmark_values.get('EX')
            B1 = landmark_values.get('EN')
            ExEn = formula(A1,B1)
            ExEn = round(ExEn,4)

            A2 = landmark_values.get('EN')
            B2 = landmark_values.get('AL')
            EnAl = formula(A2,B2)
            EnAl = round(EnAl,4)

            A3 = landmark_values.get('AL')
            B3 = landmark_values.get('EX')
            AlEx = formula(A3,B3)
            AlEx = round(AlEx,4)

            A4 = landmark_values.get('FT')
            B4 = landmark_values.get('SBAL')
            FtSbal = formula(A4,B4)
            FtSbal = round(FtSbal,4)

            A5 = landmark_values.get('SBAL')
            B5 = landmark_values.get('CH')
            SbalCh = formula(A5,B5)
            SbalCh = round(SbalCh,4)

            A6 = landmark_values.get('CH')
            B6 = landmark_values.get('FT')
            ChFt = formula(A6,B6)
            ChFt = round(ChFt,4)

            distance = [ExEn, EnAl, AlEx, FtSbal, SbalCh, ChFt]

            facialdistance_keys = ['EXEN','ENAL','ALEX','FTSBAL','SBALCH','CHFT']

            # create dictionary for output
            output_dict = create_dictionary(facialdistance_keys, distance)
            
        OP2.append(output_dict)

    return OP2



### OP3 ###

def getOP3(main_dict, SubjIDs):
    
    output = []

    # get all subject ID
    all_IDs = list(main_dict.keys())
    
    # get facial asymmetry values from all_facial_asymmetry function
    facial_asymmetry = all_facial_asymmetry(main_dict, SubjIDs)
    keysList = list(facial_asymmetry.keys())
    
    for subject in all_IDs:
        if subject in keysList:
            asym_dict = facial_asymmetry.get(subject) 
            asym_value_list = asym_dict.values() # get a list of all asym values of the subject
            total_asym = sum(asym_value_list) # sum asym values
            total_asym = round(total_asym,4) # round off to 4 decimal place     
            output.append(total_asym)
        else:
            output.append(None)
            
            
    # dictionary of total asymmetry values for each subject ID
    ID_total_asym_dict = create_dictionary(all_IDs,output)
    
    # remove None values
    new_dict = {key: value for key, value in ID_total_asym_dict.items() if value is not None}
    
    # get lowest
    lowest_5 = sorted(new_dict.items(), key=lambda x: x[1])[:5]    
    return lowest_5



# function to calculate cosine similarity score
def cos_sim_score(listA, listB):
    
    dotAB = sum(listA[i] * listB[i] for i in range(len(listA)))
    normA = sum(a**2 for a in listA)**0.5
    normB = sum(b**2 for b in listB)**0.5
    cos_sim = dotAB / (normA * normB)
    
    return cos_sim



### OP4 ###

# get cosine similarity of F1 and F2
def getOP4(main_dict, SubjIDs):
    
    try:   
        # get OP2 output (facial distances)
        OP2_output = getOP2(main_dict, SubjIDs)

        # check if any element is None in OP2 output
        if any(elem is None for elem in OP2_output):
            return None
        else:
            # create listA for F1 facial distances
            F1 = OP2_output[0]
            F1 = list(F1.values())

            # create listB for F2 facial distances
            F2 = OP2_output[1]
            F2 = list(F2.values())

            result = cos_sim_score(F1,F2)
            result = round(result,4)

            return result
        
    except ZeroDivisionError: # return None if there is zeroDivisionError
        return None