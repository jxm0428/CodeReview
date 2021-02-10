import pandas as pd

path = 'Oregon Hwy 26 Crash Data for 2019.xlsx'
df = pd.read_excel(path)

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

CrashesDF = df[df['Record Type'] == 1]
VehiclesDF = df[df['Record Type'] == 2]
ParticipantsDF = df[df['Record Type'] == 3]

#CrashesDF = CrashesDF.dropna(axis=1,how='all')
#VehiclesDF = VehiclesDF.dropna(axis=1,how='all')
#ParticipantsDF = ParticipantsDF.dropna(axis=1,how='all')

passOutput = "Assertion Pass"
failOutput = "Assertion Failed"

#Check every record has Crash ID
def test1a():
    for c_id in df['Crash ID']:
        if (c_id == None):
            print(failOutput)
    print(passOutput)


#Check every record has Vehicle ID
def test1b():
    for v_id in df['Vehicle ID']:
        if (v_id == None):
            print(failOutput)
    print(passOutput)


#The DMV crash serial number should between 1-99999
def test2a():
    for crash_serial_num in CrashesDF['Serial #']:
        if (crash_serial_num < 1 or crash_serial_num > 99999):
            print(failOutput)
    print(passOutput)


#The crash hour should between 00-99
def test2b():
    for c_hour in CrashesDF['Crash Hour']:
        if (c_hour < 0 or c_hour > 99):
            print(failOutput)
    print(passOutput)


#Add a new 'date' field include crash month, crash day and crash year
def test3a():
    df['date'] = None
    for d in df['date']:
        if d == None:
            df['date'] = df['Crash Month'].astype(str)\
                         + "/"\
                         + df['Crash Day'].astype(str) \
                         + "/"\
                         + df["Crash Year"].astype(str)
    print(df['date'])


#Add a new 'latitude' field include latitude degrees, minuts and second.
def test3b():
    df['Latitude'] = None
    for lat in df['Latitude'] :
        if lat == None :
            df['Latitude'] = df['Latitude Degrees'].astype(str) \
                             + "/"\
                             + df['Latitude Minutes'].astype(str) \
                             + "/"\
                             + df["Latitude Seconds"].astype(str)
    print(df['Latitude'])


#Check every crash has a record type 1, 2 or 3
def test5a():
    for record_type in df['Record Type'] :
        if record_type is not (1,2,3):
            print(failOutput)
    print(passOutput)

#Check every crash has a unique Crash ID
def test5b():
    if len(df['Crash ID']) > len(set(df['Crash ID'])):
        print(failOutput)
    else:
        print(passOutput)

#Every crash has a participant seq number of a known participant id.
def test6a():
    for i in ParticipantsDF.index:
        if(ParticipantsDF['Participant Display Seq#'][i] == None and ParticipantsDF['Participant ID'][i] == None):
            print('Not pair')


#every crash has a crash id with a known crash serial number
def test6b():
    for i in CrashesDF.index:
        if (CrashesDF['Serial #'][i] == None and ParticipantsDF['Crash ID'][i] == None):
            print('Not pair')


#Crashes happens more in winter(months 12, 1, 2) than summer(months 6 , 7, 8)
def test7a():
    countWinter = 0
    countSummer = 0
    for crash in CrashesDF['Crash Month']:
        if crash in (12,1,2):
            countWinter += 1
        if crash in (6,7,8):
            countSummer += 1

    print("W : S", countWinter, countSummer)
    if(countWinter < countSummer):
        print("Summer has more crashes")

    else:
        print("Winter has more crashes")


#Crashes happens more in night(18-23 and 0-5) than day(6-17)
def test7b():
    countNightcrash = 0
    countdaycrash = 0
    for crash_hour in CrashesDF['Crash Hour']:
        if crash_hour in range(6,17):
            countdaycrash += 1
        else :
            if crash_hour != 99:
                countNightcrash += 1
    print("D : N",countdaycrash,countNightcrash)
    if countNightcrash < countdaycrash:
        print("Crash happens more in day then night")
    else:
        print("Crash happens more in night then day")

test5b()


