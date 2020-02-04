# extract only flow_x and flow_y... images are discarded
python extract-flow.py -g True -f /tmp/flow/test.avi -x /tmp/flow/flow_x -y /tmp/flow/flow_y -i /dev/null -b 20 -t 1 -d 0 -s 1 -o=zip