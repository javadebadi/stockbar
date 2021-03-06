from .bar import Bar, BarNotFoundException, TestBar

class PriceBar(Bar):
    def _errorMessagePriceComparison(self, price_1, price_2):
        return "The {} must be less than or equal to {}".format(price_1, price_2)

    def _isTypeValid(self):
        """Checks weather prices are float or castable to float or not"""

        assert(type(float(self.low)) == float)
        assert(type(float(self.high)) == float)
        assert(type(float(self.close)) == float)
        assert(type(float(self.open_)) == float)

    def _isValueValid(self):
        """Checks weather prices values are compatible with logical expectations or not"""

        if self.low > self.high:
            raise ValueError(self._errorMessagePriceComparison("low", "high"))
        
        if self.open_ > self.high:
            raise ValueError(self._errorMessagePriceComparison("open","high"))

        if self.close > self.high:
            raise ValueError(self._errorMessagePriceComparison("close","high"))

        if self.low > self.close:
            raise ValueError(self._errorMessagePriceComparison("low","close"))

        if self.low > self.open_:
            raise ValueError(self._errorMessagePriceComparison("low","open"))        

    def _isValid(self):
        """Checks weather prices type and value are valid or not"""
        self._isTypeValid()
        self._isValueValid()

    def __init__(self, low, high, close, open_ , prev=None, next_=None):        
        
        super().__init__(low=low, high=high, close=close, open_=open_, prev=prev, next_=next_)
        self._isValid()
        
    def _doesPrevExist(self):
        if self.prev is not None:
            return True
        else:
            return False

    def isOpenUp(self):
        """The opening price is the first trade done between a buyer and a seller 
        on the trading day. It reflects the new day’s hopes and fears.
        """
        if not self._doesPrevExist():
            return None
        return True if self.open_ >= self.prev.close else False

    def isCloseUp(self):
        """if today close is upper than yesterday's close, it means that 
        probably more buyers want to buy the security in the upcomming days"""
        if not self._doesPrevExist():
            return None
        return True if self.close >= self.prev.close else False
    
    def isCloseDown(self):
        if self.prev is not None:
            return not self.isCloseUp()
        else:
            return None

    def diffCloseHigh(self):
        """difference of High price and close price, if this difference
        is small then it is big singal. Buyers don't want to get rid of 
        the stock and they think that tomorrow will be better"""
        return self.high - self.close

    def diffCloseLow(self):
        """difference of close and low. If this diffrence is small it 
        means that some bad news has raised"""
        return self.close - self.low

    def isCloseNearHigh(self, threshold=0.02):
        return True if (self.diffCloseHigh() / self.high) < threshold else False

    def isCloseNearLow(self, threshold=0.02):
        return True if (self.diffCloseLow() / self.close) < threshold else False
        
    def isHigherHigh(self):
        return True if self.high >= self.prev.high else False

    def isLowerHigh(self):
        return not self.isHigherHigh()

    def isHigherLow(self):
        return True if self.low >= self.prev.low else False

    def isLowerLow(self):
        return not self.isHigherLow()

    def isUp(self):
        return self.isCloseUp() and self.isHigherHigh() and self.isHigherLow()

    def isDown(self):
        return self.isCloseDown() and self.isLowerHigh() and self.isLowerLow()

    def nDaysWasUpTrending(self):
        currentBar = self
        number_of_ternding_days = 0
        while currentBar.isUp():
            number_of_ternding_days += 1
            currentBar = currentBar.prev
        return number_of_ternding_days

    def nDaysWasDownTrending(self):
        currentBar = self
        number_of_ternding_days = 0
        while currentBar.isDown():
            number_of_ternding_days += 1
            currentBar = currentBar.prev
        return number_of_ternding_days


    def __str__(self):
        result = super().__str__() + "\n"
        return result


class TestPriceBar(TestBar):
    def __init__(self):
        super().__init__()
        self.baseBar = PriceBar(low=50, high=100, open_=60, close=70)

    def reset(self):
        self.baseBar = PriceBar(low=50, high=100, open_=60, close=70)

    def test_isOpenUp(self):
        bar_1 = PriceBar(low=50, high=100, open_=60, close=70)
        bar_2 = PriceBar(low=50, high=100, open_=80, close=70, prev=bar_1)
        assert(bar_2.isOpenUp() == True)
        self.n_test += 1
        return True

    def test_isOpenDown(self):
        bar_1 = PriceBar(low=50, high=100, open_=60, close=70)
        bar_2 = PriceBar(low=50, high=100, open_=55, close=70, prev=bar_1)
        assert(bar_2.isOpenUp() == False)
        self.n_test += 1
        return True

    def test_isCloseUp(self):
        bar_1 = PriceBar(low=50, high=100, open_=60, close=70)
        bar_2 = PriceBar(low=50, high=100, open_=60, close=80, prev=bar_1)
        assert(bar_2.isCloseUp() == True)
        self.n_test += 1
        return True

    def test_isCloseDown(self):
        bar_1 = PriceBar(low=50, high=100, open_=60, close=70)
        bar_2 = PriceBar(low=50, high=100, open_=80, close=60, prev=bar_1)
        assert(bar_2.isCloseUp() == False)
        self.n_test += 1
        return True     
    
    def test_difference_of_close_and_high(self):
        bar_1 = PriceBar(low=50, high=100, open_=60, close=70)
        expected_diff = 30
        assert(expected_diff == bar_1.diffCloseHigh())
        self.n_test += 1
        return True

    def test_is_close_near_to_high(self):
        bar_1 = PriceBar(low=50, high=100, open_=60, close=70)
        assert(bar_1.isCloseNearHigh() == False)
        bar_1.close=99
        assert(bar_1.isCloseNearHigh() == True)
        self.n_test += 1
        return True       

    def test_difference_of_close_and_low(self):
        bar_1 = PriceBar(low=50, high=100, open_=60, close=70)
        expected_diff = 20
        assert(expected_diff == bar_1.diffCloseLow())
        self.n_test += 1
        return True

    def test_is_close_near_to_low(self):
        bar_1 = PriceBar(low=50, high=100, open_=60, close=70)
        assert(bar_1.isCloseNearLow() == False)
        bar_1.close=51
        assert(bar_1.isCloseNearLow() == True)
        self.n_test += 1
        return True

    def test_number_of_days_the_bar_was_upTrending(self):
        bar_1 = PriceBar(low=50, high=100, open_=60, close=70)
        bar_2 = PriceBar(low=60, high=110, open_=70, close=80, prev=bar_1)
        bar_3 = PriceBar(low=70, high=120, open_=80, close=90, prev=bar_2)
        bar_4 = PriceBar(low=80, high=130, open_=90, close=100, prev=bar_3)
        bar_5 = PriceBar(low=100, high=120, open_=105, close=105, prev=bar_4)
        assert(int(bar_1.nDaysWasUpTrending()) == 0)
        assert(int(bar_2.nDaysWasUpTrending()) == 1)
        assert(int(bar_3.nDaysWasUpTrending()) == 2)
        assert(int(bar_4.nDaysWasUpTrending()) == 3)
        assert(int(bar_5.nDaysWasUpTrending()) == 0)
        self.n_test += 1
        return True


    def testAll(self):
        test_result = super().testAll()
        test_result = test_result and self.test_isOpenUp()
        test_result = test_result and self.test_isOpenDown()
        test_result = test_result and self.test_isCloseUp()
        test_result = test_result and self.test_isCloseDown()
        test_result = test_result and self.test_difference_of_close_and_high()
        test_result = test_result and self.test_is_close_near_to_high()
        test_result = test_result and self.test_difference_of_close_and_low()
        test_result = test_result and self.test_is_close_near_to_low()
        test_result = test_result and self.test_number_of_days_the_bar_was_upTrending()
        return test_result

if __name__ == "__main__":
    TestPriceBar()