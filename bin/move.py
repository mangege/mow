import asyncio
import signal
from leek.base import ArbitrageConfig
from leek.bricklayer import Bricklayer
from leek import utils


def signal_handler(signum, frame):
    print('signal_handler')
    utils.exit_signal = True
    utils.exit_signal_count += 1
    if utils.exit_signal_count >= 5:
        exit()


signal.signal(signal.SIGINT, signal_handler)


async def main():
    bricklayer_list = []

    exchange1_id = 'gateio'
    exchange2_id = 'huobipro'
    exchange1_options = utils.get_exchange_options(exchange1_id)
    exchange2_options = utils.get_exchange_options(exchange2_id)
    config = ArbitrageConfig({
        'name': 'btc_gateio_huobipro_1',
        'base_coin': 'BTC',
        'quote_coin': 'USDT',
        'one_to_two_pure_profit_limit': 0.03,
        'two_to_one_pure_profit_limit': 0.03,
        'min_buy_num_limit_by_quote': 6,  # huobi pro 5usdt
        'max_buy_num_limit_by_quote': 20.0,  # 20 USDT
        'max_open_order_limit': 3,
        'base_coin_num': 0.002,
        'quote_coin_num': 200,
        'exchange1_api_key': exchange1_options['apiKey'],
        'exchange1_secret': exchange1_options['secret'],
        'exchange2_api_key': exchange2_options['apiKey'],
        'exchange2_secret': exchange2_options['secret'],
        'exchange1_id': exchange1_id,
        'exchange2_id': exchange2_id,
        'exchange1_taker_fee': 0.002,
        'exchange2_taker_fee': 0.002,
        'exchange1_withdraw_base_fee': 0.0005,
        'exchange1_withdraw_quote_fee': 0.0,
        'exchange2_withdraw_base_fee': 0.0005,
        'exchange2_withdraw_quote_fee': 0.0,
        'base_coin_alert_num': 0.001,
        'quote_coin_alert_num': 10,
        'bisect_coin': False,
        'enable_transfer': False,
    })
    bricklayer = Bricklayer(config)
    bricklayer_list.append(bricklayer)

    tasks = [bricklayer.run() for bricklayer in bricklayer_list]
    tasks.append(utils.run_all_exchange_ws(bricklayer_list))
    await asyncio.gather(*tasks)

asyncio.run(main())
