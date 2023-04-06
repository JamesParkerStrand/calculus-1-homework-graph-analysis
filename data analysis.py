import matplotlib.pyplot as plt
import numpy

# we will use this function to grab all of the necessary information for x and y tables of our points
def dataGrabber(file):

    dataX = []
    dataY = []

    # this loop goes over our entire file txt file
    for i in file:

        # we grab our line, then we split this into an array we can use of x and y tables
        LineOfData = i.split(" ")

        # this is here to check whether our line in our strings dont represent our spaced out x and y values
        if len(LineOfData) > 2 or len(LineOfData) <= 1:
            continue

        # this loop does some integer casting to our individual data line by line.
        for j in range(len(LineOfData)):
            LineOfData[j] = float(LineOfData[j])

        # post our individual x data then our y data line by line in the arrays
        dataX.append(LineOfData[0])
        dataY.append(LineOfData[1])

    return (dataX, dataY)

#open our files first
person_A = open("data for person a.txt")
person_B = open("data for person b.txt")

# gather the data from the file
x_For_A, y_For_A = dataGrabber(person_A)
x_For_B, y_For_B = dataGrabber(person_B)

#put our data inside these two polynomial regression models. accept one is just being treated as a linear regression model.
RegressionModelFor_A = numpy.poly1d(numpy.polyfit(x_For_A, y_For_A, 10))
RegressionModelFor_B = numpy.poly1d(numpy.polyfit(x_For_B, y_For_B, 1))

# we need to somehow know when these two functions intersect, so we need to find the difference of these two functions
difference_Of_TwoFunctions = RegressionModelFor_A - RegressionModelFor_B

#we need to solve for when our function is at equal to 0. which numpy.roots allows us to see whenever we input the right number, we get zero.
print(numpy.roots(difference_Of_TwoFunctions))

# this allows us to gather all of our rates of changes from 0-20, it brute forces like (0,1-20), (1,1-20), (2,1-20) and so on...
def getRatesOfChange(function_A, function_B):
    list_of_rates = []

    for startTime in range(0,20):
        for endTime in range(0,20):
            rate_of_change_A = ( RegressionModelFor_A(endTime) - RegressionModelFor_A(startTime) ) / (endTime - startTime)
            rate_of_change_B = (RegressionModelFor_B(endTime) - RegressionModelFor_B(startTime)) / (endTime - startTime)
            list_of_rates.append([rate_of_change_A,rate_of_change_B,startTime,endTime])
    return list_of_rates

# this allows us to retrieve when our data has the smallest range of change between each other, main equation is rate_A - rate_B, and it is used as an absolute value if statement
def findMininumRateOfChange(rates):

    min = 0

    #variable that changes based on whether a condition is a mininmum between each other, we are calculating the differences of rates a and b
    rate_A = 0
    rate_B = 0

    #variable that changes based on whether a condition is a mininmum between each other, we are calculating the differences of rates a and b
    startTime = 0
    endTime = 0

    #we are just getting the first non nan values between each other
    for i in range(len(rates) - 1):

        #if our first value is a non nan. we need to calculate the distance between rate a and rate b. subtract rate_a - rate_b
        if (not numpy.isnan(rates[i][0]) and not numpy.isnan(rates[i][1]) ):
            min = abs(rates[i][0] - rates[i][1])
            break
        else:
            continue

    # we calculate the distance between rate a and rate b... doing rate_a - rate_b. and just
    for i in range(len(rates) - 1):

        #check for three conditions, check to see if our subtracted rates together is less than our current minimum, whether or not we have a nan, and whether or not our time is more than 4 seconds
        if ( ( abs(rates[i][0] - rates[i][1]) < min ) and ( not numpy.isnan(rates[i][0]) and not numpy.isnan(rates[i][1]) ) and (rates[i][2] >= 4 and rates[i][3] >= 4) ):
            min = abs(rates[i][0] - rates[i][1])

            rate_A = rates[i][0]

            rate_B = rates[i][1]

            startTime = rates[i][2]

            endTime = rates[i][3]
        else:
            continue

    return (rate_A,rate_B,startTime,endTime)

rates = numpy.asarray(getRatesOfChange(RegressionModelFor_A, RegressionModelFor_B))

print(findMininumRateOfChange(rates))

# a variable used so that we can make our regression fit into our graph, which is 0-20 in the x-axis, and 0-80 in the y-axis
myline = numpy.linspace(0, 20, 80)

plt.scatter(x_For_A, y_For_A)
plt.scatter(x_For_B,y_For_B)
plt.plot(myline, RegressionModelFor_A(myline) )
plt.plot(myline, RegressionModelFor_B(myline) )
plt.plot()
plt.show()