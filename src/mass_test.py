from src.trade_agent import Agent
import pandas as pd
def main():
    stock_symbol = "IBM"
    number_of_mm = 1
    real_mkt = False
    total_rounds = 1000
    num_of_test = 50
    mm_return = []
    p1_return = []
    p3_return = []
    EP_ratio = []


    for i in range(num_of_test):
        trading_agent = Agent(tickers=stock_symbol, num_mm= number_of_mm,real_mkt=real_mkt, num_rounds=total_rounds)
        for round in range(total_rounds):
            trading_agent.update_markettradebook()
            trading_agent.update_price()
            trading_agent.send_book()
            trading_agent.mmtrade_submit()
            trading_agent.exchange_execution()
            trading_agent.record_allplayers()
            trading_agent.run_next_round()
        x = pd.read_csv(r"C:\Users\24395\Designated_Market_Making\output\playersIC.csv")
        x['mm_portfolio'] = x['mm1_inventory'] * x['price_history'] + x['mm1_cash']
        x['p1_portfolio'] = x['p1_inventory'] * x['price_history'] + x['p1_cash']
        x['p3_portfolio'] = x['p3_inventory'] * x['price_history'] + x['p3_cash']
        mm_return.append(x['mm_portfolio'].iloc[-1])
        p1_return.append(x['p1_portfolio'].iloc[-1])
        p3_return.append(x['p3_portfolio'].iloc[-1])
        y = pd.read_csv(r"C:\Users\24395\Designated_Market_Making\output\all_orders.csv")
        EP_ratio.append(y['status'].value_counts()["EXECUTED"]/y['status'].value_counts()["PENDING"])
        print(i)
    players_return = {"mm": mm_return, "p1": p1_return, "p3": p3_return}
    pd.DataFrame(players_return).describe().to_csv(r"C:\Users\24395\Designated_Market_Making\output\participants_return.csv")
    pd.DataFrame(EP_ratio).describe().to_csv(
        r"C:\Users\24395\Designated_Market_Making\output\EP_ratio.csv")

if __name__ == "__main__":
    main()