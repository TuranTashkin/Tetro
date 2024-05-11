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
def growth(data, curResults, grow, var1):
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
    print(maxNum)
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
        try:
            var = int(input("Enter a number here: "))
            return(var)
        except ValueError:
            print("Please enter numbers only.")


#topic: Functions for each topic







#PROGRAM


print()
print()
print('Welcome to Tetro!')

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
    print("How important is the size of the metro? 0 = not important, 10 = very important.")
    weight = intCheck()

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
        totalWeight += (weight*10)
        print()
        print(curResults)
        print(results)


    #growth rate
    print()
    print("How important is the growth rate of the city important to you? 0 = not important, 10 = very important. ")
    weight = intCheck()

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
        totalWeight += (weight*10)
        print()
        print(curResults)
        print(results)



    #politics of the city
    print()
    print("How important are the politics of the metro? 0 = not important, 10 = very important. ")
    weight = intCheck()

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
        totalWeight += (weight*10)
        print()
        print(curResults)
        print(results)

    #demographics
    print()
    print("How important are the demographics of the metro? 0 = not important, 10 = very important. ")
    weight = intCheck()

    if (weight != 0):
        round1 = 0
        x = True
        while x == True:
            round1 += 1
            print("Is there a specific community you would like to prioritize/ deprioritize?")
            print("White = 1, Latino = 2, Black = 3, Asian = 4, Native American = 5")
            print("Pacific Islander = 6, Others = 7, More Than Two Races = 8")
            priority1 = intCheck()
            race = {1:"whiteAlone", 2:"latino", 3:"blackAlone", 4:"asianAlone", 
                    5:"nativeAlone", 6:"pacificAlone", 7:"otherAlone", 8:"twoPlus"}
            
            print("To what extent do you want this group?")
            print("100 = as many as possible, 0 = as little as possible")
            priority2 = intCheck()


            cont = int(input("Do you want to adjust any other groups? 1 = yes, 0 = no. "))
            if(cont == 0):
                x = False
            else:
                curResults = Counter(curResults) + Counter(minMax(data[race[priority1]], curResults, priority2))
        
        # combines all curResults and divides curResults by the number of rounds
        curResults = Counter(curResults) + Counter(minMax(data[race[priority1]], curResults, priority2))
        curResults = Counter({key : curResults[key] / round1 for key in curResults})
        
        results = addToReport(curResults, results, weight)
        totalWeight += (weight*10)
        print()
        print(curResults)
        print(results)



    # results: declare the best metros for the user
    results = Counter({key : results[key] / totalWeight for key in results})
    print(results)
    print(totalWeight)
    break

