# ClimateSERV_ESI_data
Scripts for obtaining and comparing ESI (evaporative stress index) data from https://climateserv.servirglobal.net  
  
## Please see: ESI_flowchart.pdf
![flowchart](ESI_flowchart.pdf)
  
## SCRIPTS  
**SCRIPT:** get_ESI_select_pt.py  
**OUTPUT:** poly_ESI_df.csv  
**DESCRIPTION:** This retrieves ESI data from the https://climateserv.servirglobal.net/ website for specific point locations. User can select type of ESI data (4wk or 12wk), start and end dates, polygon size around the point location.  
  
**SCRIPT**: get_ESI_tif.py  
**OUTPUT**: ESI_tif.zip  
**DESCRIPTION**: This retrieves ESI .tif files from the https://climateserv.servirglobal.net/ website. User enters minimum and maximum decimal degree values for longitude and latitude to create a bounding box. To clip these to a more specific boundary using a .shp or .GeoJSON file, see script: ESI_tif_clip.py. When I first used climatserv, I could input a geometry. However, when I tried later, it gave me an error message about the geometry being too big. Hence, I use a simple bounding box in this script.  
  
**SCRIPT:** ESI_tif_clip.py  
**OUTPUT:** <date>_CLIP.tif (for each input tif file)  
**DESCRIPTION:** Clips all .tif files in the input directory to the geometry in the input shapefile.  
  
**SCRIPT:** tif2select_pt  
**OUTPUT:** ESI_tif2select_pt.csv  
**DESCRIPTION:** Uses output .tif files from ESI_tif_clip.py to extract ESI values from specific sites as referenced from the input meta .csv file. Input metadata file must contain columns: longitude, latitude, stationTriplet. Longitude and latitude are in decimal degrees. The stationTriplet column is just a column of names for the stations - point location names.  
  
## Comparison SCRIPTS:  
**SCRIPT**: merge_esi_csv.py  
**OUTPUT**: master_ESI_CLIP_xyz.csv  
**DESCRIPTION**: Not a stand-alone script. See flowchart for preceeding tif2xyz.sh script which produces <date>_CLIP.csv output files. These files contain xyz data for all pixel coordinates of the .tif files produced by the ESI_tif_clip.py script. xyz data is: long. and lat. for centroids (center of pixel boxes) and their corresponding ESI values.  
  
**SCRIPT**: ESI_output_comparison.py  
**OUTPUT**: comparison_output.txt  
**DESCRIPTION**: Compare the output from our 2 methods of acquiring ESI data (polygon vs tif/row/col method.)
Compare values across the 8 closest pixels (user can change that value).  
To get the closest pixels, I used centroids (or middle of the pixel) long/lats.  
NOTE TO SELF: I should change the distance comparison using the haversine method!!!  
NOTE: This is still in development for stand-alone. I may change output type as well....more to come.
  
## ENVIRONMENT - python packages and versions  
**climateSERV_env.yml**  
If you are not familiar with environments, you should get started. Here's a nice website: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html  
conda env create -f climateSERV_env.yml  
conda activate climateSERV_env  
  
  
## EXAMPE FILES:  
**SCAN_AL_metadata.csv** - metadata file containing the longitude, latitude, and station names (stationTriplet)  
  
