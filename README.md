## What is it?
This bot can help you to increase your volumes at Onederx Trading Challenge. More info about the challenge: [https://trade.onederx.com/leaderboard](https://trade.onederx.com/leaderboard)

## How does it work?
Bot makes buy and sell trades in both directions. 

## What is OnederX?
[Onederx](https://onederx.com) is crypto derivatives trading platform launched in 2018. The main trading instrument is `BTCUSD_P` which is Perpetual contract with a leverage up to **20x**.

🔥 By the way, you can trade Memes on Onederx! `MEMES-BTC` is a Perpetual contract based on Onederx Meme-Index. More info: [https://memes.onederx.com](https://memes.onederx.com).


## Before you start
1. This bot will spend small amount of money on bid-ask difference while trading in both directions and boosting your volume. Make sure you understand this point.
2. You need to keep the daily number of orders sent below 1000 to participate in Active trader nomination.
3. Bot will close your position to zero at the end.
4. Use it at your own risk. 


## How to use
0. Install Python 3.6+
1. Install `onederx` module

`$ python3 -m pip install -U onederx`

2. Clone this repository

`$ git clone https://github.com/mrvlasyuk/onederx_winner_bot`

3. Create your API keys on [https://trade.onederx.com/user/api](https://trade.onederx.com/user/api). 
4. Copy and paste API_KEY and SECRET to `keys.json` config file.
5. Run the bot

`$ python3 bot.py {VOLUME_TO_TRADE} --max_order {MAX_ORDER_VOLUME}`

## Example
1. Trade 2000 contracts on `MEMES_BTC`
2. Max volume of each order `<=150`
3. Max spread to trade is `5% = 0.05` 

`$ python3 bot.py 2000 --symbol MEMES_BTC --max_order 150 --max_spread_pcnt 0.05`


## Configuration
You can provide additional arguments

```
  --path_to_key PATH_TO_KEY
                        path to config file with your api_key and secret key.
                        (default: ./keys.json)
  --symbol SYMBOL       symbol to trade (default: BTCUSD_P)
  --max_order MAX_ORDER
                        max order amount to send (default: 200)
  --max_n_orders MAX_N_ORDERS
                        max number of orders to send (default: 500)
  --max_spread_pcnt MAX_SPREAD_PCNT
                        max spread percent we want to trade (default: 0.001)

```