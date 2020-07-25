import argparse
import logging
import exifread
import os 
import glob 
from datetime import datetime

desc = """ Import files to directory structure
"""

if __name__ == "__main__":
  parser = argparse.ArgumentParser( description = desc )
  parser.add_argument( "filenames", nargs = "+", help = "Source folders or filenames" )
  parser.add_argument( "--dst", "-s", default = "/Users/aravind/Lightroom/Photos", help = "Destination folder" )
  parser.add_argument( "--number", "-n", type = int, default = 0, help = "Number of files to process" )
  parser.add_argument( "--move", "-m", action = "store_true", help = "Move selected files to folder" )
  parser.add_argument( "--verbosity", "-v", action = "count", default = 0, help = "Verbosity level" )
  parser.add_argument( "--debug", "-d", action = "count", default = 0, help = "Debug level" )
  args = parser.parse_args()
  
  # set logging level 
  console_level = logging.WARN if args.verbosity == 0 else logging.INFO if args.verbosity == 1 else logging.DEBUG
  logging.basicConfig( level = console_level, format = '[%(levelname)s] %(message)s' )

  dst = args.dst
  logging.info( "Destination: %s" % dst )
  if not os.path.exists( dst ): 
    logging.fatal( "Destination path %s does not exist" % ( dst, ) )
  elif not os.path.isdir( dst ):
    logging.fatal( "Destination path %s is not a folder" % ( dst, ) )

  folders = set()
  moved = 0
  total = 0
  for f in args.filenames:
    filenames = []
    if os.path.isfile( f ):
      filenames.append( f )
    elif os.path.isdir( f ):
      for ext in [ "JPG", "jpg", "JPEG", "jpeg", ]:
        files = glob.glob( os.path.join( f, "*.%s" % ext ) )
        filenames.extend( files )
    if args.number > 0:
      logging.warning( "Processing %d of %d files" % ( args.number, len( filenames ) ) )
      filenames = filenames[:args.number]
    for f in filenames:
      with open( f, "rb" ) as handle:
        tags = exifread.process_file( handle )
      v = str( tags["EXIF DateTimeOriginal"] )
      dt = datetime.strptime( v, '%Y:%m:%d %H:%M:%S' )
      #print( "%s: %s" % ( f, dt ) )
      folder = os.path.join( dst, dt.strftime( "%Y" ), dt.strftime( "%Y-%m" ) ) 
      if folder not in folders: 
        logging.info( "New folder: %s" % ( folder, ) )
        folders.add( folder )
      if not os.path.exists( folder ): 
        logging.info( "Creating folder: %s" % ( folder, ) )
        os.makedirs( folder )
      prefix = dt.strftime( "%Y%m%d" )
      basename = os.path.basename( f )
      if not basename.startswith( prefix ):
        basename = "%s-%s" % ( prefix, basename )
      f2 = os.path.join( folder, basename )
      if args.move:
        if not os.path.exists( f2 ):
          logging.debug( "moving %s to %s" % ( f, f2 ) )
          os.rename( f, f2 )
          moved += 1
        else:
          logging.warning( "File exists at destination: %s" % f2 )
      else:
        logging.debug( "todo: %s to %s" % ( f, f2 ) )
    total += len( filenames )
  logging.warning( "Moved %d files / %d to %d folders" % ( moved, total, len( folders ), ) )


