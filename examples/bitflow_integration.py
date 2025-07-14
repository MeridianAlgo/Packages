"""
Example: Using MeridianAlgo with BitFlow Trading Data
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add the parent directory to the path to import meridianalgo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meridianalgo import BacktestEngine, Indicators, TradeUtils


def load_bitflow_data(file_path):
    """
    Load and process BitFlow trading data
    
    Args:
        file_path: Path to positions_sold.csv file
    
    Returns:
        pd.DataFrame: Processed trading data
    """
    try:
        # Load the CSV file with error handling
        df = pd.read_csv(file_path, on_bad_lines='skip')
        
        # Clean up any malformed data
        df = df.dropna(subset=['symbol', 'entryPrice', 'exitPrice'])
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Convert numeric columns
        df['entryPrice'] = pd.to_numeric(df['entryPrice'], errors='coerce')
        df['exitPrice'] = pd.to_numeric(df['exitPrice'], errors='coerce')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['pnl'] = pd.to_numeric(df['pnl'], errors='coerce')
        df['pnlPercent'] = pd.to_numeric(df['pnlPercent'], errors='coerce')
        
        # Remove any rows with invalid data
        df = df.dropna(subset=['entryPrice', 'exitPrice', 'quantity', 'pnl'])
        
        print(f"Successfully loaded {len(df)} valid trades")
        
        # Create OHLC data from the trading data
        # Since we have entry and exit prices, we'll create synthetic OHLC
        data = []
        
        for _, row in df.iterrows():
            entry_price = float(row['entryPrice'])
            exit_price = float(row['exitPrice'])
            
            # Create synthetic OHLC data for each trade
            # This is a simplified approach - in reality you'd need actual market data
            high = max(entry_price, exit_price)
            low = min(entry_price, exit_price)
            open_price = entry_price
            close_price = exit_price
            
            data.append({
                'timestamp': row['timestamp'],
                'open': open_price,
                'high': high,
                'low': low,
                'close': close_price,
                'volume': float(row['quantity']),
                'symbol': row['symbol'],
                'pnl': float(row['pnl']),
                'pnl_percent': float(row['pnlPercent']),
                'close_reason': row['closeReason']
            })
        
        return pd.DataFrame(data)
        
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Creating sample data instead...")
        
                # Create sample data if loading fails
        return create_sample_data()


def create_sample_data():
    """Create sample data for demonstration"""
    import numpy as np
    from datetime import datetime, timedelta
    
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    data = []
    for i, date in enumerate(dates):
        data.append({
            'timestamp': date,
            'open': 100 + i * 0.1,
            'high': 100 + i * 0.1 + 2,
            'low': 100 + i * 0.1 - 2,
            'close': 100 + i * 0.1 + np.random.normal(0, 1),
            'volume': np.random.randint(1000, 10000),
            'symbol': 'BTC/USD',
            'pnl': np.random.normal(0, 10),
            'pnl_percent': np.random.normal(0, 1),
            'close_reason': 'Sample'
        })
    
    return pd.DataFrame(data)
    

def analyze_bitflow_performance(df):
    """
    Analyze BitFlow trading performance using MeridianAlgo utilities
    
    Args:
        df: DataFrame with BitFlow trading data
    """
    print("=== BitFlow Performance Analysis ===\n")
    
    # Convert to list of trade dictionaries for analysis
    trades = df.to_dict('records')
    
    # Calculate performance metrics
    total_trades = len(trades)
    win_rate = TradeUtils.calculate_win_rate(trades)
    avg_win, avg_loss = TradeUtils.calculate_average_win_loss(trades)
    profit_factor = TradeUtils.calculate_profit_factor(trades)
    
    # Calculate total P&L
    total_pnl = sum(trade['pnl'] for trade in trades)
    total_pnl_percent = sum(trade['pnl_percent'] for trade in trades)
    
    print(f"Total Trades: {total_trades}")
    print(f"Total P&L: {TradeUtils.format_currency(total_pnl)}")
    print(f"Total P&L %: {TradeUtils.format_percentage(total_pnl_percent)}")
    print(f"Win Rate: {TradeUtils.format_percentage(win_rate)}")
    print(f"Average Win: {TradeUtils.format_currency(avg_win)}")
    print(f"Average Loss: {TradeUtils.format_currency(avg_loss)}")
    print(f"Profit Factor: {profit_factor:.2f}")
    
    # Analyze by symbol
    print(f"\n=== Performance by Symbol ===")
    symbol_stats = df.groupby('symbol').agg({
        'pnl': ['sum', 'mean', 'count'],
        'pnl_percent': 'sum'
    }).round(4)
    
    print(symbol_stats)
    
    # Analyze by close reason
    print(f"\n=== Performance by Close Reason ===")
    reason_stats = df.groupby('closeReason').agg({
        'pnl': ['sum', 'mean', 'count'],
        'pnl_percent': 'sum'
    }).round(4)
    
    print(reason_stats)


def create_strategy_from_bitflow_patterns(df):
    """
    Create a trading strategy based on BitFlow patterns
    
    Args:
        df: DataFrame with BitFlow trading data
    """
    print("\n=== Creating Strategy from BitFlow Patterns ===\n")
    
    # Analyze successful trades
    successful_trades = df[df['pnl'] > 0]
    losing_trades = df[df['pnl'] < 0]
    
    print(f"Successful trades: {len(successful_trades)}")
    print(f"Losing trades: {len(losing_trades)}")
    
    # Find most profitable symbols
    symbol_performance = df.groupby('symbol')['pnl'].sum().sort_values(ascending=False)
    print(f"\nMost profitable symbols:")
    for symbol, pnl in symbol_performance.head(3).items():
        print(f"  {symbol}: {TradeUtils.format_currency(pnl)}")
    
    # Find most successful close reasons
    reason_performance = df.groupby('closeReason')['pnl'].sum().sort_values(ascending=False)
    print(f"\nMost successful close reasons:")
    for reason, pnl in reason_performance.head(3).items():
        print(f"  {reason}: {TradeUtils.format_currency(pnl)}")


def backtest_bitflow_strategy(df):
    """
    Backtest a strategy based on BitFlow patterns
    
    Args:
        df: DataFrame with BitFlow trading data
    """
    print("\n=== Backtesting BitFlow-Inspired Strategy ===\n")
    
    # Create synthetic market data for backtesting
    # In reality, you'd use actual market data
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    # Generate realistic price data
    np.random.seed(42)
    base_price = 100
    trend = np.linspace(0, 20, len(dates))
    volatility = np.random.normal(0, 2, len(dates))
    prices = base_price + trend + volatility
    
    market_data = pd.DataFrame({
        'timestamp': dates,
        'open': prices + np.random.normal(0, 0.5, len(dates)),
        'high': prices + np.abs(np.random.normal(0, 1.5, len(dates))),
        'low': prices - np.abs(np.random.normal(0, 1.5, len(dates))),
        'close': prices,
        'volume': np.random.randint(1000, 15000, len(dates))
    })
    
    # Initialize backtest engine
    backtest = BacktestEngine(initial_capital=10000)
    backtest.load_data(market_data)
    
    # Define strategy based on BitFlow patterns
    def bitflow_inspired_strategy(row, positions, capital, data=None):
        """Strategy inspired by BitFlow trading patterns"""
        current_idx = row.name
        
        if current_idx < 20 or data is None:
            return None
        
        # Get historical data
        close_prices = data['close'].iloc[:current_idx + 1]
        
        # Calculate indicators
        sma_10 = close_prices.rolling(10).mean().iloc[-1]
        sma_20 = close_prices.rolling(20).mean().iloc[-1]
        rsi = Indicators.rsi(close_prices, 14).iloc[-1]
        current_price = row['close']
        
        symbol = 'BTC/USD'
        
        # Strategy based on BitFlow patterns:
        # - Use moving average crossovers (like many BitFlow strategies)
        # - Add RSI filter for overbought/oversold conditions
        # - Use position sizing based on risk management
        
        # Buy signal: MA crossover + RSI not overbought
        if (sma_10 > sma_20 and rsi < 70 and symbol not in positions):
            # Use 5% of capital per trade (conservative)
            quantity = (capital * 0.05) / current_price
            return {
                'symbol': symbol,
                'action': 'buy',
                'quantity': quantity
            }
        
        # Sell signal: MA crossover down + RSI not oversold
        elif (sma_10 < sma_20 and rsi > 30 and symbol in positions):
            return {
                'symbol': symbol,
                'action': 'sell',
                'quantity': positions[symbol]['quantity']
            }
        
        return None
    
    # Run backtest
    results = backtest.run_backtest(bitflow_inspired_strategy, data=market_data)
    
    # Display results
    print(f"Backtest Results:")
    print(f"Initial Capital: $10,000")
    print(f"Final Equity: {TradeUtils.format_currency(results['final_equity'])}")
    print(f"Total Return: {TradeUtils.format_percentage(results['total_return'] * 100)}")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Maximum Drawdown: {TradeUtils.format_percentage(results['max_drawdown'] * 100)}")
    print(f"Total Trades: {results['total_trades']}")


def main():
    """Main function to demonstrate BitFlow integration"""
    print("MeridianAlgo + BitFlow Integration Example")
    print("=" * 50)
    
    # Path to your BitFlow data
    bitflow_file = "../positions_sold.csv"  # Adjust path as needed
    
    try:
        # Load BitFlow data
        print("Loading BitFlow trading data...")
        df = load_bitflow_data(bitflow_file)
        print(f"Loaded {len(df)} trades from BitFlow data\n")
        
        # Analyze performance
        analyze_bitflow_performance(df)
        
        # Create strategy from patterns
        create_strategy_from_bitflow_patterns(df)
        
        # Backtest strategy
        backtest_bitflow_strategy(df)
        
        print("\n=== Integration Summary ===")
        print("MeridianAlgo can be used to:")
        print("• Analyze your BitFlow trading performance")
        print("• Create strategies based on your successful patterns")
        print("• Backtest new strategies before implementing them")
        print("• Calculate advanced performance metrics")
        print("• Manage risk and position sizing")
        
    except FileNotFoundError:
        print(f"BitFlow data file not found: {bitflow_file}")
        print("Please adjust the file path in the script.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 