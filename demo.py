#!/usr/bin/env python3
"""
Demo script for MeridianAlgo library
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from meridianalgo import TradingEngine, BacktestEngine, Indicators, TradeUtils


def create_demo_data():
    """Create demo price data"""
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-06-30', freq='D')
    
    # Generate realistic price data with trend and volatility
    base_price = 100
    trend = np.linspace(0, 15, len(dates))  # Upward trend
    volatility = np.random.normal(0, 2, len(dates))
    prices = base_price + trend + volatility
    
    data = pd.DataFrame({
        'timestamp': dates,
        'open': prices + np.random.normal(0, 0.5, len(dates)),
        'high': prices + np.abs(np.random.normal(0, 1.5, len(dates))),
        'low': prices - np.abs(np.random.normal(0, 1.5, len(dates))),
        'close': prices,
        'volume': np.random.randint(1000, 15000, len(dates))
    })
    
    return data


def demo_trading_engine():
    """Demonstrate trading engine functionality"""
    print("=== Trading Engine Demo ===\n")
    
    # Initialize trading engine
    engine = TradingEngine(paper_trading=True)
    engine.connect()
    
    # Get account info
    account_info = engine.get_account_info()
    print(f"Account Balance: ${account_info['balance']:,.2f}")
    print(f"Paper Trading: {account_info['paper_trading']}")
    
    # Place some demo trades
    print("\nPlacing demo trades...")
    
    # Buy trade
    buy_order = engine.place_order(
        symbol="BTC/USD",
        side="buy",
        quantity=0.1,
        order_type="market",
        price=50000
    )
    print(f"Buy Order: {buy_order}")
    
    # Check positions
    positions = engine.get_positions()
    print(f"Current Positions: {positions}")
    
    # Sell trade
    sell_order = engine.place_order(
        symbol="BTC/USD",
        side="sell",
        quantity=0.05,
        order_type="market",
        price=52000
    )
    print(f"Sell Order: {sell_order}")
    
    # Check updated positions
    positions = engine.get_positions()
    print(f"Updated Positions: {positions}")
    
    # Calculate P&L
    pnl = engine.calculate_pnl("BTC/USD", 52000)
    print(f"Current P&L: ${pnl:.2f}")
    
    # Get trade history
    trades = engine.get_trade_history()
    print(f"Total Trades: {len(trades)}")
    
    print("\n" + "="*50 + "\n")


def demo_indicators():
    """Demonstrate technical indicators"""
    print("=== Technical Indicators Demo ===\n")
    
    # Create sample data
    data = create_demo_data()
    print(f"Generated {len(data)} days of price data")
    
    # Calculate various indicators
    print("\nCalculating technical indicators...")
    
    # Moving averages
    sma_20 = Indicators.sma(data['close'], 20)
    ema_20 = Indicators.ema(data['close'], 20)
    print(f"20-day SMA (latest): {sma_20.iloc[-1]:.2f}")
    print(f"20-day EMA (latest): {ema_20.iloc[-1]:.2f}")
    
    # RSI
    rsi = Indicators.rsi(data['close'], 14)
    print(f"14-day RSI (latest): {rsi.iloc[-1]:.2f}")
    
    # MACD
    macd_line, signal_line, histogram = Indicators.macd(data['close'])
    print(f"MACD Line (latest): {macd_line.iloc[-1]:.4f}")
    print(f"Signal Line (latest): {signal_line.iloc[-1]:.4f}")
    print(f"Histogram (latest): {histogram.iloc[-1]:.4f}")
    
    # Bollinger Bands
    upper, middle, lower = Indicators.bollinger_bands(data['close'])
    current_price = data['close'].iloc[-1]
    print(f"Current Price: ${current_price:.2f}")
    print(f"Upper Band: ${upper.iloc[-1]:.2f}")
    print(f"Middle Band: ${middle.iloc[-1]:.2f}")
    print(f"Lower Band: ${lower.iloc[-1]:.2f}")
    
    # Stochastic
    k_percent, d_percent = Indicators.stochastic(data['high'], data['low'], data['close'])
    print(f"Stochastic %K (latest): {k_percent.iloc[-1]:.2f}")
    print(f"Stochastic %D (latest): {d_percent.iloc[-1]:.2f}")
    
    print("\n" + "="*50 + "\n")


def demo_backtest():
    """Demonstrate backtesting functionality"""
    print("=== Backtesting Demo ===\n")
    
    # Create sample data
    data = create_demo_data()
    
    # Initialize backtest engine
    initial_capital = 10000
    backtest = BacktestEngine(initial_capital=initial_capital)
    backtest.load_data(data)
    
    # Define a simple strategy
    def demo_strategy(row, positions, capital, data=None):
        """Simple demo strategy"""
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
        
        # Simple crossover strategy
        if sma_10 > sma_20 and symbol not in positions:
            quantity = (capital * 0.1) / current_price
            return {
                'symbol': symbol,
                'action': 'buy',
                'quantity': quantity
            }
        elif sma_10 < sma_20 and symbol in positions:
            return {
                'symbol': symbol,
                'action': 'sell',
                'quantity': positions[symbol]['quantity']
            }
        
        return None
    
    # Run backtest
    print("Running backtest...")
    results = backtest.run_backtest(demo_strategy, data=data)
    
    # Display results
    print(f"\nBacktest Results:")
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
        print(f"\nTrade Summary:")
        print(f"Number of trades: {len(trades_df)}")
        
        # Calculate performance metrics
        if 'revenue' in trades_df.columns and 'cost' in trades_df.columns:
            trades_df['pnl'] = trades_df['revenue'].fillna(0) - trades_df['cost'].fillna(0)
            
            win_rate = TradeUtils.calculate_win_rate(trades_df.to_dict('records'))
            avg_win, avg_loss = TradeUtils.calculate_average_win_loss(trades_df.to_dict('records'))
            profit_factor = TradeUtils.calculate_profit_factor(trades_df.to_dict('records'))
            
            print(f"Win Rate: {win_rate:.1f}%")
            print(f"Average Win: ${avg_win:.2f}")
            print(f"Average Loss: ${avg_loss:.2f}")
            print(f"Profit Factor: {profit_factor:.2f}")
    
    print("\n" + "="*50 + "\n")


def demo_utils():
    """Demonstrate utility functions"""
    print("=== Utility Functions Demo ===\n")
    
    # Position sizing
    position_size = TradeUtils.calculate_position_size(
        capital=10000,
        risk_percent=2,
        entry_price=50000,
        stop_loss=48000
    )
    print(f"Position Size (2% risk): {position_size:.4f} units")
    
    # Risk-reward ratio
    rr_ratio = TradeUtils.calculate_risk_reward_ratio(
        entry_price=50000,
        target_price=55000,
        stop_loss=48000
    )
    print(f"Risk-Reward Ratio: {rr_ratio:.2f}")
    
    # P&L calculations
    pnl = TradeUtils.calculate_pnl(
        entry_price=50000,
        exit_price=52000,
        quantity=0.1,
        side="long"
    )
    pnl_percent = TradeUtils.calculate_pnl_percent(
        entry_price=50000,
        exit_price=52000,
        side="long"
    )
    print(f"P&L: ${pnl:.2f} ({pnl_percent:.2f}%)")
    
    # Performance metrics
    returns = [2.5, -1.2, 3.1, -0.8, 1.9, 2.3, -1.5, 0.7]
    compound_return = TradeUtils.calculate_compound_return(returns)
    sharpe_ratio = TradeUtils.calculate_sharpe_ratio(returns)
    
    print(f"Compound Return: {compound_return:.2f}%")
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    
    # Formatting
    formatted_currency = TradeUtils.format_currency(1234.56, "USD")
    formatted_percent = TradeUtils.format_percentage(15.678, 1)
    print(f"Formatted Currency: {formatted_currency}")
    print(f"Formatted Percentage: {formatted_percent}")
    
    # Validation
    is_valid = TradeUtils.validate_trade_params("BTC/USD", 0.1, 50000)
    print(f"Trade Parameters Valid: {is_valid}")
    
    print("\n" + "="*50 + "\n")


def main():
    """Main demo function"""
    print("MeridianAlgo Library Demo")
    print("=" * 50)
    print("This demo showcases the main features of the MeridianAlgo library.\n")
    
    try:
        # Run all demos
        demo_trading_engine()
        demo_indicators()
        demo_backtest()
        demo_utils()
        
        print("=== Demo Complete! ===")
        print("The MeridianAlgo library provides:")
        print("• Trading engine for live trading operations")
        print("• Backtesting engine for strategy testing")
        print("• Technical indicators for analysis")
        print("• Utility functions for risk management")
        print("\nFor more examples, see the 'examples/' directory.")
        print("For detailed documentation, see README.md")
        
    except Exception as e:
        print(f"Error during demo: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")


if __name__ == "__main__":
    main() 