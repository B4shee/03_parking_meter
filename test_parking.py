import pytest
from parking_fee import calculate_parking_fee
from parking_permit import is_permit_valid


# --- calculate_parking_fee tests ---


def test_fee_zero_minutes():
  result = calculate_parking_fee(0)
  assert result == 0
  assert type(result) is int


@pytest.mark.parametrize(
    ("minutes", "expected_cents"),
    [
        (1, 200),
        (59, 200),
        (60, 200),
        (61, 400),
        (119, 400),
        (120, 400),
        (121, 600),
        (180, 600),
    ],
)
def test_fee_rounds_partial_hours_up_to_full_hour(minutes, expected_cents):
  result = calculate_parking_fee(minutes)
  assert result == expected_cents
  assert type(result) is int


@pytest.mark.parametrize("bad_minutes", [-1, -15, -120])
def test_fee_negative_minutes_raises_value_error(bad_minutes):
  with pytest.raises(ValueError):
    calculate_parking_fee(bad_minutes)


@pytest.mark.parametrize("bad_type", [True, False, 1.0, 30.5, "60", None])
def test_fee_invalid_type_raises_type_error(bad_type):
  with pytest.raises(TypeError):
    calculate_parking_fee(bad_type)


# --- is_permit_valid tests ---


@pytest.mark.parametrize("minutes", [0, 1, 60, 119, 120])
def test_permit_valid_when_active_and_within_120_minutes(minutes):
  result = is_permit_valid(True, minutes)
  assert result is True
  assert type(result) is bool


@pytest.mark.parametrize("minutes", [121, 180])
def test_permit_invalid_when_active_and_over_120_minutes(minutes):
  result = is_permit_valid(True, minutes)
  assert result is False
  assert type(result) is bool


@pytest.mark.parametrize("minutes", [0, 30, 120, 150])
def test_permit_invalid_when_inactive(minutes):
  result = is_permit_valid(False, minutes)
  assert result is False
  assert type(result) is bool


@pytest.mark.parametrize("active", [True, False])
@pytest.mark.parametrize("bad_minutes", [-1, -120])
def test_permit_negative_minutes_raises_value_error(active, bad_minutes):
  with pytest.raises(ValueError):
    is_permit_valid(active, bad_minutes)


@pytest.mark.parametrize(
    ("active", "minutes"),
    [
        (1, 30),
        (0, 30),
        ("True", 30),
        (None, 30),
        (True, True),
        (True, False),
        (True, 12.0),
    ],
)
def test_permit_invalid_types_raise_type_error(active, minutes):
  with pytest.raises(TypeError):
    is_permit_valid(active, minutes)