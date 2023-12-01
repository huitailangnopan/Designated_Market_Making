from src.trade_agent import Agent
if __name__ == "__main__":
    new_agent = Agent("IBM",1,False)
    for i in range(99):
        new_agent.update_tradebook()
        new_agent.update_price()
        new_agent.send_book()
        new_agent.trade_submit()
        new_agent.run_next_round()