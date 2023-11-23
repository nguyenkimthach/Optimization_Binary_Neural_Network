# Optimization_Binary_Neural_Network
Currently, with the strong development of computer vision and IOT systems,
the problem of saving costs, energy, and computing resources in low-cost applications
is being pursued by many projects. care and attention. In this paper, the topic proposes
a solution to optimize the weight set of the neural network, which is to quantize most
of the weights in the form of signed binary weights 1 and -1 to apply to cheap
hardware such as the Raspberry Pi Zero. Faster, more energy-efficient binary
weighting thanks to bitwise operations When training with the license plate dataset,
the GTSRB is trained with the TensorFlow artificial neural network library. The topic
has achieved 96.01% accuracy. In addition, the project also trained the BCNN
network with other data sets and achieved the accuracy of Mnist (99.81%), Cifa-10
(93.59%), Mnist-fashion (96.35) and the product box code dataset - CNPB (99.89%).
When training on the data sets Mnist, Mnist-fashion, Cifa-10, GTSRB, CNPB, the
inner set of the BCNN neural network, the storage capacity of the BCNN binary
neural network weights decreases from 6.16 to 7.59 times compared to the
conventional CNN model with the same structure. The processing speed of the BCNN
model is 5.2 times faster than a conventional CNN network with a similar structure
when deployed to low-profile hardware, the Raspberry Pi Zero with the CNPB
dataset.

link for CNPB dataset: https://www.kaggle.com/datasets/kimthchnguyn/ccnp-newdataset
