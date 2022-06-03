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

All the test were run for 7 minutes and with the GPU enabled and disabled (two different folders inside reports folder), and randomly choosing between 5 images for each request made.  

<br>

## My Hardware Specs:

<br>

* **Cpu**: Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz; 1 physical processor; 4 cores; 8 threads

* **Graphics Card**: nVidia GP107M [GeForce GTX 1050 Ti Mobile] 4 GB VRAM; Intel HD Graphics 630

* **Disk**: TOSHIBA HDD 1 TB

* **Ram**: Total memory: 16 GB; 2 modules in dual-channel: 8 GB; 2400 MHz

<br>

# Conclusions

For some reason regarding the memory, when scaling to two models using GPU, the model containers failed and closed. Consequently, inside ```reports/with_gpu``` folder, there are only tests without scaling the model.

On the other hand, without scaling the benefits of using GPU vs CPU slightly increased as the test became more demanding (10% of increase), with a mean improvement of the response time of approximately 45% using GPU (using 90%ile for calculation). I think this is a low value, given that in Sprint Project 3 when changing from CPU to GPU I've seen decreases in processing time of about 10x or more. My guess here is that Flask, redis or gunicorn impose limits when reducing the response time, but I really don't know. **EDIT:** I realized that it is due to the total sleep time of about 100 ms of the API.

Regarding scaling using the CPU, the response time was less than a half using two models, which means that the API can handle more than double RPS. Furthermore, working with 2 models on CPU gives us better results than working with only 1 model on GPU (~14 RPS vs ~10 RPS respectively).

<br>

## Conclusions [UPDATE]

<br>

Looking at the Sprint Project 5 code, I found this lines:

<br>

```
# Prevent tensorflow to allocate the entire GPU
physical_devices = config.list_physical_devices("GPU")
try:
    config.experimental.set_memory_growth(physical_devices[0], True)
except:
    pass
```

Using them the issue regarding the VRAM when scaling the model was fixed. One model container now only takes 600 MB in VRAM, and not 3.5 GB like before.

I run the tests with 4 models and the API was able to easily handle 23 predictions/s. Now we're talking xD. The reports are inside ```reports/with_gpu```.

**EDIT:** I implemented batch predicting, and ran a test with batch size of 10, in the GPU, and with 4 models. The results were worse than in the case without using batches. The report is in ```reports/batch_10``` folder.  

**EDIT 2:** I ran a test without scaling the model and using a batch size of 10, and the perfomance was very similar to that of the test scaling the model to 4, and without batch processing. So the improvement is very noticeable. Now we're talking x2 xD.