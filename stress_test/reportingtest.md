Report

DESKTOP Characteristics
Intel(R) Core(TM) i7-8650U CPU @ 1.90GHz 2.11 GHz
16,0 GB RAM

First Term:

-number of users: 10
-spawn rate: 1
-time: 13 min
-average size: 219
-not scaled

results:
GET
-requests: 966
-fails: 0
-rps: 1.7
POST
-requests: 832
-fails: 10
-rps: 1.3

total rps: 3

Second Term:

-number of users: 50
-spawn rate:1
-time:19 min
-average size: 345
-not scaled

results:
GET
-requests: 1382
-fails: 0
-rps: 1.4
POST
-requests: 1334
-fails: 138
-rps: 1.1

total rps: 2.5

Third Term:

-number of users: 100
-spawn rate: 1
-time: 14 min
-average size: 207
-not scaled

results:
GET
-requests: 1092
-fails: 0
-rps: 1.1
POST
-requests: 1062
-fails: 120
-rps: 1.6
-not scaled

total rps: 2.7

SCALED: with 10, 50 and 100 users

<img src="locust report.png" alt="locust_index" width="500"/>

To sum up:
Total rps: 2.6. The model scaled with the three-fold modality shows a significant difference in performance improvement
