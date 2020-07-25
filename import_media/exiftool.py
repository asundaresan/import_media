import subprocess
import logging
import datetime

def get_metadata( filename, ):
  exifdata = exiftool( filename )
  for key, value in exifdata.items(): 
    logging.debug( "  %20s: %s" % ( key, value, ) )
  metadata = {}
  for key in [ "Create Date", ]:
    if key in exifdata:
      metadata[key] = datetime.datetime.strptime( exifdata[key], '%Y:%m:%d %H:%M:%S' )
  for key in [ "Make", "Model", ]:
    if key in exifdata:
      metadata[key] = exifdata[key]
  return metadata

def exiftool( filename, options = [], debug = 0 ):
  """ Call exiftool and parse the output to return a dict
  """
  exif = {}
  cmd = ["exiftool", filename] + options
  if debug > 0:
    logging.info( "cmd: %s" % cmd )

  try:
    output_raw = subprocess.check_output( cmd )
    if debug > 0:
      logging.info( "output_raw: type = %s, value = %s" % ( type( output_raw ), output_raw ) )
  except:
    logging.error( "exiftool failed on %s" % filename )
    return exif
  try:
    output = str( output_raw.decode( "ascii" ) )
  except UnicodeDecodeError as e:
    logging.error( "%s: UnicodeDecodeError (%s)" % ( filename, e ) )
    return exif

  for line in output.splitlines():
    data = line.split( ":" )
    if len( data ) > 1:
      key = data[0].strip()
      val = ":".join( d for d in data[1:] ).strip()
      exif.update( { key: val } )
      if debug > 0:
        logging.debug( "  %s:%s" % ( key, val ) )
  return exif


def exiftool_get( filename, tags = [], verbose = 0 ):
  """ Get the tag values for tag names in tags 
      The tags here are exiftool option tags (createdate, etc) and not the same as in exif.keys()
  """
  options = list( "-%s" % tag for tag in tags )
  exif = exiftool( filename, options = options, verbose = verbose )
  return exif



def exiftool_set( filename, tagvalues = {}, verbose = 0 ):
  """ Set tag = value for the (tag, value) pairs in tagvalues
      The tags here are exiftool option tags (createdate, etc) and not the same as in exif.keys()
  """
  options = list( "-%s=%s" % ( tag, val ) for ( tag, val ) in tagvalues.items() )
  exif = exiftool( filename, options, verbose = verbose )
  return exif



def get_exif_tag_values( filename, tags, verbose = 0 ):
  """ Get datetime for all tags
  """
  tag_value_dict = {}
  for tag in tags:
    exif = exiftool_get( filename, [tag] )
    for key, val in exif.items():
      try:
        val2 = strptime( val )
        tag_value_dict.update( {tag:val2} )
      except ValueError as e:
        print( "Error reading %s: %s" % ( filename, e ) )
  return tag_value_dict



def set_exif_tag_values( filename, tag_value_dict ):
  """ Set date time for all key, value pairs in tag_value_dict
      The values must be datetime
  """
  exif = { key: val.strftime( "%Y:%m:%d\ %H:%M:%S" ) for key, val in tag_value_dict.items() }
  exiftool_set( filename, exif )




