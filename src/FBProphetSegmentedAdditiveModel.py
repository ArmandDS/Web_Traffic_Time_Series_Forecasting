import numpy as np
import pandas as pd
import datetime
import copy,sys
from fbprophet import Prophet


startS = int(sys.argv[1])
endS= int(sys.argv[2])
prophet = int(sys.argv[3])
removeOutliers = int(sys.argv[4])

if prophet==1:
    prophet=True
else:
    prophet=False

if removeOutliers==1:
    removeOutliers=True
else:
    removeOutliers=False


#Define prediction period strings for Phase 1
startDate = datetime.date(year=2017,month=1,day=1)
endDate= datetime.date(year=2017,month=3,day=1)
dateStrings=[]
while startDate <=endDate:
    dateStrings.append("_" + startDate.strftime("%Y-%m-%d"))
    startDate = startDate + datetime.timedelta(days=1)
nr_predictions=len(dateStrings)

#Create test DF for Phase 1
startDate = datetime.date(year=2017,month=1,day=1)
endDate= datetime.date(year=2017,month=3,day=1)
testDateArray=[]
while startDate <=endDate:
    testDateArray.append(copy.copy(startDate))
    startDate = startDate + datetime.timedelta(days=1)

test_date_df = pd.DataFrame(testDateArray, columns=["ds"],index=range(0,len(testDateArray)))

#Create train DF for Phase 1
startDate = datetime.date(year=2015,month=7,day=1)
endDate = datetime.date(year=2016,month=12,day=31)
trainDateArray=[]
while startDate <=endDate:
    trainDateArray.append(copy.copy(startDate))
    startDate = startDate + datetime.timedelta(days=1)

train_date_df = pd.DataFrame(trainDateArray, columns=["ds"],index=range(0,len(trainDateArray)))

#Eliminate Nan
train_df = pd.read_csv("../input/train_1.csv").fillna(0)

#We iterate over all series
pageArray = []
VisitsArray = []

if prophet:

    for i in range(startS, endS):
        entry = train_df.iloc[i]
        page = entry[0]

        visits = pd.DataFrame(entry[1:].values,columns=["y"])

        orig = copy.deepcopy(visits)

        if removeOutliers:
            visits['median'] = pd.rolling_median(visits, 50, min_periods=1)
            std_mult = 1.5
            visits.loc[np.abs(visits['y'] - visits['y'].median()) >= (std_mult * visits['y'].std()), 'y'] =\
                visits.loc[np.abs(visits['y'] - visits['y'].median()) >= (std_mult * visits['y'].std()), 'median']



        visits['ds'] = train_date_df
        X = visits



        try:
            #Predict
            m = Prophet()
            m.fit(X)

            print(i)

            #Forecast
            forecast = m.predict(test_date_df)

            # For each series, we are going to write the predictions
            pageArray += [str(page + x) for x in dateStrings]
            VisitsArray += forecast['yhat'].values.tolist()

        except:
            visits = entry[-68:-8].median()
            pageArray += [str(page+x) for x in dateStrings]
            VisitsArray += ([visits] * nr_predictions)

else:
    for i in range(startS, endS):
        entry = train_df.iloc[i]
        page = entry[0]
        visits = entry[-68:-8].median()
        pageArray += [str(page + x) for x in dateStrings]
        VisitsArray += ([visits] * nr_predictions)


result_df= pd.DataFrame(data={"Page":pageArray,"Visits":VisitsArray},columns=["Page","Visits"])

result_df.to_csv(path_or_buf="../partial/"+str(startS)+"_"+str(endS)+".csv",columns=["Page","Visits"],index=False)