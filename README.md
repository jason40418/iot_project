# iot_project

![](documentation/image/logo_full.svg)

- To read more detail document, you could visit this [page](https://hackmd.io/c/Ers4gemdQ6abEiLBeTVNYw).

> Version: 1.0.0
> 
> Date: 2019-12-31
> 
> Video:

## 1. Introduction
### Why environment monitor important?
- With the quality of life is gradually improving, more and more people would be focus on their own health.
- Therefore, monitor an environment is important for a person who may easier affect the health by the environment.
- According to the declaration data of National Health Insurance from Ministry of Health and Welfare in Taiwan in 2017, every 100,000 population 14,495 people have the allergy, such as allergic rhinitis and allergic conjunctivitis, and winter is the season that easiest cause these kinds of diseases. 
- Data source: [MOHW, Taiwan](https://www.mohw.gov.tw/dl-54765-dee004d9-348a-45eb-ad79-654f0966dcd7.html).

### Why this project roll out?
- Because the author has the congenital disease that allergy and asthma, the humidity and the quality of the air may induce these diseases especially the **“cold air”**.
- Therefore, I want to make a PiEnvir to monitor the whole environment that could customize the own profiles by their own expected.
- Meanwhile, each room have different purpose to use, so it is important to confirm the purpose and who is using this room currently and its best configuration. As a result, to build a room profile and personal profile is important for this project.

### How the data presentation?
- In this project how to display the monitor data and warn the user is another key point to success.
- Therefore, I plan to display the value on seven-segment display, use the LED emit light and the speed of the motor to represent the different situation.
-  The final key point is connected to the Internet, transfer the real time data about this room through the Internet is another import thing and user could remote to control the any component on the Raspberry Pi.
-  To achieve this goal, there are a famous technology called “Face Recognition”, it could easier to identify the person real time through the camera. 
    -  Steps:
        1. One thing you must need to do is given the certain figures about the person who you want to identify and train the model.
        2. Then, give the label about this person, Finally, it could easier to identify the person in a short period.
        3. Therefore, the person who enter or exit the room no need to key in or submit some request through the form or read the ID card to Raspberry Pi or anything else way.
        4. The one thing you need to do is show the face in front of the camera and let PiEnvir identify who you are.

### Why using the face recongnization?
- This technology is famous in recently year and it is also having a lot of advance applications, such as punch in the work, emotion detection, and take the parcels from the mailbox.
- Moreover, I have not doing this technology in the past and I consider that this technology in project would reduce the trouble to the user.
- Also, the most important is that I am interesting to implement this technology, as a result, I want to do this technology on this final project. 
- :star2: **Notice that**: Face recongnization is very convenience because the person need to stand in front of camera only. He/She no need to take out the card or enter any data.
- However, it still has accuracy and precision problem need to improve.
    - You may use the photo to pass the identification.
    - If you wear any mask on your face, it may difficult to identify who you are.
> :sparkles: But in this project, I would not improve and care about the face recognition challenges which mention above.

## 2. Screenshots
- ![real-time](https://i.imgur.com/VXSiJse.gif)
- ![history](https://i.imgur.com/eP0NXmE.gif)
- ![](https://i.imgur.com/YoFpzvb.png)
- ![](https://i.imgur.com/lIeEI6P.png)
- ![](https://i.imgur.com/Nb8Lem0.png)
- ![](https://i.imgur.com/Zt3eAGT.png)

## 3. Features
- The ***“PiEnvir”*** project is a smart room design idea inspired by the smart house and author own body condition.
- It would help user to monitor the environment data through the sensors, such as temperature, air quality, and humidity.
- User could customize their own prefer profile and know who are using the room now.
- In this project, provide a chart-based website to view back the history data and latest an hour data. Meanwhile, this website is a responsive website design. You could view on different kinds of device including laptop, smartphone, or tablet.
- You account password would be encrypted by **Bcrypt** with salt and RSA-2048 key.
- If you send the privacy data to server, you data would be encrypt by the public key which send for you while request the pages. Each key expired in 600 seconds.
- ***PiEnvir*** also provide a clear user interface (UI) design that make you easier to read the data and warns you the room environment is suit for you or not currently.

## 4. Prepare
### 4.1. Hardward
1. Raspberry Pi Model 3B *1
2. Personal Computer (Windows OS) *1
3. USB Cable for Raspberry Pi *1
4. AC Power Adaptor *1
5. Micro SD Card 16GB+ *1
6. Keyboard, Mouse, and Monitor *1 set
7. HDMI Cable *1
8. Internet Connection
9. SD Card Reader *1
10. HDMI to Video Graphics Array (VGA Cable) *1
11. Keyboard, Video and Mouse (KVM) Switch *1

### 4.2. Software
1. SD Card Formatter — 5.0.1
2. Raspbian OS — 2019-09-26
3. Win32 Disk Imager — 1.0
4. RealVNC Client — 6.19.923
5. Berryconda — 2.0.0
6. Visaul Studio Code — 1.41.1

### 4.3. Accessories
1. Plantower G5 PMS5003 *1
2. Grove - Gas Sensor MQ2 (Seed Studio) *1
3. MCP3008 10-bit Analog-to-Digital Converter (ADC) *1
4. 3.3V-to-5V Logical Level Converter *1
5. DHT22 Temperature Humidity Sensor Module *1
6. LED (Green *1, Red *1)
7. Resistor (220 Ohms) *5
8. Raspberry Pi Camera Module *1
9. Servo Motor (SG90) *1
10. Piezo Buzzer *1
11. Passive Infrared Sensor *1
12. 2.54mm Pin Header *12
13. 2.54mm Dupont Line
14. Breadboard *1

## 5. Setup and Installation
### 5.1. Download from GitHub
- You need to download latest verion of this via the GitHub.
- You could visit the repository on GitHub in [here](https://github.com/jason40418/iot_project).
- If you have git install on your Raspberry Pi, you could download via the ```clone``` commend.
```shell=
$ git clone https://github.com/jason40418/iot_project.git
```
- If you use the linux-based OS, you also could download via the ```wget``` commend.
```shell=
$ wget https://github.com/jason40418/iot_project/archive/master.zip
```
- If you use have no idea, you could download via the http directly [here](https://github.com/jason40418/iot_project/archive/master.zip).
    - Otherwise, you could use default application to uncompress the file.
    - You also could install others software to achieve this goal.
    - [7-Zip](https://www.7-zip.org/)、[Bandizip](https://en.bandisoft.com/bandizip/)、[winrar](https://www.rarlab.com/)
    - You also could use the commend to decompress the zip file
    ```shell=
    $ unzip master.zip
    ```
### 5.2. Setup the Environment
- :sparkles: Make sure you have been disabled the serial termianal and enable the serial port. It is very important for this project or PMS5003 would not work properly.
- You need to prepare a Windows-X OS computer.
    - In this project, I use Windows 10 Pro 1910 as example.
- Make sure you have enable all needed interfaces as the following figure.
    - ![](https://i.imgur.com/fiBLqAb.png)
- :star2: **Notice that**: Make sure you have been set up the Samba and Crontab. Make this Raspberry Pi could use the share folder and schedule the periodly to execute the auto monitor script. If you not setup finished, you could visit [here](/InxvIs0vSVO_BIFnQ08P9w).


### 5.3. Setting up Secondary Camera
- Then, you need to setup another computer with secondary camera.
- In this project, I use laptop to do as my secondary camera. Therefore, I no need to buy another webcam or need to setup anything.
- If you use desktop, you may need to buy one and install some driver or software. You need to follow its mannual step and make sure that camera could cpature the real-time figure.
- :star2: **Notice that**: You need to setup the Sambea finish and login with your Samba account and password to connect to the share folder.
    - ![](https://i.imgur.com/Gzcy40y.png)
        - You may need to enter the account and password on this promp box.
    - ![](https://i.imgur.com/YOetIxl.png)
        - You could see it mount on Z:.
- Then you need to execute the```face_identify_exit.bat``` script.
    - You may need to modify this file to fit your environment first.
    - In here, I install the MiniConda to manage my Python package.
    - You need to modify the path and share folder path. (Default is point to miniconda path and mount on Z:/)
    ```shell=
    # Change to the MiniConda execute binary file
    cd C:\Users\user\Miniconda3\condabin
    
    # Activate the environment
    call conda activate
    
    # Change to share folder
    cd /D Z:\iot_project
    
    # Execute the face recongnize model via share folder
    python recognize_exit.py --detector model/face/face_detection_model \
            --embedding-model model/face/openface_nn4.small2.v1.t7 \
            --recognizer model/face/output/recognizer.pickle \
            --le model/face/output/le.pickle
    ```
- It may take a period of time to download the file and execute via SSH. Be patient on it.
    - ![](https://i.imgur.com/oqco6uE.png)
        - The speed to load the model is opt to your computer speed, hard disk speed, and network speed.
        - While the model load success, the light of camera would emit.
    - :star2: **Notice that**: Unlike the PiCamera. This script is used the model while the first time load. It means that you need to restart this script file to load the latest model which has been changed while executing this script file.
    - :star2: This is because it is have trouble to set up the subprocess on Windows based system.
- After you finish the setup you would see the real-time video on your computer. The fps is low is normal situation do not worry about it. 
- You could press ```ctrl+c``` to terminate the program.

### 5.4. Import iot.sql to Database
- In here, I use a GUI software (dbForge Studio Express for MySQL) to operate the MySQL. You need to point to the specfic IP, port , user account, password, and database first.
    - ![](https://i.imgur.com/QLPeQFF.png)
        - You need to enter the needed information to build a connection.
        - If you not sure correct or not, you could press test connection.
    - ![](https://i.imgur.com/naTbQeF.png)
- You could download this software free community version in [here](https://www.devart.com/dbforge/mysql/studio/download.html). The express version is enough for you to develope. (In here I use 8.2 version.)
- Then you need import the ```iot.sql``` to this database.
    - create a new database.
        - ![](https://i.imgur.com/5d75LYd.png)
        - recommend that you naming it iot.
    - choose database and open sql file then click execute to import the tables.
        - ![](https://i.imgur.com/Ct3g0aF.png)

- After setting up all thing, you could opereate and store the monitor, member, and accessories data.


## 6. Versioning
- This library uses SemVer for versioning. For the versions available, see the tags on this repository.

## 7. Author
- Hung Chih Lin
- A graduate student at Nation Central Univery in Taiwan
- Major in Information Management

## 8. References
### 8.1. Vendor Plugin
- In this project, I uses lots of plugin to achieve this beautiful UI and complete system.
- Thanks for these plugins make me could develope this system in a short time.

| Plugin                     | Version | Description                                                                                                                                                                           | Website                                                 |
| -------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| animate.css                | 3.7.2   | This is uset to make words have awesome animation.                                                                                                                                    | https://daneden.github.io/animate.css/                  |
| awesome-bootstrap-checkbox | 0.3.7   | This is used to make checkbox more beautiful                                                                                                                                          | https://github.com/flatlogic/awesome-bootstrap-checkbox |
| blueimp                    | 2.36.0  | This is used to make upload avatars could view as gallery.                                                                                                                            | https://blueimp.github.io/Gallery/                      |
| bootstrap                  | 3.4.1   | This version is used to fit the flask-upload                                                                                                                                          | https://getbootstrap.com/docs/3.4/                      |
| bootstrap-toggle           | 2.2.2   | This is used to make sensor switch more morden.                                                                                                                                       | https://www.bootstraptoggle.com/                        |
| bootstrap-validator        | 0.11.9  | This plugin is used to vaildate the form.                                                                                                                                             | https://1000hz.github.io/bootstrap-validator/           |
| chart.js                   | 2.9.3   | This is used to display the data as the chart in front-end.                                                                                                                           | https://www.chartjs.org/                                |
| chart.js-plugin-streaming  | 1.8.0   | It is a plugin to stream the real-time data with chart.js                                                                                                                             | https://github.com/nagix/chartjs-plugin-streaming       |
| cors                       | None    | This is a part of the flask-upload.                                                                                                                                                   | https://github.com/ngoduykhanh/flask-file-uploader      |
| flipping-clock             | None    | This is to display the right-top conor real-time clock                                                                                                                                | https://codepen.io/harshabhat86/pen/tAxuF/              |
| forge                      | 0.9.1   | This plugin is to use RSA public key to encrypt.                                                                                                                                      | https://github.com/digitalbazaar/forge                  |
| font-awesome               | 4.7.0   | This is use for icons.                                                                                                                                                                | https://fontawesome.com/v4.7.0                          |
| highlight                  | 9.16.2  | This is used to highlight the code block based on program language                                                                                                                    | https://highlightjs.org/                                |
| highligh-line-number       | 2.7.0   | This is used to let code block has line number.                                                                                                                                       | https://github.com/wcoder/highlightjs-line-numbers.js/  |
| ion.rangeSlider            | 2.3.1   | This plugin makes you could scroll a range as a slider.                                                                                                                               | http://ionden.com/a/plugins/ion.rangeSlider/            |
| jquery                     | 3.4.1   | This plugin let you could use javascipt with simply.                                                                                                                                  | https://jquery.com/                                     |
| jquery-confirm.js          | 3.3.4   | This plugin makes you could promp out with a modern alert-box.                                                                                                                        | https://craftpip.github.io/jquery-confirm/              |
| jquery.fileupload          | 1.7.2   | This plugin let you could upload the file through drag and drop. You also could preview the image, audio, and video. Most important, it provide detail Flask-side and front-side API. | https://github.com/ngoduykhanh/flask-file-uploader      |
| jquery.number              | 2.1.6   | This makes you easily to format the number                                                                                                                                            | https://github.com/customd/jquery-number                |
| jquery.ui.widget           | 1.12.1  | This is jquery based widget                                                                                                                                                           | https://jqueryui.com/widget/                            |
| moment.js                  | 2.24.0  | This plugin make you easy to fomrate the datetime.                                                                                                                                    | https://momentjs.com                                    |
| polyfill                   | None    | Make writing CSS polyfills much, much easier.                                                                                                                                         | https://github.com/philipwalton/polyfill/               |
| popper.js                  | 1.16.0  | This is use for tooltip.                                                                                                                                                              | https://popper.js.org/                                  |
| slick                      | 1.8.1   | This makes div could like slideshow                                                                                                                                                   | http://kenwheeler.github.io/slick/                      |
| socket.io-client           | 2.2.0   | This plugin is used to emit,receive, and build the websocket connection.                                                                                                              | https://github.com/socketio/socket.io-client            |
| toastr                     | 2.1.4   | This is used to display the right-top side real-time alert.                                                                                                                           | https://github.com/CodeSeven/toastr |

### 8.2. Websites
1. https://medium.com/@DannyAziz97/rsa-encryption-with-js-python-7e031cbb66bb
2. https://stackoverflow.com/questions/17415579/how-to-iso-8601-format-a-date-with-timezone-offset-in-javascript
3. https://github.com/1000hz/bootstrap-validator/issues/52
4. https://stackoverflow.com/questions/35854244/how-can-i-create-a-horizontal-scrolling-chart-js-line-chart-with-a-locked-y-axis
5. https://bestjquery.com/tutorial/tab/demo77/
6. https://jsfiddle.net/dhirajbodicherla/wmaftobx/13/
7. http://jsfiddle.net/M4Fcd/186/
8. https://github.com/dabeaz/python-cookbook/blob/master/src/9/multiple_dispatch_with_function_annotations/example1.py
9. https://pjchender.blogspot.com/2017/01/html-5-data-attribute.html
