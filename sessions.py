import sys
import time
from helper import get_session_data, get_all_sessions, attach_prefix_to_number, attach_suffix_to_number

def get_session_info(start_time: int):
    session_data = get_session_data(int(start_time))
    if not session_data:
        print(f"Could not find session {start_time}")
        return

    start_time = time.ctime(session_data["start_time"])
    starting_balance = session_data["starting_balance"]
    balance = round(session_data["balance"], 2)
    profit = round(balance - starting_balance, 2)
    shares = session_data["shares"]
    
    print(f"Start Time: {start_time}")
    print(f"Starting Balance: ${starting_balance}")
    print(f"Balance: ${balance}")
    print(f"Profit: ${profit}")
    print(f"Shares: {shares}")

    trades_count = len(session_data["trades"])
    if trades_count < 2:
        return

    trades = []
    win_trades = 0
    loss_trades = 0
    for i, buy_trade in enumerate(session_data["trades"]):
        if buy_trade["type"] == "buy":
            try:    
                sell_trade = session_data["trades"][i + 1]
                if sell_trade["price"] >= buy_trade["price"]:
                    win_trades += 1
                else:
                    loss_trades += 1
            except IndexError:
                pass

    win_rate = round(win_trades / (win_trades + loss_trades), 4) * 100
    price_change = session_data["trades"][-1]["price"] - session_data["trades"][0]["price"]

    print(f"Trades: {trades_count}")
    print(f"Win Trades: {win_trades}")
    print(f"Loss Trades: {loss_trades}")
    print(f"Win Rate: {win_rate}%")
    print(f"Price Change: ${price_change}")

def get_session_trades(start_time: int):
    session_data = get_session_data(int(start_time))
    if not session_data:
        print(f"Could not find session {start_time}")
        return

    for i, buy_trade in enumerate(session_data["trades"]):
        if buy_trade["type"] == "buy":
            try:
                sell_trade = session_data["trades"][i + 1]
                
                buy_price = buy_trade["price"]
                sell_price = sell_trade["price"]
                profit = round(sell_price - buy_price, 2)
                profit_percent = round(profit / buy_price * 100, 2)

                buy_price = attach_prefix_to_number(buy_price, "$")
                sell_price = attach_prefix_to_number(sell_price, "$")
                profit = attach_prefix_to_number(profit, "$")
                profit_percent = attach_suffix_to_number(profit_percent, "%")

                print(f"{buy_price} -> {sell_price} | {profit} ({profit_percent})")            
            except IndexError:
                pass

def __main__():
    while True:
        input_text = input("> ")
        arguments = input_text.split(" ")
        command = arguments[0]
        
        if command == "help":
            print("getallsessions                  Gets start times for all stored sessions.")
            print("getsessioninfo <start_time>     Gets info for a session.")
            print("getsessiontrades <start_time>   Gets all trades for a session.")
            print("help                            Shows this menu.")
            print("exit                            Stops the script.")
        elif command == "getallsessions":
            for session_data in get_all_sessions():
                print(session_data["start_time"])
        elif command == "getsessioninfo":
            start_time = arguments[1]
            get_session_info(start_time)
        elif command == "getsessiontrades":
            start_time = arguments[1]
            get_session_trades(start_time)
        elif command == "exit":
            sys.exit()
        else:
            print("Invalid command")

if __name__ == "__main__":
    __main__()
