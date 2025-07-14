# MeridianAlgo Usage Guide

## 🎯 **What is MeridianAlgo?**

MeridianAlgo is a **universal algorithmic trading library** that anyone can use to:
- Create and test trading strategies
- Calculate technical indicators
- Analyze trading performance
- Manage risk and position sizing
- Backtest strategies on historical data

## 📦 **Installation**

### Quick Install
```bash
cd MeridianAlgo
python install.py
```

### Manual Install
```bash
pip install -r requirements.txt
pip install -e .
```

## 🔧 **Basic Usage**

### Import the Library
```python
from meridianalgo import TradingEngine, BacktestEngine, Indicators, TradeUtils
```

### 1. Trading Engine (Live Trading)
```python
# Initialize trading engine
engine = TradingEngine(paper_trading=True)  # Use paper trading for safety
engine.connect()

# Get account info
account_info = engine.get_account_info()
print(f"Balance: ${account_info['balance']}")

# Place a trade
order = engine.place_order(
    symbol="BTC/USD",
    side="buy",
    quantity=0.1,
    order_type="market"
)

# Check positions
positions = engine.get_positions()
print(f"Current positions: {positions}")
```

### 2. Technical Indicators
```python
import pandas as pd

# Load your price data
data = pd.read_csv('your_price_data.csv')

# Calculate indicators
rsi = Indicators.rsi(data['close'], period=14)
sma_20 = Indicators.sma(data['close'], 20)
ema_20 = Indicators.ema(data['close'], 20)

# MACD
macd_line, signal_line, histogram = Indicators.macd(data['close'])

# Bollinger Bands
upper, middle, lower = Indicators.bollinger_bands(data['close'])

# Stochastic
k_percent, d_percent = Indicators.stochastic(data['high'], data['low'], data['close'])
```

### 3. Backtesting
```python
# Load historical data
data = pd.read_csv('historical_data.csv')
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Initialize backtest
backtest = BacktestEngine(initial_capital=10000)
backtest.load_data(data)

# Define your strategy
def my_strategy(row, positions, capital, data=None):
    """Your trading strategy logic"""
    current_idx = row.name
    
    if current_idx < 20 or data is None:
        return None
    
    # Get historical data
    close_prices = data['close'].iloc[:current_idx + 1]
    
    # Calculate indicators
    sma_10 = close_prices.rolling(10).mean().iloc[-1]
    sma_20 = close_prices.rolling(20).mean().iloc[-1]
    current_price = row['close']
    
    symbol = 'BTC/USD'
    
    # Buy signal
    if sma_10 > sma_20 and symbol not in positions:
        quantity = (capital * 0.1) / current_price
        return {
            'symbol': symbol,
            'action': 'buy',
            'quantity': quantity
        }
    
    # Sell signal
    elif sma_10 < sma_20 and symbol in positions:
        return {
            'symbol': symbol,
            'action': 'sell',
            'quantity': positions[symbol]['quantity']
        }
    
    return None

# Run backtest
results = backtest.run_backtest(my_strategy, data=data)

# View results
print(f"Total Return: {results['total_return']:.2%}")
print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
print(f"Max Drawdown: {results['max_drawdown']:.2%}")
```

### 4. Utility Functions
```python
# Position sizing
position_size = TradeUtils.calculate_position_size(
    capital=10000,
    risk_percent=2,  # Risk 2% of capital
    entry_price=50000,
    stop_loss=48000
)

# Risk-reward ratio
rr_ratio = TradeUtils.calculate_risk_reward_ratio(
    entry_price=50000,
    target_price=55000,
    stop_loss=48000
)

# P&L calculation
pnl = TradeUtils.calculate_pnl(
    entry_price=50000,
    exit_price=52000,
    quantity=0.1,
    side="long"
)

# Performance metrics
trades = [
    {'pnl': 100}, {'pnl': -50}, {'pnl': 200}, {'pnl': -30}
]
win_rate = TradeUtils.calculate_win_rate(trades)
avg_win, avg_loss = TradeUtils.calculate_average_win_loss(trades)
profit_factor = TradeUtils.calculate_profit_factor(trades)
```

## 🎮 **Running Examples**

### Demo Script
```bash
python demo.py
```

### Simple Strategy Example
```bash
python examples/simple_strategy.py
```

### BitFlow Integration (if you have BitFlow data)
```bash
python examples/bitflow_integration.py
```

## 🔍 **Available Indicators**

| Indicator | Function | Description |
|-----------|----------|-------------|
| Simple Moving Average | `Indicators.sma(data, period)` | Basic moving average |
| Exponential Moving Average | `Indicators.ema(data, period)` | Weighted moving average |
| RSI | `Indicators.rsi(data, period=14)` | Relative Strength Index |
| MACD | `Indicators.macd(data)` | Moving Average Convergence Divergence |
| Bollinger Bands | `Indicators.bollinger_bands(data)` | Volatility bands |
| Stochastic | `Indicators.stochastic(high, low, close)` | Stochastic oscillator |
| ATR | `Indicators.atr(high, low, close)` | Average True Range |
| Williams %R | `Indicators.williams_r(high, low, close)` | Williams %R oscillator |
| CCI | `Indicators.cci(high, low, close)` | Commodity Channel Index |

## 📊 **Performance Metrics**

The library calculates various performance metrics:

- **Total Return**: Overall profit/loss percentage
- **Annualized Return**: Return adjusted for time period
- **Sharpe Ratio**: Risk-adjusted return measure
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Gross profit / Gross loss
- **Average Win/Loss**: Average profit and loss per trade

## 🛡️ **Risk Management**

Built-in risk management tools:

- **Position Sizing**: Calculate position size based on risk percentage
- **Risk-Reward Ratio**: Evaluate trade setup quality
- **Stop Loss Calculation**: Determine appropriate stop loss levels
- **Portfolio Risk**: Manage overall portfolio exposure

## 🔧 **Customization**

You can easily extend the library:

1. **Add New Indicators**: Create custom technical indicators
2. **Custom Strategies**: Implement your own trading logic
3. **Risk Models**: Add sophisticated risk management
4. **Data Sources**: Connect to different data providers

## 📝 **Data Format**

The library expects data in this format:

```python
data = pd.DataFrame({
    'timestamp': pd.to_datetime(['2023-01-01', '2023-01-02', ...]),
    'open': [100, 101, 102, ...],
    'high': [105, 106, 107, ...],
    'low': [95, 96, 97, ...],
    'close': [103, 104, 105, ...],
    'volume': [1000, 1100, 1200, ...]
})
```

## 🚀 **Next Steps**

1. **Start with the demo**: `python demo.py`
2. **Try the examples**: Check the `examples/` directory
3. **Read the documentation**: See `README.md` for detailed API docs
4. **Create your own strategy**: Use the backtesting framework
5. **Connect to live data**: Integrate with your preferred data source

## 💡 **Tips**

- Always start with paper trading
- Test strategies thoroughly before live trading
- Use proper risk management
- Monitor performance metrics regularly
- Keep learning and improving your strategies

## 🆘 **Need Help?**

- Check the examples in the `examples/` directory
- Read the comprehensive `README.md`
- Look at the test files for usage patterns
- The library is well-documented with docstrings

Remember: This library is for educational and research purposes. Always do your own research and use proper risk management when trading. 