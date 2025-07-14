"""
Tests for the Indicators module
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to the path to import meridianalgo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meridianalgo.indicators import Indicators


class TestIndicators:
    """Test class for Indicators module"""
    
    def setup_method(self):
        """Set up test data"""
        # Create sample price data
        np.random.seed(42)
        dates = pd.date_range(start='2023-01-01', end='2023-01-31', freq='D')
        
        self.data = pd.DataFrame({
            'open': np.random.uniform(100, 110, len(dates)),
            'high': np.random.uniform(110, 120, len(dates)),
            'low': np.random.uniform(90, 100, len(dates)),
            'close': np.random.uniform(100, 110, len(dates)),
            'volume': np.random.randint(1000, 10000, len(dates))
        })
        self.data.index = dates
    
    def test_sma(self):
        """Test Simple Moving Average calculation"""
        period = 10
        sma = Indicators.sma(self.data['close'], period)
        
        # Check that SMA is a pandas Series
        assert isinstance(sma, pd.Series)
        
        # Check that first (period-1) values are NaN
        assert sma.iloc[:period-1].isna().all()
        
        # Check that SMA values are reasonable
        assert sma.iloc[period:].notna().all()
        assert (sma >= 0).all() or sma.isna().all()
    
    def test_ema(self):
        """Test Exponential Moving Average calculation"""
        period = 10
        ema = Indicators.ema(self.data['close'], period)
        
        # Check that EMA is a pandas Series
        assert isinstance(ema, pd.Series)
        
        # Check that EMA values are reasonable
        assert ema.notna().all()
        assert (ema >= 0).all()
    
    def test_rsi(self):
        """Test Relative Strength Index calculation"""
        period = 14
        rsi = Indicators.rsi(self.data['close'], period)
        
        # Check that RSI is a pandas Series
        assert isinstance(rsi, pd.Series)
        
        # Check that RSI values are between 0 and 100 (or NaN)
        valid_rsi = rsi.dropna()
        if len(valid_rsi) > 0:
            assert (valid_rsi >= 0).all()
            assert (valid_rsi <= 100).all()
    
    def test_macd(self):
        """Test MACD calculation"""
        macd_line, signal_line, histogram = Indicators.macd(self.data['close'])
        
        # Check that all components are pandas Series
        assert isinstance(macd_line, pd.Series)
        assert isinstance(signal_line, pd.Series)
        assert isinstance(histogram, pd.Series)
        
        # Check that all have the same length
        assert len(macd_line) == len(signal_line) == len(histogram)
        
        # Check that histogram equals macd_line - signal_line
        assert histogram.equals(macd_line - signal_line)
    
    def test_bollinger_bands(self):
        """Test Bollinger Bands calculation"""
        upper, middle, lower = Indicators.bollinger_bands(self.data['close'])
        
        # Check that all bands are pandas Series
        assert isinstance(upper, pd.Series)
        assert isinstance(middle, pd.Series)
        assert isinstance(lower, pd.Series)
        
        # Check that all have the same length
        assert len(upper) == len(middle) == len(lower)
        
        # Check that upper >= middle >= lower (where not NaN)
        valid_mask = upper.notna() & middle.notna() & lower.notna()
        if valid_mask.any():
            assert (upper[valid_mask] >= middle[valid_mask]).all()
            assert (middle[valid_mask] >= lower[valid_mask]).all()
    
    def test_stochastic(self):
        """Test Stochastic Oscillator calculation"""
        k_percent, d_percent = Indicators.stochastic(
            self.data['high'], 
            self.data['low'], 
            self.data['close']
        )
        
        # Check that both are pandas Series
        assert isinstance(k_percent, pd.Series)
        assert isinstance(d_percent, pd.Series)
        
        # Check that both have the same length
        assert len(k_percent) == len(d_percent)
        
        # Check that values are between 0 and 100 (or NaN)
        valid_k = k_percent.dropna()
        valid_d = d_percent.dropna()
        
        if len(valid_k) > 0:
            assert (valid_k >= 0).all()
            assert (valid_k <= 100).all()
        
        if len(valid_d) > 0:
            assert (valid_d >= 0).all()
            assert (valid_d <= 100).all()
    
    def test_atr(self):
        """Test Average True Range calculation"""
        atr = Indicators.atr(
            self.data['high'], 
            self.data['low'], 
            self.data['close']
        )
        
        # Check that ATR is a pandas Series
        assert isinstance(atr, pd.Series)
        
        # Check that ATR values are positive (or NaN)
        valid_atr = atr.dropna()
        if len(valid_atr) > 0:
            assert (valid_atr >= 0).all()
    
    def test_volume_sma(self):
        """Test Volume Simple Moving Average calculation"""
        period = 10
        volume_sma = Indicators.volume_sma(self.data['volume'], period)
        
        # Check that volume SMA is a pandas Series
        assert isinstance(volume_sma, pd.Series)
        
        # Check that values are reasonable
        assert volume_sma.notna().all() or volume_sma.iloc[:period-1].isna().all()
        assert (volume_sma >= 0).all() or volume_sma.isna().all()
    
    def test_price_channels(self):
        """Test Price Channels calculation"""
        upper, lower, middle = Indicators.price_channels(
            self.data['high'], 
            self.data['low']
        )
        
        # Check that all channels are pandas Series
        assert isinstance(upper, pd.Series)
        assert isinstance(lower, pd.Series)
        assert isinstance(middle, pd.Series)
        
        # Check that all have the same length
        assert len(upper) == len(lower) == len(middle)
        
        # Check that upper >= middle >= lower (where not NaN)
        valid_mask = upper.notna() & middle.notna() & lower.notna()
        if valid_mask.any():
            assert (upper[valid_mask] >= middle[valid_mask]).all()
            assert (middle[valid_mask] >= lower[valid_mask]).all()
    
    def test_williams_r(self):
        """Test Williams %R calculation"""
        williams_r = Indicators.williams_r(
            self.data['high'], 
            self.data['low'], 
            self.data['close']
        )
        
        # Check that Williams %R is a pandas Series
        assert isinstance(williams_r, pd.Series)
        
        # Check that values are between -100 and 0 (or NaN)
        valid_wr = williams_r.dropna()
        if len(valid_wr) > 0:
            assert (valid_wr >= -100).all()
            assert (valid_wr <= 0).all()
    
    def test_cci(self):
        """Test Commodity Channel Index calculation"""
        cci = Indicators.cci(
            self.data['high'], 
            self.data['low'], 
            self.data['close']
        )
        
        # Check that CCI is a pandas Series
        assert isinstance(cci, pd.Series)
        
        # Check that CCI values are reasonable (can be positive or negative)
        assert cci.notna().all() or cci.iloc[:20].isna().all()  # First 20 values might be NaN


if __name__ == "__main__":
    pytest.main([__file__]) 