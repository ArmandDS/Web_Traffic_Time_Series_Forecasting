import os,sys
import pandas as pd

file=str(sys.argv[1])

#CSVfiles = [f for f in os.listdir('../partial') if os.path.isfile(f) and len(f) > 4 and f[-4:]==".csv"]

CSVfiles = os.listdir('../partial')


result_df= pd.DataFrame(data={"Page":[],"Visits":[]},columns=["Page","Visits"])

for f in CSVfiles:
    if f[-4:]==".csv":
        aux_df = pd.read_csv('../partial/'+f)
        result_df = pd.concat([result_df, aux_df], ignore_index=True)



key_df = pd.read_csv("../input/key_1.csv")

submission_df = pd.merge(key_df, result_df, on='Page')
submission_df.to_csv(path_or_buf="../output/"+file,columns=["Id","Visits"],index=False)