# **1. Objectives** 
The objectives of this project are for students to have some hands-on experiences of graphics programming and to develop a graphics application. Students are given a Python/OpenGL program with a virtual jeep game and asked to extend this program to provide additional features.

# **2. Basic Requirements**
**1) Creating new objects (10 marks)**

Create or import at least one new object with color/material/texture properties and put it them at suitable locations.

**2) Menu and Lighting (10 marks)**

Add a pop-up menu to switch between different light properties (ambient, diffuse, specular and position, point lights, directional lights, spotlights).

**3) Manipulation (10 marks)**

Use keyboard/mouse to manipulate an object (size, position and angle) and the camera (position, angle and zoom-in/out).

**4) Adding autonomous objects (10 marks)**

Set an object to move around automatically and react to the environment (e.g. light).

**5) Window resolution (10 marks)**

Allow user to set/select the window resolution, enable/disable full screen mode before or during the application.

**6) Accelerating ribbon (10 marks)**

Set an accelerating ribbon on the road, and the jeep can be accelerated after passing the ribbon.

# **3. Advanced Requirements**
**1) Scouring and ranking system** 

When the game end, if the player can get the better result of the current top 10 ranking it will record and show the result.

# **How to play**

1. Move the jeep using keyboard: left, right, up, down
2. Chang screen size using keyboard: 1
3. Using mouse scroll to zoom in or zoom out
4. Hold the mouse and right-click moving the viewpoint in a 3D way in camera view
5. Right-click to open menu setting

# **How to run**

Method 1 (directly run the .exe file):

I have deployed the .py file which is an easy way to run the programs without the requirement of installing any libraries, packages or downloading python on your computer. You can find the .exe file in src/main.exe.


Method 2 (install corresponding library and python version 2.7):

1. Step1: Download and unzip the file
2. Step2: Download and install Anaconda for the website https://www.anaconda.com/
3. Step3: Create a virtual environment of python 2.7 in Anaconda
4. Step4: Open created virtual environment in Anaconda and run the command “cd [file download path + \src]”
5. Step5: Run the command “pip install -r requirements.txt”
6. Step6: Run the command “python main.py”
