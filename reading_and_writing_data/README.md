# reading_and_writing_data

In this project, I show you how to read and write data to and from a TensorFlow graph. I've also included two additional files, [png_to_record.py](./png_to_record) and [record_to_png](./record_to_png) both extend the work of [main.py](./main.py). png_to_record looks for images in a directory and converts each into an example, which is written to a TFRecord file. record_to_png parses the TFRecord file and converts each example into a .PNG. In addition, I have included [csv_to_record.py](./csv_to_recordy) and [record_to_csv.py](./record_to_csv) to demonstrate how you might go about reading CSV data, write a record, and read the record.

# Table of Contents

1. Requirements.
1. Installation.
1. Usage.
1. Contributions.
1. Credits.

# Requirements

I have used the following tools and libraries to create and run each project:

1. [TensorFlow](https://www.tensorflow.org/).
1. [Anaconda](https://www.continuum.io/).
1. [Nvidia CUDA](https://developer.nvidia.com/cuda-zone).
1. [Nvidia CUDNN](https://developer.nvidia.com/cudnn).
1. [Microsoft Visual Studio Code (Code)](https://code.visualstudio.com/).
1. [Code Python Extension](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python).

The project has been compiled and run on PCs running Windows 7 x64 and Windows 10 x64 to ensure they work.

Please note: if you want to use TensorFlow on a GPU, you'll need to make sure your GPU supports Nvidia's CUDA, and install CUDA and CUDNN.

# Installation

The following is a list of steps to follow to get started with using this project':

1. Clone the tensorflow_projects repo'.
1. Install Anaconda and create a Python 3.5 environment for TensorFlow, e.g. 'tf' for TensorFlow running on a CPU or 'tf-gpu' for TensorFlow running on a GPU. Activate the environment and install jupyer, matplotlib, scipy, and tensorflow/tensorflow-gpu.
1. Install Code and the Python extension. 
1. Open a Windows command line and activate an environment. Type 'code' to open Code, then browse to the reading_and_writing_data directory. Open main.py.
1. Use Code's built-in console and type 'python main.py' to run the script.

At this point, everything should compile and run.

Please note: you can also run main.py from within Code by typing 'F1', then 'run'.

# Usage 

To run the main.py script, browse to reading_and_writing_data directory and run the following command in a command line window:

    python main.py

You should see the following outputs:

![Output](./data/output/Capture.PNG)

# Contributions

If you feel like you can make a contribution; please, feel free to make a request.

# Credits

Dr. Frazer K. Noble. 
 
Follow me on Twitter at [@FrazerNoble](https://twitter.com/FrazerNoble).
