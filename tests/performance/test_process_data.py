import re
from collections import OrderedDict

import pytest

DATA = [
    {
        "title": "# Scenario 1 | No concurrence | Execution 1 | No Shared session\n",
        "output": """
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
""",
    },
    {
        "title": "# Scenario 1 | No concurrence | Execution 1 | Shared session\n",
        "output": """
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
""",
    },
    {
        "title": "# Scenario 1 | No concurrence | Execution 2 | No Shared session\n",
        "output": """
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
        """,
    },
    {
        "title": "# Scenario 1 | No concurrence | Execution 2 | Shared session\n",
        "output": """
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
        """,
    },
    {
        "title": "# Scenario 1 | No concurrence | Execution 3 | No Shared session\n",
        "output": """
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
        """,
    },
    {
        "title": "# Scenario 1 | No concurrence | Execution 3 | Shared session\n",
        "output": """
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
        """,
    },
    {
        "title": "# Scenario 2 | With concurrence | Execution 1 | Shared session\n",
        "output": """
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
        """,
    },
    {
        "title": "# Scenario 2 | With concurrence | Execution 1 | No Shared session\n",
        "output": """
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
        """,
    },
    {
        "title": "# Scenario 2 | With concurrence | Execution 2 | Shared session\n",
        "output": """
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
        """,
    },
    {
        "title": "# Scenario 2 | With concurrence | Execution 2 | No Shared session\n",
        "output": """
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
        """,
    },
    {
        "title": "# Scenario 2 | With concurrence | Execution 3 | Shared session\n",
        "output": """
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
        """,
    },
    {
        "title": "# Scenario 2 | With concurrence | Execution 3 | No Shared session\n",
        "output": """
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
        """,
    },
]


@pytest.mark.skip
def test_convert_to_csv():
    FILE = "data-processed.txt"
    for item in DATA:
        data = item["output"]
        data = data.split("\n")
        # format data in csv
        result = []
        for row in data:
            # remove seconds (s) from duration
            row = row.replace("s ", " ")
            # convert spaces to comma
            row = re.sub(r"\s+", ",", row)
            result.append(row)

        result_dict = OrderedDict()
        for row in result:
            if not row:
                continue
            new = row.split(",")
            if not new[0]:
                continue
            duration = float(new[0])
            stage = new[1]
            # sum duration of stages
            result_dict[stage] = round(result_dict.get(stage, 0) + duration, 2)
            result_dict["duration"] = result_dict.get("duration", 0) + duration
        result_dict["title"] = item["title"]
        result_dict[stage] = round(result_dict[stage], 2)
        result_dict["duration"] = round(result_dict["duration"], 2)
        # sample: {'setup': 7.11, 'teardown': 3.66, 'call': 17.86}
        print(result_dict)
        with open(FILE, "a") as f:
            f.write(f"{str(result_dict)}\n")
    with open(FILE, "a") as f:
        f.write("=====\n")
    print(f"Data saved to {FILE}")
