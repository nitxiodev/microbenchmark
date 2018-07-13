## Run with[.../microbenchmark/tests/$]: nosetests --with-coverage --cover-package=.. __init__.py
import unittest

import nose, mock
from hamcrest import assert_that, greater_than, has_entries, equal_to, raises, calling

from microbenchmark.src import Microbenchmark

dummy_method = lambda x: 1 + x
METHODS = {
    0: {'a': lambda: dummy_method},
    1: {'b': lambda: int('hello')}
}


class testMicrobenchmark(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _build_instance(self, method=0):
        return Microbenchmark(METHODS[method])

    def testRunRightAverageSync(self):
        m = self._build_instance()
        m.run(1)
        assert_that(m.execution_time, has_entries({'a': greater_than(0)}))

    def testRunRightAverageAsync(self):
        m = self._build_instance()
        m.run(1, async=True)
        assert_that(m.execution_time, has_entries({'a': greater_than(0)}))

    def testExceptioninRunGivesNoExecTime(self):
        m = self._build_instance(1)
        m.run(1)
        assert_that(m.execution_time, has_entries({'b': equal_to(0)}))

    def testExceptionPlot(self):
        m = self._build_instance(0)
        assert_that(calling(m.plot), raises(KeyError, 'You must run first before plotting data.'))

    def testBadFigpath(self):
        m = self._build_instance(0)
        m.run(1)
        assert_that(calling(m.plot).with_args('aa'), raises(ValueError))

    @mock.patch('matplotlib.pyplot.savefig', return_value=None)
    def testCoverage1(self, mock_savefig):
        m = self._build_instance(0)
        m.run(1)
        m.plot('a.pdf')

    @mock.patch('matplotlib.pyplot.show', return_value=None)
    def testCoverage1(self, mock_show):
        m = self._build_instance(0)
        m.run(1)
        m.plot()


if __name__ == '__main__':
    nose.run()
