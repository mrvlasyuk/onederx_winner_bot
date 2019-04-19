## What is it?
This bot can help you to increase your volumes at Onederx Trading Challenge . More info about challenge: [https://trade.onederx.com/leaderboard](https://trade.onederx.com/leaderboard)

## How it works?
Bot make buy and sell trades in both directions. 

## What is OnederX?
[Onederx](https://onederx.com) is crypto derivatives trading platform launched in 2018. The main trading instrument is `BTCUSD_P` which is Perpetual contract with a leverage up to **20x**.

🔥 By the way, you can trade Memes on Onederx! `MEMES-BTC` is a Perpetual contract based on Onederx Meme-Index. More info: [https://memes.onederx.com](https://memes.onederx.com).


## Before you start
1. Trading in both sides your lose small amount of money on spread difference. Make sure you understand this point.
2. There are limits on orders number sent within a day to participate in Active trader nomination (max 1000 orders a day). 
3. Bot close your position to zero.
4. Use it to your own risk.


## How to use
0. Install Python 3.6+
1. Install `onederx` module

`$ pip install -U onederx`

2. Clone this repository

`$ git clone https://github.com/mrvlasyuk/onederx_winner_bot`

3. Create your API keys on [https://trade.onederx.com/user/api](https://trade.onederx.com/user/api). 
4. Copy and paste API_KEY and SECRET to `keys.json` config file.
5. Run the bot

`$ python3 bot.py {VOLUME_TO_TRADE} --max_order {MAX_ORDER_VOLUME}`

## Configuration
You can provide additional arguments

```
  --path_to_key PATH_TO_KEY
                        path to config file with your api_key and secret key.
                        (default: ./keys.json)
  --symbol SYMBOL       symbol to trade (default: BTCUSD_P)
  --max_order MAX_ORDER
                        max order amount to sent (default: 2000)
  --max_n_orders MAX_N_ORDERS
                        max number of orders to sent (default: 500)
  --max_spread_pcnt MAX_SPREAD_PCNT
                        max spread percent we want to trade (default: 0.001)```