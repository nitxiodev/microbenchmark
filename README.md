# microbenchmark
Just a simple microbenchmarking tool written in Python.

### Dependencies
- numpy
- gevent (async mode, but required in any case)
- matplotlib (optional, only required if you want to plot ```execution_time```)
- nose, coverage, pyhamcrest (optional, only for testing).

### Usage

```python
import numpy as np
import math, random

SIZE = 10000

# Define functions for benchmarking
from microbenchmark.src import Microbenchmark


def pure_python(size):
    return math.sin(random.choice([float(i) for i in xrange(size)]))


def numpy_version(size):
    return np.sin(np.random.choice(np.arange(size)))


functions = {
    'python': lambda: pure_python(SIZE),
    'numpy': lambda: numpy_version(SIZE)
}

# Instance Microbenchmark tool
microbenchmark = Microbenchmark(functions)

# Run benchmark (async mode)
microbenchmark.run(async=True, verbose=True)

# Get percentage of execution time of each one of them
exec_times = np.array(microbenchmark.execution_time.values())
exec_times = (exec_times / exec_times.sum()) * 100

print 'Exec times: {}: {:.1f}%, {}: {:.1f}%'.format('python', exec_times[0], 'numpy', exec_times[1])

# Show plot (matplotlib needed)
microbenchmark.plot()
```
### Results
```bash
Exec times: python: 98.1%, numpy: 1.9%
```

### Tests
```bash
/microbenchmark/tests/$: nosetests --with-coverage --cover-package=.. __init__.py
```
