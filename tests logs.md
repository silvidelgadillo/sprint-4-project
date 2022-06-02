AXX01@DESKTOP-0GQ5H5T MINGW64 ~
$ pwd
/c/Users/AXX01

AXX01@DESKTOP-0GQ5H5T MINGW64 ~
$ cd sprint-4-project/

AXX01@DESKTOP-0GQ5H5T MINGW64 ~/sprint-4-project (RICARDOSORIA_assignment)
$ cd api

AXX01@DESKTOP-0GQ5H5T MINGW64 ~/sprint-4-project/api (RICARDOSORIA_assignment)
$ docker build -t flask_api_test --progress=plain --target test .
#1 [internal] load build definition from Dockerfile
#1 sha256:ae5c23cf3152d8f9b6740f83f2fbf0cc2b3760040fb7e08f2fca2e58e85dcd17
#1 transferring dockerfile: 355B 0.0s done
#1 DONE 0.0s

#2 [internal] load .dockerignore
#2 sha256:82b3de3567f1436249a9cb2015948e9a8bad4e22b219ed6e9ee7b0fb6c4321d9
#2 transferring context: 2B done
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/python:3.8.13
#3 sha256:b4c4e39c4ea3cc183ec0280e50649099607635bc8d0b1d20249d0b1b5028bfb8
#3 DONE 0.0s

#4 [base 1/5] FROM docker.io/library/python:3.8.13
#4 sha256:a3ce4c276dccdb4f94088f8c11a66398f97e180bed5d4bd6b2f37209a2da314e
#4 DONE 0.0s

#5 [internal] load build context
#5 sha256:6f5cf39888ebc5f5bcdd585e74894fd1dcfc809cd516711b4f35b267d336840a
#5 transferring context: 53.50kB 0.0s done
#5 DONE 0.0s

#6 [base 2/5] ADD requirements.txt .
#6 sha256:5eb44921c306946846078e6cbb9894bfae5aba9390b8d53fd9e5131017007804
#6 CACHED

#7 [base 3/5] RUN pip3 install -r requirements.txt
#7 sha256:52d1b881f56726957959abb690fac2f25a3569de44d4303d28aebc03279668a7
#7 CACHED

#8 [base 4/5] ADD ./ /src/
#8 sha256:97d207c5606ae11e58905ca0ac28d91c7b4997817e70e28f11c7b0364cda55a6
#8 CACHED

#9 [base 5/5] WORKDIR /src
#9 sha256:476febdfe979b300247f5769f4521d2a3d26f0c1cd14d55ebf8d2343f888f35b
#9 CACHED

#10 [test 1/1] RUN ["pytest", "-v", "/src/tests"]
#10 sha256:c7623620e5dcf48a53732e28f9a31c173e77f68303fd546e615f08d9e8493263
#10 1.622 ============================= test session starts ==============================
#10 1.622 platform linux -- Python 3.8.13, pytest-7.1.1, pluggy-1.0.0 -- /usr/local/bin/python
#10 1.622 cachedir: .pytest_cache
#10 1.622 rootdir: /src
#10 1.622 collecting ... collected 8 items
#10 2.143
#10 2.143 tests/test_api.py::TestIntegration::test_feedback PASSED                 [ 12%]
#10 2.189 tests/test_api.py::TestIntegration::test_predict_bad_parameters PASSED   [ 25%]
#10 2.194 tests/test_api.py::TestIntegration::test_predict_ok PASSED               [ 37%]
#10 2.205 tests/test_api.py::TestEnpointsAvailability::test_feedback PASSED        [ 50%]
#10 2.209 tests/test_api.py::TestEnpointsAvailability::test_index PASSED           [ 62%]
#10 2.215 tests/test_api.py::TestEnpointsAvailability::test_predict PASSED         [ 75%]
#10 2.219 tests/test_utils.py::TestUtils::test_allowed_file PASSED                 [ 87%]
#10 2.222 tests/test_utils.py::TestUtils::test_get_file_hash PASSED                [100%]
#10 2.226
#10 2.226 ============================== 8 passed in 0.60s ===============================
#10 DONE 2.3s

#11 exporting to image
#11 sha256:e8c613e07b0b7ff33893b694f7759a10d42e180f2b4dc349fb57dc6b71dcab00
#11 exporting layers 0.1s done
#11 writing image sha256:220e97e780ed7d2336719a242ce455979c26815d2752d9ba1855c7330ff72a37
#11 writing image sha256:220e97e780ed7d2336719a242ce455979c26815d2752d9ba1855c7330ff72a37 done
#11 naming to docker.io/library/flask_api_test done
#11 DONE 0.1s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them

AXX01@DESKTOP-0GQ5H5T MINGW64 ~/sprint-4-project/api (RICARDOSORIA_assignment)
$ cd ../model

AXX01@DESKTOP-0GQ5H5T MINGW64 ~/sprint-4-project/model (RICARDOSORIA_assignment)
$ docker build -t model_test --progress=plain --target test .
#1 [internal] load build definition from Dockerfile
#1 sha256:53559c98a5b0da9de876e4f7b271b495884ca02fd1d74f1023da8791f327ad24
#1 DONE 0.0s

#1 [internal] load build definition from Dockerfile
#1 sha256:53559c98a5b0da9de876e4f7b271b495884ca02fd1d74f1023da8791f327ad24
#1 transferring dockerfile: 326B done
#1 DONE 0.0s

#2 [internal] load .dockerignore
#2 sha256:bd66211e3b2f3aee61fb4f35440be8dc14bc1d6bdc23e80178d1051a7ea94100
#2 transferring context: 2B done
#2 DONE 0.0s

#3 [internal] load metadata for docker.io/library/python:3.8.13
#3 sha256:b4c4e39c4ea3cc183ec0280e50649099607635bc8d0b1d20249d0b1b5028bfb8
#3 DONE 0.0s

#4 [base 1/5] FROM docker.io/library/python:3.8.13
#4 sha256:a3ce4c276dccdb4f94088f8c11a66398f97e180bed5d4bd6b2f37209a2da314e
#4 DONE 0.0s

#5 [internal] load build context
#5 sha256:dff0ba5ecbda8871f7e397b0ab6fbf90273d5d32f98ebef63a0ff7c8dc5da0b1
#5 transferring context: 39.78kB done
#5 DONE 0.0s

#7 [base 3/5] RUN pip3 install -r requirements.txt
#7 sha256:51bf1b3733d1c5a46c187a172ae3dd0c03822042301b7aca0b523e03c4c1a05b
#7 CACHED

#8 [base 4/5] ADD ./ /src/
#8 sha256:2eb5ee8123a5d83c546ef2a8b1d6ad7f30b068d2a067ed579d5d27cbbb906c26
#8 CACHED

#9 [base 5/5] WORKDIR /src
#9 sha256:dd877a097225f07864c44422162d2835e16e9ff114ba030331ab96fd6327629f
#9 CACHED

#6 [base 2/5] ADD requirements.txt .
#6 sha256:ed375f52130591347a08a237440bea0e36efd641e3e8874adb0ad5da047c818a
#6 CACHED

#10 [test 1/1] RUN ["pytest", "-v", "/src/tests"]
#10 sha256:9f874ad93e24c5ff5fa48c117ff2285d2ec8040af200cbbe3ec03a74e8100890
#10 CACHED

#11 exporting to image
#11 sha256:e8c613e07b0b7ff33893b694f7759a10d42e180f2b4dc349fb57dc6b71dcab00
#11 exporting layers done
#11 writing image sha256:81780a0a54c7e6e4e2c9caa820233f56d9e5f13755c426ab1f70f67fa02416aa done
#11 naming to docker.io/library/model_test done
#11 DONE 0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them

AXX01@DESKTOP-0GQ5H5T MINGW64 ~/sprint-4-project/model (RICARDOSORIA_assignment)
$ cd ..

AXX01@DESKTOP-0GQ5H5T MINGW64 ~/sprint-4-project (RICARDOSORIA_assignment)
$ python tests/test_integration.py
No se encontr▒ Python; ejecuta sin argumentos para instalar desde Microsoft Store o deshabilita este acceso directo en Configuraci▒n > Administrr alias de ejecuci▒n de la aplicaci▒n.

AXX01@DESKTOP-0GQ5H5T MINGW64 ~/sprint-4-project (RICARDOSORIA_assignment)
$ py tests/test_integration.py
.C:\Users\AXX01\AppData\Local\Programs\Python\Python39\lib\unittest\case.py:550: ResourceWarning: unclosed file <_io.BufferedReader name='tests/og.jpeg'>
  method()
ResourceWarning: Enable tracemalloc to get the object allocation traceback
.
----------------------------------------------------------------------
Ran 2 tests in 2.566s

OK

