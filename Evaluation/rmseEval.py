import os
import argparse
from FrameEval import *
import pickle


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_1','-i1', nargs='+', help="First set of inputs")
    parser.add_argument('--input_2','-i2', nargs='+', help="Second set of inputs")
    parser.add_argument('--output','-o', help="path to output directory")
    args = parser.parse_args()

    input_path_1 = args.input_1
    input_path_2 = args.input_2

    rmsemodel = FrameEval()
    assert len(input_path_1) == len(input_path_2)

    if len(input_path_1) == 1 and os.path.isdir(input_path_1[0]):
        input_path_1 = [os.path.join(input_path_1[0], p) for p in os.listdir(input_path_1[0])]
        input_path_2 = [os.path.join(input_path_2[0], p) for p in os.listdir(input_path_2[0])]

    #the input is a single file
    if len(input_path_1) == 1:
        total_rmse = 0.0
        name = os.path.basename(input_path_1[0])
        rmsemodel.eval(input_path_1, input_path_2)
        output = {}
        output['channel_rmse'] = rmsemodel.channel_rmse
        output['frame_rmse'] = rmsemodel.frame_rmse
        for i in rmsemodel.frame_rmse:
            total_rmse += i
        print 'Total rmse for the given inputs: ', total_rmse / len(rmsemodel.frame_rmse)
        with open(os.path.join(args.output, name + '_rmse.pickle'),'w') as f:
            pickle.dump(output, f)
    else:
        output = {}
        average_rmse = 0.0
        for path1 in input_path_1:
            total_rmse = 0.0
            name1 = os.path.basename(path1)
            for path2 in input_path_2:
                name2 = os.path.basename(path2)
                if name1 == name2:
                    rmsemodel.eval(path1, path2)
                    output['record'] = name1
                    output['channel_rmse'] = rmsemodel.channel_rmse
                    output['frame_rmse'] = rmsemodel.frame_rmse
                    for i in rmsemodel.frame_rmse:
                        total_rmse += i
                    average_rmse += total_rmse / len(rmsemodel.frame_rmse)
                    break
        print 'Total rmse for the given inputs: ', average_rmse / len(input_path_1)
        with open(os.path.join(args.output, 'rmse_results.pickle'), 'w') as f:
            pickle.dump(output, f)








