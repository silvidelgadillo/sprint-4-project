# Spring 4 Stress Test Report
The idea of performing stress tests to the entire system running is to get an impression of how many users it can handle before getting timeouts or it stops responding.
We will try different combinations of model containers, quantity of users and Spawn rate to get a closer picture of the overall behavior of the complete system.

## Hardware specs of the server:
Below are the hardware specifications of the machine used to test the whole server running the API/Frontend and the model.

    Hardware Overview:
      Model Name: MacBook Pro
      Model Identifier: MacBookPro14,1
      Processor Name: Dual-Core Intel Core i5
      Processor Speed: 2,3 GHz
      Number of Processors: 1
      Total Number of Cores: 2
      L2 Cache (per Core): 256 KB
      L3 Cache: 4 MB
      Hyper-Threading Technology: Enabled
      Memory: 8 GB

## Different tests done with locust.

### Test run with **ONE MODEL** instance and **users**:100 **Spawn rate**:20.   

![First test](/stress_test/Report/m1-u100-sr20.png)  

### Test run with **TWO MODELS** instances and **users**:100 **Spawn rate**:20.
 
![First test](/stress_test/Report/m2-u100-sr20.png)

### Test run with **FOUR MODEL** instances and **users**:100 **Spawn rate**:20.
 
![First test](/stress_test/Report/m4-u100-sr20.png)

## Summary

One quick idea we can get from these tests is that the service is totally dependent of the amount of users and increasing the models running by **two**, we can improve the response per second the server is able to handle, but if we continue growing the amount of model containers running the server starts to decrease the amount of simultaneous responses, because each container uses more hardware to run and begins to decrease the final system response.