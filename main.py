import csv
import cv2
import numpy as np
import os

def detectAdubo(img):
    """ Utilizado o algoritmo de detecção de bordas de Canny, 
    onde é utilizado uma matriz de convolução para detectar as bordas do adubo, 
    após isso é utilizado um filtro de dilatação para aumentar o tamanho das bordas e 
    assim aumentar a precisão da detecção. Após isso é feito a detecção de contornos, 
    onde é utilizado o algoritmo de detecção de contornos de canny, 
    onde é utilizado uma matriz de convolução para detectar os contornos do adubo, 
    após isso é utilizado um filtro de dilatação para aumentar o tamanho dos contornos e 
    assim aumentar a precisão da detecção.
    """
    
    # convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # apply histogram equalization
    gray = cv2.equalizeHist(gray)

    # apply gaussian blur
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # apply canny edge detection
    canny = cv2.Canny(blur, 50, 150)

    # apply dilation
    kernel = np.ones((5,5), np.uint8)
    dilation = cv2.dilate(canny, kernel, iterations=1)

    # find contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # draw contours
    cv2.drawContours(img, contours, -1, (0,255,0), 3)

    # find the biggest contour (c) by the area
    c = max(contours, key = cv2.contourArea)

    # create a mask
    mask = np.zeros(img.shape[:2], np.uint8)

    # create a background model
    bgdModel = np.zeros((1,65), np.float64)

    # create a foreground model
    fgdModel = np.zeros((1,65), np.float64)

    # create a rectangle with the position of the adubo
    rect = cv2.boundingRect(c)

    # apply grabcut
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # create a mask with the position of the adubo
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')

    # apply the mask to the image
    img = img*mask2[:,:,np.newaxis]

    return img

def extract_frames_from_video(video):
    
    # read video "video_adubo.mp4" and extract frames 
    cap = cv2.VideoCapture(video)

    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        # rotate frame 90 degrees
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite('frames/frame'+str(i)+'.jpg',frame)
        i+=1
        
    cap.release()
    cv2.destroyAllWindows()
    return 0
    
def main():
    
    # extract frames from video
    extract_frames_from_video('video_adubo.mp4')

    # count how many files are in the folder "frames"
    count = len([name for name in os.listdir('frames') if os.path.isfile(os.path.join('frames', name))])
    
    # apply grabcut to each frame
    for i in range(0, count-1):
        
        original_img = cv2.imread('frames/frame'+str(i)+'.jpg')
        img = original_img.copy()
        
        # apply sharpening filter and grabcut before overlaying the image
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        img = cv2.filter2D(img, -1, kernel)

        # apply contrast enhancement
        img = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
        
        detectedAdubo = detectAdubo(img)
        
        original_img = cv2.addWeighted(original_img, 0.5, detectedAdubo, 0.5, 0)
        
    #     # cv2.imshow('img', original_img)
    #     # cv2.imshow('imgADUB', detectedAdubo)
    #     # cv2.waitKey(0)
        
        cv2.imwrite('frames/frame'+str(i)+'.jpg',original_img)
        
    # create a video from the frames
    os.system('ffmpeg -framerate 30 -i frames/frame%d.jpg -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p output.mp4')

if __name__ == '__main__':
    main()

