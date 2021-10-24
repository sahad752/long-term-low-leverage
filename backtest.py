import config, strategy
from datetime import datetime

def backtest():
    print("\n_Big_ Timeframe : " + strategy.big___timeframe)
    print("Entry Timeframe : " + strategy.entry_timeframe + "\n")

    all_pairs = 0
    for i in range(len(config.coin)):
        klines = strategy.klines(i)
        swing_trades = strategy.swing_trade(i, klines)

        print("Start Time Since " + str(datetime.fromtimestamp(swing_trades["timestamp"].iloc[0]/1000)))
        long_result = round(check_for_long(i, swing_trades), 2)
        short_reult = round(check_for_short(i, swing_trades), 2)
        overall_result = round(long_result + short_reult, 2)
        all_pairs = round(all_pairs + overall_result, 2)

        print("PNL for _Long Positions: " + str(long_result) + "%")
        print("PNL for Short Positions: " + str(short_reult) + "%")
        print("PNL for _BOTH Positions: " + str(overall_result) + "%")
        # print("This backtest is generated based on past " + str(strategy.query) + " candlesticks")
        print()
    print("ALL PAIRS PNL : " + str(all_pairs) + "%\n")

def check_for_long(i, swing_trades):
    position = False
    total_pnl, realized_pnl, entry_price = 0, 0, 0

    for index in range(len(swing_trades)):
        if not position:
            if swing_trades["GO_LONG"].iloc[index]:
                position = True
                entry_price = swing_trades['close'].iloc[index]
        else:
            if swing_trades["EXIT_LONG"].iloc[index]:
                position = False
                realized_pnl = (swing_trades['close'].iloc[index] - entry_price) / entry_price * 100 * config.leverage[i]
                total_pnl = total_pnl + realized_pnl

    return round(total_pnl, 2)

def check_for_short(i, swing_trades):
    position = False
    total_pnl, realized_pnl, entry_price = 0, 0, 0

    for index in range(len(swing_trades)):
        if not position:
            if swing_trades["GO_SHORT"].iloc[index]:
                position = True
                entry_price = swing_trades['close'].iloc[index]
        else:
            if swing_trades["EXIT_SHORT"].iloc[index]:
                position = False
                realized_pnl = (swing_trades['close'].iloc[index] - entry_price) / entry_price * 100 * config.leverage[i]
                total_pnl = total_pnl + realized_pnl

    return round(total_pnl, 2)

backtest()