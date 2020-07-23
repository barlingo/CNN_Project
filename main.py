# !./.env/bin/python
"""
Run python module
"""
import argparse
import logging
import scraptube


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s | %(name)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler(__name__ + ".log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", type=str,
                    help="Performs search on yt")
parser.add_argument("-a", "--added_search", type=str,
                    help="Added arguments to main search query add + for each")
parser.add_argument("-d", "--download", action="store_true",
                    help="Downloads videos from query result ")
parser.add_argument("-f", "--format", type=int,
                    help="Format videos into chucks of N seconds")
parser.add_argument("-c", "--clean", type=str,
                    help="Performs data clean of specified folder")

args = parser.parse_args()


if args.search is not None:
    PATH = './output/' + args.search
    query = args.search + ", " + args.added_search
    yt_search = scraptube.search.YoutubeSearch(query)
    youtube_ids = yt_search.to_list()
    logger.info(f'Found {yt_search.count} youtube videos for {args.search},\
          {args.added_search}')

if args.download:
    try:
        extractor = scraptube.down.extractVideos(PATH, youtube_ids)
        logger.info("Starting download...")
        extractor.parallel_download()
        extractor.merge_logs(args.search)
        extractor.purge_logs()
    except NameError:
        logger.error("Search required before downloading files.")

# if args.format:
#     print(f"Trimming videos on {args.format} seconds chunks")
#     PATH = "./output/push up"
#     processor = vedit.SubFolderProcessing(PATH)
#     processor.clip_files(args.format)

if args.clean:
    logger.debug(f"Procesing folder {args.clean}")
    processor = scraptube.label.SubFolderProcessing(args.clean)
    processor.label_videos()
