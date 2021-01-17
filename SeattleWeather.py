import csv
import numpy as np

# read in dates, precipitation, and temperatures from csv file and append to array days
with open('Seattle2014.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x = np.array([int(row['DATE']), int(row['PRCP']), int(row['TMAX']), int(row['TMIN'])])
        if int(row['DATE']) == 20140101:
            days = np.array([x])
        else:
            days = np.append(days,[x],axis=0)

# How many days out of the year does it actually rain?
# count how many nonzeros are in the array days and assign variable to the value for the second column for precipitation
nonzeros_count = np.count_nonzero(days,axis=0)
days_rain = nonzeros_count[1]

# What is the average and standard deviation of precipitation (in inches) when it does rain?
# average rain
# creates an array for days it rains and calculates averages of its columns
days_itrains = days[days[:,1] != 0]
print(days_itrains)
rain_avgs = np.mean(days_itrains,axis=0)
print(rain_avgs)
# assign average from second column to variable, convert from mm to inches, and round to the tenths place
avg_rain = np.round(rain_avgs[1]*0.0393701, 1)
print(avg_rain)

# standard deviation
# calculate the standard deviation of each column in array days_itrains
std = np.std(days_itrains, axis=0)
# assign stdev from second column to variable, convert from mm to inches, and round to the tenths place
std_rain = np.round(std[1]*0.0393701, 1)

# subarrays for each month
jan = days[:31,:4]
feb = days[31:59,:4]
mar = days[59:90,:4]
apr = days[90:120,:4]
may = days[120:151,:4]
jun = days[151:181,:4]
jul = days[181:212,:4]
aug = days[212:243,:4]
sep = days[243:273,:4]
octo = days[273:304,:4]
nov = days[304:334,:4]
dec = days[334:365,:4]

# lists of subarrays and month names
months = {'January': jan, 'February': feb, 'March': mar, 'April': apr, 'May': may, 'June': jun, 'July': jul, 'August': aug, 'September': sep, 'October': octo, 'November': nov, 'December': dec}
month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']

# calculate days/inches of rain and min/max temp per month
def month_statistics(month_name, month):

    # How many days does it rain per month?
    # counts number of nonzeros in month array and assigns second column value to a variable
    nonzeros = np.count_nonzero(month,axis=0)
    month_rain = nonzeros[1]
    
    # How many total inches does it rain per month?
    # calculates sums of each column, assigns variable to second column sum, converts from mm to inches and rounds to the tenths place
    sums = np.sum(month,axis=0)
    month_inches = np.round(sums[1]*0.0393701, 1)

    # What is the minimum and maximum recorded temperature per month?
    # calculates min and max of each column and assigns value for third and fourth columns to variables
    mins = np.min(month,axis=0)
    month_mintemp = mins[3]

    maxs = np.max(month,axis=0)
    month_maxtemp = maxs[2]

    # creates an array to output the calculated statistics for each month
    month_data = [month_name, month_rain, month_inches, month_mintemp, month_maxtemp]

    return month_data

# appends the statistics of each month to the list
months_data = []
for month_name in months:
    months_data.append(month_statistics(month_name, months[month_name]))

# Is it hot rain or chilly rain? 
# What is the average minimum and maximum recorded temperatures on days that it rains? 
# How does that compare to days that it doesn’t rain?

# assigns variables to columns 3 and 4 of the array of averages for when it does rain and rounds to the tenths place
rain_mintemp = np.round(rain_avgs[3], 1)
rain_maxtemp = np.round(rain_avgs[2], 1)

# creates an array for days it doesn't rain and calculates averages of its columns
days_norain = days[days[:,1] == 0]
norain_avgs = np.mean(days_norain,axis=0)
# assigns variables to averages from columns 3 and 4 and rounds to the tenths places
norain_mintemp = np.round(norain_avgs[3], 1)
norain_maxtemp = np.round(norain_avgs[2], 1)
# On average it is usually hotter on days that it doesn't rain as compared to days that it does rain
# However, it is still pretty warm on average on days that it does rain

# writes annual statistics to a file with labels
g = open('Seattle_Data.csv','w')
g.write('Annual Statistics:\n')
g.write('# of days it rains: ')
g.write(str(days_rain))
g.write('\n')
g.write('Avg (stdev) rainfall: ')
g.write(str(avg_rain))
g.write(' +/- ')
g.write(str(std_rain))
g.write(' inches\n')
g.write('Avg min & max temperature on rainy days: ')
g.write(str(rain_mintemp))
g.write(' F - ')
g.write(str(rain_maxtemp))
g.write(' F\n')
g.write('Avg min & max temperature on non-rainy days: ')
g.write(str(norain_mintemp))
g.write(' F - ')
g.write(str(norain_maxtemp))
g.write(' F\n\n')
g.write('Monthly Statistics:\n')

# writes monthly statistics to the csv file
with g:
    writer = csv.writer(g)
    writer.writerow(['Month', '# days it rains', '# inches of rain', 'Min temp (F)', 'Max temp (F)'])
    for month_data in months_data:
        writer.writerow(month_data)

g.close()