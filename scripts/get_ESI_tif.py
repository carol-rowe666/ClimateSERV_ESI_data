"""
Description: This retrieves ESI .tif files from the https://climateserv.servirglobal.net/ website. User enters minimum and maximum decimal degree values for longitude and latitude to create a bounding box.

File Name: get_ESI_tif.py
Author: Carol A. Rowe
Date Created: 2021-05-07

Usage: python get_ESI_tif.py xmin = -188.473227 xmax = -84.88908 ymin = 30.223334 ymax = 35.008028

Required inputs (4):
    min and max values of longitude (xmin and xmax) and latitude (ymin and ymax) to create a bounding box for the tif files

Optional inputs (3):
    ESI_type: global ESI 4 week (ESI_4) or global ESI 12 week (ESI_12)
    start: start date. Defualt is toady's date minus one month
    end: end date. Defualt is today's date.

Output: ESI_tif.zip

See help: python get_ESI_tif.py --help

NOTES:
    - see GitHub for climateSERV_env.yml and other files
        https://github.com/carol-rowe/ClimateSERV_ESI_data

"""

import argparse
from datetime import datetime, date
from dateutil.relativedelta import *
import climateserv.api

__author__ = "Carol A. Rowe"

def get_ESI_tif(xmin,xmax, ymin, ymax, esi_Type, startDate, endDate):
    # the dates get a timestamp attached to the end. Remove the time.
    startDate = startDate.strftime('%m/%d/%Y')
    endDate = endDate.strftime('%m/%d/%Y')
    # make a box around the area of interest uisng the lat min and max, and the long min and max
    GeometryCoords = [[xmin, ymax], [xmax, ymax], [xmax, ymin], [xmin, ymin], [xmin, ymax]]
    # assign values to the other needed variables to run the climateserve.api
    # Assign ESI 4-week or 12-week
    DatasetType = str(esi_Type)
    assert (DatasetType == 'ESI_4') or (DatasetType == 'ESI_12'), "esi_Type must be 'ESI_4' or 'ESI_12'"
    # get the average value from the polyogn (vs. min or max)
    OperationType = 'Download'
    # next two variables are not needed for the ESI-4, but still need to assign the '' value to them
    SeasonalEnsemble = ''
    SeasonalVariable = ''
    # we are going to save this to a variable (esi in this case), so use the 'memory_object' as the outfile
    Outfile = 'ESI_tif.zip'
    # Call the climateserv api
    climateserv.api.request_data(DatasetType, OperationType,
                                 startDate, endDate, GeometryCoords,
                                 SeasonalEnsemble, SeasonalVariable, Outfile)

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
    # First 4 arguments are mandatory
    parser.add_argument('xmin', metavar='min_longitude', help="Enter the minimum longitude in decimal degrees for the bounding box.")
    parser.add_argument('xmax', metavar='max_longitude', help="Enter the maximum longitude in decimal degrees for the bounding box.")
    parser.add_argument('ymin', metavar='min_latitude', help="Enter the minimum latitude in decimal degrees for the bounding box.")
    parser.add_argument('ymax', metavar='max_latitude', help="Enter the maximum latitude in decimal degrees for the bounding box.")
    # Next 3 arguments are optional
    parser.add_argument('-t','--esi_Type', help="ESI data type either: ESI_4 or ESI_12. Default = ESI_4", type=str, default='ESI_4', required=False)
    parser.add_argument('-s','--start', help="Start date for query in form of: mm/dd/yyyy. Default = one month previous to today's date", type=invalid_date, default=(date.today() - relativedelta(months=1)).strftime('%m/%d/%Y'), required=False)
    parser.add_argument('-e', '--end', help="End date for query in form of: mm/dd/yyyy. Default = today's date", type=invalid_date, default=datetime.now().strftime('%m/%d/%Y'), required=False)

    # Array for all arguments passed to script:
    args = parser.parse_args()
    # Now, we can access the arguments input by the user (or use defaults), and apply to our function
    get_ESI_tif(args.xmin, args.xmax,args.ymin,args.ymax, args.esi_Type, args.start, args.end)
