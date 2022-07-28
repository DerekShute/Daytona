"""
    Unit test master script

    ***RUN TESTS FROM HERE***
"""

import sys
import time
import pytest


if __name__ == '__main__':
    sys.path.insert(0, './daytona/')
    start = time.process_time()
    pytest.main(["--cov=daytona",
                 "--cov-branch",
                 "--no-cov-on-fail",
                 "--cov-report=term-missing",
                 "tests"])
    end = time.process_time()

    print(f'=== TEST RUN TIME: {end - start} microseconds')

# EOF
