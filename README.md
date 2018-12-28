# Flowers
Created By Sagar Saxena
06/14/18
Computer Vision Period 7
## Programs Included In This Directory
    cifarDemo.py - Classifies the cifar dataset. Found in TensorFlow Chapter 4
    flowers10.py - Classifies 10 flowers using the same strategy as the Cifar Demo
    train.py - Trains a Convulutional Neural Network Using Keras
    Models.py - Models that can be trained by train.py
    test.py - Tests a Single Image against a Saved Model
    databases/database.py - Creates Directories of Images Into Pickled Cifar-like Batches
    databases/imDownloader.py - Grabs Links from Google Images Using a Chrome WebBot
    databases/linkDownloader.py - Converts all image links to images
    databases/mousePy.py - Gives Control of the Mouse To Python
## Databases Included In This Directory
    databases/cifar-10-batches-py - Cifar 10 Batches
    databases/mnist - Database of MNIST Handwritten Digits
    databases/flowers10 - Database of 10 Flowers
    databases/flowers91 - Database of 91 Flowers
## Running Programs
    Virtual Environment
        Enable: source/bin/activate
        Disable: deactivate
    CifarDemo
        python3 cifarDemo.py
        python3 cifarDemo.py [Number of Steps] [Batch Size] [Print Skips]
        ex: python3 cifarDemo.py 5000 500 500
    Flowers10
        python3 flowers10.py
        python3 flowers10.py [Number of Steps] [Batch Size] [Print Skips]
        ex: python3 cifarDemo.py 5000 200 500
    Train
        python3 train.py -d [path to data batch] -m [path to model] -p [path to plot image] -e [Number of Epochs] -c [Number of Classes] -b [Size of Batch] -t [Type of Model]
        ex: python3 train.py -d databases/flowers10/data.pkl -m models/flowers10.model -p plotFlowers10.png -e 100 -c 10 -b 200 -t LeNet
        ex: python3 train.py -d databases/flowers10/data.pkl -m models/flowers10_c.model -p plotFlowers10_c.png -e 100 -c 10 -b 200 -t Cifar
        ex: python3 train.py -d databases/flowers91/data_batch_1.pkl -m models/flowers91.model -p plotFlowers91.png -e 100 -c 91 -b 200 -t LeNet
    Models
        No Main Method
    Test
        python3 test.py -m [path to model] -i [path to image] -l [path to labels file]
        ex: python3 test.py -m models/flowers10.model -i databases/flowers10/data/Columbine/3.jpg -l databases/flowers10/labels.txt
    Database
        No Main Method
        python3
            from database import *
            genLabelFiles([Directory of Folders], [Path to Outfile], [Number To Skip])
            save_batches([Path To Directory of Folders], [Path To Label File], [Number of Batches], [Number of Images In Each Batch], [Directory To Save Data Batches])

            ex:
            genLabelFiles('./flowers10/data', './flowers10/labels.txt', 0)
            save_batches('./flowers10/data', './flowes10/labels.txt', 1, 600, './flowers10')
    ImDownloader
        python3 imDownloader.py
        0
        __Name of Flower__

        #although other methods exist in this program (i.e. more than just method '0'), those methods should not be used as they were depreciated with the creation of linkDownloader.py
    LinkDownloader.py
        No Main Method
        python3
            downloadFolder([Directory of Image Link Text Files], [Directory To Store Image Directories])
    MousePy
        No Main Method
        Depreciated With imDownloader.py
