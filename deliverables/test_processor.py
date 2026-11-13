# Name: Reyansh | SRN: PES2UG24CS401 | Lab 7
import math
from hypothesis import given, strategies as st
from processor import parse_reading, wind_category, rainfall_spread

# ---------------------------------------------------------------------------
# Tests for parse_reading
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_reading_no_crash(s):
    """Robustness: parse_reading must not crash with unhandled exception on text or None."""
    result = parse_reading(s)
    assert result is None or (isinstance(result, tuple) and len(result) == 2)


@given(st.one_of(st.text(), st.integers(), st.none(), st.lists(st.integers())))
def test_parse_reading_robustness_mixed_types(val):
    """Robustness: parse_reading must safely handle mixed and unexpected input types."""
    result = parse_reading(val)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[0], float)
        and isinstance(result[1], int)
    )


@given(
    temp=st.floats(min_value=-50.0, max_value=60.0, allow_nan=False, allow_infinity=False),
    humidity=st.integers(min_value=0, max_value=100),
)
def test_parse_reading_correctness(temp, humidity):
    """Correctness: round-trip parsing of valid formatted temperature and humidity."""
    temp_round = round(temp, 2)
    reading_str = f"{temp_round}/{humidity}"
    result = parse_reading(reading_str)
    assert result is not None
    parsed_temp, parsed_hum = result
    assert math.isclose(parsed_temp, temp_round, rel_tol=1e-5, abs_tol=1e-5)
    assert parsed_hum == humidity
    assert isinstance(parsed_temp, float)
    assert isinstance(parsed_hum, int)


# ---------------------------------------------------------------------------
# Tests for wind_category
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_wind_category_no_crash(s):
    """Robustness: wind_category must not crash with unhandled exception on text or None."""
    result = wind_category(s)
    assert result in ('warning', 'advisory', 'none', None)


@given(st.one_of(st.text(), st.integers(), st.none(), st.lists(st.integers())))
def test_wind_category_robustness_mixed_types(val):
    """Robustness: wind_category must safely handle mixed and unexpected input types."""
    result = wind_category(val)
    assert result in ('warning', 'advisory', 'none', None)


@given(speed=st.integers(min_value=0, max_value=500))
def test_wind_category_correctness(speed):
    """Correctness: verify category thresholds (>=89 warning, >=39 advisory, else none)."""
    result = wind_category(str(speed))
    if speed >= 89:
        assert result == 'warning'
    elif speed >= 39:
        assert result == 'advisory'
    else:
        assert result == 'none'


# ---------------------------------------------------------------------------
# Tests for rainfall_spread
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_rainfall_spread_no_crash(s):
    """Robustness: rainfall_spread must not crash with unhandled exception on text or None."""
    result = rainfall_spread(s)
    assert result is None or (isinstance(result, float) and result >= 0.0)


@given(st.one_of(st.text(), st.integers(), st.none(), st.lists(st.integers())))
def test_rainfall_spread_robustness_mixed_types(val):
    """Robustness: rainfall_spread must safely handle mixed and unexpected input types."""
    result = rainfall_spread(val)
    assert result is None or (isinstance(result, float) and result >= 0.0)


@given(
    st.lists(
        st.floats(min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False),
        min_size=1,
        max_size=20,
    )
)
def test_rainfall_spread_correctness(readings):
    """Correctness: spread should equal max(readings) - min(readings) >= 0."""
    csv_str = ",".join(str(round(r, 2)) for r in readings)
    rounded_readings = [round(r, 2) for r in readings]
    expected_spread = max(rounded_readings) - min(rounded_readings)
    result = rainfall_spread(csv_str)
    assert result is not None
    assert math.isclose(result, expected_spread, rel_tol=1e-5, abs_tol=1e-5)
    assert result >= 0.0
