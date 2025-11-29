# Scenario 1 - No concurrence
## Execution 1
### No shared session
```bash
python -m pytest -k test_big_scenario_of_functions_without_session_http --durations=0 -random-order
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=1382528414
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 301 items / 291 deselected / 10 selected                                                                             

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1 PASSED               [ 10%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5 PASSED               [ 20%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9 PASSED               [ 30%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10 PASSED              [ 40%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4 PASSED               [ 50%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8 PASSED               [ 60%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2 PASSED               [ 70%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6 PASSED               [ 80%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7 PASSED               [ 90%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3 PASSED               [100%]

====================================================== slowest durations =======================================================
3.42s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
2.23s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
1.84s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
1.79s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
1.78s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
1.78s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
1.77s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
1.73s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
1.70s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
1.69s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
1.55s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
0.43s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
0.42s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.40s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
0.40s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
0.40s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
============================================= 10 passed, 291 deselected in 28.95s ==============================================

```

## Shared session
```bash
python -m pytest -k test_big_scenario_of_functions_with_session_http --durations=0 -random-order
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=2805815262
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 301 items / 291 deselected / 10 selected                                                                             

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10 PASSED                 [ 10%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8 PASSED                  [ 20%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4 PASSED                  [ 30%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9 PASSED                  [ 40%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1 PASSED                  [ 50%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5 PASSED                  [ 60%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7 PASSED                  [ 70%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3 PASSED                  [ 80%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2 PASSED                  [ 90%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6 PASSED                  [100%]

====================================================== slowest durations =======================================================
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
1.65s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
1.63s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
1.62s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
1.54s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
1.54s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
1.51s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
1.50s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
1.49s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
1.45s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
1.40s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
1.38s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
0.59s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
0.47s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.44s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
0.43s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
0.43s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
0.43s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
0.42s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
0.40s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
============================================= 10 passed, 291 deselected in 24.69s ==============================================
```

## Execution 2
### No shared session
```bash
python -m pytest -k test_big_scenario_of_functions_without_session_http --durations=0 -random-order
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=55218217
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 301 items / 291 deselected / 10 selected                                                                             

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5 PASSED               [ 10%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1 PASSED               [ 20%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9 PASSED               [ 30%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4 PASSED               [ 40%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8 PASSED               [ 50%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6 PASSED               [ 60%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2 PASSED               [ 70%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3 PASSED               [ 80%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7 PASSED               [ 90%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10 PASSED              [100%]

====================================================== slowest durations =======================================================
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
2.01s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
1.86s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
1.84s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
1.79s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
1.73s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
1.65s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
1.61s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
1.59s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
1.58s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
1.53s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
1.27s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
0.61s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.60s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
0.57s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
0.53s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
0.46s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
0.43s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
0.42s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
0.42s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
============================================= 10 passed, 291 deselected in 26.84s ==============================================

```
### Shared session
```bash
python -m pytest -k test_big_scenario_of_functions_with_session_http --durations=0 -random-order
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=1872312787
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 301 items / 291 deselected / 10 selected                                                                             

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4 PASSED                  [ 10%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8 PASSED                  [ 20%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1 PASSED                  [ 30%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5 PASSED                  [ 40%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9 PASSED                  [ 50%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7 PASSED                  [ 60%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3 PASSED                  [ 70%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10 PASSED                 [ 80%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2 PASSED                  [ 90%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6 PASSED                  [100%]

====================================================== slowest durations =======================================================
3.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
1.91s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
1.69s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
1.61s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
1.56s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
1.56s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
1.48s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
1.47s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
1.46s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
1.46s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
1.44s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
1.44s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.52s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
0.51s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
0.46s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
0.45s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
0.44s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
0.43s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.43s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
============================================= 10 passed, 291 deselected in 25.11s ==============================================
```

## Execution 3
### No shared session
```bash
python -m pytest -k test_big_scenario_of_functions_without_session_http --durations=0 -random-order
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=299171876
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 301 items / 291 deselected / 10 selected                                                                             

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10 PASSED              [ 10%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6 PASSED               [ 20%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2 PASSED               [ 30%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3 PASSED               [ 40%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7 PASSED               [ 50%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5 PASSED               [ 60%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1 PASSED               [ 70%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9 PASSED               [ 80%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4 PASSED               [ 90%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8 PASSED               [100%]

====================================================== slowest durations =======================================================
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
1.88s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
1.72s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
1.67s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
1.66s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
1.62s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
1.62s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
1.62s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
1.51s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
1.50s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
1.46s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
1.32s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
0.63s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
0.47s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
0.46s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.45s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
0.44s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
0.42s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
0.42s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
0.40s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
============================================= 10 passed, 291 deselected in 25.62s ==============================================
```
### Shared session
```bash
python -m pytest -k test_big_scenario_of_functions_with_session_http --durations=0 -random-order
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=874562232
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
collected 301 items / 291 deselected / 10 selected                                                                             

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5 PASSED                  [ 10%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1 PASSED                  [ 20%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9 PASSED                  [ 30%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4 PASSED                  [ 40%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8 PASSED                  [ 50%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10 PASSED                 [ 60%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6 PASSED                  [ 70%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2 PASSED                  [ 80%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3 PASSED                  [ 90%]
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7 PASSED                  [100%]

====================================================== slowest durations =======================================================
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
1.67s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
1.60s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
1.51s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
1.48s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
1.48s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
1.47s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
1.44s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
1.44s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
1.43s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
1.43s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
1.28s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
0.49s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.47s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
0.46s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
0.45s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
0.45s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
0.45s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
0.44s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
0.42s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
0.41s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
0.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
============================================= 10 passed, 291 deselected in 24.23s ==============================================
```
# Secenario 2 - with concurrence (-n auto)
## Execution 1
### Shared session
```bash
python -m pytest -k test_big_scenario_of_functions_with_session_http --durations=0 -random-order -n auto
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=4074239062
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
4 workers [10 items]    
scheduling tests via LoadScheduling

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6 
[gw3] [ 10%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10 
[gw1] [ 20%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9 
[gw2] [ 30%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2 
[gw0] [ 40%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5 
[gw3] [ 50%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7 
[gw2] [ 60%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2 
[gw0] [ 70%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5 
[gw1] [ 80%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3 
[gw3] [ 90%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7 
[gw1] [100%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3 

====================================================== slowest durations =======================================================
3.79s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
3.75s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
3.69s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
3.60s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
3.59s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
3.56s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
3.48s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
3.41s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
3.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
3.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
2.23s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
2.14s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
2.12s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
2.12s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
1.72s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
1.31s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
1.30s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
1.17s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
1.08s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
1.04s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
0.82s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
0.51s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
===================================================== 10 passed in 18.04s ======================================================
```
### No shared session
```bash
python -m pytest -k test_big_scenario_of_functions_without_session_http --durations=0 -random-order -n auto
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=1525082352
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
4 workers [10 items]    
scheduling tests via LoadScheduling

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7 
[gw0] [ 10%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2 
[gw1] [ 20%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3 
[gw2] [ 30%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1 
[gw3] [ 40%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5 
[gw1] [ 50%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4 
[gw0] [ 60%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6 
[gw2] [ 70%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8 
[gw3] [ 80%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10 
[gw1] [ 90%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4 
[gw0] [100%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8 

====================================================== slowest durations =======================================================
3.69s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
3.63s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
3.60s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
3.58s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
3.48s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
3.47s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
3.34s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
3.33s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
3.15s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
3.14s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
3.06s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
2.47s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
2.47s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
2.38s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
2.31s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
1.93s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
1.85s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
1.66s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
1.64s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
1.59s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
1.54s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
0.94s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
0.91s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
0.15s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
0.13s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
0.11s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
0.11s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
===================================================== 10 passed in 18.93s ======================================================

```

## Execution 2
### Shared session
```bash
python -m pytest -k test_big_scenario_of_functions_with_session_http --durations=0 -random-order -n auto
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=3270874462
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
4 workers [10 items]    
scheduling tests via LoadScheduling

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10 
[gw2] [ 10%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10 
[gw0] [ 20%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3 
[gw1] [ 30%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2 
[gw3] [ 40%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1 
[gw0] [ 50%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3 
[gw2] [ 60%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5 
[gw3] [ 70%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1 
[gw1] [ 80%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6 
[gw0] [ 90%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9 
[gw2] [100%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5 

====================================================== slowest durations =======================================================
3.81s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
3.69s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
3.65s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
3.62s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
3.55s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
3.36s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
3.32s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
3.32s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
3.14s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
3.12s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
3.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
3.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
2.70s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
2.63s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
2.39s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
2.29s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
1.90s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
1.88s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
1.47s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
1.46s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
1.37s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
1.34s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
0.85s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
0.85s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
0.17s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.13s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
0.10s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
===================================================== 10 passed in 18.89s ======================================================

```
### No shared session
```bash
python -m pytest -k test_big_scenario_of_functions_without_session_http --durations=0 -random-order -n auto
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=1413430422
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
4 workers [10 items]    
scheduling tests via LoadScheduling

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7 
[gw2] [ 10%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10 
[gw1] [ 20%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1 
[gw3] [ 30%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5 
[gw0] [ 40%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8 
[gw0] [ 50%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8 
[gw2] [ 60%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10 
[gw1] [ 70%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6 
[gw3] [ 80%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3 
[gw2] [ 90%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2 
[gw1] [100%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6 

====================================================== slowest durations =======================================================
3.51s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
3.46s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
3.45s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
3.44s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
3.43s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
3.43s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
3.37s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
3.33s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
3.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
3.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
3.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
2.49s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
2.39s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
2.29s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
2.29s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
1.93s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
1.90s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
1.56s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
1.55s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
1.55s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
1.36s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
0.77s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
0.75s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
0.15s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.12s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
0.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
===================================================== 10 passed in 18.52s ======================================================

```

## Execution 3
### Shared session
```bash
python -m pytest -k test_big_scenario_of_functions_with_session_http --durations=0 -random-order -n auto
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=700748289
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
4 workers [10 items]    
scheduling tests via LoadScheduling

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1 
[gw0] [ 10%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2 
[gw3] [ 20%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1 
[gw2] [ 30%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6 
[gw1] [ 40%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3 
[gw2] [ 50%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9 
[gw0] [ 60%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6 
[gw3] [ 70%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4 
[gw1] [ 80%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3 
[gw0] [ 90%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8 
[gw3] [100%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4 

====================================================== slowest durations =======================================================
3.86s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
3.82s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
3.79s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
3.61s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
3.57s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
3.35s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
3.26s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
3.24s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
3.14s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
3.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
2.59s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
2.52s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
2.45s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
2.34s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
1.90s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
1.89s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
1.88s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
1.77s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
1.74s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http3
1.45s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http9
0.93s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http4
0.86s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http8
0.19s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http10
0.15s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http7
0.12s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http1
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http5
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http6
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_with_session_http2
===================================================== 10 passed in 19.41s ======================================================
```
### No shared session
```bash
python -m pytest -k test_big_scenario_of_functions_without_session_http --durations=0 -random-order -n auto
===================================================== test session starts ======================================================
platform linux -- Python 3.12.3, pytest-9.0.1, pluggy-1.6.0
Using --randomly-seed=3110200315
rootdir: /home/douglas/repo/caqui
configfile: pytest.ini
plugins: xdist-3.8.0, randomly-4.0.1, asyncio-1.3.0
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=function, asyncio_default_test_loop_scope=function
4 workers [10 items]    
scheduling tests via LoadScheduling

tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1 
[gw3] [ 10%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7 
[gw2] [ 20%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1 
[gw0] [ 30%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8 
[gw1] [ 40%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5 
[gw3] [ 50%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6 
[gw2] [ 60%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9 
tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2 
[gw0] [ 70%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8 
[gw1] [ 80%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5 
[gw3] [ 90%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6 
[gw2] [100%] PASSED tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2 

====================================================== slowest durations =======================================================
3.67s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
3.56s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
3.54s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
3.54s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
3.45s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
3.43s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
3.43s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
3.38s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
3.14s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
3.10s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
3.07s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
2.52s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
2.43s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
2.40s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
2.26s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
1.93s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
1.88s call     tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
1.51s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
1.46s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http8
1.39s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http5
1.22s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.86s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http6
0.85s setup    tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http2
0.14s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http10
0.10s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http4
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http7
0.09s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http1
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http9
0.08s teardown tests/performance/test_single_session_http.py::test_big_scenario_of_functions_without_session_http3
===================================================== 10 passed in 18.60s ======================================================

```

# Data processing
```bash
python -m pytest -k process_data -s 
```
# Result
- In scenarios without concurrence all executions using shared session (code bellow) performed better
```python
    async with ClientSession() as session_http:
        page = AsyncPage(server_url, capabilities, PAGE_URL, session_http=session_http)
```
- In scenarios with concurrent (`pytest -n auto`) the results were almost the same for shared and non-shared session

```bash
# Data organized by lowest 'duration'
OrderedDict({'teardown': 3.67, 'duration': 23.94, 'call': 14.95, 'setup': 5.32, 'title': '# Scenario 1 | No concurrence | Execution 3 | Shared session\n'})
OrderedDict({'teardown': 3.68, 'duration': 24.41, 'call': 15.17, 'setup': 5.56, 'title': '# Scenario 1 | No concurrence | Execution 1 | Shared session\n'})
OrderedDict({'teardown': 3.66, 'duration': 24.80, 'call': 15.62, 'setup': 5.52, 'title': '# Scenario 1 | No concurrence | Execution 2 | Shared session\n'})
OrderedDict({'teardown': 3.67, 'duration': 25.35, 'call': 16.26, 'setup': 5.42, 'title': '# Scenario 1 | No concurrence | Execution 3 | No Shared session\n'})
OrderedDict({'teardown': 3.68, 'duration': 26.59, 'call': 17.19, 'setup': 5.72, 'title': '# Scenario 1 | No concurrence | Execution 2 | No Shared session\n'})
OrderedDict({'teardown': 3.66, 'duration': 28.63, 'call': 17.86, 'setup': 7.11, 'title': '# Scenario 1 | No concurrence | Execution 1 | No Shared session\n'})
```

```bash
# Data organized by lowest accumulated duration (sum the duration of all threads)
OrderedDict({'call': 32.73, 'duration': 59.24, 'teardown': 12.81, 'setup': 13.70, 'title': '# Scenario 2 | With concurrence | Execution 1 | Shared session\n'})
OrderedDict({'call': 31.25, 'duration': 61.18, 'teardown': 12.93, 'setup': 17.00, 'title': '# Scenario 2 | With concurrence | Execution 2 | No Shared session\n'})
OrderedDict({'call': 31.81, 'duration': 61.67, 'teardown': 12.96, 'setup': 16.90, 'title': '# Scenario 2 | With concurrence | Execution 3 | No Shared session\n'})
OrderedDict({'call': 32.10, 'duration': 62.52, 'teardown': 13.07, 'setup': 17.35, 'title': '# Scenario 2 | With concurrence | Execution 2 | Shared session\n'})
OrderedDict({'call': 31.90, 'duration': 62.89, 'teardown': 13.08, 'setup': 17.91, 'title': '# Scenario 2 | With concurrence | Execution 1 | No Shared session\n'})
OrderedDict({'call': 32.27, 'duration': 63.90, 'teardown': 13.08, 'setup': 18.55, 'title': '# Scenario 2 | With concurrence | Execution 3 | Shared session\n'})
```

# Tuning web driver
TO run all tests do `python -m pytest -k TestPerformance`. All results are ordered by lowest duration.
## Scenario 1 - no aditional arguments in driver
- Execution 1 (duration): 64.65s
- Execution 2 (duration): 66.40s
- Execution 3 (duration): 67.16s

## Scenario 2 - added arguments to driver
```python
options = ChromeOptionsBuilder().args([
    "headless",
    "blink-settings=imagesEnabled=false",
    "disable-extensions", 
    "disable-plugins", 
    "disable-background-timer-throttling" 
    ])
# and page_load_strategy("eager")
capabilities = (
    ChromeCapabilitiesBuilder()
    .accept_insecure_certs(True)
    .add_options(options)
    .page_load_strategy("eager")
```
- Execution 3 (duration): 46.42s
- Execution 1 (duration): 47.54s
- Execution 2 (duration): 48.12s

## Scenario 3 - reuse server instance
Not dispose the server after finishe the test
```python
@fixture(autouse=True, scope="session")
def setup_server():
    server = Server.get_instance(port=SERVER_PORT)
    server.start()
    # yield
    # server.dispose(delay=3)
```
- Execution 3 (duration): 42.80s
- Execution 2 (duration): 42.93s
- Execution 1 (duration): 43.27s

## Scenario 4 - run in multiprocessing
```python
# add -n auto
python -m pytest -k TestPerformance -n auto
```
- Execution 2 (duration): 28.19s
- Execution 3 (duration): 28.53s
- Execution 1 (duration): 29.96s

## Scenario 5 - using `ujson` module instead of built-in `json`
Executed with a fresh server instance
- Execution 1 (duration): 27.49s
- Execution 2 (duration): 27.68s
- Execution 3 (duration): 28.44s
- mean: 27.87s

## Scenario 6 - using `orjson` module
Executed with a fresh server instance
- Execution 1 (duration): 27.57s
- Execution 3 (duration): 27.90s
- Execution 2 (duration): 28.11s
- mean: 27.86s

## Scenario 7 - using `urllib3` module instead of `requests`
- Execution 1 (duration): 27.84s
- Execution 2 (duration): 34.95s
- Execution 3 (duration): 28.32s