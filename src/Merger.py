import os
import pandas as pd

CSVfiles = [f for f in os.listdir('.') if os.path.isfile(f) and len(f) > 4 and f[-4:]==".csv"]


result_df= pd.DataFrame(data={"Page":[],"Visits":[]},columns=["Page","Visits"])

for f in CSVfiles:
    aux_df = pd.read_csv(f)
    print(aux_df)
    result_df = pd.concat([result_df, aux_df], ignore_index=True)


key_df = pd.read_csv("../input/key_1.csv")

submission_df = pd.merge(key_df, result_df, on='Page')

submission_df.to_csv(path_or_buf="../output/fbProphet_first15000TS_with_8missing_submission.csv",columns=["Id","Visits"],index=False)