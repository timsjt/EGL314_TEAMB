<h1>
Hardware setup for RFID readers and ultrasonic sensors
</h1>


<h2>
System Flowchart
</h2>




```mermaid
graph LR

A[Laptop VNC] <--WIFI connection-->B[Raspberry Pi 1]
D[HC-SR04 ultrasonic sensor 1]--GPIO-->B
E[HC-SR04 ultrasonic sensor 2]--GPIO-->B
F[HC-SR04 ultrasonic sensor 3]--GPIO-->B
G[HC-SR04 ultrasonic sensor 4]--GPIO-->B
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

* [HC-SR04 Ultrasonic sensor x4](https://projecthub.arduino.cc/Isaac100/getting-started-with-the-hc-sr04-ultrasonic-sensor-7cabe1)
* Large LED Arcade Button
* [Raspberry PI model 4b x3](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
* [Phidgets 1023 RFID reader x4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
* RFID Tags


<h2>
Explanations for battery pack setup
</h2>

<img src="sensor.jpg">

<br>
<br>

<h2>
Explanations for battery setup
</h2>

<img src="battery.jpg">

<br>
<br>

<h2>
Explanations for cable management
</h2>

<img src="cover_cable.jpg">
<img src="triangle.jpg">