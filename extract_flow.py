import time
import os
import argparse

def calculate_flow(use_gpu=True, device_id=None, vid_file=None, flow_x=None, flow_y=None, image=None, boundary=20, opt_type=1, step=1, out_type='dir'):
    
    command = ''
    if use_gpu:
        command += './extract_gpu '
    else:
        command += './extract_cpu '

    if device_id is not None:
        command = command + '-d='+str(device_id)+' '
    
    if vid_file is not None:
        command = command + '-f='+vid_file+' '
    else:
        print('No video file informed')
        return

    if flow_x is not None:
        command = command + '-x='+flow_x+' '
    else:
        print('No flow_x destination informed')
        return
    
    if flow_y is not None:
        command = command + '-y='+flow_y+' '
    else:
        print('No flow_y destination informed')
    
    if image is not None:
        command = command + '-i='+image+' '

    if boundary is not None:
        command = command + '-b='+str(boundary)+' ' 
    else:
        print('Boundary is not defined')
        return
    
    if opt_type is not None:
        command = command + '-t='+str(opt_type)+' ' 
    else:
        print('Algorithm is not defined')
        return

    if step is not None:
        command = command + '-s='+str(step)+' '
    else:
        print('Step is not defined')
        return
    
    if out_type is not None and out_type in ['dir', 'zip']:
        command = command + '-o='+out_type
    else:
        print('Output type is not defined or is invalid')
        return

    os.system(command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpticalFlow estimator for CPU or GPU')
    parser.add_argument('-g', '--use_gpu', type=bool, help='True to execute with GPU and False to execute with CPU')
    parser.add_argument('-d', '--device_id', type=int, help='GPU id')
    parser.add_argument('-f', '--file', help='path to the original video')
    parser.add_argument('-x', '--flow_x', help='path to the x direction of the flows')
    parser.add_argument('-y', '--flow_y', help='path to the y direction of the flows')
    parser.add_argument('-i', '--image', help='path to the image of the frame')   
    parser.add_argument('-b', '--boundary', type=int, help='Optical flow value upper and lower limit: values outside of (-bound, bound) are truncated. (Default = 20)')
    parser.add_argument('-t', '--type', type=int, help='optical flow algorithm (0 = Farneback, 1 = TVL1, 2 = Brox). (Default = 1)')
    parser.add_argument('-s', '--step', type=int, help='number of frames to skip when saving optical flow and rgb frames (Default = 1)')
    parser.add_argument('-o', '--out_type', help='output type - dir = images saved in directories -- zip = images saved in zip files')

    args = parser.parse_args()
    calculate_flow(use_gpu=args.use_gpu, device_id=args.device_id, vid_file=args.file, flow_x=args.flow_x, flow_y=args.flow_y, image=args.image, boundary=args.boundary, opt_type=args.type, step=args.step, out_type=args.out_type)
