import cv2
import math

source = 'source/Transient/'
result = 'result/Transient/'
name = 'frame_24'
fileType = '.JPG'

path = source+name+fileType
px = 1400
py = 1050
# path = 'Angle/angle_2.jpg'
imS = cv2.imread(path)
img = imS
# img = cv2.resize(imS, (px, py))
pointsList = []
count = 0;

def gradient(pts1, pts2):
    gr = (pts2[1] - pts1[1]) / (pts2[0] - pts1[0])
    return gr

def getAngle(ptlist):
    p1, p2, p3 = ptlist[-3:]
    m1 = gradient(p1,p2)
    m2 = gradient(p1,p3)
    print(m1,m2)
    angR = math.atan((m1-m2)/(1+m1*m2))
    angD = math.degrees(angR)
    print(angD)

def mousepoints(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(pointsList) == 0:
            # Reference Axis
            pt1 = [x, y]
            pt2 = [x + 750, y]
            pt_plus = [x - 750, y]
            print(x)
            print(y)
            cv2.circle(img, tuple(pt1), 3, (0, 0, 255),cv2.FILLED)
            cv2.circle(img, tuple(pt2), 3, (0, 0, 255),cv2.FILLED)
            cv2.line(img, tuple(pt_plus), tuple(pt2), (0,0,255), 2)
            pointsList.append(pt1)
            pointsList.append(pt2)

        elif len(pointsList) == 2:
            pt3 = [x, y]
            pointsList.append(pt3)
            cv2.circle(img, tuple(pt3), 3, (0, 0, 255), cv2.FILLED)

        elif len(pointsList) == 3:
            pt4 = [x,y]
            pointsList.append(pt4)
            pt = pointsList[-2]
            pt0 = pointsList[-4]
            cv2.circle(img, tuple(pt4), 3, (0, 0, 255), cv2.FILLED)
            cv2.line(img, tuple(pt), tuple(pt4), (0, 0, 255), 2)

            # Create Center Point of The Soft Robot Tip (use pt and pt4)
            pt5 = [round((pt4[0]+pt[0])/2), round((pt4[1]+pt[1])/2)]
            cv2.circle(img, tuple(pt5), 3, (0, 0, 255), cv2.FILLED)

            m1 = gradient(pt, pt4)
            m = -1/m1

            # Create Intersection Point with X-Axis (Center)
            x6 = round(((pt0[1] - pt5[1]) * m) + pt5[0])
            pt6 = [pt0[0],pt0[1]]
            cv2.circle(img, tuple(pt6), 3, (0, 0, 255), cv2.FILLED)
            cv2.line(img, tuple(pt5), tuple(pt6), (0, 0, 255), 2)

            pointsList.append(pt5)
            pointsList.append(pt6)

            # Calculate the Angle
            x1 = abs(pt[0]-pt4[0])
            y1 = abs(pt[1]-pt4[1])
            print(x1)
            print(y1)
            angR = math.atan(y1/x1)
            angD = math.degrees(angR)
            print(angD)
            print(m1)
            print(m)
            if(pt[0]<pt0[0]):
                if(m<0):
                    angD = 180 - angD
            elif(pt[0]>pt0[0]):
                if(m>0):
                    angD = 180 +angD
                else:
                    angD = 360 - angD
            angD = (angD+90) % 360
            print(angD)
            cv2.putText(img, str(round(angD)), (pt5[0]+20, pt5[1]+20),
                        cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,0), 2)

while True:
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mousepoints)
    if cv2.waitKey(1) & 0xFF == ord('a'):
        pointsList = []
        imS = cv2.imread(path)
        img = imS
        #img = cv2.resize(imS, (px, py))
    elif cv2.waitKey(1) & 0xFF == ord('s'):
        status = cv2.imwrite(result + name + '_finalDec' +fileType, img)
        print("Image written to file-system : ", status)