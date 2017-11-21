import os
from scipy import misc
import numpy as np



class FrameEval():

    def __init__(self):
        self.channel_rmse = []
        self.frame_rmse = []

    def color_rmse(self, frame1, frame2):
        #print frame1, frame2
        frame1 = misc.imread(frame1)
        frame2 = misc.imread(frame2)[:,:,0:3]
        #print frame2.shape, frame1.shape
        assert frame1.shape == frame2.shape

        '''Pixel wise RMSE per channel'''
        channel_rmse = np.sqrt(np.mean(np.square(frame1 - frame2), axis=(0,1)))      #(3,)

        '''Total RMSE between the frames'''
        frame_rmse = np.mean(channel_rmse)

        return channel_rmse, frame_rmse


    def get_datapaths(self, path):
        frame_paths = []
    
        if os.path.isdir(path):
            image_paths = os.listdir(path)
            for p in image_paths:
                frame_paths.append(os.path.join(path, p))
        elif os.path.isfile(path):
            frame_paths.append(path)
        return frame_paths


    def eval(self, input_path_1, input_path_2):
        #print input_path_1, input_path_2
        input_path_1 = self.get_datapaths(input_path_1)
        input_path_2 = self.get_datapaths(input_path_2)

        assert len(input_path_1) == len(input_path_2)
        #print input_path_1, input_path_2
        if len(input_path_1) == 1:
            channel_rmse, frame_rmse = self.color_rmse(input_path_1[0], input_path_2[0])
            self.channel_rmse.append(channel_rmse)
            self.frame_rmse.append(frame_rmse)
        else:

            for frame1_path in input_path_1:
                frame1_name = os.path.basename(frame1_path)
                for path in input_path_2:
                    frame2_name = os.path.basename(path)
                    if frame2_name == frame1_name:
                        frame2_path = path
                        break

                crmse, frmse = self.color_rmse(frame1_path, frame2_path)
                self.channel_rmse.append(crmse)
                self.frame_rmse.append(frmse)

