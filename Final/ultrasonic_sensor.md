<h1 align="center"> 
Explanation for ultrasonic code
</h1>


<h2>
Python/txt files that are used for ultrasonic sensors
</h2>

-[calibration.py](./Code_used/calibration.py)

-[tryy.py](./Code_used/tryy.py)

-[thresholds.txt](./Code_used/thresholds.txt)


----
<h2>
calibration.py 
</h2>
This code is for calibrating the ultrasonic sensors before the start of our game to ensure that during the game even if the batteries are placed in weird postions, the sensors will still be able to give out the right distances.

<br>

Before you run the code make sure that you have typed in the right  TRIG and ECHO which can be found at **line 10-13**. Also make sure you have chosen the right sensor you would like to calibrate at **line 50** by changing the numbers from 0-3 (where 0 is the first sensor).

<br>

Once you have run the code you will be able to see multiple readings for the distances every 0.2 which you can change at **line 66**.

<br>

**Do take note that this code does not affect the main code and its only purpose is to calibrate the sensors so mistakes can be prevented during the game.**

------

<h2>
tryy.py 
</h2>

This code is for converting a range of distances detected using the ultrasonic sensor into a fixed distance so that the main code will be able to use it to check for the results.

Before running the code ensure that you have linked the right txt files in **line 31**. Also make sure that you have typed in the right  TRIG and ECHO which can be found at **line 6-9**. 

How this code works is that it will take the distance of whatever you have set in the txt file for example in **line 59-68** if you set t1 as 15, t2 as 20, t3 as 25. If the distance shown is 22 it will set the distance as 20 as if the distance is less then 25 and more or equal then 20 so in this case 22 fits this requirement hence will set the value as 20.
<br>
<br>
```
def quantize_distance(distance, thresholds):<br>
    t1, t2, t3 = thresholds<br>
    if distance <= t1:<br>
        return 10<br>
    elif distance <= t2:<br>
        return 20<br>
    elif distance <= t3:<br>
        return 30<br>
    else:<br>
        return 40
```
------
<h2>
thresholds.txt
</h2>

This txt file is for to help tryy.py to set the range so that it will provide the right distance and is easier to change the range compared to doing it in a python file and will be safer as no code will be touched.

So how it works is that for example in the txtf file on **line 2** 01_02: 20, 01 relates to which battery pack it is (In this case battery pack 1), 02 relates to which slot it is (In this case slot 2) and finally 20 relates to which the range you would want to set so that within that range you will get your desired value.

--------
<h2>
Explanation for Ultrasonic_sensor code is now complete
</h2>