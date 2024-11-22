import pytest

from honeybee_revive.fuels import Fuel, FuelCollection


def test_Fuel_initialization():
    fuel = Fuel(_fuel_type="ELECTRICITY")
    assert fuel.fuel_type == "ELECTRICITY"


def test_default_Fuel_dict_round_trip():
    f1 = Fuel()
    d1 = f1.to_dict()
    f2 = Fuel.from_dict(d1)
    assert d1 == f2.to_dict()


def test_Fuel_to_dict():
    fuel = Fuel(_fuel_type="ELECTRICITY")
    fuel_dict = fuel.to_dict()
    assert fuel_dict["fuel_type"] == "ELECTRICITY"

    nat_gas = Fuel(
        _fuel_type="NATURAL_GAS",
        _purchase_price_per_kwh=0.17984,
        _sale_price_per_kwh=0.132,
        _annual_base_price=200.0,
    )
    nat_gas_dict = nat_gas.to_dict()
    assert nat_gas_dict["fuel_type"] == "NATURAL_GAS"
    assert nat_gas_dict["purchase_price_per_kwh"] == 0.17984
    assert nat_gas_dict["sale_price_per_kwh"] == 0.132
    assert nat_gas_dict["annual_base_price"] == 200.0


def test_Fuel_from_dict():
    fuel_dict = {
        "type": "Fuel",
        "fuel_type": "ELECTRICITY",
        "purchase_price_per_kwh": 0.17984,
        "sale_price_per_kwh": 0.132,
        "annual_base_price": 200.0,
    }
    fuel = Fuel.from_dict(fuel_dict)
    assert fuel.fuel_type == "ELECTRICITY"

    nat_gas_fuel_dict = {
        "type": "Fuel",
        "fuel_type": "NATURAL_GAS",
        "purchase_price_per_kwh": 0.17984,
        "sale_price_per_kwh": 0.132,
        "annual_base_price": 200.0,
    }
    nat_gas = Fuel.from_dict(nat_gas_fuel_dict)
    assert nat_gas.fuel_type == "NATURAL_GAS"
    assert nat_gas.purchase_price_per_kwh == 0.17984
    assert nat_gas.sale_price_per_kwh == 0.132
    assert nat_gas.annual_base_price == 200.0


def test_duplicate_electricity():
    fuel = Fuel(
        _fuel_type="ELECTRICITY",
        _purchase_price_per_kwh=0.17984,
        _sale_price_per_kwh=0.132,
        _annual_base_price=200.0,
    )
    new_fuel = fuel.duplicate()
    assert new_fuel.fuel_type == "ELECTRICITY"
    assert new_fuel.purchase_price_per_kwh == 0.17984
    assert new_fuel.sale_price_per_kwh == 0.132
    assert new_fuel.annual_base_price == 200.0


def test_duplicate_gas():
    fuel = Fuel(
        _fuel_type="NATURAL_GAS",
        _purchase_price_per_kwh=0.17984,
        _sale_price_per_kwh=0.132,
        _annual_base_price=200.0,
    )
    new_fuel = fuel.duplicate()
    assert new_fuel.fuel_type == "NATURAL_GAS"
    assert new_fuel.purchase_price_per_kwh == 0.17984
    assert new_fuel.sale_price_per_kwh == 0.132
    assert new_fuel.annual_base_price == 200.0


# ----------------------------------------------------------------------------------------------------------------------


def test_FuelCollection_initialization():
    collection = FuelCollection()
    assert collection._storage == {}


def test_FuelCollection_add_fuel():
    collection = FuelCollection()
    fuel = Fuel(_fuel_type="ELECTRICITY")
    collection.add_fuel(fuel)
    assert collection._storage["ELECTRICITY"] == fuel


def test_FuelCollection_to_dict():
    collection = FuelCollection()
    fuel = Fuel(_fuel_type="ELECTRICITY")
    collection.add_fuel(fuel)
    collection_dict = collection.to_dict()
    assert collection_dict["ELECTRICITY"]["fuel_type"] == "ELECTRICITY"


def test_FuelCollection_from_dict():
    collection_dict = {
        "Test Fuel": {
            "type": "Fuel",
            "fuel_type": "ELECTRICITY",
            "purchase_price_per_kwh": 0.17984,
            "sale_price_per_kwh": 0.132,
            "annual_base_price": 200.0,
        }
    }
    collection = FuelCollection.from_dict(collection_dict)
    assert collection._storage["ELECTRICITY"].fuel_type == "ELECTRICITY"
    assert collection._storage["ELECTRICITY"].purchase_price_per_kwh == 0.17984
    assert collection._storage["ELECTRICITY"].sale_price_per_kwh == 0.132
    assert collection._storage["ELECTRICITY"].annual_base_price == 200.0


def test_non_Fuel_dict_from_dict_raises_error():
    fuel_dict = {
        "type": "Not A Fuel",
        "fuel_type": "Test Fuel",
    }
    with pytest.raises(ValueError):
        Fuel.from_dict(fuel_dict)


def test_duplicate_fuel_collection():
    collection = FuelCollection()
    fuel = Fuel(_fuel_type="ELECTRICITY")
    collection.add_fuel(fuel)
    new_collection = collection.duplicate()
    assert new_collection._storage["ELECTRICITY"].fuel_type == "ELECTRICITY"
    assert new_collection._storage["ELECTRICITY"].purchase_price_per_kwh == 0.0
    assert new_collection._storage["ELECTRICITY"].sale_price_per_kwh == 0.0
    assert new_collection._storage["ELECTRICITY"].annual_base_price == 0.0


def test_duplicate_fuel_collection_with_two_fuels():
    collection = FuelCollection()
    fuel1 = Fuel(_fuel_type="ELECTRICITY")
    fuel2 = Fuel(_fuel_type="NATURAL_GAS")
    collection.add_fuel(fuel1)
    collection.add_fuel(fuel2)
    new_collection = collection.duplicate()
    assert new_collection._storage["ELECTRICITY"].fuel_type == "ELECTRICITY"
    assert new_collection._storage["ELECTRICITY"].purchase_price_per_kwh == 0.0
    assert new_collection._storage["ELECTRICITY"].sale_price_per_kwh == 0.0
    assert new_collection._storage["ELECTRICITY"].annual_base_price == 0.0

    assert new_collection._storage["NATURAL_GAS"].fuel_type == "NATURAL_GAS"
    assert new_collection._storage["NATURAL_GAS"].purchase_price_per_kwh == 0.0
    assert new_collection._storage["NATURAL_GAS"].sale_price_per_kwh == 0.0
    assert new_collection._storage["NATURAL_GAS"].annual_base_price == 0.0
