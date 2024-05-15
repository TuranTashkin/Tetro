# Turan Tashkin
# Metro-advisor
# 8/29/2023

import pandas as pd
import math as m
from collections import Counter


# FUNCTIONS

#commit: commits each answer to the report

#population preferences: adjust report to according to how big they want their metro to be
def pop(data, curResults, size0, size1, size2):
    for x in data:
        if(data[x] < size1 and data[x] > size2):
            curResults[x] = 10 - abs(size0 - data[x]) * 5.88  #5.88 because popLog range is 5.6 to 7.3, difference = 1.7, 10/1.7 = 5.88 because the difference needs to be adjusted to 10
        else:
            curResults[x] = 0
    return(curResults)
    
#growth rate preference: 
def growth(data, curResults, grow, var1): # grow = ideal, var1 is how much from each side of grow should be considered
    for x in data:
        curResults[x] = (10/var1) * (var1 - abs(grow - data[x]))
        if(curResults[x] < 0):
            curResults[x] = 0
    return(curResults)

def minMax(data, curResults, priority2):
    maxNum = 0
    minNum = 100
    for x in data:
        if(maxNum < data[x]):
            maxNum = data[x]
        if(minNum > data[x]):
            minNum = data[x]
    var1 = maxNum - minNum
    idealNum = var1 * (priority2/100) + minNum
    for x in data:
        curResults[x] = (var1 - abs(idealNum - data[x]))/maxNum * 10
        if(curResults[x] < 0):
            curResults[x] = 0
    return(curResults)


#update report: adds the newly found information to the report
def addToReport(curResults, results, weight):
    for x in results:
        if(x in curResults):
            results[x] = (curResults[x] * weight) + results[x]
    return(results)

#asks for an int input, keeps trying until it finds
def intCheck():

    while True:
        var = input("Enter a number here: ")              
        try:
            var = int(var)
            return(var)
        except ValueError:
            if(var == 'x' or var == 'X'):
                exit()
            print("Please enter numbers only.")


#topic: Functions for each topic







#PROGRAM


print()
print()
print('Welcome to Tetro!')
print("Enter x at anytime to quit.")

weight = int()
totalWeight = 0
#types of calculations: do at end
#print("Would you like to: ")
#topic = input("0- weigh all metros equally, 1- rank each metro first, 2- give each topic weight?: ")
#type = input("1- rank each metro from 1 to 118 or 2- weigh each metro according to accuracy?: ")



# report: create new report, where everything will be saved

data1 = pd.read_excel(io="C:\\Users\\turan\\Documents\\metroData.xlsx", sheet_name="metroData", index_col='ID')
report1 = pd.read_excel(io="C:\\Users\\turan\\Documents\\metroData.xlsx", sheet_name="report", index_col='ID')

data = data1.to_dict()
report = report1.to_dict()
results = report["results"]
curResults = report["curResults"]



# questions: where questions will be asked and functions called

while True:

    #ideal size of metro
    print()
    print()
    print("How important is the size of the metro? 0 = not important, 10 = very important.")
    weight = intCheck()
    print()

    if(weight != 0):
        
        print("What is your ideal size of a metro? (Largest is 20M, smallest 475K)")        
        print("Please enter your ideal population size.")
        size0 = m.log10(intCheck())
        print("Please enter the highest acceptable range. If no upper limit, enter 1.")
        size1 = intCheck()
        if size1 == 1:
            size1 = 21000000
        size1 = m.log10(size1) 
        print("Please enter the lowest acceptable range. If no lower limit, enter 0.")
        size2 = intCheck()
        if size2 == 0:
            size2 = 475000
        size2 = m.log10(size2)        

        results = addToReport(pop(data["popLog"], curResults, size0, size1, size2), results, weight)
        totalWeight += weight


    #growth rate
    print()
    print()
    print("How important is the growth rate of the city important to you? 0 = not important, 10 = very important. ")
    weight = intCheck()
    print()

    if (weight != 0):
        print("Enter your ideal metro growth rate (2010 to 2020 growth in parathesis)")
        print("(-1% to 1%) Cities that don't change.")
        print("(1% to 5%) Slow growth")
        print("(5% to 10%) Moderate growth")
        print("(10% to 15%) Fast growth")
        print("(15% to 33%) Booming growth")

        print("Your preference: ")
        grow = intCheck()/100
        results = addToReport(growth(data["decadeGrowth"], curResults, grow, .1), results, weight)
        totalWeight += weight


    #politics of the city
    print()
    print()
    print("How important are the politics of the metro? 0 = not important, 10 = very important. ")
    weight = intCheck()
    print()

    if (weight != 0):
        print("Enter your ideal political leaning (2020 presidential election margins in parathesis)")
        print("(-60% to -30%) As liberal as possible")
        print("(-30% to -15%) Very liberal")
        print("(-15% to -8%) Moderately liberal")
        print("(-8% to 8%) Mixed politics")
        print("(8% to 15%) Moderately conservative")
        print("(15% to 30%) Very conservative")
        print("(30% to 45%) As conservative as possible")

        print("Your preference: ")
        politics = intCheck()/100
        results = addToReport(growth(data["margin"], curResults, politics, .3), results, weight)
        totalWeight += weight


    #demographics
    print()
    print()
    print("How important are the racial demographics of the metro? 0 = not important, 10 = very important. ")
    weight = intCheck()
    print()

    if (weight != 0):
        round1 = 0
        while True:
            round1 += 1
            print("Is there a specific community you would like to prioritize/ deprioritize?")
            print("White = 1, Latino = 2, Black = 3, Asian = 4, Native American = 5")
            print("Pacific Islander = 6, Others = 7, More Than Two Races = 8")
            priority1 = intCheck()
            race = {1:"whiteAlone", 2:"latino", 3:"blackAlone", 4:"asianAlone", 
                    5:"nativeAlone", 6:"pacificAlone", 7:"otherAlone", 8:"twoPlus"}
            
            print("What percentage of the metro should this group be?")
            print("100 = as many as possible, 0 = as little as possible")
            priority2 = intCheck()

            if(round1 == 1):
                curResults = Counter(minMax(data[age[priority1]], curResults, priority2))
            else:
                curResults = Counter(curResults) + Counter(minMax(data[race[priority1]], curResults, priority2))
            
            cont = int(input("Do you want to adjust any other groups? 1 = yes, 0 = no. "))
            if(cont == 0):
                break
        
        # divides curResults by the number of rounds
        curResults = Counter({key : curResults[key] / round1 for key in curResults})
        
        results = addToReport(curResults, results, weight)
        totalWeight += weight


    # diversity
    print()
    print()
    print("How important is the level of diversity of the metro? 0 = not important, 10 = very important. ")
    weight = intCheck()
    print()

    if (weight != 0):
        print("How diverse is your ideal metro?")
        print("66-75 = no group has clear majority (80-100)")
        print("55-66 = one group (likely) has a slim majority (66-80)")
        print("40-55 = the vast majority is one group (50-66)")
        print("10-40 = little to no diversity (0-50)")

        print("Your preference: ")
        diverse = intCheck()/100   #adjust down to the scale of data if choose 0-100 scale: *.007445
        results = addToReport(growth(data["diversityPerc"], curResults, diverse, .2), results, weight)
        totalWeight += weight


    # similar age
    print()
    print()
    print("How important is it for the city to have a lot/ less people of a certain age group?")
    print("0 = not important, 10 = very important. ")
    weight = intCheck()
    print() 

    if (weight != 0):
        round = 1

        while True:
            print("Is there a specific age brackets you would like to prioritize/ deprioritize?")
            print("Ages 0-18 = 1, Ages 18-24 = 2, Ages 25-44 = 3, Ages 45-64 = 4, Ages 65 and up = 5")
            priority1 = intCheck()
            age = {1:"0to18", 2:"18to24", 3:"25to44", 4:"45to64", 5:"65plus"}
            
            print("How much of this group should be in this metro?")
            print("100 = as many as possible, 0 = as little as possible")
            priority2 = intCheck()

            if(round == 1):
                curResults = Counter(minMax(data[age[priority1]], curResults, priority2))
                round += 1
            else:
                curResults = Counter(curResults) + Counter(minMax(data[age[priority1]], curResults, priority2))
            
            cont = int(input("Do you want to adjust any other age brackets? 1 = yes, 0 = no. "))
            if(cont == 0):
                break

        # divides curResults by the number of rounds
        curResults = Counter({key : curResults[key] / round for key in curResults})
        results = addToReport(curResults, results, weight)
        totalWeight += weight


    # median age
    print()
    print()
    print("How important is the overall median age of the metro? 0 = not important, 10 = very important. ")
    weight = intCheck()
    print()

    if (weight != 0):
        print("How young or old should it be overall?")
        print("0 = as young as possible, 100 = as old as possible")

        print("Your preference: ")
        diverse = (intCheck()-25.3) * 3.55872
        results = addToReport(growth(data["medianAge"], curResults, diverse, 15), results, weight)
        totalWeight += weight


    # education adjust
    print()
    print()
    print("How important is the education level of people in the metro?")
    print("0 = not important, 10 = very important. ")
    weight = intCheck()
    print() 

    if (weight != 0):
        round = 1

        while True:
            print("Which education level would you like to prioritize/ deprioritize?")
            print("Less than high school = 1, High school = 2, Some college = 3, Bachelors and up = 4")
            priority1 = intCheck()
            age = {1:"lessHighSchoolPerc", 2:"highSchoolPerc", 3:"someCollegePerc", 4:"bachelorPlusPerc"}
            
            print("How much of this group should be in this metro?")
            print("100 = as many as possible, 0 = as little as possible")
            priority2 = intCheck()

            if(round == 1):
                curResults = Counter(minMax(data[age[priority1]], curResults, priority2))
                round += 1
            else:
                curResults = Counter(curResults) + Counter(minMax(data[age[priority1]], curResults, priority2))
            
            cont = int(input("Do you want to adjust any other age brackets? 1 = yes, 0 = no. "))
            if(cont == 0):
                break

        # divides curResults by the number of rounds
        curResults = Counter({key : curResults[key] / round for key in curResults})
        results = addToReport(curResults, results, weight)
        totalWeight += weight


    # education level
    print()
    print()
    print("How important is the overall education level of the metro? 0 = not important, 10 = very important. ")
    weight = intCheck()
    print()

    # may be able to get rid of these prints and just have weight equal diverse
    if (weight != 0):
        print("How important is education levels of the metro?")
        print("0 = education isn't important, 100 = education is important")

        print("Your preference: ")
        diverse = (intCheck()/112.3595506)+2.29   #adjusts 0-100 into 2.29-3.18
        results = addToReport(growth(data["educationLevel"], curResults, diverse, .35), results, weight)
        totalWeight += weight


    # green transport
    print()
    print()
    print("How important is the availability of green transportation (public transporation, walking, biking)?")
    print("0 = not important, 10 = very important. ")
    weight = intCheck() * 10
    print()

    if (weight != 0):
        green = (weight/2.84091)+1   #adjusts 0-100 into 1-36.2
        results = addToReport(growth(data["greenTransport"], curResults, green, 25), results, weight)
        totalWeight += weight


    # travel time
    print()
    print()
    print("How important is travel time to work? 0 = not important, 10 = very important. ")
    weight = intCheck()
    print()

    if (weight != 0):
        print("How important are short travel times to work for you? 0 = not important, 100 = very important")
        print("Your preference: ")
        travel = (abs(100-intCheck())/1.39082)+20.2   #adjusts 0-100 into 20.2-92.1
        results = addToReport(growth(data["travelTimeMins"], curResults, travel, 25), results, weight)
        totalWeight += weight


    # types of transport
    print()
    print()
    print("How important is the availability of specific transportation methods?")
    print("0 = not important, 10 = very important. ")
    weight = intCheck()
    print() 

    if (weight != 0):
        round = 1

        while True:
            print("Which transportation method would you like to prioritize/ deprioritize?")
            print("Vehicles = 1, Public transportation = 2, Walking = 3, Biking = 4")
            priority1 = intCheck()
            transport = {1:"vehicle", 2:"publicTransport", 3:"walking", 4:"biking"}
            
            print("How much should you priorize this method of transportation in metros?")
            print("100 = as many as possible, 0 = as little as possible")
            priority2 = intCheck()

            if(round == 1):
                curResults = Counter(minMax(data[transport[priority1]], curResults, priority2))
                round += 1
            else:
                curResults = Counter(curResults) + Counter(minMax(data[transport[priority1]], curResults, priority2))
            
            cont = int(input("Do you want to adjust any other transportation methods? 1 = yes, 0 = no. "))
            if(cont == 0):
                break
        print(curResults)

        # divides curResults by the number of rounds
        curResults = Counter({key : curResults[key] / round for key in curResults})
        results = addToReport(curResults, results, weight)
        totalWeight += weight


    # work from home
    print()
    print()
    print("How important is the level of work from home in the metro? 0 = not important, 10 = very important. ")
    weight = intCheck()
    print()

    if (weight != 0):
        travel = (abs(100-weight())/11.111111)+3.5   #adjusts 0-100 into 3.5-12.5
        results = addToReport(growth(data["workFromHome"], curResults, travel, 3.5), results, weight)
        totalWeight += weight









    # results: declare the best metros for the user
    results = Counter({key : results[key] / totalWeight for key in results})
    print()
    print(results)
    print(totalWeight)
    break

