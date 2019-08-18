import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
#function to convert an image to sketch
def canny(image):
    #to change the image to gray scale
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    #to reduce noice in grayscale image
    blur=cv2.GaussianBlur(gray,(5,5),0)
    #used to meashure the change in intensity and produce a outline of gray image
    #syntax: cv2.Canny(image,low_threshold,high_threshold)
    image=cv2.Canny(blur,50,150)
    return image
#function to calculate average slope optimised
def average_slope_intercept(image,lines):
    #left_fit --> empty list to store leftlane lines
    #right_fit --> empty list to store rightlane HoughLines
    left_fit=[]
    right_fit=[]
    for line in lines:
        #reshape each pt in 1D
        x1,y1,x2,y2 = line.reshape(4)
        #fit 1st degree polynomial
        parameters = np.polyfit((x1,x2),(y1,y2),1)
        slope=parameters[0]
        #y intercept
        intercept=parameters[1]
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average =np.average(right_fit,axis=0)
    #print(left_fit_average,"left")
    #print(right_fit_average,"right")
    left_line=make_coordinates(image,left_fit_average)
    right_line=make_coordinates(image,right_fit_average)
    print(left_line,"left")
    print(right_line,"right")
    return np.array([left_line,right_line])

#function to make coordinates
def make_coordinates(image,line_parameters):
    slope,intercept = line_parameters
    print(image.shape)
    y1=image.shape[0]
    y2=int(y1*(3/5))
    #seting values
    x1=int((y1-intercept)/slope)
    x2=int((y2-intercept)/slope)
    return np.array([x1,y2,x2,y2])


#function to get the lines to display
def display_lines(image,lines):
    #creating an empty black image as the original images
    line_image=np.zeros_like(image)
    #check array is not empty
    if lines is not None:
        for line in lines:
            '''print(line) #the output will be a 2D array ((ie) a coloured image)we need 1D array'''
            #reshaping the 2D array to 1D array
            x1,y1,x2,y2 =line.reshape(4)
            #to draw the line on black images
            #syntax: cv2.line(line_image black image,coordinate of space,color(B,G,R),intensity)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
            return line_image





#function to get the region of intrest
def region_of_intrest(image):
    #to get the height of an image
    height = image.shape[0]
    #dimension of our triangluar polygon
    triangle = np.array([[(200,height),(1000,height),(550,250)]])
    #setting up mask for our polygon which is totally black image like our original
    mask = np.zeros_like(image)
    #filling the mask with our polygon
    cv2.fillPoly(mask,triangle,255)
    #performing bitwise and operation on both the images to get specific region_of_intrest
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image




image = cv2.imread('test_image.jpg')
#######using matplot
'''limage=plt.imshow(image,cmap='gray')
plt.show()
#print(limage)'''
############
#to copy the image
limage=np.copy(image)
canny_image=canny(limage)
#to get images coordinates use matplot library
'''plt.imshow(canny_image)
plt.show()'''
dg=np.pi/180#math.degrees(math.pi / 180)
cropped_image = region_of_intrest(canny_image)
#detecting lines in cropped image by the function HoughLines
#syntax: cv2.HoughLinesP(#src_image,no of pixels,1 degree position(pi/180),minimum no if intersection,a placeholder array (empty array),length of line in pixels that are detected,max_dist_between pixels that are allowed to be a single line)
lines = cv2.HoughLinesP(cropped_image,2,math.radians(1),15,np.array([]),minLineLength=40,maxLineGap=5)
#print("xxxx",dg)
averaged_lines=average_slope_intercept(limage,lines)
line_image = display_lines(limage,lines)
#adding lines to image (original_image,multiply,line_image,multiply, scalar_values)
combo_image=cv2.addWeighted(limage,0.8,line_image,1,1)
cv2.imshow("combo",combo_image)
cv2.imshow("canny",canny_image)
cv2.imshow("crop",cropped_image)
cv2.imshow("image",image)
#cv2.imwrite("combo.png",combo_image)
#cv2.imwrite("canny.png",canny_image)
#cv2.imwrite("crop.png",cropped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
