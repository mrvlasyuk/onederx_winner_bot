import time
import json
import argparse

from decimal import Decimal
from onederx import OnederxREST


class Symbol:
    def __init__(self, symbol, api_key, secret):
        self.symbol = symbol
        self.rest_api = OnederxREST(base_url="https://api.onederx.com", api_key=api_key, secret=secret)
        self.l2 = None
        self.ask = None
        self.bid = None
        self.mean_price = None
    
    def cancel_orders(self):
        self.rest_api.cancel_all_orders(self.symbol)
        
    def send_limit(self, side, price, volume):
        self.rest_api.new_order(
            symbol=self.symbol,
            my_id="",
            side=side,
            price=price,
            volume=volume,
            order_type="limit",
            time_in_force="ioc",
            is_post_only=False,
            is_stop=False)
        
    def get_position(self):
        pos = [p for p in self.rest_api.get_positions() if p["symbol"] == self.symbol]
        assert len(pos) == 1
        return pos[0]["position"]
    
    def update_l2(self):
        self.l2 = self.rest_api.get_l2_snapshot(self.symbol)
        for level in self.l2:
            level["price"] = Decimal(level["price"])
            level["volume"] = Decimal(level["volume"])
        
        self.levels = {
            "sell": [l for l in self.l2 if l["side"] == "sell"],
            "buy": [l for l in self.l2 if l["side"] == "buy"]
        }

        self.ask = min([l["price"] for l in self.levels["sell"]] + [Decimal(1e10)])
        self.bid = max([l["price"] for l in self.levels["buy"]] + [Decimal(0)])
        self.mean_price = (self.ask + self.bid) / 2
    
    def max_vol_till_price(self, side, price):
        if side == "buy":
            return sum(l["volume"] for l in self.levels[side] if l["price"] >= price)
        else:
            return sum(l["volume"] for l in self.levels[side] if l["price"] <= price)


class Trader:
    def __init__(self, 
        symbol, 
        max_order_volume=2000, 
        max_spread_pcnt=0.001,
        max_n_orders=500):

        self.symbol = symbol
        self.max_order_volume = max_order_volume
        self.max_n_orders = max_n_orders
        self.max_spread_pcnt = max_spread_pcnt

        self.vol_sent = 0
        self.n_orders_sent = 0

    def calc_buy_and_sell_prices(self):
        mean_price = float(self.symbol.mean_price)
        max_buy_price = int(mean_price * (1 + self.max_spread_pcnt / 2) )
        min_sell_price = int(mean_price * (1 - self.max_spread_pcnt / 2) )
        return max_buy_price, min_sell_price

    def calc_max_order_vol(self, volume_left):
        symbol = self.symbol

        max_buy_price, min_sell_price = self.calc_buy_and_sell_prices()
        max_sell_vol = symbol.max_vol_till_price("buy", min_sell_price)
        max_buy_vol = symbol.max_vol_till_price("sell", max_buy_price)

        max_vol_to_trade = min(max_buy_vol, max_sell_vol)
        max_vol_to_trade = min(max_vol_to_trade, self.max_order_volume)
        max_vol_to_trade = min(max_vol_to_trade, (volume_left + 1) // 2)
        return max_vol_to_trade
    
    def close_position(self):
        symbol = self.symbol
        while True: 
            print("Trying to close position ...")
            symbol.update_l2()
            position = symbol.get_position()
            if position == 0:
                print("Position is closed")
                break

            max_buy_price, min_sell_price = self.calc_buy_and_sell_prices()

            if position < 0:
                max_vol = symbol.max_vol_till_price("sell", max_buy_price)
                if max_vol > 0:
                    symbol.send_limit("buy", max_buy_price, abs(position))
            else:
                max_vol = symbol.max_vol_till_price("buy", min_sell_price)
                if max_vol > 0: 
                    symbol.send_limit("sell", min_sell_price, abs(position))
            time.sleep(1)

    def make_volume(self, volume_to_trade):
        symbol = self.symbol
        print(f"Canceling all orders on {symbol.symbol}")
        symbol.cancel_orders()

        volume_left = volume_to_trade
        for _ in range(1000):
            symbol.update_l2()

            max_vol_to_trade = self.calc_max_order_vol(volume_left)
            max_buy_price, min_sell_price = self.calc_buy_and_sell_prices()

            if max_vol_to_trade > 0:
                position = symbol.get_position()
                if position < 0:
                    symbol.send_limit("buy", max_buy_price, max_vol_to_trade + abs(position))
                    symbol.send_limit("sell", min_sell_price, max_vol_to_trade)
                else:
                    symbol.send_limit("sell", min_sell_price, max_vol_to_trade + abs(position))
                    symbol.send_limit("buy", max_buy_price, max_vol_to_trade)
                    
                self.n_orders_sent += 2
                traded_vol = max_vol_to_trade * 2 + abs(position) 
                self.vol_sent += traded_vol
                volume_left -= traded_vol
                print(f"Sent {max_vol_to_trade}x2 orders. Total sent: volume = {self.vol_sent}  / number_of_orders = {self.n_orders_sent}")

                if volume_left <= 0:
                    print(f"Success. I have sent {self.vol_sent}. Job is done.")
                    break
                
                if self.n_orders_sent > self.max_n_orders:
                    print(f"I'm stopping because I sent more than {self.max_n_orders} orders. ")
                    break

            else:
                print(f"Can't send orders. Probably spread is too high.")
            print(f"Cycle end, left {volume_left} volume to send")
            time.sleep(1)


def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("volume", type=int, help="volume in contracts you want to trade")
    parser.add_argument("--path_to_key", type=str, default="./keys.json", help="path to config file with your api_key and secret key.")        
    parser.add_argument("--symbol", type=str, default="BTCUSD_P", help="symbol to trade")
    parser.add_argument("--max_order", type=int, default=200, help="max order amount to send")
    parser.add_argument("--max_n_orders", type=int, default=500, help="max number of orders to send")
    parser.add_argument("--max_spread_pcnt", type=float, default=0.001, help="max spread percentage bot wants to trade")
    args = parser.parse_args()
    return args


def read_config(path):
    config = json.load(open(path))
    if config["api_key"] == "PUT_API_KEY_HERE" or config["secret"] == "PUT_SECRET_HERE":
        print(f"Error: You should put your API and SECRET keys to {path} config file")
        return None
    return config


if __name__ == "__main__":
    args = parse_args()
    print(f"Starting with params: {args}")

    config = read_config(args.path_to_key)
    if config:
        symbol_api = Symbol(args.symbol, config["api_key"], config["secret"])
        trader = Trader(symbol_api, args.max_order, args.max_spread_pcnt, args.max_n_orders)
        trader.make_volume(args.volume)
        trader.close_position()
