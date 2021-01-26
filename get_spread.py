def get_spread(currency_id, data):
    """
    Calculates the optimal bid/ask spread for a crypto/exchange pair.
    """

    filtered = list(filter(lambda x: x['id'] == currency_id, data))
    buy_info = [(item['buy_price'], item['exchange']) for item in filtered]
    sell_info = [(item['sell_price'], item['exchange']) for item in filtered]
    buy_at = min(buy_info, key=lambda x: x[0])
    sell_at = max(sell_info, key=lambda x: x[0])
    return f"[{currency_id}]: Buy from {buy_at[1]} for {buy_at[0]}. " \
           f"Sell to {sell_at[1]} for {sell_at[0]}.\n"
