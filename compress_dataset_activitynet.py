import os
import argparse
import json
import glob
from dense_flow.extract_flow import create_flow_video
from tqdm import tqdm
from dirutils.filetree import File


def compress_streams(dataset_dir='', id_video='', delete_image_files=True, dimension=(342,256), frame_rate=20):
    id_dir = os.path.join(dataset_dir, id_video)   
    streams_dir = os.path.join(id_dir,'streams')

    if not os.path.isdir(id_dir) or not os.path.isdir(streams_dir):
        return
            
    create_flow_video(directory=streams_dir, filter='flow_x', video_path=os.path.join(id_dir,'flow_x.avi'), frame_rate=frame_rate, dimension=dimension,delete_image_files=delete_image_files)
    create_flow_video(directory=streams_dir, filter='flow_y', video_path=os.path.join(id_dir,'flow_y.avi'), frame_rate=frame_rate, dimension=dimension,delete_image_files=delete_image_files)

    if delete_image_files:
        # delete if exists rgb files (flipped)
        files = glob.glob(streams_dir+'/rgb*.jpg')
        files.sort(reverse=False)       
        for x in files:
            os.system('rm '+x)             
        os.system('rm -R '+streams_dir)
