# Name: Reyansh | SRN: PES2UG24CS401 | Lab 7
"""
Weather Alert Processor module.
Provides robust parsing and classification functions for meteorological data.
"""

import math


def parse_reading(text):
    """
    Parse a weather reading formatted as 'temperature/humidity'.

    Parameters:
        text (str): A string in the format '<temp>/<humidity>' (e.g. '35.5/80').

    Returns:
        tuple[float, int] | None: A tuple of (temperature, humidity) if valid,
                                  or None if the input is malformed, None,
                                  non-string, or non-numeric.
    """
    if text is None or not isinstance(text, str):
        return None

    cleaned = text.strip()
    if not cleaned or '/' not in cleaned:
        return None

    parts = cleaned.split('/')
    if len(parts) != 2:
        return None

    temp_part, hum_part = parts[0].strip(), parts[1].strip()
    if not temp_part or not hum_part:
        return None

    try:
        temp_val = float(temp_part)
        if math.isnan(temp_val) or math.isinf(temp_val):
            return None
    except ValueError:
        return None

    try:
        hum_val = int(hum_part)
    except ValueError:
        return None

    return temp_val, hum_val


def wind_category(speed_text):
    """
    Classify wind speed into a severity category.

    Categories:
        - 'warning':  speed >= 89 km/h
        - 'advisory': 39 <= speed < 89 km/h
        - 'none':     0 <= speed < 39 km/h

    Parameters:
        speed_text (str | int | float): Wind speed value or string representation.

    Returns:
        str | None: Category string ('warning', 'advisory', 'none') if valid,
                    or None if input is invalid, negative, non-numeric, or None.
    """
    if speed_text is None or isinstance(speed_text, bool):
        return None

    if isinstance(speed_text, (int, float)):
        if isinstance(speed_text, float) and (math.isnan(speed_text) or math.isinf(speed_text)):
            return None
        speed = int(speed_text)
    elif isinstance(speed_text, str):
        cleaned = speed_text.strip()
        if not cleaned:
            return None
        try:
            val = float(cleaned)
            if math.isnan(val) or math.isinf(val):
                return None
            speed = int(val)
        except ValueError:
            return None
    else:
        return None

    if speed < 0:
        return None

    if speed >= 89:
        return 'warning'
    if speed >= 39:
        return 'advisory'
    return 'none'


def rainfall_spread(readings_csv):
    """
    Calculate the spread (max - min) of hourly rainfall readings from CSV.

    Parameters:
        readings_csv (str): Comma-separated rainfall numbers in mm (e.g. '2,5.5,10').

    Returns:
        float | None: Spread (max - min) as a non-negative float if valid,
                      or None if input is malformed, empty, negative, or contains
                      invalid values.
    """
    if readings_csv is None or not isinstance(readings_csv, str):
        return None

    cleaned = readings_csv.strip()
    if not cleaned:
        return None

    tokens = cleaned.split(',')
    readings = []
    for token in tokens:
        t = token.strip()
        if not t:
            return None
        try:
            val = float(t)
            if math.isnan(val) or math.isinf(val):
                return None
            if val < 0.0:
                return None
            readings.append(val)
        except ValueError:
            return None

    if not readings:
        return None

    return max(readings) - min(readings)


def main():
    print("==== Running parse_reading ====")
    user_input = input("Enter temperature/humidity (e.g. 35.5/80): ")
    result = parse_reading(user_input)
    print("Temperature and Humidity:", result)

    print("\n==== Running wind_category ====")
    user_input = input("Enter a wind speed in km/h (e.g. 45): ")
    result = wind_category(user_input)
    print("Wind Category:", result)

    print("\n==== Running rainfall_spread ====")
    user_input = input("Enter hourly rainfall in mm as CSV (e.g. 2,5.5,10): ")
    result = rainfall_spread(user_input)
    print("Rainfall Spread:", result)


if __name__ == "__main__":
    main()
