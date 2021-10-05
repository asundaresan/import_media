import argparse
import logging
import os 
from datetime import datetime
from import_media.exiftool import get_metadata

desc = """ Import files to directory structure
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("filenames", nargs="+", help="Filenames to print meta data for")
    parser.add_argument("--verbosity", "-v", action="count", default=0, help="Verbosity level")
    parser.add_argument("--debug", "-d", action="count", default=0, help="Debug level")
    args = parser.parse_args()

    # set logging level 
    console_level = logging.WARN if args.verbosity == 0 else logging.INFO if args.verbosity == 1 else logging.DEBUG
    logging.basicConfig(level=console_level, format='[%(levelname)s] %(message)s')

    for f in args.filenames:
        m = get_metadata(f)
        logging.info("%s: %s" % (f, m,))

