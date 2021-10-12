import cv2
import math

path = 'Angle/img.png'
img = cv2.imread(path)
pointsList = []
count = 0;

def gradient(pts1, pts2):
    return (pts2[1] - pts1[1]) / (pts2[0] - pts1[0])

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
            pt1 = [x, y]
            pt2 = [x+350, y]
            cv2.circle(img, tuple(pt1), 3, (0, 0, 255),cv2.FILLED)
            cv2.circle(img, tuple(pt2), 3, (0, 0, 255),cv2.FILLED)
            cv2.line(img, tuple(pt1), tuple(pt2), (0,0,255), 2)
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
            pt5 = [round((pt4[0]+pt[0])/2), round((pt4[1]+pt[1])/2)]
            cv2.circle(img, tuple(pt5), 3, (0, 0, 255), cv2.FILLED)

            m = -1/gradient(pt, pt4)
            m1 = gradient(pt, pt4)
            x6 = round(-((pt0[1] - pt5[1]) * m1) + pt5[0])
            pt6 = [x6, pt0[1]]
            cv2.circle(img, tuple(pt6), 3, (0, 0, 255), cv2.FILLED)
            cv2.line(img, tuple(pt5), tuple(pt6), (0, 0, 255), 2)

            pointsList.append(pt5)
            pointsList.append(pt6)

            x1 = -(pt[0]-pt4[0])
            x2 = pt[1]-pt4[1]
            angR = math.atan2(-x1, -x2)
            angD = math.degrees(angR)
            if(pt4[1]>pt0[1]):
               angD += 180
            if(angD>180):
                angD -=360
            print(angD)
            cv2.putText(img,str(round(angD)), (pt6[0]+40, pt6[1]-40),
                        cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,0), 2)

while True:
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', mousepoints)
    if cv2.waitKey(1) & 0xFF == ord('a'):
        pointsList = []
        img = cv2.imread(path)

