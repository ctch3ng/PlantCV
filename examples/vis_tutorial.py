#!/usr/bin/python

# All codes below are from http://plantcv.readthedocs.io/en/latest/vis_tutorial/

import sys, traceback
import cv2
import numpy as np
import argparse
import string
import plantcv as pcv
#from matplotlib import pyplot as plt

### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r","--result", help="result file.", required= False )
    parser.add_argument("-w","--writeimg", help="write out images.", default=False)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", default=None)
    args = parser.parse_args()
    return args
    
    
### Main pipeline
def main():
    # Get options
    args = options()

    # Read image
    img, path, filename = pcv.readimage(args.image)

    # Pipeline step
    device = 0
    
    debug=args.debug 

    # print('Original image')
    # pcv.plot_image(img)

    # Convert RGB to HSV and extract the Saturation channel
    device, s = pcv.rgb2gray_hsv(img, 's', device, debug)
    # print('Convert RGB to HSV and extract the Saturation channel')
    # plt.imshow(s)
    # plt.show()
    
    # Threshold the Saturation image
    device, s_thresh = pcv.binary_threshold(s, 100, 255, 'light', device, debug)
    # print('Threshold the Saturation image')
    # plt.imshow(s_thresh)
    # plt.show()
    # 
    # Median Filter
    device, s_mblur = pcv.median_blur(s_thresh, 5, device, debug)
    device, s_cnt = pcv.median_blur(s_thresh, 5, device, debug)
    # print('Median Filter')
    # plt.imshow(s_mblur)
    # plt.show()
    # 
    # Convert RGB to LAB and extract the Blue channel
    device, b = pcv.rgb2gray_lab(img, 'b', device, debug)
    # print('Convert RGB to LAB and extract the Blue channel')
    # plt.imshow(b)
    # plt.show()

    # Threshold the blue image
    device, b_thresh = pcv.binary_threshold(b, 160, 255, 'light', device, debug)
    device, b_cnt = pcv.binary_threshold(b, 160, 255, 'light', device, debug)
    # print('Threshold the blue image')
    # plt.imshow(b_cnt)
    # plt.show()
    # Fill small objects
    #device, b_fill = pcv.fill(b_thresh, b_cnt, 10, device, debug)
    # 
    
    # Join the thresholded saturation and blue-yellow images
    device, bs = pcv.logical_or(s_mblur, b_cnt, device, debug)
    
    
    # print('Join the thresholded saturation and blue-yellow images')
    # plt.imshow(bs)
    # plt.show()
    # 
    # Apply Mask (for vis images, mask_color=white)
    device, masked = pcv.apply_mask(img, bs, 'white', device, debug)
    # print('Apply Mask 1 (for vis images, mask_color=white)')
    # plt.imshow(masked)
    # plt.show()
    # 
    # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
    device, masked_a = pcv.rgb2gray_lab(masked, 'a', device, debug)
    device, masked_b = pcv.rgb2gray_lab(masked, 'b', device, debug)

    # Threshold the green-magenta and blue images
    device, maskeda_thresh = pcv.binary_threshold(masked_a, 115, 255, 'dark', device, debug)
    device, maskeda_thresh1 = pcv.binary_threshold(masked_a, 135, 255, 'light', device, debug)
    device, maskedb_thresh = pcv.binary_threshold(masked_b, 128, 255, 'light', device, debug)

    # Join the thresholded saturation and blue-yellow images (OR)
    device, ab1 = pcv.logical_or(maskeda_thresh, maskedb_thresh, device, debug)
    device, ab = pcv.logical_or(maskeda_thresh1, ab1, device, debug)
    device, ab_cnt = pcv.logical_or(maskeda_thresh1, ab1, device, debug)

    # Fill small objects
    device, ab_fill = pcv.fill(ab, ab_cnt, 200, device, debug)

    # Apply mask (for vis images, mask_color=white)
    device, masked2 = pcv.apply_mask(masked, ab_fill, 'white', device, debug)
    # print('Apply Mask 2 (for vis images, mask_color=white)')
    # plt.imshow(masked2)
    # plt.show()
    # 
    #Identify objects
    device, id_objects,obj_hierarchy = pcv.find_objects(masked2, ab_fill, device, debug)

    # 
    # Define ROI
    # device, roi1, roi_hierarchy= pcv.define_roi(masked2, 'rectangle', device, None, 'default', debug, True, 67, 377, -125, -368)
    device, roi1, roi_hierarchy= pcv.define_roi(masked2, 'rectangle', device, None, 'default', debug, True, 1, 1, -1, -1)
    # 
    # Decide which objects to keep
    device,roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img, 'partial', roi1, roi_hierarchy, id_objects, obj_hierarchy, device, debug)
    # 
    # Object combine kept objects
    device, obj, mask = pcv.object_composition(img, roi_objects, hierarchy3, device, debug)
    
    
############### Analysis ################

    outfile=False
    if args.writeimg==True:
        outfile=args.outdir+"/"+filename

    # Find shape properties, output shape image (optional)
    device, shape_header, shape_data, shape_img = pcv.analyze_object(img, args.image, obj, mask, device, debug, args.outdir + '/' + filename)

    # Shape properties relative to user boundary line (optional)
    device, boundary_header, boundary_data, boundary_img1 = pcv.analyze_bound(img, args.image, obj, mask, 1680, device, debug, args.outdir + '/' + filename)

    # Determine color properties: Histograms, Color Slices and Pseudocolored Images, output color analyzed images (optional)
    device, color_header, color_data, color_img = pcv.analyze_color(img, args.image, kept_mask, 256, device, debug, 'all', 'v', 'img', 300, args.outdir + '/' + filename)

    # Write shape and color data to results file
    result=open(args.result,"a")
    result.write('\t'.join(map(str,shape_header)))
    result.write("\n")
    result.write('\t'.join(map(str,shape_data)))
    result.write("\n")
    for row in shape_img:  
        result.write('\t'.join(map(str,row)))
        result.write("\n")
    result.write('\t'.join(map(str,color_header)))
    result.write("\n")
    result.write('\t'.join(map(str,color_data)))
    result.write("\n")
    for row in color_img:
        result.write('\t'.join(map(str,row)))
        result.write("\n")
    result.close()

if __name__ == '__main__':
    main()