import numpy as np
import pandas as pd
import datetime

"""
i=0
entry=train_df.iloc[i]
values=entry[1:].as_matrix()
page=entry[0]

fig=plt.figure()
ax = fig.add_subplot(111)
ax.set(title=str(page))
ax.plot(values)
plt.show()
"""

#Define prediction period strings for Phase 1
startDate = datetime.date(year=2017,month=9,day=13)
endDate= datetime.date(year=2017,month=11,day=13)
dateStrings=[]
while startDate <=endDate:
    dateStrings.append("_" + startDate.strftime("%Y-%m-%d"))
    startDate = startDate + datetime.timedelta(days=1)
nr_predictions=len(dateStrings)

#Eliminate Nan
train_df = pd.read_csv("../input/train_2.csv").fillna(0)


print(len(train_df.index))

#We iterate over all series
pageArray = []
VisitsArray = []
for i in range(0,len(train_df.index)):
    entry = train_df.iloc[i]
    #visits = entry[1:].median()
    visits = entry[-120:].median()
    page = entry[0]
    #For each series, we are going to write the predictions
    pageArray += [str(page+x) for x in dateStrings]
    VisitsArray +=  ([visits]*nr_predictions)


    if i % 5000 == 0:
        print(str(datetime.datetime.now())," ,we have processed series nr: ",i)



result_df= pd.DataFrame(data={"Page":pageArray,"Visits":VisitsArray},columns=["Page","Visits"])

key_df = pd.read_csv("../input/key_2.csv")

submission_df = pd.merge(key_df, result_df, on='Page')

submission_df.to_csv(path_or_buf="../output/median2_last120.csv",columns=["Id","Visits"],index=False)







