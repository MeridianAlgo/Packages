"""
Simple Moving Average Crossover Strategy Example
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path to import meridianalgo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meridianalgo import BacktestEngine, Indicators, TradeUtils


def create_sample_data():
    """Create sample price data for demonstration"""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    # Generate sample price data with some trend and noise
    base_price = 100
    trend = np.linspace(0, 20, len(dates))  # Upward trend
    noise = np.random.normal(0, 2, len(dates))
    prices = base_price + trend + noise
    
    data = pd.DataFrame({
        'timestamp': dates,
        'open': prices + np.random.normal(0, 0.5, len(dates)),
        'high': prices + np.abs(np.random.normal(0, 1, len(dates))),
        'low': prices - np.abs(np.random.normal(0, 1, len(dates))),
        'close': prices,
        'volume': np.random.randint(1000, 10000, len(dates))
    })
    
    return data


def ma_crossover_strategy(row, positions, capital, fast_period=10, slow_period=20, data=None):
    """
    Simple moving average crossover strategy
    
    Args:
        row: Current market data row
        positions: Current positions
        capital: Available capital
        fast_period: Fast moving average period
        slow_period: Slow moving average period
        data: Historical data for calculations
    
    Returns:
        dict: Trading signal or None
    """
    # Get the current index to access historical data
    current_idx = row.name
    
    # Need enough data to calculate moving averages
    if current_idx < slow_period or data is None:
        return None
    
    # Get historical close prices
    close_prices = data['close'].iloc[:current_idx + 1]
    
    # Calculate moving averages
    fast_ma = close_prices.rolling(fast_period).mean().iloc[-1]
    slow_ma = close_prices.rolling(slow_period).mean().iloc[-1]
    
    current_price = row['close']
    symbol = 'BTC/USD'  # Using a sample symbol
    
    # Buy signal: fast MA crosses above slow MA
    if fast_ma > slow_ma and symbol not in positions:
        # Use 10% of available capital
        quantity = (capital * 0.1) / current_price
        return {
            'symbol': symbol,
            'action': 'buy',
            'quantity': quantity
        }
    
    # Sell signal: fast MA crosses below slow MA
    elif fast_ma < slow_ma and symbol in positions:
        return {
            'symbol': symbol,
            'action': 'sell',
            'quantity': positions[symbol]['quantity']
        }
    
    return None


def main():
    """Main function to run the strategy example"""
    print("=== Simple Moving Average Crossover Strategy Example ===\n")
    
    # Create sample data
    print("Creating sample price data...")
    data = create_sample_data()
    print(f"Generated {len(data)} days of price data")
    print(f"Price range: ${data['close'].min():.2f} - ${data['close'].max():.2f}\n")
    
    # Initialize backtest engine
    initial_capital = 10000
    backtest = BacktestEngine(initial_capital=initial_capital)
    
    # Load data
    backtest.load_data(data)
    
    # Run backtest
    print("Running backtest...")
    results = backtest.run_backtest(ma_crossover_strategy, fast_period=10, slow_period=20, data=data)
    
    # Display results
    print("\n=== Backtest Results ===")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Final Equity: ${results['final_equity']:,.2f}")
    print(f"Total Return: {results['total_return']:.2%}")
    print(f"Annualized Return: {results['annualized_return']:.2%}")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Maximum Drawdown: {results['max_drawdown']:.2%}")
    print(f"Total Trades: {results['total_trades']}")
    
    # Get trade details
    trades_df = backtest.get_trades()
    if not trades_df.empty:
        print(f"\n=== Trade Summary ===")
        print(f"Number of trades: {len(trades_df)}")
        
        # Calculate win rate
        if 'revenue' in trades_df.columns and 'cost' in trades_df.columns:
            trades_df['pnl'] = trades_df['revenue'].fillna(0) - trades_df['cost'].fillna(0)
            win_rate = TradeUtils.calculate_win_rate(trades_df.to_dict('records'))
            print(f"Win Rate: {win_rate:.1f}%")
            
            # Calculate average win and loss
            avg_win, avg_loss = TradeUtils.calculate_average_win_loss(trades_df.to_dict('records'))
            print(f"Average Win: ${avg_win:.2f}")
            print(f"Average Loss: ${avg_loss:.2f}")
            
            # Calculate profit factor
            profit_factor = TradeUtils.calculate_profit_factor(trades_df.to_dict('records'))
            print(f"Profit Factor: {profit_factor:.2f}")
    
    # Show equity curve
    equity_df = backtest.get_equity_curve()
    print(f"\n=== Equity Curve ===")
    print(f"Starting equity: ${equity_df['equity'].iloc[0]:,.2f}")
    print(f"Peak equity: ${equity_df['equity'].max():,.2f}")
    print(f"Ending equity: ${equity_df['equity'].iloc[-1]:,.2f}")
    
    print("\n=== Strategy Analysis ===")
    print("This simple moving average crossover strategy:")
    print("- Buys when the fast moving average crosses above the slow moving average")
    print("- Sells when the fast moving average crosses below the slow moving average")
    print("- Uses 10% of available capital for each trade")
    print("- Demonstrates basic trend-following behavior")
    
    print("\nNote: This is a simplified example for educational purposes.")
    print("Real trading strategies should include proper risk management,")
    print("position sizing, and more sophisticated entry/exit rules.")


if __name__ == "__main__":
    main() 