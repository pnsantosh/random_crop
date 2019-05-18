import os
import cv2
import numpy as np
# import scipy.misc as smi
# import tensorflow as tf

def check_area_percentage(orig_mask, cropped_mask, value, ratio):
	# print 'orig_mask.shape, mask.shape, value, percent'
	# print orig_mask.shape, cropped_mask.shape, value, ratio

	area_orig = len(np.where(orig_mask == value)[0])
	area_cropped = len(np.where(cropped_mask == value)[0])

	print( 'ratio', float(area_cropped) / float(area_orig), float(area_cropped) / float(area_orig) >= ratio)	
	if float(area_cropped) / float(area_orig) >= ratio:
		return True
	else:
		return False


def random_crop(rgb_img, orig_mask, crop_size, pixel_value, ratio):
    assert rgb_img.shape[0] == orig_mask.shape[0]
    assert rgb_img.shape[1] == orig_mask.shape[1]

    height, width, _ = rgb_img.shape
    w_range = (width - crop_size[0]) // 2 if width>crop_size[0] else 0
    h_range = (height - crop_size[1]) // 2 if height>crop_size[1] else 0
    
    w_offset = 0 if w_range == 0 else np.random.randint(w_range)
    h_offset = 0 if h_range == 0 else np.random.randint(h_range)
    
    cropped_rgb = rgb_img[h_offset:h_offset+crop_size[0], w_offset:w_offset+crop_size[1], :]
    cropped_mask = orig_mask[h_offset:h_offset+crop_size[0], w_offset:w_offset+crop_size[1]]
    
    Area_status = check_area_percentage(orig_mask.copy(), cropped_mask.copy(), pixel_value, ratio)
    
    return cropped_rgb, cropped_mask, Area_status

def main():
	rgb_image = cv2.imread('rgb_img.png')
	mask = cv2.imread('mask.png', cv2.IMREAD_UNCHANGED)
	crop_size = [256, 256]
	
	# set number of maximum trials for random crop (simply to test)
	max_trials = 10

	# area
	min_area_ratio = 0.3

	# actual values in mask
	segment =  {'backgrond':0, 'human':255}
	
	# which segment to be checked for area
	consider = 'human'

	print ('minimum ratio:', min_area_ratio)
	print ('rgb_images mask values:', np.unique(mask))
	print ('Area to be checked for:', consider, segment[consider]  )
	print ('----------------------------')

	for trial in range(max_trials):	
		cropped_img, cropped_mask, Area_status = random_crop(rgb_image.copy(), mask.copy(), crop_size, segment[consider], min_area_ratio)
		
		cv2.imshow('show_mask', cropped_mask)
		cv2.waitKey(0)

		if Area_status:
			cv2.imwrite('random_crop_out/rgb/rgb'+str(trial)+'.png', cropped_img)
			cv2.imwrite('random_crop_out/mask/mask'+str(trial)+'.png', cropped_mask)

	print( '----------------------------')

if __name__=="__main__":
	main()
