"""
-------------------------------------------------------------------------------------------------
Description: Uses output .tif files from ESI_tif_clip.py to extract ESI values from
 specific sites as referenced from the input meta .csv file. These .tif files were
 originally obtained from https://climateserv.servirglobal.net/ where I selected for
 ESI downloads.

Usage example: python tif2select_pt.py /path/to/tif/files/ ./metadata.csv
Usage example: python tif2select_pt.py /path/to/tif/files/ /path/to/metadata.csv

help: python tif2select_pt.py --help

File Name: tif2select_pt.py
Author: Carol A. Rowe
Date Created: 2021-05-03

NOTES:
    - input tif files are expected to be named by date followed by '_CLIP.tif'.
    - You can easily modify this script to read in .tif files without the "_CLIP"
    - Since the .tif file contains a date in its name, I made the final dataframe
      to contain a datetime column as headed "Date".
    - metadata.csv input file must contain columns labeled:
        longitude
        latitude
        stationTriplet
    - see GitHub for raster_env.yml and other files
        https://github.com/carol-rowe/ClimateSERV_ESI_data

"""

import pandas as pd
import glob
from pathlib import Path
import rasterio as rs
import argparse

__author__ = "Carol A. Rowe"

def tif2select_pts(directory, metadata):
    tif_Counter = len(glob.glob1(directory, '*.tif'))
    meta = pd.read_csv(metadata)
    num_pts = meta.shape[0]
    upper_range = tif_Counter * num_pts

    # function to go through each tif file and extract the date, esi, and station name
    def tif_to_esi(meta, directory, upper_range, num_pts):
        table = pd.DataFrame(index=range(0,upper_range),columns=['Date', 'ESI', 'station'])
        # i counts from 0 through number of lines in the output dataframe (the upper_range)
        i=0
        # in case other files in folder, want those where last 4 chars are .tif
        for filepath in glob.glob(directory + "*_CLIP.tif"):
            base = Path(filepath).stem
            date = base.split('_')[0]
            # ind counts 1 - 18 since there are 18 stations
            ind = 0
            dataset = rs.open(filepath)
            for ind in range(0,num_pts):
                x = meta.loc[ind,'longitude']
                y = meta.loc[ind, 'latitude']
                stn = meta.loc[ind, 'stationTriplet']
                row, col = dataset.index(x,y)
                data_array = dataset.read(1)
                # copy data to Date col
                table['Date'].loc[i] = date
                # get esi
                table['ESI'].loc[i] = data_array[int(row), int(col)]
                # add the station name
                table['station'].loc[i] = stn
                ind += 1
                i += 1
                # using print statements so you can see what is happeining with the two variables
                #print(ind)
                #print(i)
        table['Date'] = table['Date'].apply(pd.to_datetime)
        return table

    my_df = tif_to_esi(meta, directory, upper_range, num_pts)
    my_df.to_csv(directory + 'ESI_tif2select_pt.csv', index='False')



# if name in main so that we can run the script by itself (main)
# or, it can be used embedded (import ESI_tf_clip.py) within another script
if __name__ in '__main__':
    # This allows the --help to show the docstring
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # Add the input arguments (2), both of which are mandatory
    parser.add_argument('directory', metavar='directory_to_files', help="Enter the pathway to your tif files. For example: '/home/name/my_tif_files/'")
    parser.add_argument('metadata', metavar='metadata.csv', help="Enter the pathway and filename for your shapefile. i.e. './SCAN_metadata.csv'  File must contain columns: longitude, latitude, stationTriplet")
    # array for all arguments passed to the script
    args = parser.parse_args()

    # now you can access the arguments input by the user and apply to our function
    tif2select_pts(args.directory, args.metadata)