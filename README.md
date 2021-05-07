# ClimateSERV_ESI_data
Scripts for obtaining and processing ESI (evaporative stress index) data from https://climateserv.servirglobal.net  
  
## SCRIPTS  
**SCRIPT:** get_ESI_select_pt.py  
**OUTPUT:** poly_ESI_df.csv  
**DESCRIPTION:** This retrieves ESI data from the https://climateserv.servirglobal.net/ website for specific point locations. User can select type of ESI data (4wk or 12wk), start and end dates, polygon size around the point location.  
  
**SCRIPT:** ESI_tif_clip.py  
**OUTPUT:** <date>_CLIP.tif (for each input tif file)  
**DESCRIPTION:** Clips all .tif files in the input directory to the geometry in the input shapefile.  
  
**SCRIPT:** tif2select_pt  
**OUTPUT:** ESI_tif2select_pt.csv  
**DESCRIPTION:** Uses output .tif files from ESI_tif_clip.py to extract ESI values from specific sites as referenced from the input meta .csv file. Input metadata file must contain columns: longitude, latitude, stationTriplet. Longitude and latitude are in decimal degrees. The stationTriplet column is just a column of names for the stations - point location names.  
  
  
## ENVIRONMENT - python packages and versions  
**climateSERV_env.yml**  
If you are not familiar with environments, you should get started. Here's a nice website: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html  
conda env create -f climateSERV_env.yml  
conda activate climateSERV_env  
  
  
## EXAMPE FILES:  
**SCAN_AL_metadata.csv** - metadata file containing the longitude, latitude, and station names (stationTriplet)  
  
