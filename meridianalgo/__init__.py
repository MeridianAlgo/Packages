"""
MeridianAlgo - Advanced stock prediction system using Yahoo Finance
Zero setup, no API keys required

Organized modules:
- prediction: ML models and ensemble methods for stock prediction
- analysis: Technical indicators and AI-powered market analysis  
- trading: Trading engines and backtesting capabilities
- utils: Utility functions and helpers
"""

__version__ = "0.3.2"
__author__ = "MeridianAlgo"
__email__ = "meridianalgo@gmail.com"

# Import submodules
from . import prediction
from . import analysis
from . import trading

# Import main classes for backward compatibility
from .prediction.ml_predictor import MLPredictor
from .prediction.ensemble_models import EnsembleModels
from .analysis.indicators import Indicators
from .analysis.ai_analyzer import AIAnalyzer
from .trading.trading_engine import TradingEngine
from .trading.backtest_engine import BacktestEngine
from .utils import TradeUtils

__all__ = [
    # Main classes
    "MLPredictor",
    "EnsembleModels", 
    "Indicators",
    "AIAnalyzer",
    "TradingEngine",
    "BacktestEngine",
    "TradeUtils",
    
    # Submodules
    "prediction",
    "analysis", 
    "trading",
    "utils"
]