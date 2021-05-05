"""
-------------------------------------------------------------------------------------------------
Description: Clips all .tif files in the input directory to the geometry in the input shapefile.

Usage example: python ESI_tif_clip.py /path/to/tif/files/ ./your_shapefile.GeoJSON
Usage example: python ESI_tif_clip.py /path/to/tif/files/ /path/to/shapefile.shp

help: python ESI_tif_clip.py --help

File Name: ESI_tif_clip.py
Author: Carol A. Rowe
Date Created: 2021-05-03

NOTES:
    - This was designed for .tif files with ESI data that I had downloaded from https://climateserv.servirglobal.net/
    - However, this should also work for most any tif file.
    - Likewise, I used a shapefile with the extension .GeoJSON. This should also work with .shp files as well.
    - see GitHub for raster_env.yml and other files
        https://github.com/carol-rowe/ClimateSERV_ESI_data

---------------------------------------------------------------------------------------------------
"""

import argparse
import rasterio as rs
import fiona
from rasterio.mask import mask
from glob import glob
from pathlib import Path

__author__ = "Carol A. Rowe"

def tif_clip(directory, shapefile):
    # make a new subdirectory for the output files
    outpath = directory + "clipped_files/"
    # if subdirectory doesn't already exist, make it
    Path(outpath).mkdir(parents=True, exist_ok=True)

    # open the shapefile that we want to crop the tif to
    # and save the area of interest (aoi) geometry to a variable
    with fiona.open(shapefile) as f:
        my_aoi = [feature['geometry'] for feature in f]
        my_prop = [feature['properties'] for feature in f]
    for filepath in glob(directory+"*.tif"):
        # will want the file basename to create the output filename
        base = Path(filepath).stem
        new_file = base + '_CLIP.tif'
        # open the tif file to be clipped
        # clipping and converting to decimal lat/long
        with rs.open(filepath, "r") as img:
            clipped, transform = mask(img, my_aoi, crop=True)
            # in clipping the area outside the clip has a different null value than within the clipped
            #np.place(clipped, clipped == -9999, -9.9990000e+03)
            # now create the cropped file
            meta = img.meta.copy()
            meta.update({'transform': transform, 'height': clipped.shape[1], 'width': clipped.shape[2]})
            with rs.open(outpath + new_file , 'w', **meta) as dst:
                dst.write(clipped)


# if name in main so that we can run the script by itself (main)
# or, it can be used embedded (import ESI_tf_clip.py) within another script
if __name__ in '__main__':
    # This allows the --help to show the docstring
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # Add the input arguments (2), both of which are mandatory
    parser.add_argument('directory', metavar='directory_to_files', help="Enter the pathway to your tif files. For example: '/home/name/my_tif_files/'")
    parser.add_argument('shapefile', metavar='shapefile', help="Enter the pathway and filename for your shapefile. i.e. './AL_state.GeoJSON'")
    # array for all arguments passed to the script
    args = parser.parse_args()

    # now you can access the arguments input by the user and apply to our function
    tif_clip(args.directory, args.shapefile)