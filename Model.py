import os
import cv2
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten


class MyModel:
    def __init__(self):
        self.Categories = []
        self.model = self.getModel()
        self.Train_Model()

    def predict(self, url):
        self.model.load_weights('./static/model_data/cnn.h5')
        img = cv2.imread(url)
        img1 = cv2.resize(img, (128, 128), cv2.INTER_AREA)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img1 = np.array([img1]).astype('float') / 255.0
        y = self.model.predict(img1)
        return self.Categories[np.argmax(y[0])], y[0][np.argmax(y[0])]

    def Train_Model(self):
        (self.X_data, self.Y_data) = self.load_data_from_dataset()
        if(len(self.X_data) != 0):
            self.Update_Categories()
            X_train, X_test, Y_train, Y_test = train_test_split(self.X_data, self.Y_data, test_size=0.3)
            self.model = self.getModel()
            self.model.fit(X_train, to_categorical(Y_train), epochs=10)
            self.model.save_weights('./static/model_data/cnn.h5')

    def getModel(self, num_filters=8, filter_size=3, pool_size=2):
        layers = [Conv2D(num_filters, filter_size, input_shape=(128, 128, 1,)),
                  MaxPooling2D(pool_size=pool_size), Flatten(),
                  Dense(len(self.Categories), activation='softmax')]
        model = Sequential(layers)
        model.compile('adam', loss='categorical_crossentropy', metrics=['accuracy'], )
        return model

    def load_data_from_dataset(self):
        Images = []
        Labels = []
        files = os.scandir('./static/model_data/dataset')
        for file in files:
            if file.is_file():
                img = cv2.imread('./static/model_data/dataset/' + file.name)
                img = cv2.resize(img, (128, 128), cv2.INTER_AREA)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                Images.append(img)
                Labels.append(file.name.split('-')[0])
        Images = np.array(Images).astype('float') / 255.0
        return Images, Labels

    def Update_Categories(self):
        self.Categories.clear()
        i = 0
        while len(self.Y_data) > i:
            self.Categories.append(self.Y_data[i])
            i = i + 100
        for i in range(len(self.Y_data)):
            self.Y_data[i] = self.Categories.index(self.Y_data[i])

    def AddNewDataIntoDataSet(self, i, label, video):
        vid = cv2.VideoCapture(video)
        flag = True
        paths = []
        frames = []
        while vid.isOpened():
            ret, frame = vid.read()
            if not ret:
                flag = False
                break
            i = i + 1
            paths.append('./static/model_data/dataset/' + label + '-' + str(i) + '.png')
            frames.append(frame)
            if i == 100:
                break
        vid.release()
        if flag:
            for index in range(len(paths)):
                cv2.imwrite(paths[index], frames[index])
            self.Train_Model()
        else:
            print('i will not add this in dataset i need a little bit large')