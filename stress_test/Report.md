
Introduction:
I have made some tests about the capabillity of the API on the “índex” and “predict” endpoints. I launched two different tests, the first and simpler one with 5 users (at peak concurrency) and with just 1 user Spawn rate (users started per second). The second test was with 50 and 1 in this respective fields. Then, I tested how it would work the API not only with one instance of the model container but also with 3 containers created and running, looking for better results… 

OBS   :Each test last aprox. 5 minutes each.    
OBS(I):On my particular case I have a processor of 2,2 GHz Intel Core i7 and a memory of 16 GB 1600 MHz DDR3.     

Definitions:
TestA = TA = 5 users at peak concurrency and 1 at spawn rate.    
TestB = TB = 50 users at peak concurrency and 1 at spawn rate.    
TestAScaled = TAS = 5 users at peak concurrency and 1 at spawn rate, with 3 model containers running.    
TestBScaled = TBS = 50 users at peak concurrency and 1 at spawn rate, with 3 model containers running.    
requests = requests simulated from locust to our API.        
fails = total requests that failed.    
RPS = requests per second.    
fails% = failures/requests.    

Results:
TA  -> "/"        113 requests, fails=0, RPS=0.3, fails%=0.   
    -> "/predict  393 requests, fails=0, RPS=1.2, fails%=0.    

TAS -> "/"        141 requests, fails=0, RPS=0.3, fails%=0.    
    -> "/predict  398 requests, fails=0, RPS=1.2, fails%=0.    

TB  -> "/"        240 requests, fails=0, RPS=0.8, fails%=0.    
    -> "/predict  739 requests, fails=54, RPS=2.5, fails%=0.07.    

TBS -> "/"        389 requests, fails=0, RPS=1.4, fails%=0.    
    -> "/predict  1201 requests, fails=22, RPS=4.4, fails%=0.01.    


Analysis:
On the reports we can see that practically there is no difference between TA with TAS on each metric. The RPS of the endpoints "/" and /"predict" on both tests is exactly the same, we could have expected this due to that with this level of users and requests I am not demanding the API a lot, so scaling in this particular case is kind of silly because there is not a huge demand of requests (from another point of view, more abstract and particulary related to how we have been sending the requests to the model on this project. When the model is recieving requests stored in the queue of redis, as this queue is not long enough to demand more models, there will be no difference if we add more models in production as they are not required).
It is a whole different picture in the comparison of TB with TBS, as there were much more requests on this cases, a scaling of the model container should improve the speed and capabilty of the API. If we see the charts it is what happened, on TBS we can observe a better RPS and a lower percentage of failures than on TB.
In conclussion, we have to know and understand the specifics demands of our API endpoints in order to administrate better our resources. Going back to our tests, it would make sense to scale the model container if we have a demand of the amount of TB users or requests but it would not make sense with a demand of TA. 
