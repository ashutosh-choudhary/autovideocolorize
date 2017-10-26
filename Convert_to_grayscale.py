from scipy import misc
import os
import sys
import numpy as np


def convert_to_grayscale(image_path):
    image = misc.imread(image_path)
    new_image = np.mean(image, axis=-1)
    return new_image



if __name__=='__main__':
    input_paths = sys.argv[1:-1]
    output_path = sys.argv[-1]
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    for path in input_paths:
        if os.path.isdir(path):
            image_paths = [os.path.join(path, file) for file in os.listdir(path)]
        elif os.path.isfile(path):
            image_paths = [path]
        for i, path in enumerate(image_paths):
            name = os.path.basename(path)
            new_image = convert_to_grayscale(path)
            misc.imsave(os.path.join(output_path, 'grayscale_' + name), new_image)
            print 'done: %d/%d' % (i+1, len(image_paths))
