# Turan Tashkin
# Metro-advisor
# 8/29/2023

import pandas as pd
import math as m
from collections import Counter


# FUNCTIONS

#commit: commits each answer to the report

#population preferences: adjust report to according to how big they want their metro to be
def pop(data, curResults, size0, size1, size2, var1):
    for x in data:
        if(data[x] < size1 and data[x] > size2):
            curResults[x] = 10 - abs(size0 - data[x]) * var1 
        elif(data[x] == 0):
            curResults[x] = 5
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

#includes indifference 
def risky(data, curResults, risk, var1): # grow = ideal, var1 is how much from each side of grow should be considered
    for x in data:                       # weeds out number that should be indifferent to
        if(data[x] < risk):
            curResults[x] = 10
        else:
            curResults[x] = (10/var1) * (var1 - abs(risk - data[x]))
            if(curResults[x] < 0):
                curResults[x] = 0
    return(curResults)

# uses the min and max in giving out points
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

#asks for an int input between 0 and 10, keeps trying until it finds
def intCheckTen():

    while True:
        var = input("Enter a number here between 0 and 10: ")              
        try:
            var = int(var)
            if(var >= 0 and var <= 10):
                return(var)
        except ValueError:
            if(var == 'x' or var == 'X'):
                exit()
            print("Please enter numbers only.")

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
print()

weight = int()
totalWeight = 0
#types of calculations: do at end
#print("Would you like to: ")
#topic = input("0- weigh all metros equally, 1- rank each metro first, 2- give each topic weight?: ")
#type = input("1- rank each metro from 1 to 118 or 2- weigh each metro according to accuracy?: ")



# report: create new report, where everything will be saved

data1 = pd.read_excel(io="C:\\Users\\turan\\Documents\\metroData.xlsx", sheet_name="metroData", index_col='metro')
report1 = pd.read_excel(io="C:\\Users\\turan\\Documents\\metroData.xlsx", sheet_name="report", index_col='metro')

data = data1.to_dict()
report = report1.to_dict()
results = report["results"]
curResults = report["curResults"]
demoResults = report["base1"]
climResults = report["base2"]
econResults = report["base3"]
homeResults = report["base4"]
cultResults = report["base5"]


# questions: where questions will be asked and functions called

while True:

    print("Please determine, on a scale of 0 to 10,how important these aspects of metros are:")
    print("Demographics, economy, home and transport, climate, and culture")
    print("0 = not important, 10 = very important")
    print()
    print("Demographics of the metro (age, racial, religiosity, education, politics):")
    demoWeight = intCheckTen()
    print("Economy and worklife of the metro (income, prices, worklife):")
    econWeight = intCheckTen()
    print("Home and transportation of the metro (home costs, home and transportation types): ")
    homeWeight = intCheckTen()
    print("Climate of the metro (weather, sunshine, natural disasters): ")
    climWeight = intCheckTen()
    print("Culture of the metro(sports): ")
    cultWeight = intCheckTen()

    sectionWeight = demoWeight + econWeight + homeWeight + climWeight + cultWeight



    if(demoWeight != 0):
        print()
        print("DEMOGRAPHICS OF THE METRO")

        #ideal size of metro
        print()
        print()
        print("How important is the size of the metro (population)?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
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

            demoResults = addToReport(pop(data["popLog"], curResults, size0, size1, size2, 5.88), demoResults, weight) #5.88 because popLog range is 5.6 to 7.3, difference = 1.7, 10/1.7 = 5.88 because the difference needs to be adjusted to 10
            totalWeight += weight

        #population growth rate
        print()
        print()
        print("How important is the growth rate of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
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
            demoResults = addToReport(growth(data["decadeGrowth"], curResults, grow, .1), demoResults, weight)
            totalWeight += weight


        # diversity
        print()
        print()
        print("How important is the level of racial diversity of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if (weight != 0):
            print("How diverse is your ideal metro?")
            print("66-75 = no group has clear majority (80-100)")
            print("55-66 = one group (likely) has a slim majority (66-80)")
            print("40-55 = the vast majority is one group (50-66)")
            print("10-40 = little to no diversity (0-50)")

            print("Your preference: ")
            diverse = intCheck()/100   #adjust down to the scale of data if choose 0-100 scale: *.007445
            demoResults = addToReport(growth(data["diversityPerc"], curResults, diverse, .2), demoResults, weight)
            totalWeight += weight


        #racial demographics
        print()
        print()
        print("How important are the racial demographics of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
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
                    curResults = Counter(minMax(data[race[priority1]], curResults, priority2))
                else:
                    curResults = Counter(curResults) + Counter(minMax(data[race[priority1]], curResults, priority2))
                
                cont = int(input("Do you want to adjust any other groups? 1 = yes, 0 = no. "))
                if(cont == 0):
                    break
            
            # divides curResults by the number of rounds
            curResults = Counter({key : curResults[key] / round1 for key in curResults})
            
            demoResults = addToReport(curResults, demoResults, weight)
            totalWeight += weight


        # age
        print()
        print()
        print("How important are the age demographics of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if (weight != 0):
            print("Would you like to adjust by the median age of the metro OR adjust specific age groups?")
            print("1 = adjust by median age, 2 = adjust specific age groups?")
            aging = intCheck()

            if(aging == 1):
                print("How young or old should it be overall?")
                print("0 = as young as possible, 100 = as old as possible")

                print("Your preference: ")
                diverse = (intCheck()-25.3) * 3.55872
                demoResults = addToReport(growth(data["medianAge"], curResults, diverse, 15), demoResults, weight)
                totalWeight += weight

            if(aging == 2):
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
                demoResults = addToReport(curResults, demoResults, weight)
                totalWeight += weight


        # education level
        print()
        print()
        print("How important is the overall education level of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if (weight != 0):
            print("Would you like to adjust the overall education level of the metro OR specific levels of education?")
            print("1 = overall education level, 2 = specific levels of education")
            educate = intCheck()

            if(educate == 1):
                print("How important is education levels of the metro?")
                print("0 = education isn't important, 100 = education is important")

                print("Your preference: ")
                diverse = (intCheck()/112.3595506)+2.29   #adjusts 0-100 into 2.29-3.18
                demoResults = addToReport(growth(data["educationLevel"], curResults, diverse, .35), demoResults, weight)
                totalWeight += weight


            if (educate == 2):
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
                demoResults = addToReport(curResults, demoResults, weight)
                totalWeight += weight


        #religiosity
        print()
        print()
        print("How important is the religiosity of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if(weight != 0):
            print("Do you prefer less religious or more religious metros?")
            print("0 = as irreligious as possible, 100 = as religious as possible")

            print("Your preference: ")

            religious = (intCheck()/1.768745)+32.1657   #adjusts 0-100 into 32.1657-88.70297
            demoResults = addToReport(growth(data["religiousIndivPerc"], curResults, religious, .28), demoResults, weight)
            totalWeight += weight


        #politics of the city
        print()
        print()
        print("How important are the politics of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
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
            demoResults = addToReport(growth(data["margin"], curResults, politics, .3), demoResults, weight)
            totalWeight += weight

        demoResults = Counter({key : demoResults[key] / totalWeight * demoWeight for key in demoResults})
        totalWeight = 0



    if(econWeight != 0):
        print()
        print("ECONOMY AND WORKLIFE OF THE METRO")

        # travel time
        print()
        print()
        print("How important is the average travel time to work in the metro (relates to traffic levels)?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if (weight != 0):
            print("How important are short travel times to work for you? 0 = not important, 100 = very important")
            print("Your preference: ")
            travel = (abs(100-intCheck())/1.39082)+20.2   #adjusts 0-100 into 20.2-92.1
            econResults = addToReport(growth(data["travelTimeMins"], curResults, travel, 25), econResults, weight)
            totalWeight += weight


        # work from home
        print()
        print()
        print("How important is the popularity of work from home in the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if (weight != 0):
            travel = (weight/11.111111)+3.5   #adjusts 0-100 into 3.5-12.5
            econResults = addToReport(growth(data["workFromHome"], curResults, travel, 3.5), econResults, weight)
            totalWeight += weight


        #per capital personal income
        print()
        print()
        print("How important is the level of wealth of people in the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if (weight != 0):
            print("Do you prefer to live in a poorer or richer area?")
            print("0 = as poor as possible, 100 = as rich as possible")

            print("Your preference: ")

            income = (intCheck()/0.00110539)+31153   #adjusts 0-100 into 31153-121619
            econResults = addToReport(growth(data["perCapitaPersonalIncome"], curResults, income, 50000), econResults, weight)
            totalWeight += weight


        # regional price parity
        print()
        print()
        print("How important are the price levels of goods and services in the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if (weight != 0):
            print("Does it matter if the metro is expensive?")
            print("0 = yes- I prefer cheaper metros, 100 = no- I'm happy with expensive metros")

            print("Your preference: ")

            price = (intCheck()/4.2312)+88.488   #adjusts 0-100 into 88.488-112.122
            econResults = addToReport(growth(data["regionalPriceParity"], curResults, price, 12), econResults, weight)
            totalWeight += weight

        econResults = Counter({key : econResults[key] / totalWeight * econWeight for key in econResults})
        totalWeight = 0



    if(homeWeight != 0):
        print()
        print("HOME AND TRANSPORTATION IN THE METRO")

        # types of transport
        print()
        print()
        print("How important is the availability of specific transportation methods in the metro?")
        print("0 = not important, 10 = very important. ")
        weight = intCheckTen()
        print() 

        if (weight != 0):
            round = 1

            while True:
                print("Which transportation method would you like to prioritize/ deprioritize?")
                print("Vehicles = 1, Public transportation = 2, Walking = 3, Biking = 4, Any kind of green transportation = 5")
                priority1 = intCheck()
                transport = {1:"vehicle", 2:"publicTransport", 3:"walking", 4:"biking", 5:"greenTransport"}
                
                print("How much should you priorize this method of transportation in metros?")
                print("100 = as many as possible, 0 = as little as possible")
                priority2 = intCheck()

                if(round == 1):
                    curResults = Counter(minMax(data[transport[priority1]], curResults, priority2))
                else:
                    curResults = Counter(curResults) + Counter(minMax(data[transport[priority1]], curResults, priority2))
                round += 1

                cont = int(input("Do you want to adjust any other transportation methods? 1 = yes, 0 = no. "))
                if(cont == 0):
                    break

            # divides curResults by the number of rounds
            curResults = Counter({key : curResults[key] / round for key in curResults})
            homeResults = addToReport(curResults, homeResults, weight)
            totalWeight += weight

        #housing costs
        print()
        print()
        print("How important is the cost of housing in a metro (measured in single family housing)?")
        print("0 = not important, 10 = very important.")

        weight = intCheckTen()
        print()

        if(weight != 0):
            
            print("What is your ideal average cost of a metro?")
            print("Largest is 1577K, smallest 135K. Measured in single family housing.)")        
            print("Please enter your ideal average cost.")
            size0 = m.log10(intCheck()/1000)
            print("Please enter the highest acceptable range. If no upper limit, enter 1.")
            size1 = intCheck()/1000
            if size1 == 1:
                size1 = 1576
            print("Please enter the lowest acceptable range. If no lower limit, enter 0.")
            size2 = intCheck()/1000
            if size2 == 0:
                size2 = 135

            homeResults = addToReport(pop(data["housingCost2022q4"], curResults, size0, size1, size2, 0.006935), homeResults, weight)
            totalWeight += weight


        # housing types
        print()
        print()
        print("How important is the availability of different types of housing options?")
        print("(Example: availability of single family housing, duplex, apartments, etc.)")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print() 

        if (weight != 0):
            round = 1

            while True:
                print("What type of housing would you like to prioritize/ deprioritize?")
                print("Single family detached = 1, Single family attached = 2, Duplex = 3")
                print("3 to 4 units = 4, 5 to 9 units = 5, 10 or more units = 6, Mobile housing and others = 7")

                priority1 = intCheck()
                houses = {1:"SFDetachedPerc", 2:"SFAttachedPerc", 3:"2apartments", 4:"3to4apartments", 5:"5to9apartments",
                            6:"10plusApartments", 7: "mobileAndOtherHomes"}
                
                print("How much should you priorize/ deprioritize this housing option in metros?")
                print("0 = as little as possible, 100 = as much as possible")
                priority2 = intCheck()

                if(round == 1):
                    curResults = Counter(minMax(data[houses[priority1]], curResults, priority2))
                    round += 1
                else:
                    curResults = Counter(curResults) + Counter(minMax(data[houses[priority1]], curResults, priority2))
                
                cont = int(input("Do you want to adjust any other housing options? 1 = yes, 0 = no. "))
                if(cont == 0):
                    break

            # divides curResults by the number of rounds
            curResults = Counter({key : curResults[key] / round for key in curResults})
            homeResults = addToReport(curResults, homeResults, weight)
            totalWeight += weight


        #housing age
        print()
        print()
        print("How important is the age of the housing stock?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if(weight != 0):
            print("What is your ideal age of housing in a metro?")
            print("0 = as young as possible, 100 = as old as possible")

            print("Your preference: ")

            nat = (intCheck()*0.374)+38
            homeResults = addToReport(risky(data["approxAvgAgeHousing"], curResults, nat, 20), homeResults, weight)
            totalWeight += weight


        #owner occupied
        print()
        print()
        print("How important is the amount of owner occupied units in the metro (also reflects how many rentals are available)?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if(weight != 0):
            print("How much of the metro should be owner occupied units?")
            print("0 = as little as possible, 100 = as much as possible")

            print("Your preference: ")

            owner = (intCheck()/100*.28)+.49
            homeResults = addToReport(risky(data["ownerOccupiedPerc"], curResults, owner, 14), homeResults, weight)
            totalWeight += weight

        homeResults = Counter({key : homeResults[key] / totalWeight * homeWeight for key in homeResults})
        totalWeight = 0



    if(climWeight != 0):
        print()
        print("CLIMATE OF THE METRO")

        # temperature
        print()
        print()
        print("How important is the temperature of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if(weight != 0):
            print("Do you prefer colder or warmer weather?")
            print("0 = coldest possible, 100 = hottest possible")

            print("Your preference: ")

            temp = (intCheck()/3.215434)+46.9   #adjusts 0-100 into 46.9-78
            climResults = addToReport(growth(data["avgTemp"], curResults, temp, 15), climResults, weight)
            totalWeight += weight


        #sunlight
        print()
        print()
        print("How important are the sunlight levels of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if(weight != 0):
            print("Do you prefer little sun or sunnier metros?")
            print("0 = as little sunny as possible, 100 = as much sun as possible")

            print("Your preference: ")

            sunny = (intCheck()/0.014459392)+13680.24   #adjusts 0-100 into 13680.24-20596.16
            climResults = addToReport(growth(data["avgDailySunlight"], curResults, sunny, 30), climResults, weight)
            totalWeight += weight


        #precipitation
        print()
        print()
        print("How important are the rain/ precipitation levels of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if(weight != 0):
            print("Do you prefer little rain or rainier metros?")
            print("0 = as little rain as possible, 100 = as much rain as possible")

            print("Your preference: ")

            temp = (intCheck()/1.570845)+4.18   #adjusts 0-100 into 4.18-67.84
            climResults = addToReport(growth(data["precipInches"], curResults, temp, 3500), climResults, weight)
            totalWeight += weight


        #snow
        print()
        print()
        print("How important are the snow levels of the metro?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if(weight != 0):
            print("Do you prefer little snow or snowier metros?")
            print("0 = as little snow as possible, 100 = as much snow as possible")

            print("Your preference: ")

            temp = (intCheck()/0.78247)   #adjusts 0-100 into 0-127.8
            climResults = addToReport(growth(data["snowInches"], curResults, temp, 50), climResults, weight)
            totalWeight += weight


        # overall disaster
        print()
        print()
        print("How important is the level of natural disasters in metros?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print()

        if(weight != 0):
            print("How much risk of natural disasters do you prefer?")
            print("0 = as little risk as possible, 100 = indifferent to the risk")

            print("Your preference: ")

            nat = intCheck()
            climResults = addToReport(risky(data["disasterRiskIndex"], curResults, nat, 50), climResults, weight)
            totalWeight += weight


        # specific disasters
        print()
        print()
        print("How important is the potential of specific natural disasters?")
        print("0 = not important, 10 = very important.")
        weight = intCheckTen()
        print() 

        if (weight != 0):
            round = 1

            while True:
                print("Do you have any natural disaster you are particularly fearful of?")
                print("Avalanche = 1, Coastal flooding = 2, Cold Wave = 3, Drought = 4, Earthquake = 5")
                print("Hail = 6, Heatwave = 7, Hurricane = 8, Ice storm = 9, Landslide = 10")
                print("Lightning = 11, River flooding = 12, Strong winds = 13, Tornado = 14")
                print("Tsunami = 15, Volcano = 16, Wildfire = 17, Winter Weather = 18")

                priority1 = intCheck()
                nature = {1:"avalanche", 2:"coastalFlooding", 3:"coldWave", 4:"drought", 5:"earthquake",
                            6:"hail", 7: "heatWave", 8:"hurricane", 9:"iceStorm", 10:"landSlide",
                            11:"lightning", 12:"riverFlooding", 13:"strongWinds", 14:"tornado",
                            15:"tsunami", 16:"volcano", 17:"wildfire", 18:"winterWeather"}
                
                print("How much should you priorize this natural disaster in metros?")
                print("0 = high risk, 100 = low risk")
                priority2 = abs(100-intCheck())

                if(round == 1):
                    curResults = Counter(minMax(data[nature[priority1]], curResults, priority2))
                    round += 1
                else:
                    curResults = Counter(curResults) + Counter(minMax(data[nature[priority1]], curResults, priority2))
                
                cont = int(input("Do you want to adjust any other transportation methods? 1 = yes, 0 = no. "))
                if(cont == 0):
                    break

            # divides curResults by the number of rounds
            curResults = Counter({key : curResults[key] / round for key in curResults})
            climResults = addToReport(curResults, climResults, weight)
            totalWeight += weight
        
        climResults = Counter({key : climResults[key] / totalWeight * climWeight for key in climResults})
        totalWeight = 0



    if(cultWeight != 0):
        print()
        print("CULTURAL ASPECTS OF THE METRO")

    #sports
        print()
        print()
        print("How important is it for the metro to have sports teams?")
        print("0 = not important, 10 = very important.")
        weight = intCheck()
        print()

        if (weight != 0):
            round = 0
            curResults1 = curResults
            while True:
                print("Which sports do you care about?")
                print("All = 1, Baseball = 2, Football = 3, Basketball = 4, Hockey = 5, Soccer = 6")

                priority1 = intCheck()
                houses = {1:"sportsTeams", 2:"MLBteams", 3:"NFLteams", 4:"NBAteams", 5:"NHLteams", 6:"MLSteams"}
                            
                for x in data:
                    if(data[x] != 0):
                        curResults1[x] = 10
                    else:
                        curResults1[x] = 0

                if(round != 0):
                    curResults = Counter(curResults) + Counter(curResults1)
                round += 1

                cont = int(input("Do you want to adjust any other sports? 1 = yes, 0 = no. "))
                if(cont == 0):
                    break

            # divides curResults by the number of rounds
            curResults = Counter({key : curResults[key] / round for key in curResults})
            results = addToReport(curResults, cultResults, weight)
            totalWeight += weight

        cultResults = Counter({key : cultResults[key] / totalWeight * cultWeight for key in cultResults})
        totalWeight = 0



#RESULTS
    print()
    print()
    print()
    print("FINAL RESULTS")
    print()

    # results: declare the best metros for the user
    results = Counter(demoResults) + Counter(econResults) + Counter(homeResults) + Counter(climResults) + Counter(cultResults)
    results = Counter({key : results[key] /sectionWeight for key in results})
    print()
    print(results)
    print(totalWeight)
    break

