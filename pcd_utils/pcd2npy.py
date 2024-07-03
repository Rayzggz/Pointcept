import os
import open3d
import numpy as np
import glob
from tqdm import tqdm

# this script is used to convert pcd files to npy files
# these npy files is similar to the scannet dataset
# which allows us to use the same data processing pipeline as the scannet dataset

# this script is alternative to the preprocess script
# after running this script, you can use the train program of the scannet dataset to train the model
# Note: you need to modify the label part to fit the label of the pcd files




# get the list of all pcd files
fileList = glob.glob('../Data/*.pcd')

def fileprocessor(processFileList, savePath="../pointcloud/"):
    for i in tqdm(range(len(processFileList))):
        filename = processFileList[i].split('/')[-1].split('.')[0]
        pointCloud = open3d.io.read_point_cloud(processFileList[i])

        # create directory if savePath does not exist
        if not os.path.exists(savePath):
            os.makedirs(savePath)

        # create npy directory
        if not os.path.exists(savePath + filename):
            os.makedirs(savePath + filename)

        # process the coordinate data
        saveName = savePath + filename + '/coord.npy'
        np.save(saveName, np.asarray(pointCloud.points))

        # process the color data
        saveName = savePath + filename + '/color.npy'
        np.save(saveName, np.asarray(pointCloud.colors))

        # compute and process the normal data
        saveName = savePath + filename + '/normal.npy'
        pointCloud.estimate_normals()
        np.save(saveName, np.asarray(pointCloud.normals))

        # process label data
        # suppose the label is the 5th column in the pcd file
        saveName = savePath + filename + '/label.npy'
        labels = []
        start_reading = False
        with open(processFileList[i], 'r') as file:
            for line in file:
                if start_reading:
                    parts = line.strip().split()
                    label = int(parts[4])
                    labels.append(label)
                elif line.strip() == "DATA ascii":
                    start_reading = True
        np.save(saveName, np.asarray(labels))




#randomly shuffle the fileList
np.random.shuffle(fileList)

#set separate ratio
test_ratio = 0.2
val_ratio = 0.1
train_ratio = 1 - test_ratio - val_ratio


#split the fileList
trainList = fileList[:int(len(fileList) * train_ratio)]
valList = fileList[int(len(fileList) * train_ratio):int(len(fileList) * (train_ratio + val_ratio))]
testList = fileList[int(len(fileList) * (train_ratio + val_ratio)):]


#process the files
print("Processing trainList")
fileprocessor(trainList,"../pointcloud/train/")
print("Processing valList")
fileprocessor(valList,"../pointcloud/val/")
print("Processing testList")
fileprocessor(testList,"../pointcloud/test/")
print("Processing finished")






