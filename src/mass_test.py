from src.trade_agent import Agent
import pandas as pd
import numpy as np
import os
def main():
    #for rebate_rate in np.arange(-0.0026, -0.0014, 0.0002):
    for rebate_rate in [-0.002]:
        for mm_no in range(1, 2):
            stock_symbol = "IBM"
            number_of_mm = mm_no
            real_mkt = False
            total_rounds = 1000
            num_of_test = 1
            mm_return = []
            p1_return = []
            p3_return = []
            liquidity = {"EP_ratio" : [], "qs": [], "DB": [], "RS5": [], "RS10": [], "AS5": [], "AS10": []}
            days_correction = []

            # Define the directory path
            dir_path = f"C:\\Users\\24395\\Designated_Market_Making\\output3\\MM{number_of_mm}_RR{rebate_rate}"

            # Check if the directory does not exist
            if not os.path.exists(dir_path):
                # Create the directory
                os.makedirs(dir_path)

            for i in range(num_of_test):
                trading_agent = Agent(tickers=stock_symbol, num_mm= number_of_mm,real_mkt=real_mkt, num_rounds=total_rounds, rebate_rate=rebate_rate)
                trading_agent.update_directories(dir_path)
                for round in range(total_rounds):
                    trading_agent.update_markettradebook()
                    trading_agent.send_book()
                    trading_agent.mmtrade_submit()
                    trading_agent.exchange_execution()
                    trading_agent.record_allplayers()
                    trading_agent.run_next_round()
                x = pd.read_csv(f"{dir_path}\\playersIC.csv")
                x['mm_portfolio'] = x['mm1_inventory'] * x['price_history'] + x['mm1_cash']
                x['p1_portfolio'] = x['p1_inventory'] * x['price_history'] + x['p1_cash']
                x['p3_portfolio'] = x['p3_inventory'] * x['price_history'] + x['p3_cash']
                mm_return.append(x['mm_portfolio'].iloc[-1])
                p1_return.append(x['p1_portfolio'].iloc[-1])
                p3_return.append(x['p3_portfolio'].iloc[-1])
                nums_days = count_price_correction(x)
                days_correction.append(nums_days)
                y = pd.read_csv(f"{dir_path}\\all_orders.csv")
                liquidity["EP_ratio"].append(y['status'].value_counts()["EXECUTED"]/y['status'].value_counts()["PENDING"])
                matched_orders = pd.read_csv(f"{dir_path}\\matched_orders.csv")
                matched_orders = matched_orders.set_index("Time")
                for i in range(10,total_rounds-10):
                    try:
                        liquidity["RS5"].append(abs(np.mean(matched_orders.loc[[i]]["Matched Price"] - x["price_history"].iloc[i+5]))/x["price_history"].iloc[i])
                        liquidity["RS10"].append(abs(np.mean(matched_orders.loc[[i]]["Matched Price"] - x["price_history"].iloc[i+10]))/x["price_history"].iloc[i])
                        liquidity["AS5"].append(abs(np.mean(x["price_history"].iloc[i+5] - x["price_history"].iloc[i]))/x["price_history"].iloc[i])
                        liquidity["AS10"].append(abs(np.mean(x["price_history"].iloc[i+10] - x["price_history"].iloc[i]))/x["price_history"].iloc[i])
                    except (ValueError, KeyError):
                        continue
                z = pd.read_csv(f"{dir_path}\\liquidity.csv")
                liquidity["qs"].append(np.mean(z['qs']))
                liquidity["DB"].append(np.mean(z['DB']))
                print(i)
            players_return = {"mm": mm_return, "p1": p1_return, "p3": p3_return}
            pd.DataFrame(players_return).describe().to_csv(f"{dir_path}\\participants_return.csv")
            pd.DataFrame(dict([(k, pd.Series(v)) for k, v in liquidity.items()])).describe().to_csv(
                f"{dir_path}\\liquidity_analysis.csv")
            pd.DataFrame(dict([(k, pd.Series(v)) for k, v in liquidity.items()])).to_csv(
                f"{dir_path}\\liquidity_all.csv")
            pd.DataFrame(days_correction).to_csv(f"{dir_path}\\days_correction.csv")

def count_price_correction(x):
    nums_days = 0
    for i in range(500,len(x)):
        if abs(x['price_history'].iloc[i] - x['fundamental_price'].iloc[i])/x['fundamental_price'].iloc[i] < 0.01:
            break
        nums_days += 1
    return nums_days

if __name__ == "__main__":
    main()