import numpy as np
import cv2
import pickle
from decimal import Decimal
import pandas as pd


width = 640
height = 480
threshold = 0.65 # MINIMUM PROBABILITY TO CLASSIFY

apple = pd.read_csv("text files/orange_fruit.csv",squeeze=True, usecols=["class"])
catagory = list(apple)

#### LOAD THE TRAINNED MODEL
pickle_in = open("models/orange_fruit_Model.p","rb")
model = pickle.load(pickle_in)

#### PREPORCESSING FUNCTION
def preProcessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.equalizeHist(img)
    img = img/255
    return img

imgOriginal = cv2.imread(r"Test image/orange_fruit/12.png")
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
print(i," catagory = ",catagory[i])
imgOriginal = cv2.resize(imgOriginal, (int(imgOriginal.shape[1]) * 2, int(imgOriginal.shape[0]) * 2))
if probVal> threshold:
    cv2.putText(imgOriginal,str(catagory[i]),(10,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,12,255),2)
    cv2.putText(imgOriginal,"acc = "+ac+'%',(10, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
cv2.imshow("Original Image",imgOriginal)
cv2.waitKey(0)
cv2.destroyAllWindows()

