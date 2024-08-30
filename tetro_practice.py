# Turan Tashkin
# Metro-advisor
# 8/29/2023

import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
import plotly.offline as py
import math as m
from collections import Counter


st.title('Tetro')


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


#PROGRAM


print()
print()
print()
print('*** WELCOME TO TETRO! ***')
print("Enter x at anytime to quit.")
print()
print()

weight = int()
totalWeight = 0

# report: creates a new report, where everything will be saved

data1 = pd.read_excel(io="C:\\Users\\turan\\Documents\\metroData.xlsx", sheet_name="metroData", index_col='metro')
report1 = pd.read_excel(io="C:\\Users\\turan\\Documents\\metroData.xlsx", sheet_name="report", index_col='metro')

data = data1.to_dict()
report = report1.to_dict()
results = report["results"]
regions = report["region"]
curResults = report["curResults"]
demoResults = report["base1"]

# questions: where questions will be asked and functions will be called

while True:

    print("Please determine, on a scale of 0 to 10, how important these aspects of a city are to you:")
    print("DEMOGRAPHICS,    ECONOMY,    HOME AND TRANSPORTATION,    CLIMATE,    CULTURE")
    print("0 = not important, 10 = very important")
    print()
    print("Demographics of the metro (age, racial makeup, religiosity, education, politics):")
    demoWeight = 6
    print()


    sectionWeight = demoWeight 


    if(demoWeight != 0):
        print()
        print()
        print()
        print()
        print("** DEMOGRAPHICS OF THE METRO **")

        #ideal size of metro
        print()
        print()
        print("How important is the size of the metro?")
        print("(Do you prefer or need to live in a metro with a small or large population?)")
        weight = 6
        print()

        if(weight != 0):
            
            print("How many people should your ideal metro have? (largest: 20M, smallest: 475K)")        
            print("Please enter your ideal population size.")
            size0 = m.log10(5000000)
            print("Please enter the highest acceptable population. If there is no upper limit, enter 0.")
            size1 = 0
            if size1 == 0:
                size1 = 21000000
            size1 = m.log10(size1) 
            print("Please enter the lowest acceptable population. If there is no lower limit, enter 0.")
            size2 = 0
            if size2 == 0:
                size2 = 475000
            size2 = m.log10(size2)        

            demoResults = addToReport(pop(data["popLog"], curResults, size0, size1, size2, 5.88), demoResults, weight) #5.88 because popLog range is 5.6 to 7.3, difference = 1.7, 10/1.7 = 5.88 because the difference needs to be adjusted to 10
            totalWeight += weight


#RESULTS
    print()
    print("FINAL RESULTS")
    print()

    # results: declare the best metros for the user
    results = Counter(demoResults)
    results = Counter({key : results[key] /sectionWeight for key in results})
    print()


    df = pd.DataFrame.from_dict(results, orient='index', columns=['values'])
    df['region'] = df.index.map(regions)
    df1 = df.sort_values(by='values', ascending=False).head(25)

    data = [go.Bar(x=df1.index, y=df1['values'].round(2), 
                   marker_color=df1['region'].apply(lambda x: {'Northeast': 'deepskyblue', 'South': 'orangered', 
                                                               'West': 'gold', 'Midwest': 'limegreen'}.get(x, 'gray')),
            )]
    
    name = 'd'

    layout = go.Layout(
    title= {'text':'Tetro Results: The Best Metro Areas for ' + name,
            'y': 0.95, 'x': 0.5, 'font':dict(size=30)},
    annotations=[
        dict(
            text="Subtitle: A detailed analysis of metro areas",  # Your subtitle here
            x=0.5,
            y=0.87,

            showarrow=False,
            font=dict(size=12, color="gray")
        )
    ],
    xaxis=dict(title='US Metropolitan Areas'),
    yaxis=dict(title='Scores'),

    )

    # Create the figure with data and layout
    fig = go.Figure(data=data, layout=layout)

    # Plot the figure
    py.iplot(fig)

    break

