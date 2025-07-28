"""
MeridianAlgo - Advanced stock prediction system using Yahoo Finance
Zero setup, no API keys required

Organized modules:
- prediction: ML models and ensemble methods for stock prediction
- analysis: Technical indicators and AI-powered market analysis  
- trading: Trading engines and backtesting capabilities
- utils: Utility functions and helpers
"""

__version__ = "0.3.1"
__author__ = "MeridianAlgo"
__email__ = "meridianalgo@gmail.com"

# Import from organized modules
from .prediction import MLPredictor, EnsembleModels
from .analysis import Indicators, AIAnalyzer
from .trading import TradingEngine, BacktestEngine
from .utils import TradeUtils

# Backward compatibility - direct imports
from .prediction.ml_predictor import MLPredictor
from .prediction.ensemble_models import EnsembleModels
from .analysis.indicators import Indicators
from .analysis.ai_analyzer import AIAnalyzer
from .trading.trading_engine import TradingEngine
from .trading.backtest_engine import BacktestEngine

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