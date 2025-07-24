<h1 align="center"> 
Audio Configuration
</h1>


<h2>
Software Required for adding audio into project
</h2>


* L-ISA Processor
* L-ISA Controller
* LoopMIDI
* Reaper
* Dante Virtual Soundcard
* Dante Controller

<h2>
Audio Configuration
</h2>

<h3>
Setting up L-ISA Processor and L-ISA Controller Software
</h3>

1. Open up L-ISA Processor software
2. Refer to Figure 1 and follow the following steps below
3. Click on the Audio Device Type (Red Circle), on the dropdown menu select ASIO 
4. Click on Output (Green Circle), on the dropdown menu select Dante VSC
5. Make sure the sample rate is 48000 Hz and also under Input Channel Range, it is [1,96]
<img src="./Audio Images Used/L-ISA Processor1.png">
(Figure 1)
<br>
<br>

6. Open up L-ISA Controller software
7. Refer to figure 2 and follow the following steps below
8. Click on Processors at the top right (Red Circle)
9. Click on the dropdown menu under "Main" (Green Circle), Select your laptop 
10. Click on Connect (Yellow Circle)
<img src="./Audio Images Used/L-ISA Processor2.png">
(Figure 2)

11. Setting up of L-ISA is complete

----------

<h3>
Setting up LoopMidi Software
</h3>

1. Open up LoopMIDI software
2. Refer to Figure 3 and follow the following steps below
3. Change the port name to whichever you want (Red Circle)
4. Click on the + icon on the bottom left (Green Circle) and the name you changed will appear in the middle

<img src="./Audio Images Used/LoopMIDI1.png">
(Figure 3)

5. Setting up of LoopMIDI is complete

----------

<h3>
Setting up Reaper Software
</h3>

1. Open up Reaper software
2. Refer to Figure 4 and follow the following steps below
3. Either click on Options (Red Circle) and in the dropdown menu click on Preferences (Green Circle) or press "cntrl + p" on your keyboard 

<img src="./Audio Images Used/Reaper1.png">
(Figure 4)
<br>
<br>

4. Refer to Figure 5 and follow the following steps below

5. Navigate and find "MIDI Outputs" (Red Circle) and check if your name that you set in the LoopMIDI (Figure 3) shows up (Green Circle)

<img src="./Audio Images Used/Reaper2.png">
(Figure 5)
<br>
<br>

6. Refer to Figure 6 and follow the following steps below

7. To generate the timecode for reaper, click on insert (Red Circle)

8. In the drop down menu click on SMPTE LTC/MTC Time code Generator (Green Circle)

<img src="./Audio Images Used/Reaper3.png">
(Figure 6)
<br>
<br>

9. If successful, the time code generator will appear in reaper(Figure 7)

<img src="./Audio Images Used/Reaper4.png">
(Figure 7)
<br>
<br>

10. Setting up of Reaper is complete

----------

<h3>
Audio Configuration is now complete
</h3>