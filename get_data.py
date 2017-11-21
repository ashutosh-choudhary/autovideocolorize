import os, sys
import requests
from collections import defaultdict
from pprint import pprint
import select
import numpy

TIMEOUT = 5 # number of seconds your want for timeout

DATA_DIR = 'data'
VERTICAL_ID = 100

def extract_all_video_urls(data_dir_path):

    # Get the verticals metadata
    csv_prefix = "http://www.yt8m.org/csv"
    r = requests.get("{0}/verticals.json".format(csv_prefix))
    verticals = r.json()

    block_urls = defaultdict(list)
    count = defaultdict(int)
    total_count = 0
    # Get all vertical names and their corresponding urls files
    for cat, urls in verticals.items():
        for url in urls:
            jsurl = "{0}/j/{1}.js".format(csv_prefix, url.split("/")[-1])
            block_urls[cat[1:]].append(jsurl)
            count[cat[1:]] += 1 #lazy.
            total_count += 1

    # Display menu and wait for TIMEOUT seconds for response

    print('----------------------------------')
    print(' Id |     Vertical')
    print('----------------------------------')
    print('{0} | {1}'.format(str(0).rjust(3), 'All'))
    for id, vertical in enumerate(block_urls.keys()):
        print('{0} | {1}'.format(str(id+1).rjust(3), vertical))
    print('----------------------------------')


    print("\nPlease enter the id of the vertical you want to download[{0}s]: ".format(TIMEOUT))

    i, o, e = select.select( [sys.stdin], [], [], TIMEOUT)
    if (i):
        try:
            vertical_id = int(sys.stdin.readline().strip()) - 1
            print("\nDownloading '{0}' vertical...".format(block_urls.keys()[vertical_id]))
        except:
            vertical_id = -1
            print("\nDownloading all verticals...")
    else:
        vertical_id = -1
        print("\nDownloading all verticals...")


    vertical_name = 'all' if vertical_id == -1 else block_urls.keys()[vertical_id]

    # Download video urls for all or specified vertical

    ids_by_cat = defaultdict(list)
    urls_path = os.path.join(data_dir_path, 'urls')
    if not os.path.exists(urls_path):
        os.makedirs(urls_path)

    total_downloaded = 0.0
    for cat_name, block_file_urls in block_urls.items():
        downloaded = 0.0
        if vertical_id != -1:
            total_downloaded = downloaded
            total_count = count[cat_name]
        if vertical_name == 'all' or vertical_name == cat_name:
            cat_file = os.path.join(urls_path, "{0}.txt".format(cat_name))
            if os.path.exists(cat_file):
                print("'{0}' vertical already downloaded".format(cat_name))
                continue
            for block_file_url in block_file_urls:
                print("[{0}% | {1}%] Downloading block file: {2} {3}".format(str(round(100.0*downloaded/count[cat_name],1)).rjust(2), str(round(100.0*total_downloaded/total_count,1)).rjust(2), block_file_url, cat_name))
                try:
                    r = requests.get(block_file_url)
                    idlist = r.content.split("\"")[3]
                    ids = [n for n in idlist.split(";") if len(n) > 3]
                    ids_by_cat[cat_name] += ids
                except IndexError, IOError:
                    print("Failed to download or process block at {0}".format(block_file_url))
                downloaded += 1 #increment even if we've failed.
                total_downloaded += 1

            with open(cat_file, "w") as idfile:
                print("Writing ids to {0}.txt".format(cat_name))
                for vid in ids_by_cat[cat_name]:
                    idfile.write("{0}\n".format(vid))
                print("Done.")

def create_dat_dir():
    cwd = os.path.dirname(os.path.abspath(__file__))
    data_dir_path = os.path.join(cwd, DATA_DIR)
    if not os.path.exists(data_dir_path):
        print('\nCreating data directory: {0}\n'.format(data_dir_path))
        os.makedirs(data_dir_path)
    return data_dir_path

if __name__ == "__main__":
    data_dir_path = create_dat_dir()
    extract_all_video_urls(data_dir_path)


