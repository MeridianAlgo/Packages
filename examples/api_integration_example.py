"""
Example: How to Integrate MeridianAlgo with Real Trading APIs
"""

import os
from meridianalgo import TradingEngine, BacktestEngine, Indicators, TradeUtils


class RealTradingEngine(TradingEngine):
    """
    Extended trading engine that can connect to real trading platforms
    """
    
    def __init__(self, api_key=None, secret_key=None, exchange="alpaca", paper_trading=True):
        """
        Initialize with API credentials
        
        Args:
            api_key: Your API key
            secret_key: Your secret key
            exchange: Trading platform (alpaca, binance, etc.)
            paper_trading: Whether to use paper trading
        """
        super().__init__(api_key, secret_key, paper_trading)
        self.exchange = exchange
        self.connected = False
        
    def connect(self):
        """
        Connect to the trading platform using your API keys
        """
        if not self.api_key or not self.secret_key:
            print("⚠️  No API keys provided - using paper trading mode")
            self.paper_trading = True
            return True
        
        try:
            # Example: Connect to Alpaca
            if self.exchange.lower() == "alpaca":
                # You would add actual Alpaca SDK here
                print(f"🔗 Connecting to Alpaca (Paper Trading: {self.paper_trading})")
                print(f"📊 API Key: {self.api_key[:8]}...")
                self.connected = True
                
            # Example: Connect to Binance
            elif self.exchange.lower() == "binance":
                # You would add actual Binance SDK here
                print(f"🔗 Connecting to Binance (Paper Trading: {self.paper_trading})")
                print(f"📊 API Key: {self.api_key[:8]}...")
                self.connected = True
                
            else:
                print(f"⚠️  Exchange {self.exchange} not implemented - using paper trading")
                self.paper_trading = True
                self.connected = True
                
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("🔄 Falling back to paper trading mode")
            self.paper_trading = True
            self.connected = True
            
        return self.connected
    
    def place_order(self, symbol, side, quantity, order_type="market", price=None):
        """
        Place order with real API connection
        """
        if not self.connected:
            print("❌ Not connected to trading platform")
            return None
            
        if self.paper_trading:
            # Paper trading - simulate order
            return super().place_order(symbol, side, quantity, order_type, price)
        else:
            # Real trading - use actual API
            print(f"🚀 Placing REAL order: {side} {quantity} {symbol}")
            # Here you would add actual API calls
            # For example with Alpaca:
            # order = alpaca_api.submit_order(symbol, quantity, side, order_type, price)
            
            # For now, simulate success
            return {
                "id": f"real_order_{len(self.trade_history) + 1}",
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "type": order_type,
                "price": price,
                "status": "filled",
                "real_trade": True
            }


def setup_api_keys():
    """
    Set up API keys from environment variables or config file
    """
    # Method 1: Environment variables (recommended)
    alpaca_api_key = os.getenv('ALPACA_API_KEY')
    alpaca_secret_key = os.getenv('ALPACA_SECRET_KEY')
    
    binance_api_key = os.getenv('BINANCE_API_KEY')
    binance_secret_key = os.getenv('BINANCE_SECRET_KEY')
    
    # Method 2: Config file (create api_config.py)
    try:
        from api_config import API_KEYS
        alpaca_api_key = alpaca_api_key or API_KEYS.get('alpaca', {}).get('api_key')
        alpaca_secret_key = alpaca_secret_key or API_KEYS.get('alpaca', {}).get('secret_key')
        binance_api_key = binance_api_key or API_KEYS.get('binance', {}).get('api_key')
        binance_secret_key = binance_secret_key or API_KEYS.get('binance', {}).get('secret_key')
    except ImportError:
        print("ℹ️  No api_config.py found - using environment variables only")
    
    return {
        'alpaca': {'api_key': alpaca_api_key, 'secret_key': alpaca_secret_key},
        'binance': {'api_key': binance_api_key, 'secret_key': binance_secret_key}
    }


def demo_with_api_keys():
    """
    Demonstrate how to use the library with real API keys
    """
    print("=== MeridianAlgo with Real API Keys ===\n")
    
    # Get API keys
    api_keys = setup_api_keys()
    
    # Check what keys are available
    print("🔑 Available API Keys:")
    for exchange, keys in api_keys.items():
        if keys['api_key']:
            print(f"  ✅ {exchange.upper()}: {keys['api_key'][:8]}...")
        else:
            print(f"  ❌ {exchange.upper()}: Not configured")
    
    print("\n" + "="*50 + "\n")
    
    # Example 1: Paper Trading (No API keys needed)
    print("📊 Example 1: Paper Trading (No API Keys)")
    paper_engine = RealTradingEngine(paper_trading=True)
    paper_engine.connect()
    
    # Place paper trade
    order = paper_engine.place_order("BTC/USD", "buy", 0.1)
    print(f"Paper Order: {order}")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Real Trading with Alpaca
    if api_keys['alpaca']['api_key']:
        print("🚀 Example 2: Real Trading with Alpaca")
        real_engine = RealTradingEngine(
            api_key=api_keys['alpaca']['api_key'],
            secret_key=api_keys['alpaca']['secret_key'],
            exchange="alpaca",
            paper_trading=False  # WARNING: This would place real trades!
        )
        real_engine.connect()
        
        # WARNING: This would place a real trade!
        # Uncomment only if you want to place real trades
        # order = real_engine.place_order("BTC/USD", "buy", 0.01)
        # print(f"Real Order: {order}")
        
        print("⚠️  Real trading disabled for safety")
    else:
        print("❌ Example 2: No Alpaca API keys configured")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Backtesting (No API keys needed)
    print("📈 Example 3: Backtesting (No API Keys)")
    print("Backtesting works with historical data - no API keys required!")
    
    # You can use your BitFlow data for backtesting
    print("You can load your positions_sold.csv and backtest strategies")
    
    print("\n" + "="*50 + "\n")


def create_api_config_template():
    """
    Create a template for API configuration
    """
    config_content = '''# api_config.py - API Keys Configuration
# WARNING: Never commit this file to version control!
# Add api_config.py to your .gitignore file

API_KEYS = {
    'alpaca': {
        'api_key': 'your_alpaca_api_key_here',
        'secret_key': 'your_alpaca_secret_key_here'
    },
    'binance': {
        'api_key': 'your_binance_api_key_here',
        'secret_key': 'your_binance_secret_key_here'
    },
    'bitflow': {
        'api_key': 'your_bitflow_api_key_here',
        'secret_key': 'your_bitflow_secret_key_here'
    }
}

# Usage:
# from api_config import API_KEYS
# api_key = API_KEYS['alpaca']['api_key']
'''
    
    with open('api_config_template.py', 'w') as f:
        f.write(config_content)
    
    print("📝 Created api_config_template.py")
    print("📋 Copy this file to api_config.py and add your actual API keys")


def main():
    """
    Main function to demonstrate API integration
    """
    print("MeridianAlgo API Integration Guide")
    print("=" * 50)
    
    # Create API config template
    create_api_config_template()
    
    print("\n" + "="*50 + "\n")
    
    # Demo with API keys
    demo_with_api_keys()
    
    print("\n=== Summary ===")
    print("✅ MeridianAlgo works WITHOUT API keys for:")
    print("   • Backtesting strategies")
    print("   • Calculating technical indicators")
    print("   • Paper trading simulation")
    print("   • Performance analysis")
    print("   • Risk management calculations")
    
    print("\n🔑 API keys are ONLY needed for:")
    print("   • Live trading execution")
    print("   • Real-time market data")
    print("   • Account balance/position queries")
    
    print("\n💡 Recommendation:")
    print("   • Start with paper trading (no API keys needed)")
    print("   • Test strategies thoroughly with backtesting")
    print("   • Only add API keys when ready for live trading")
    print("   • Always use paper trading first!")


if __name__ == "__main__":
    main() 