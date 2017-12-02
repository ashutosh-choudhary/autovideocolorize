import sys
import numpy as np
import os
from collections import defaultdict
from scipy import misc

if __name__=='__main__':

	input_paths = sys.argv[1:-1]
	output_path = sys.argv[-1]

	if not os.path.exists(output_path):
		os.mkdir(output_path)

	print 'collecting paths'
	paths = {}
	for path in input_paths:
		if os.path.isdir(path):
			paths[path] = [os.path.join(path, p) for p in os.listdir(path)]
                else:
                    paths[path] = [path]

	print 'all paths collected'

	ensemble_output = {}
	for parent_path, files in paths.items():
		for f in files:
			if os.path.isfile(f):
				name = os.path.basename(f)
				print f, name
				image = misc.imread(f)[:,:,0:3]
				if name not in ensemble_output.keys():
					ensemble_output[name] = image
                                        print image[0,0,:], ensemble_output[name][0,0,:]
				else:
					print name
					ensemble_output[name] = (image/float(len(input_paths)) + ensemble_output[name]/float(len(input_paths)))
                                        print image[0,0,:], ensemble_output[name][0,0,:]
        print float(len(input_paths))
	for key, val in ensemble_output.items():
		misc.imsave(os.path.join(output_path, key), val / float(len(input_paths)))





