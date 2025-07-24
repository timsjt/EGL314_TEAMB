<h1>
Hardware setup for RFID readers and ultrasonic sensors
</h1>


<h2>
System Flowchart
</h2>




```mermaid
graph LR

A[Laptop VNC] <--WIFI connection-->B[Raspberry Pi 1]<--I²C-->C[ADC converter]
D[URM09 ultrasonic sensor 1]-->C
E[URM09 ultrasonic sensor 2]-->C
F[URM09 ultrasonic sensor 3]-->C
G[URM09 ultrasonic sensor 4]-->C
H[Push Button]-- one-wire -->B
K[RFID Readers 1 & 2]--USB A TO B -->J[Raspberry pi 2]
M[RFID Readers 3 & 4]--USB A TO B-->L[Raspberry pi 3]
J[Raspberry pi 2]--WIFI connection-->B[Raspberry Pi 1]
L[Raspberry pi 3]--WIFI connection-->B[Raspberry Pi 1]


```

------

<h2>
Hardware used
</h2>

* 3 Raspberry Pis 
* 4 URM09 ultrasonic sensor
* 1 Push button
* 4 RFID readers
* 16 RFID tags
* 1 ADC converter

<h2>
Explanations for battery pack setup
</h2>

<img src="Our box.png">
<img src="RFID on the battery pack.png">
<img src="Ultrasonic sensor.png">
<img src="Button.png">

<br>
<br>

<h2>
Explanations for battery setup
</h2>

<img src="Battery(back).png">
<img src="Battery(front).png">

<br>
<br>

<h2>
Explanations for cable management
</h2>

<img src="cable manage.png">
<img src="pi & breadboard.png">