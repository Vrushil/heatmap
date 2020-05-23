'''
To create a heatmap  that shows recent movements for a video or camera
'''
import numpy as np
import cv2
import copy
import  time
def main():
    cap = cv2.VideoCapture(0)
    # pip install opencv-contrib-python
    
    fgbg=cv2.createBackgroundSubtractorMOG2()  # for subtracting the background which helps to detect any movements
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    last_recorded_time_1 = time.time() # initializing last recorded time as current time
    
    first_iteration_indicator = 1
    while(cap.isOpened()):
        
        curr_time = time.time() #getting the current time
        ret, frame = cap.read()
        if first_iteration_indicator == 1: # initializing on first frame

            
            first_frame = copy.deepcopy(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape[:2]
            accum_image = np.zeros((height, width), np.uint8) # creating a black image of dimension height and width
            #cv2.imshow('accum_image',accum_image)
            first_iteration_indicator = 0

        
        
        
            
        # To clear the accumulated image after 7 seconds
        if curr_time - last_recorded_time_1 >=7.0: 
            accum_image = np.zeros((height, width), np.uint8) 
            last_recorded_time_1 = curr_time # updates the last recorded time
        
        
            
            
        else:
            ret, frame = cap.read()  # read a frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grayscale

            fgmask = fgbg.apply(gray)  # remove the background
            #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

            # for testing purposes, show the result of the background subtraction
            #cv2.imshow('BackgroundSubtraction', fgmask)

            # apply a binary threshold only keeping pixels above thresh and setting the result to maxValue.  If you want
            # motion to be picked up more, increase the value of maxValue.  To pick up the least amount of motion over time, set maxValue = 1
            thresh = 15
            maxValue = 40
            ret, th1 = cv2.threshold(fgmask, thresh, maxValue, cv2.THRESH_TRUNC)
            # for testing purposes, show the threshold image
            #cv2.imshow('Threshold',th1)
            # cv2.imwrite('diff-th1.jpg', th1)

            # add to the accumulated image
            accum_image = cv2.add(accum_image, th1)
            # for testing purposes, show the accumulated image
            #cv2.imshow('diff-accum.jpg', accum_image)
            #cv2.imshow('accumulated image', accum_image)

            

        
        # apply a color map
        # COLORMAP_PINK also works well, COLORMAP_BONE is acceptable if the background is dark
    
        color_image = im_color = cv2.applyColorMap(accum_image, cv2.COLORMAP_HOT)
        #cv2.imshow('heat', color_image)
        result_overlay = cv2.addWeighted(frame, 1, color_image, 0.7, 0)
        # Displaying the final output
        cv2.imshow('result over', result_overlay)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    
    # save the final overlay image
    cv2.imwrite('diff-overlay.jpg', result_overlay)

    # cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()