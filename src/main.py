# main.py
# Overview: This script initializes and runs a trading agent simulation for designated market making.
# The trading agent is configured to operate on the "IBM" stock symbol for a series of 300 iterations.

from src.trade_agent import Agent
import argparse

def main():
    # Configuration parameters (could be moved to a separate config file)
    stock_symbol = "IBM"
    number_of_mm = 1
    real_mkt = False
    total_rounds = 299
    parser = argparse.ArgumentParser(description='Run the trading simulation.')
    parser.add_argument('--num_rounds', type=int, required=True)
    parser.add_argument('--num_market_makers', type=int, required=True)
    parser.add_argument('--use_real_market', action='store_true')
    args = parser.parse_args()
    number_of_mm = args.num_market_makers
    total_rounds = args.num_rounds
    real_mkt = args.use_real_market


    # Initialize the trading agent
    trading_agent = Agent(tickers=stock_symbol, num_mm= number_of_mm,real_mkt=real_mkt, num_rounds=total_rounds)

    # Main trading simulation loop
    for round in range(total_rounds):
        trading_agent.send_book()
        trading_agent.update_markettradebook()
        trading_agent.mmtrade_submit()
        trading_agent.exchange_execution()
        trading_agent.update_price()
        trading_agent.record_allplayers()
        trading_agent.run_next_round()
    print("program finished")

if __name__ == "__main__":
    main()
