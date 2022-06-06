# Stress Test powered by LOCUST

## Install and run

Install the Locust new library:

```
$ py -m pip install locust
```

Check you have build up the containers with docker compose and then 
run the service where the locustfile.py lives:

```
$ cd stress_test/
$ py -m locust
```

You should see something like this:

```
[2022-06-06 15:28:42,651] DESKTOP-0GQ5H5T/INFO/locust.main: Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)
[2022-06-06 15:28:42,667] DESKTOP-0GQ5H5T/INFO/locust.main: Starting Locust 2.9.0

```
Now you are able to start the stress test.

To stop the service:

```
$ exit
```

## Stress Test

1. Open your browser and reach the localhost & port url as mention in the locust service log. Enter values and press the start button:

<img src="locust_index.jpg" alt="locust_index" width="600"/>

2. Check 