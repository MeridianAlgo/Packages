#!/usr/bin/env python3
"""
Installation script for MeridianAlgo
"""

import subprocess
import sys
import os


def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Required packages installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False
    return True


def install_package():
    """Install the package in development mode"""
    print("Installing MeridianAlgo in development mode...")
    try:
        subprocess.check_call([sys.executable, "setup.py", "develop"])
        print("✓ MeridianAlgo installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing package: {e}")
        return False
    return True


def run_tests():
    """Run basic tests to verify installation"""
    print("Running basic tests...")
    try:
        # Try to import the package
        import meridianalgo
        print("✓ Package imports successfully")
        
        # Test basic functionality
        from meridianalgo import TradingEngine, BacktestEngine, Indicators, TradeUtils
        print("✓ All modules import successfully")
        
        # Test indicators
        import pandas as pd
        import numpy as np
        
        data = pd.Series([1, 2, 3, 4, 5])
        sma = Indicators.sma(data, 3)
        print("✓ Basic indicator calculation works")
        
        print("✓ All tests passed!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Test error: {e}")
        return False


def main():
    """Main installation function"""
    print("=== MeridianAlgo Installation ===\n")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Install package
    if not install_package():
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        sys.exit(1)
    
    print("\n=== Installation Complete! ===")
    print("You can now use MeridianAlgo in your Python projects.")
    print("\nExample usage:")
    print("from meridianalgo import TradingEngine, BacktestEngine, Indicators")
    print("engine = TradingEngine(paper_trading=True)")
    print("engine.connect()")
    
    print("\nFor more examples, see the 'examples/' directory.")
    print("For documentation, see README.md")


if __name__ == "__main__":
    main() 