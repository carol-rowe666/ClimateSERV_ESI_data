import pandas as pd
from glob import glob
from pathlib import Path

directory = '/home/carol/Dropbox/UAH_project/Corey_start/ESI/temp3/tif2csv_files/'
master_df = pd.DataFrame()
for filepath in glob(directory + "20*_CLIP.csv"):
    base = Path(filepath).stem
    print(base)
    date = base.split('_')[0]
    # will want the file basename to create the output filename
    df = pd.read_csv(filepath)
    df['Date'] =date
    df['Date'] = df['Date'].apply(pd.to_datetime)
    #print(df.shape[0])
    master_df = master_df.append(df, ignore_index=True,sort=False)
    #print(master_df.shape[0])

#master_df['Date'] = master_df['Date'].apply(pd.to_datetime)
master_df.to_csv(directory + 'master_ESI_CLIP_xyz.csv', index=False)
print(master_df.shape)
