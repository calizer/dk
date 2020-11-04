import numpy as np
import cv2


cap = cv2.VideoCapture(0)
Ht = 320
Wd = 480
cap.set(3, Wd) #Set frame Width
cap.set(4, Ht) #Set frame height
_, frame = cap.read() #Store captured frame of camera to variable "frame"
rows, cols, ch = frame.shape #Get frame size 
x_medium = int(cols / 2) #Initialize horizontal position 
y_medium = int(rows / 2) #Initialize vertical positon

while(True):
  # Capture frame-by-frame
   ret, frame = cap.read()
   frame = cv2.flip(frame, -1)
   hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   # Our operations on the frame come here
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    cv2.imshow('Grey',gray)
#    blur = cv2.GaussianBlur(gray,(5,5),0)
#    edges= cv2.Canny(blur, 50,100)
#    cv2.imshow("edges", edges)
#    ret, thresh_img = cv2.threshold(blur,100,100,cv2.THRESH_BINARY)
#    cv2.imshow("thresh", thresh_img)

    #Colour Filter Range
   low = np.array([0, 100, 125])
   high = np.array([22, 255, 255])
   colour_mask = cv2.inRange(hsv_frame, low, high)
   filtered = cv2.bitwise_and(frame, frame, mask = colour_mask)

#    contours =  cv2.findContours(colour_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
#    for c in contours:
#        cv2.drawContours(frame, [c], -1, (0,255,0), 3)
       
   _, contours, _ = cv2.findContours(colour_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # Findig Contours
   contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True) # Arrange Contours in Assending
   for cnt in contours: # Draw rectangle on First contors on image
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x , y) , (x + w, y + h) , (0, 255, 0), 2) # Getting Position of rectangle & line colour & thickness
        break # Break loop to draw only one rectangle. if comment we get all red object rectangle
   for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        x_medium = int((x + x + w) / 2) # Checking horizontal center of red object & save to variable
        y_medium = int((y + y + h) / 2) # Checking Vertical center of red object & save to variable
        break
   cv2.line(frame, (x_medium, 0), (x_medium, Ht), (0, 255, 0), 2) #Draw horizontal centre line of red object
   cv2.line(frame, (0, y_medium), (Wd, y_medium), (0, 255, 0), 2) #Draw Vertical centre line of red object
   cv2.imshow("IN Frame", frame) #Printing frame with rectangle &  lines
 
   #print('% x_medium, % y_medix_medium,y_medium)
   mapped_x = (x_medium - 0) * (100 - 0) / (480 - 0) + 0;
   print("Position offset: ", mapped_x)   
      
      
      
      

     # Display the resulting frame
#    cv2.imshow('frame',frame)
   if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
