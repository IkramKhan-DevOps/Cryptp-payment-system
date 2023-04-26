
def convert_crypto(crypto1, crypto2, amount):
    # Define conversion rates
    conversion_rates = {
        'BTC': {'DOGE': 119246.85, 'ETHEREUM': 27.37, 'SHEBA': 0.000014},
        'DOGE': {'BTC': 0.00000839, 'ETHEREUM': 0.000229, 'SHEBA': 0.00062},
        'ETHEREUM': {'BTC': 0.036, 'DOGE': 4374.06, 'SHEBA': 0.00043},
        'SHEBA': {'BTC': 71563.48, 'DOGE': 1613.65, 'ETHEREUM': 2317.39}
    }
    print(crypto1)
    print(crypto2)
    # Check if both cryptocurrencies are valid and conversion rate is available
    if crypto1 in conversion_rates and crypto2 in conversion_rates[crypto1]:
        # Convert cryptocurrency
        converted_amount = amount * conversion_rates[crypto1][crypto2]
        print(converted_amount)
        print("in")
        return float(converted_amount)
    else:
        print("Out")
        return 10


def convert_to_float(str_value):
    try:
        float_value = float(str_value)
        return float_value
    except ValueError:
        return None
