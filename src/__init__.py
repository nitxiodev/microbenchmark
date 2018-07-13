from gevent.monkey import patch_all
patch_all()

from datetime import datetime
import multiprocessing
from gevent.pool import Pool
import numpy as np
import matplotlib.pyplot as plt

SUPPORTED_FORMATS = ('.pdf', '.png', '.ps', '.eps', '.svg')


class Microbenchmark(object):
    def __init__(self, methods):
        self._methods = methods
        self._exec_time = {}
        self._improvements = {}
        self._pool = Pool(multiprocessing.cpu_count())

    def __del__(self):
        self._pool.kill()

    @property
    def execution_time(self):
        return self._exec_time

    def run(self, executions=10, async=False, verbose=False):
        """
        Performs microbenchmark over 'n' executions and get the average of them.\n
        :param executions: Number of executions (default: 10; max: 10000).
        :param async: Run in async mode (with gevent).
        """

        executions = int(10e4 if executions > 10e4 else executions)

        for method in self._methods:
            self._exec_time[method] = self._pool.apply_async(self._inner_run,
                                                             (self._methods[method], executions, verbose,))
            if not async:
                self._exec_time[method] = self._exec_time[method].get()

        if async:
            self._pool.join()
            for i in self._exec_time:
                self._exec_time[i] = self._exec_time[i].get()

    def _inner_run(self, method, executions, verbose):
        average = 0

        for execution in xrange(executions):
            init_time = datetime.now()
            try:
                method()
                end_time = datetime.now() - init_time

                # Incremental averaging
                average += float(end_time.total_seconds() - average) / (execution + 1)
            except Exception as e:
                average = 0
                if verbose:
                    print 'Method {} raised the following exception: {}'.format(method, e)
                break
        return average * 1000  # milliseconds

    def plot(self, fig_path=None):
        if not self._exec_time:
            raise KeyError('You must run first before plotting data.')

        ind = np.arange(len(self._exec_time))
        width = .3

        plt.bar(ind, self._exec_time.values(), width, align='edge')
        plt.gca().set_xticks(ind + width / 2)
        plt.gca().set_xticklabels(self._exec_time)

        if fig_path:
            if not fig_path.lower().endswith(SUPPORTED_FORMATS):
                raise ValueError(
                    'Path {} doesnt contain one of supported formats: {}'.format(fig_path, SUPPORTED_FORMATS))
            plt.savefig(fig_path)
        else:
            plt.show()