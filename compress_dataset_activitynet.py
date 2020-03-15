import os
import argparse
import json
import glob
from extract_flow import create_flow_video
from tqdm import tqdm
from dirutils.filetree import File

def compress_streams(dataset_dir='', id_video='', delete_image_files=True, dimension=(342,256), frame_rate=20):
    id_dir = os.path.join(dataset_dir, id_video)   
    hflipped_dir = os.path.join(id_dir,'hflipped')
    original_dir = os.path.join(id_dir,'original')
    hflipped_streams = os.path.join(hflipped_dir,'streams')
    original_streams = os.path.join(original_dir,'streams')

    if not os.path.isdir(id_dir) or not os.path.isdir(hflipped_dir) or not os.path.isdir(original_dir) or not os.path.isdir(hflipped_streams) or not os.path.isdir(original_streams):
        return
            
    create_flow_video(directory=hflipped_streams, filter='flow_x', video_path=os.path.join(hflipped_dir,'flow_x.avi'), frame_rate=frame_rate, dimension=dimension,delete_image_files=delete_image_files)
    create_flow_video(directory=hflipped_streams, filter='flow_y', video_path=os.path.join(hflipped_dir,'flow_y.avi'), frame_rate=frame_rate, dimension=dimension,delete_image_files=delete_image_files)

    create_flow_video(directory=original_streams, filter='flow_x', video_path=os.path.join(original_dir,'flow_x.avi'), frame_rate=frame_rate, dimension=dimension,delete_image_files=delete_image_files)
    create_flow_video(directory=original_streams, filter='flow_y', video_path=os.path.join(original_dir,'flow_y.avi'), frame_rate=frame_rate, dimension=dimension,delete_image_files=delete_image_files)

    if delete_image_files:
        # delete if exists rgb files (flipped)
        files = glob.glob(hflipped_streams+'/rgb*.jpg')
        files.sort(reverse=False)       
        for x in files:
            os.system('rm '+x)
        
        # delete if exists rgb files (original)
        files = glob.glob(original_streams+'/rgb*.jpg')
        files.sort(reverse=False)
        for x in files:
            os.system('rm '+x)

        # delete hflipped_streams
        os.system('rm -R '+hflipped_streams)

        # delete original_streams
        os.system('rm -R '+original_streams)



def dataset_preprocess(original_dataset_dir='',videos_dir='', file_ids='', start_index=0, end_index=0, dimension=(342,256), frame_rate=20, delete_files=True):
    
    activitynetcaptions = File(original_dataset_dir, load=True)
    ids = json.loads(open(activitynetcaptions.get_file_by_name(file_ids).get_path()).read())
   
    if start_index <= end_index:
        ids = ids[start_index:end_index]
    else:
        ids = ids[end_index:start_index]
    

    for id in tqdm(ids[:]):    
        print(id)
        compress_streams(dataset_dir=videos_dir, id_video=id, delete_image_files=delete_files, dimension=dimension, frame_rate=frame_rate)    


#compress_streams(dataset_dir='/home/valter/teste/activitynet_videos/train',id_video='v_0AjYz-s4Rek', delete_image_files=True, dimension=(342,256), frame_rate=20)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ActivityNet Captions Compress Utility')
    parser.add_argument('-dd', '--original_dataset_dir', help='Path to the original dataset')
    parser.add_argument('-vd', '--videos_dir', help='Path to the videos directory')
    parser.add_argument('-fid', '--file_ids', help='Path to the file containing the youtube ids')
    parser.add_argument('-s', '--start_id', type=int, help='Start index in ids list')
    parser.add_argument('-e', '--end_id', type=int, help='End index in ids list')
    #parser.add_argument('-d', '--dimension', help='Video dimension in the format width-height ex: 342-256')
    parser.add_argument('-fr', '--frame_rate', help='Frame rate')
    parser.add_argument('-df', '--delete_files', type=bool, help='Delete files')        
    args = parser.parse_args()            
    
    #dim = args.dimension.split('-')
    #dimension = (342,256)
    dataset_preprocess(original_dataset_dir=args.original_dataset_dir, videos_dir=args.videos_dir, file_ids=args.file_ids, start_index=args.start_id, end_index=args.end_id, dimension=(342,256), frame_rate=args.frame_rate, delete_files=args.delete_files)

# exemplo de comando
# python compress_dataset_activitynet.py -dd /media/valter/Arquivos/Datasets/actions/activitynet/captions -vd /media/valter/Arquivos/Datasets/actions/activitynet_videos/train -fid train_ids.json -s 0 -e 2000 -fr 20 -df True