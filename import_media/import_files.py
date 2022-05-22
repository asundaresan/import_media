import argparse
import logging
import os 
import glob 
import datetime 
from typing import Tuple, List

import tqdm

from .exiftool import get_metadata

def get_filenames(paths: List[str], extensions: List[str]=[]) -> List[str]:
    filenames = []
    for path in paths:
        if os.path.isfile(path):
            filenames.append(path)
        elif os.path.isdir(path):
            for ext in extensions:
                files = glob.glob(os.path.join(path, f"*.{ext}"))
                filenames.extend(files)
    return filenames


desc = """ Import files to directory structure.

To import files from a source folder as a dry run with verbose option. 

    import_files ~/Pictures/to_be_imported/nikon/107D7100.1/ -v 

Use the -m option to actually move the files. 

    import_files ~/Pictures/to_be_imported/nikon/107D7100.1/ -vm
"""

def main():
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("filepaths", nargs="+", help="Source folders or filenames")
    parser.add_argument("--dst_photos", "-dp", default="/Users/aravind/Lightroom/Photos", help="Destination folder for photos")
    parser.add_argument("--dst_videos", "-dv", default="/Users/aravind/Lightroom/Videos", help="Destination folder for videos")
    parser.add_argument("--number", "-n", type=int, default=0, help="Number of files to process")
    parser.add_argument("--video", action="store_true", help="Target is a video")
    parser.add_argument("--no-prefix", "-np", action="store_true", help="Do not attach prefix to files")
    parser.add_argument("--move", "-m", action="store_true", help="Move selected files to folder")
    parser.add_argument("--verbosity", "-v", action="count", default=0, help="Verbosity level")
    parser.add_argument("--debug", "-d", action="count", default=0, help="Debug level")
    args = parser.parse_args()
    
    # set logging level 
    console_level = logging.WARN if args.verbosity == 0 else logging.INFO if args.verbosity == 1 else logging.DEBUG
    logging.basicConfig(level=console_level, format='[%(levelname)s] %(message)s')

    dst = args.dst_videos if args.video else args.dst_photos
    logging.info("Destination: %s" % dst)
    if not os.path.exists(dst): 
        logging.fatal("Destination path %s does not exist" % (dst,))
    elif not os.path.isdir(dst):
        logging.fatal("Destination path %s is not a folder" % (dst,))

    extensions_photos =  ["JPG", "jpg", "JPEG", "jpeg",]
    extensions_videos =  ["MOV", "mov", "MP4", "mp4",]
    extensions = extensions_videos if args.video else extensions_photos
    filenames = get_filenames(args.filepaths, extensions=extensions)
    total = len(filenames)
    if args.number > 0:
        print(f"Processing {args.number} of {total} files")
        filenames = filenames[:args.number]

    folders = set()
    moved = 0
    will_move = 0
    num_exists = 0
    for f in tqdm.tqdm(filenames, desc="Importing"):
        try: 
            metadata = get_metadata(f)
            dt = metadata["Create Date"]
        except: 
            logging.warning("Failed to get metdata for %s" % (f,))
            continue
        folder = os.path.join(dst, dt.strftime("%Y"), dt.strftime("%Y-%m")) 
        if folder not in folders: 
            logging.info("New folder: %s" % (folder,))
            folders.add(folder)
        os.makedirs(folder, exist_ok=True)
        basename = os.path.basename(f)
        if not args.no_prefix:
            prefix = dt.strftime("%Y%m%d")
            if not basename.startswith(prefix):
                basename = "%s-%s" % (prefix, basename)
        f2 = os.path.join(folder, basename)
        if not os.path.exists(f2):
            if args.move:
                logging.debug("moving %s to %s" % (f, f2))
                os.rename(f, f2)
                moved += 1
            else:
                will_move += 1
        else:
            num_exists += 1
            logging.info("File exists at destination: %s" % f2)
    if num_exists > 0:
        print(f"{num_exists} files exist in destination")
    if args.move:
        print(f"Moved {moved} files/{total} to {len(folders)} folders")
    else:
        print(f"Use '-m' option to move {will_move} files/{total} to {len(folders)} folders")


