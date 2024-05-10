# Turan Tashkin
# Metro-advisor
# 8/29/2023

import pandas as pd
import math as m


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
    

def growth(data, curResults, grow):
    for x in data:
        curResults[x] = 100 * (.1 - abs(grow - data[x]))
        if(curResults[x] < 0):
            curResults[x] = 0
    return(curResults)




#update report: adds the newly found information to the report
def addToReport(curResults, results, weight):
    for x in results:
        if(x in curResults):
            results[x] = (curResults[x] * weight) + results[x]
    return(results)

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
    weight = int(input("How important is the size of the metro? 0 = not important, 10 = very important."))

    if(weight != 0):
        print("What is your ideal size of a metro? (Largest is 20M, smallest 475K)")
        while True:
            try:
                size0= int(input("Please enter your ideal population size.  "))
                size1= int(input("Please enter the upper acceptable range. If no upper limit, enter 1.  "))
                size2 = int(input("Please enter the lowest acceptable range. If no lower limit, enter 0.  "))
                break
            except ValueError:
                print("Please enter numbers only.")

        if size1 == 1:
            size1 = 21000000
        if size2 == 0:
            size2 = 475000

        size0 = m.log10(size0)
        size1 = m.log10(size1)
        size2 = m.log10(size2)

        totalWeight += (weight*10)
        results = addToReport(pop(data["popLog"], curResults, size0, size1, size2), results, weight)

    #growth rate

    print()
    while True:
        try:
            weight = int(input("How important is the growth rate of the city important to you? 0 = not important, 10 = very important. "))
            break
        except ValueError:
            print("Please enter numbers only.")

    if (weight != 0):
                print("Enter ideal growth range (reference below and 2010 to 2020 growth in parathesis)")
                print("I prefer cities that don't change. (-1% to 1%)")
                print("I like natural growth.(1% to 5%)")
                print("I want moderate growth.(5% to 10%)")
                print("I prefer fast growing cities.(10% to 15%)")
                print("I want to live in a booming city.(15% to 33%)")

                while True:
                    try:
                        grow = (int(input("Your preference: ")))/100
                        break
                    except ValueError:
                        print("Please enter numbers only.")

                totalWeight += (weight*10)
                results = addToReport(growth(data["decadeGrowth"], curResults, grow), results, weight)

    print(results)
    print(totalWeight)
    break




# results: declare the best metros for the user




