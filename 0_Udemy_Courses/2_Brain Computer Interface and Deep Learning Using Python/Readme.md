# Brain Computer Interface and Deep Learning Using Python

- Brain Computer Interface (BCI) is a technology that allows you to control a computer or device using your brain.
- Deep Learning is a type of machine learning that uses neural networks to learn from data.


## EEG

- EEG stands for Electroencephalogram, which is a technology that records the electrical activity of the brain.

- Electrodes are placed on the scalp to record the electrical activity of the brain.

- The electrodes are connected to a device that records the electrical activity of the brain.

- The device is connected to a computer that processes the data.



### Section 1:

- Describing BCI, EEG and ways to set up and use Google Colab.

### Section 2:

- What is Deep Learning?

    - Deep Learning is a type of machine learning that uses neural networks to learn from data. Different types of neural networks include Convolutional Neural Networks (CNNs), Recurrent Neural Networks (RNNs), and Long Short-Term Memory (LSTM) networks.

- MNIST Dataset

    - MNIST is a dataset of 28x28 grayscale images of handwritten digits (0-9).

    - The dataset is split into 60,000 training images and 10,000 test images.
    
    
    - `1_Mnist.ipynb` (inside the `CODES` folder) is a Jupyter notebook that contains the code to load the MNIST dataset and display the first image. 

- Data Preprocessing 

    - Data Preprocessing is the process of preparing the data for the model. Each image is a 28x28 grayscale image, which is a 2D array. Each pixel is a value between 0 and 255.

    - The data is normalized to have a mean of 0 and a standard deviation of 1, by dividing each pixel by 255.

    - The data is flattened to have a 1D array of 784 pixels.

    - Need to have batches of data to train the model, because the dataset is too large to fit into memory, so what we do is we take a small batch of data and train the model on that, then we take the next batch of data and train the model on that, and so on. So if the batch size is 64, then we take 64 images and train the model on that, then we take the next 64 images and train the model on that, and so on.

    - The batches are created using the `DataLoader` class.

    - Shuffle is set to True, so the data is shuffled before each epoch, which helps the model to generalize better, and not memorize the data.

    - So batch size means the number of images that will be used to train the model at a time, and here we have set it to 64, and shuffle means that the data will be shuffled before each epoch.

    - `2_data_preprocessing.ipynb` (inside the `CODES` folder) is a Jupyter notebook that contains the code for data preprocessing, displaying the first image and label, and displaying a batch of images and labels.

- Simple Neural Network

    - A simple neural network is a neural network that has only one layer, which is the output layer.

    - The input layer is the data, and the output layer is the prediction.

    - Here we have a simple neural network with 784 input features and 10 output features.

- Training the Neural Network

    - The model tries to find the best weights and biases to predict the output, by minimizing the loss function.

    - The loss function is the difference between the predicted output and the actual output.

    - The model updates the weights and biases using the gradient descent algorithm.

    - Here Gradient Descent is a backpropagation algorithm, which is a way to update the weights and biases of the model, by calculating the gradient of the loss function with respect to the weights and biases. So how it works is the model predicts the output, and then the loss is calculated, and then the gradient is calculated, and then the weights and biases are updated.

### Section 3:

- Project 1: Brain Computer Interface

    - Load the numpy array, sampling rate of the EEG data is 160Hz, meaning it can generate 160 samples/time points per second.

    - The numpy array is loaded using the `np.load` function, and it has around 259520 data points, and each has 65 values, which are the values of the EEG channels.[dataset.shape: (259520, 65)]


- CNN Model

    - Convolutional Neural Network (CNN) is a type of neural network that is used for image classification.

    - Usually in CNNs, we have a convolutional layer, activation function, pooling layer, and a fully connected layer.

        - The convolutional layer is used to extract features from the image.

        - The activation function is used to introduce non-linearity into the model.

        - The pooling layer is used to reduce the dimensionality of the data.

    - use  `optuna` to find the best hyperparameters for the model.
