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
            if os.path.isfile(path):
                name = os.path.basename(path)
                new_image = convert_to_grayscale(path)
                misc.imsave(os.path.join(output_path, name), new_image)
                print 'done: %d/%d' % (i+1, len(image_paths))
            else:
                dirname = os.path.basename(path)
                outdir = os.path.join(output_path, dirname)
                if not os.path.exists(outdir):
                    os.mkdir(outdir)
                filelist = os.listdir(path)
                for j, name in enumerate(filelist):
                    filepath = os.path.join(path, name)
                    new_image = convert_to_grayscale(filepath)
                    misc.imsave(os.path.join(outdir, name), new_image)
                    print 'done: %d/%d for folder %d/%d' % (i + 1, len(filelist), j, len(image_paths))
