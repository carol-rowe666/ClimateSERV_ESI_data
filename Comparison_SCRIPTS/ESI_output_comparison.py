"""
Description: Compare the output from our 2 methods of acquiring ESI data (polygon vs tif/row/col method.)
Compare values across the 8 closest pixels (user can change that value).
To get the closest pixels, I used centroids (or middle of the pixel) long/lats.
NOTE TO SELF: I should change the distance comparison using the haversine method!!!

File Name: get_ESI_tif.py
Author: Carol A. Rowe
Date Created: 2021-05-10

Usage: python ESI_output_comparison.py SCAN_AL_metadata.csv poly_ESI_df.csv ESI_tif2select_pt.csv master_ESI_CLIP_xyz.csv

THIS IS IN PROGRESS....MAY NOT BE FUNCTIONAL AS A STAND-ALONE SCRIPT AS OF YET!!!!!!
"""

__author__ = "Carol A. Rowe"

import pandas as pd
import argparse

def ESI_output_comparison(metadata, poly_ESI, tif_ESI, xyz, date, num_nearest):
    metad = pd.read_csv(metadata)
    meta = metad[['longitude', 'latitude', 'stationTriplet']]
    poly = pd.read_csv(poly_ESI)
    tif = pd.read_csv(tif_ESI)
    xyz = pd.read_csv(xyz)

    # want the print statements into a txt file
    with open("comparison_output.txt", "a") as f:
        # for each station print out comparison of 8 closest pts in the centroids
        for i in range(0,meta.shape[0]):
            # Getting the actual lat/long coords
            xx = meta.loc[i, 'longitude'].astype(float)
            yy = meta.loc[i, 'latitude'].astype(float)
            print('---------------------NEXT-------------------', file=f)
            print('Actual location: {}', format(xx, yy), file=f)
            # get station name
            stn = meta.loc[i, 'stationTriplet']
            print('Station is: {}'.format(stn), file=f)
            # get the lat and long closest to the centroid lat/long (output from either merge_esi_csv.py or tif2xyz.sh)
            # getting the 8 closest centroids using absolute value of subtracting the actual lat/long to centroid lat/long
            # this returns a pd.Series with the index values of the 8 centroids
            index_xyz = ( xyz['x'].sub(xx).abs() + xyz['y'].sub(yy).abs()).argsort()[:num_nearest]
            # make a list of the index values of the 8 closest centroids
            index_list = index_xyz.values.tolist()
            # use index values to subset the xyz dataframe
            xyz_mini = xyz.iloc[index_list, :]
            # make a new column to show a proxy of dist between pt and centroid using absolute value of simple subtraction
            xyz_mini['abs_min'] = ((xyz_mini['x']-xx).abs()) + ((xyz_mini['y']-yy).abs())

            # get the ESI value from the poly csv file; apply that value to entire new column
            poly_mini = poly[ (poly['station']==stn) & (poly['date']==date)]
            poly_mini.reset_index(drop=True, inplace=True)
            poly_vals = poly_mini.loc[0,'avg']
            # add value to the output dataframe
            xyz_mini['poly'] = poly_vals

            # get the ESI value from the tif csv file; apply that value to entire new column
            tif_mini = tif[ (tif['station']==stn) & (tif['Date']==date)]
            tif_mini.reset_index(drop=True, inplace=True)
            tif_vals = tif_mini.loc[0,'ESI']
            # add value to the output dataframe
            xyz_mini['tif'] = tif_vals

            print(xyz_mini, file=f)

# if name in main so that we can run the script by itself (main)
# or, it can be used embedded (import ESI_tf_clip.py) within another script
if __name__ in '__main__':
    # This allows the --help to show the docstring
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # Add the input arguments: 4 mandatory, 2 optional
    parser.add_argument('metadata', metavar='metadata.csv', help="Enter the pathway and filename for your shapefile. i.e. './SCAN_metadata.csv'  File must contain columns: longitude, latitude, stationTriplet")
    parser.add_argument('poly_ESI', metavar='poly_ESI_df.csv', help="Enter the pathway and filename for your poly_ESI_df.csv file. This is the output file from script:get_ESI_select_pt.py")
    parser.add_argument('tif_ESI', metavar='ESI_tif2select_pt.csv', help="Enter the pathway and filename for your ESI_tif2select_pt.csv file. This is the output file from script: tif2select_pts.py")
    parser.add_argument('xyz', metavar='master_ESI_CLIP_xyz.csv', help="Enter the pathway and filename to your master_ESI_CLIP_xyz.csv or individual <date>_CLIP.csv file. Output from either tif2xyz.sh or merge_esi_csv.py")

    # Next 2 arguments are optional
    parser.add_argument('-d', '--date', help="Enter date of ESI file as yyyy-mm-dd", type=str,
                        default='2021-03-30', required=False)
    parser.add_argument('-n', '--num_nearest',
                        help="Enter the number of nearest centroids you want to compare to. Default = 8",
                        type=int, default=8, required=False)

    # array for all arguments passed to the script
    args = parser.parse_args()

    # now you can access the arguments input by the user and apply to our function
    ESI_output_comparison(args.metadata, args.poly_ESI, args.tif_ESI, args.xyz, args.date, args.num_nearest)
