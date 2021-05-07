"""
Description: This retrieves ESI data from the https://climateserv.servirglobal.net/ website for specific point locations.

File Name: get_ESI_select_pt.py
Author: Carol A. Rowe
Date Created: 2021-05-06

Usage: python get_ESI_select_pt.py /location/to/metadata_file.csv

required input: metadata file. A csv file containing latitude, longitude, and stationTriplet columns.
                latitude and longitude should be in decimal degrees
optional inputs:
    precision: degrees around point location to create a polygon. i.e. 0.0001
        any value >= 0.001 will return the same ESI value
    ESI_type: global ESI 4 week (ESI_4) or global ESI 12 week (ESI_12)
    start: start date. Defualt is toady's date minus one month
    end: end date. Defualt is today's date.

See help: python get_ESI_select_pt.py --help

NOTES:
    - see GitHub for raster_env.yml and other files
        https://github.com/carol-rowe/ClimateSERV_ESI_data

"""

import pandas as pd
import argparse
from datetime import datetime, date
from dateutil.relativedelta import *
import time
import climateserv.api

__author__ = "Carol A. Rowe"

def get_ESI_select_pt(metadata, precision, esi_Type, startDate, endDate):
    # the dates get a timestamp attached to the end. Remove the time.
    startDate = startDate.strftime('%m/%d/%Y')
    endDate = endDate.strftime('%m/%d/%Y')
    # This file contains the station name, and corresponding longitudes and latitudes (and other data that we don't need)
    meta = pd.read_csv(metadata)
    # loop through all rows in the meta file:
    df_master = pd.DataFrame()
    for i in range(0, meta.shape[0]):
        print("index {} out of {}.".format(i, meta.shape[0]))
        # assing longitude, latitude, and station to variables
        x = meta.loc[i, 'longitude']
        y = meta.loc[i, 'latitude']
        stn = meta.loc[i, 'stationTriplet']
        # factor for which we will add/sub. to form the polygon
        precision = precision
        # create the polygon around the station location
        GeometryCoords = [[x - precision, y + precision], [x + precision, y + precision],
                          [x + precision, y - precision], [x - precision, y - precision],
                          [x - precision, y + precision]]
        # assign values to the other needed variables to run the climateserve.api
        # Getting the ESI 4-week data
        DatasetType = str(esi_Type)
        # get the average value from the polyogn (vs. min or max)
        OperationType = 'Average'
        # enter dates of interest
        EarliestDate = str(startDate)
        #print(EarliestDate)
        LatestDate = str(endDate)
        #print(LatestDate)
        # next two variables are not needed for the ESI-4, but still need to assign the '' value to them
        SeasonalEnsemble = ''
        SeasonalVariable = ''
        # we are going to save this to a variable (esi in this case), so use the 'memory_object' as the outfile
        Outfile = 'memory_object'
        # Call the climateserv api
        esi = climateserv.api.request_data(DatasetType, OperationType,
                                           EarliestDate, LatestDate,
                                           GeometryCoords,
                                           SeasonalEnsemble,
                                           SeasonalVariable,
                                           Outfile)
        # convert the nested dictionaries of esi into a dataframe
        # this results in a single column which contains another dictionary
        esi2 = pd.DataFrame.from_dict(esi)
        # convert the esi output to a dataframe - this will take two steps
        # this first step results in all data as a single 'data' column which contains a dictionary
        df = pd.concat([esi2.drop(['data'], axis=1), esi2['data'].apply(pd.Series)], axis=1)
        # Check to see if there is any data in the dataframe
        assert df.shape[0] > 0, "There is no data. Please try using other dates."
        # there is one remaining dictionary to split
        df = pd.concat([df.drop(['value'], axis=1), df['value'].apply(pd.Series)], axis=1)
        # add station name to the dataframe
        df['station'] = stn
        # append each station's data to the master dataframe
        df_master = df_master.append(df)
        # print statement so you can see the size of the master dataframe as it grows...
        print(df_master.shape)
        # not sure if this sleep time is needed. First time I ran the full script, it crashed. I added this and it worked.
        # in past web-scraping experience, adding the time-out can keep a user from getting blocked-out from too many reuquest. However, I don't think that should be an issue for this website
        time.sleep(4)

    # I prefer the date as per the ISO standard: yyyy-mm-dd
    df_master['date'] = df_master['date'].apply(pd.to_datetime)
    # don't need the workid or the epochtime. Just select desired columns
    df_master1 = df_master[['date', 'avg', 'station']]
    # Finally, make sure you save the final dataframe!!!!
    df_master1.to_csv('./poly_ESI_df.csv', index=False)

def invalid_date(s):
    try:
        return datetime.strptime(s, '%m/%d/%Y')
    except ValueError:
        raise argparse.ArgumentTypeError('Invalid date. Date format should be: mm/dd/yyyy')

# if name in main so we can run vcf2hetAlleleDepth.py by itself (main)
# or it can still be used if you use it embedded (import vcf2hetAlleleDepth) within another script (name)
if __name__ in '__main__':
    # This allows the --help to show the docstring at the top of this script.
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # First argument is mandatory
    parser.add_argument('metadata', metavar='metadata.csv', help="Enter the pathway and filename for your shapefile. i.e. './SCAN_metadata.csv'  File must contain columns: longitude, latitude, stationTriplet")
    # Next 4 arguments are optional
    parser.add_argument('-p','--precision', help='Area around the point location to make the polygon. Default = 0.00001', type=float, default=0.00001, required=False)
    parser.add_argument('-t','--esi_Type', help="ESI data type either: ESI_4 or ESI_12. Default = ESI_4", type=str, default='ESI_4', required=False)
    parser.add_argument('-s','--start', help="Start date for query in form of: mm/dd/yyyy. Default = one month previous to today's date", type=invalid_date, default=(date.today() - relativedelta(months=1)).strftime('%m/%d/%Y'), required=False)
    parser.add_argument('-e', '--end', help="End date for query in form of: mm/dd/yyyy. Default = today's date", type=invalid_date, default=datetime.now().strftime('%m/%d/%Y'), required=False)
    #parser.add_argument('-e', '--end', help="End date for query in form of: mm/dd/yyyy. Default = today's date",type=validate, default=datetime.now().strftime('%m/%d/%Y'),required=False)

    # Array for all arguments passed to script:
    args = parser.parse_args()
    # Now, we can access the arguments input by the user (or use defaults), and apply to our function
    get_ESI_select_pt(args.metadata, args.precision, args.esi_Type, args.start, args.end)
