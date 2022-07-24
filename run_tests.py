"""
    Unit test master script

    ***RUN TESTS FROM HERE***
"""

import pytest
import sys
import time

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
