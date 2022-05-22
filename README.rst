Tool to import photographs
==========================

Tool to move photographs and video files from SD card to folder of structure. :: 

  YYYY/YYYY-MM/

Examples 
--------

Check with a trial run of what files to move where. ::

  uberwald:import_media aravind$ python3 bin/import_files.py ~/Pictures/to_be_imported/nikon/107D7100.1/ -v 
  [INFO] Destination: /Users/aravind/Lightroom/Photos
  [INFO] New folder: /Users/aravind/Lightroom/Photos/2020/2020-08
  [WARNING] Moved 0 files / 130 to 1 folders
    
Add a `move` (`-m`) option to actually move the files. ::

  uberwald:import_media aravind$ python3 bin/import_files.py ~/Pictures/to_be_imported/nikon/107D7100.1/ -vm
  [INFO] Destination: /Users/aravind/Lightroom/Photos
  [INFO] New folder: /Users/aravind/Lightroom/Photos/2020/2020-08
  [WARNING] Moved 130 files / 130 to 1 folders

Using Mac OS Photos 
-------------------

1. Create a smart album on the Photos for the iPhone model that you have. 
2. Connect phone to Mac and import all new photos - these will automatically appear in the smart album. 
3. Select new photos and export photos
