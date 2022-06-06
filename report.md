# REPORT

## Hardware specs - ThinkPad X280
```
Processor: Intel(R) Core(TM) i5-7300U CPU @ 2.60GHz, 3M Cache, up to 3.50 GHz (2 cores / 4 threads)
RAM: 8,00 GB
Integrated Graphic Processor: Intel(R) HD Graphics 620
OS: Windows 10 Pro 21H2
```

## Stress testing with *locust*

### With 1 model:

Without scaling, the webservice hardly accepts more than 5 users per second without failing after reaching 100 users (total number of users tested).

### With 2 models:

Here is a little bit of improvment aldo not enough to take positive conclusion about scaling the model.
There surely are benefits to the practice with real paralisation on a better hardware.

## Batch processing