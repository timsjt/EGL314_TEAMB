<h1>
Enabling Communication between Reaper and Raspi
</h1>

<h2>
Reaper configuration (OSC)
</h2>

1. Open up Reaper software
2. Refer to Figure 4 and follow the following steps below
3. Either click on Options (Red Circle) and in the dropdown menu click on Preferences (Green Circle) or press "cntrl + p" on your keyboard 

<img src="./Audio Images Used/Reaper1.png">
(Figure 1)
<br>
<br>


4. Refer to Figure 2 and follow the following steps below
5. Navigate to Control/OSC/Web (Red Circle) and click on Add (Green Circle)

<img src="./Audio Images Used/Reaper5.png">
(Figure 2)
<br>
<br>

6. Refer to Figure 3 and follow the following steps below
7. Make sure that you select the control surface mode as OSC (Open Sound Control)
8. Click on the mode (Red Circle) and in the dropdown menu and select Configure device IP+local port
9. You will have to change the **local listen port** and **local IP** depending on your setup (but this configuration is only for my current project)

<img src="./Audio Images Used/Reaper6.png">
(Figure 3)
<br>
<br>

10. Setting up of Reaper OSC is complete

<h2>
Raspi configuration
</h2>

1. Create a directory folder for the required python files. In this particular case, we are going to name the folder *reaper*.

```
mkdir reaper
```

2. Please copy the following files into the folder directory `~/reaper`

```
Reaper_test.py
```

3. Go to the directory `reaper`

```
cd ~/reaper
```

4. Edit the *IP Address* of the *Laptop (running Reaper)* in the respective python files

- Line 17 of `Reaper_test.py`
```
PI_A_ADDR = "10.10.10.10"
```

5. Run the python files `lisagui.py` (please ensure you have configured marker 1 in Reaper). If the script is executed successfully, it will play/stop the playback on reaper.

```
python3 lisagui.py
```

6. Raspi configuration for reaper is complete
