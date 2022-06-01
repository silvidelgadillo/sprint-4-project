# README

I made a script to automate the testing process. It runs ```docker compose up``` with a certain value for the ```--scale``` parameter, and after that
it run locust multiple times with a configurable combination of parameters. 

For each locust run, it saves an html report in the reports folder, with the next format in the name:

```
{number of model containers running}_{number of users}_{spawn rate}.html
```

### The configurable parameters are:

* ```num_models_list```: A list with the different number of model containers.
* ```num_users_list```: A list the different number of users.
* ```spawn_rate_list```: A list the different spawn rates.
* ```run_time```: A string with the execution time per each run.
* ```host```: A string with the host.

<br>

All the test were run with the GPU enabled and disabled (two different folders inside reports folder), and randomly choosing between 5 images for each request made.  

<br>

## My Hardware Specs:

<br>

* **Cpu**: Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz; 1 physical processor; 4 cores; 8 threads

* **Graphics Card**: nVidia GP107M [GeForce GTX 1050 Ti Mobile] 4 GB VRAM; Intel HD Graphics 630

* **Disk**: TOSHIBA MQ02ABD1; 1 TB

* **Ram**: Total memory: 16 GB; 2 modules in dual-channel: 8 GB; 2400 MHz

<br>

# Conclusions

For some reason regarding the memory, when scaling to two models using GPU, the model containers failed and closed. I didn't deep dive into that issue. In any case, I leave the locust reports for them in the respective folder.

On the other hand without scaling, the benefits of using GPU vs using CPU increased noticeably as the test became more demanding, but not as much when the test was light. When using 10 users and 1 in spawn rate, the response time decreased by ~25% using GPU. I think this is due to the limits that Flask or gunicorn impose in reducing the response time.

Regarding scaling using the CPU, globally, the response time was less than a half, which means that the API can handle more than double RPS using two model containers.

