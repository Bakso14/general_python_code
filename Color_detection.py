import cv2 
import numpy as np

cap = cv2.VideoCapture(0)

#trackbar callback fucntion to update HSV value
def callback(x):
	global H_low,H_high,S_low,S_high,V_low,V_high
	#assign trackbar position value to H,S,V High and low variable
	H_low = cv2.getTrackbarPos('low H','controls')
	H_high = cv2.getTrackbarPos('high H','controls')
	S_low = cv2.getTrackbarPos('low S','controls')
	S_high = cv2.getTrackbarPos('high S','controls')
	V_low = cv2.getTrackbarPos('low V','controls')
	V_high = cv2.getTrackbarPos('high V','controls')


#create a seperate window named 'controls' for trackbar
cv2.namedWindow('controls',2)
cv2.resizeWindow("controls", 550,10);


#global variable
H_low = 0
H_high = 179
S_low= 0
S_high = 255
V_low= 0
V_high = 255

#create trackbars for high,low H,S,V 
cv2.createTrackbar('low H','controls',0,179,callback)
cv2.createTrackbar('high H','controls',179,179,callback)

cv2.createTrackbar('low S','controls',0,255,callback)
cv2.createTrackbar('high S','controls',255,255,callback)

cv2.createTrackbar('low V','controls',0,255,callback)
cv2.createTrackbar('high V','controls',255,255,callback)

while(1):

    _, frame = cap.read()                               #karena nilai ret tidak di akan di proses maka dapat di ganti dengan _
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)          #mengubah gambar dari bgr menjadi hsv, gambar yang di ambil oleh opencv selalu menggunakan urutan bgr bukan rgb

    lower_blue = np.array([H_low,S_low,V_low])                  #nilai-nilai hsv untuk threshold bawah
    upper_blue = np.array([H_high,S_high,V_high])                #nilai-nilai hsv untuk threshold atas

    mask = cv2.inRange(hsv, lower_blue, upper_blue)      #nilai-nilai pada variabel hsv yang masuk kedalam threshold lower_blue dan upper_blue akan diberi angka 1 atau high sedangkan yang tidak masuk diberi angka 0 atau low
    res = cv2.bitwise_and(frame,frame, mask= mask)       #melakukan operasi 'and' antara gambar awal (frame) dengan hasil pemilihan (mask) sehingga didapatkan gambar dengan hanya area seleksi yang muncul

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #cv2.imshow('hsv',hsv)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()


#why using hsv instead of bgr:
#Because the R, G, and B components of an objectÃ¢â‚¬â„¢s color in a digital image are all correlated with the amount of light hitting the object,
#and therefore with each other, image descriptions in terms of those components make object discrimination difficult. 
#Descriptions in terms of hue/lightness/chroma or hue/lightness/saturation are often more relevant.