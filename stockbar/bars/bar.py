class BarNotFoundException(Exception):
    pass

class BarConflictException(Exception):
    pass

class Bar:
    """Base class for all Bars"""

    def _areNextAndPrevBar(self):
        """checks if next and prev objects are subclasses of Bar"""
        if self.next_ is not None:
            assert(issubclass(type(self.next_),Bar))
        if self.prev is not None:
            assert(issubclass(type(self.prev), Bar))
        if self.prev is not None:
            if self.prev.next_ is None:
                self.prev.next_ = self
            else:
                raise BarConflictException("the previous Bar for this Bar has another next_ Bar setted ...")
        if self.next_ is not None:
            if self.next_.prev is None:
                self.next_.prev = self
            else:
                raise BarConflictException("the next Bar for this Bar has another prev Bar setted ...")
    
    def __init__(self, low=None, high=None, close=None, open_=None, prev=None, next_=None):
        self.low = low
        self.high = high
        self.close = close
        self.open_ = open_
        self.prev = prev
        self.next_ = next_
        self._areNextAndPrevBar()
        self.values = {"low":self.low, "high":self.high, "close":self.close, "open":self.open_}


    def __str__(self):
        return str(self.values)


class TestBar():

    def __init__(self):
        self.baseBar = Bar(low=10, high=20, open_=14, close=18)
        self.n_test = 0

    def _reset(self):
        self.baseBar = Bar(low=10, high=20, open_=14, close=18)

    def test_init_with_prev_Bar(self):
        self._reset()
        newBar = Bar(low=30, high=50, open_=39, close=40, prev=self.baseBar)
        assert(newBar.prev == self.baseBar)
        self.n_test += 1
        return True

    def test_init_with_prev_Bar_with_existing_next_Bar(self):
        self._reset()
        nextBarOfBaseBar = Bar(low=40, high=100, close=60, open_=75, prev=self.baseBar)
        try:
            newBar = Bar(low=30, high=50, open_=39, close=40, prev=self.baseBar)
        except BarConflictException:
            pass
        except:
            print("Test FAILED ... test_init_with_prev_Bar_with_existing_next_Bar")
            self.n_test += 1
            return False
        self.n_test += 1
        return True
        
    def test_init_with_next_Bar(self):
        self._reset()
        newBar = Bar(low=30, high=50, open_=39, close=40, next_=self.baseBar)
        assert(newBar.next_ == self.baseBar)
        self.n_test += 1
        return True

    def test_init_with_next_Bar_with_existing_prev_Bar(self):
        self._reset()
        prevBarOfBaseBar = Bar(low=40, high=100, close=60, open_=75, next_=self.baseBar)
        try:
            newBar = Bar(low=30, high=50, open_=39, close=40, next_=self.baseBar)
        except BarConflictException:
            pass
        except:
            print("Test FAILED ... test_init_with_prev_Bar_with_existing_next_Bar")
            self.n_test += 1
            return False

        self.n_test += 1
        return True

    def testAll(self):
        self._reset()
        test_result = True
        test_result = test_result and self.test_init_with_prev_Bar()
        test_result = test_result and self.test_init_with_next_Bar()
        test_result = test_result and self.test_init_with_prev_Bar_with_existing_next_Bar()
        test_result = test_result and self.test_init_with_next_Bar_with_existing_prev_Bar()
        return test_result

    def __str__(self):
        test_result = self.testAll()
        return f"OK: {self.n_test} tests run" if test_result else f"FAILED: {self.n_test} tests run"

    def __del__(self):
        print(self)
        

if __name__ == "__main__":
    TestBar()