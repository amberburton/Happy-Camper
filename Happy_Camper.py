# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import urllib.request
import json
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import datetime

def postcode_to_grid():
    postcode = input("Input postcode of desired camping location: ")
    day = input("Input the day you wish to visit in the form DD")
    month = input("Input the month you wish to visit in the form MM")
    duration =input("Input the number of days you'll want to be there for")
    request = "http://api.postcodes.io/postcodes/" + postcode
    contents = urllib.request.urlopen(request).read()
    d = json.loads(contents)
    eastings = d['result']['eastings']
    northings = d['result']['northings']
    
    #This returns the Easting and Northing points for the 5km square that the met office has recorded data for. 
    EGrid_point = round(eastings/5000) * 5000 -2500
    NGrid_point = round(northings/5000) * 5000 -2500
    
    #This returns the wider group that this 5km square belongs to which is found in the file name.
    File_Epoint = round_down_file(EGrid_point)
    File_Npoint = round_down_file(NGrid_point)
    
    path = "C:/Users/wrigh/Documents/Rainfall/" 
    path1 = "C:/Users/wrigh/Documents/MeanTemp/" 
    file_name = "ukcp09_gridded-land-obs-daily_timeseries_rainfall_" + str(File_Epoint) + "E_" + str(File_Npoint) + "N_19580101-20161231.csv"
    file_name1 = "ukcp09_gridded-land-obs-daily_timeseries_mean-temperature_" + str(File_Epoint) + "E_" + str(File_Npoint) + "N_19600101-20161231.csv"
    csv_file = csv.reader(open(path+file_name), delimiter=",")
    csv_file1 = csv.reader(open(path1+file_name1), delimiter=",")
    data0 = [r for r in csv_file]
    data1 = [r for r in csv_file1]
    day = str(day)
    month = str(month)
    col0 = 0
    col1 = 0
    day_month = month+"-"+day
    
    #Gives the number of years we have rainfall records for, to be used in our x axis in plot.
    year_rainfall = []
    for i in range(59):
        year_rainfall.append(1958+i)
        
    #Gives the number of years we have mean daily temperature records for, to be used in our x axis in plot.
    year_mean_temp = []
    for q in range(57):
        year_mean_temp.append(1960+q)
       
    Rainfall_column = column(data0,EGrid_point,NGrid_point,col0)
    Mean_temp_column = column(data1,EGrid_point,NGrid_point,col1)
    Trip_rainfall = []
    Trip_mean_temp = []
    
    # This plots the historic rainfall and mean temp for every day and outputs expected rainfall and mean temp for each day
    for p in range(int(duration)):
        values0 = []
        values1 = []
        # Plots 
        historic_plot(year_rainfall,(listing(data0,daysafter(day_month,p),Rainfall_column,values0)),"Rainfall in mm on " +daysafter(day_month,p),"Rainfall in mm")
        print(round(sum(listing(data0,daysafter(day_month,p),Rainfall_column,values0))/len(listing(data0,daysafter(day_month,p),Rainfall_column,values0)),2))
        Trip_rainfall.append(round(sum(listing(data0,daysafter(day_month,p),Rainfall_column,values0))/len(listing(data0,daysafter(day_month,p),Rainfall_column,values0)),2))
        historic_plot(year_mean_temp,(listing(data1,daysafter(day_month,p),Mean_temp_column,values1)), "Mean temperature in degrees on "+daysafter(day_month,p),"Mean temperature in degrees")
        print(round(sum(listing(data1,daysafter(day_month,p),Mean_temp_column,values1))/len(listing(data1,daysafter(day_month,p),Mean_temp_column,values1)),2))
        Trip_mean_temp.append(round(sum(listing(data1,daysafter(day_month,p),Mean_temp_column,values1))/len(listing(data1,daysafter(day_month,p),Mean_temp_column,values1)),2))
    
    print(sum(Trip_rainfall)/len(Trip_rainfall))
    print(sum(Trip_mean_temp)/len(Trip_mean_temp))
    
# This function returns the new date after 'd' days.
def daysafter(day_month,d):
    start_date = day_month
    date_1 = datetime.datetime.strptime(start_date, "%m-%d")
    end_date = date_1 + datetime.timedelta(days=d)
    final_date = datetime.datetime.strftime(end_date, '%m-%d')
    return(str(final_date))    
    
# This returns the column in our csv file where we want to extract our records from.
def column(data,EGrid_point,NGrid_point,col):
    for n in range(len(data[0])-1):
        easting = data[0][n]
        northing = data[1][n]
        if easting == str(EGrid_point) and northing == str(NGrid_point):
            return(n)

# This makes a list of all the records for the particular day we want for each year.        
def listing(data,day_month,col,values):
    for i in data:
        if i[0].endswith(day_month):
            values.append(float(i[col]))
    return(values)
    
#  Returns a plot of the historic data for rainfall/ mean temp 
def historic_plot(x,y,title,y_label):
    fig,axs = plt.subplots(1,1)
    b = np.array(x)
    c = np.array(y)
    axs.plot(b,c)
    locator=MaxNLocator(prune='both',nbins=10)
    axs.xaxis.set_major_locator(locator)
    plt.tight_layout()
    plt.xlabel("Year")
    plt.ylabel(y_label)
    plt.title(title)
    fig.show()
    
# This allows us to find the name of the corresponding file as their names are organised by 50000
def round_down_file(num):
    return num - (num%50000)