import os
import argparse
import json
import glob
from dense_flow.extract_flow import create_flow_video
from tqdm import tqdm
from dirutils.filetree import File

def compress_streams(video_dir=None, delete_image_files=True, dimension=(342,256), frame_rate=20):
    
    if not os.path.isdir(video_dir):
        return
    
    streams_dir = os.path.join(video_dir,'streams')
            
    create_flow_video(directory=streams_dir, filter='flow_x', video_path=os.path.join(video_dir,'flow_x.avi'), frame_rate=frame_rate, dimension=dimension,delete_image_files=delete_image_files)
    create_flow_video(directory=streams_dir, filter='flow_y', video_path=os.path.join(video_dir,'flow_y.avi'), frame_rate=frame_rate, dimension=dimension,delete_image_files=delete_image_files)

    if delete_image_files:
        # delete if exists rgb files
        files = glob.glob(streams_dir+'/rgb*.jpg')
        files.sort(reverse=False)       
        for x in files:
            os.system('rm '+x)
        # delete streams dir
        os.system('rm -R '+streams_dir)



