import numpy as np
import cv2
import pickle
from decimal import Decimal

width = 640
height = 480
threshold = 0.65 # MINIMUM PROBABILITY TO CLASSIFY

catagory = ["Airplane","Gun"]
# cap = cv2.VideoCapture(0)
# cap.set(3,width)
# cap.set(4,height)

#### LOAD THE TRAINNED MODEL
pickle_in = open("model_trained.p","rb")
model = pickle.load(pickle_in)

#### PREPORCESSING FUNCTION
def preProcessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = img/255
    return img

while True:

    # success,imgOriginal = cap.read()
    imgOriginal = cv2.imread(r"Test/p5.jpg")
    img = np.asarray(imgOriginal)
    img = cv2.resize(img,(32,32))
    img = preProcessing(img)
    # cv2.imshow("Processsed Image",img)
    img = img.reshape(1,32,32,1)
    i = int(model.predict_classes(img))

    predictions = model.predict(img)
    probVal= np.amax(predictions)
    # print(i,probVal)


    probVal = Decimal(float(probVal*100))
    probVal = round(probVal,2)
    ac = str(probVal)
    if probVal> threshold:
        cv2.putText(imgOriginal,str(catagory[i]),(50,70),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
        cv2.putText(imgOriginal,"acc = "+ac+'%',(30, 140), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
        imgOriginal = cv2.resize(imgOriginal, (int(imgOriginal.shape[1] * 2), int(imgOriginal.shape[0] * 2)))

    cv2.imshow("Original Image",imgOriginal)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
