import pytest

from honeybee_revive.CO2_measures import CO2ReductionMeasure, CO2ReductionMeasureCollection


def test_CO2ReductionMeasure_initialization():
    measure = CO2ReductionMeasure(
        name="Test Measure",
        measure_type="PERFORMANCE",
        year=2022,
        cost=10000.0,
        kg_CO2=500.0,
        country_name="USA",
        labor_fraction=0.5,
    )
    assert measure.name == "Test Measure"
    assert measure.measure_type == "PERFORMANCE"
    assert measure.year == 2022
    assert measure.cost == 10000.0
    assert measure.kg_CO2 == 500.0
    assert measure.country_name == "USA"
    assert measure.labor_fraction == 0.5


def test_default_CO2ReductionMeasure_dict_round_trip():
    m1 = CO2ReductionMeasure()
    d1 = m1.to_dict()
    m2 = CO2ReductionMeasure.from_dict(d1)
    assert d1 == m2.to_dict()


def test_CO2ReductionMeasure_to_dict():
    measure = CO2ReductionMeasure(
        name="Test Measure",
        measure_type="PERFORMANCE",
        year=2022,
        cost=10000.0,
        kg_CO2=500.0,
        country_name="USA",
        labor_fraction=0.5,
    )
    measure_dict = measure.to_dict()
    assert measure_dict["name"] == "Test Measure"
    assert measure_dict["measure_type"] == "PERFORMANCE"
    assert measure_dict["year"] == 2022
    assert measure_dict["cost"] == 10000.0
    assert measure_dict["kg_CO2"] == 500.0
    assert measure_dict["country_name"] == "USA"
    assert measure_dict["labor_fraction"] == 0.5


def test_CO2ReductionMeasure_from_dict():
    measure_dict = {
        "type": "CO2ReductionMeasure",
        "name": "Test Measure",
        "measure_type": "PERFORMANCE",
        "year": 2022,
        "cost": 10000.0,
        "kg_CO2": 500.0,
        "country_name": "USA",
        "labor_fraction": 0.5,
    }
    measure = CO2ReductionMeasure.from_dict(measure_dict)
    assert measure.name == "Test Measure"
    assert measure.measure_type == "PERFORMANCE"
    assert measure.year == 2022
    assert measure.cost == 10000.0
    assert measure.kg_CO2 == 500.0
    assert measure.country_name == "USA"
    assert measure.labor_fraction == 0.5


def test_CO2ReductionMeasureCollection():
    collection = CO2ReductionMeasureCollection()
    measure1 = CO2ReductionMeasure(name="Measure 1")
    measure2 = CO2ReductionMeasure(name="Measure 2")
    collection.add_measure(measure1)
    collection.add_measure(measure2)
    assert len(collection) == 2
    assert measure1 in collection
    assert measure2 in collection
    assert collection.keys() == sorted([measure1.unique_id, measure2.unique_id])
    assert collection.values() == sorted([measure1, measure2], key=lambda x: x.unique_id)


def test_CO2ReductionMeasureCollection_to_dict():
    collection = CO2ReductionMeasureCollection()
    measure1 = CO2ReductionMeasure(name="Measure 1")
    measure2 = CO2ReductionMeasure(name="Measure 2")
    collection.add_measure(measure1)
    collection.add_measure(measure2)
    collection_dict = collection.to_dict()
    assert measure1.unique_id in collection_dict
    assert measure2.unique_id in collection_dict


def test_CO2ReductionMeasureCollection_from_dict():
    collection_dict = {
        "Measure 1-PERFORMANCE-60-8500-0.4": {
            "type": "CO2ReductionMeasure",
            "name": "Measure 1",
            "measure_type": "PERFORMANCE",
            "year": 60,
            "cost": 8500.0,
            "kg_CO2": 0.0,
            "country_name": "USA",
            "labor_fraction": 0.4,
        },
        "Measure 2-NON_PERFORMANCE-60-8500-0.4": {
            "type": "CO2ReductionMeasure",
            "name": "Measure 2",
            "measure_type": "NON_PERFORMANCE",
            "year": 60,
            "cost": 8500.0,
            "kg_CO2": 0.0,
            "country_name": "USA",
            "labor_fraction": 0.4,
        },
    }
    collection = CO2ReductionMeasureCollection.from_dict(collection_dict)
    assert len(collection) == 2
    assert "Measure 1-PERFORMANCE-60-8500-0.4" in collection
    assert "Measure 2-NON_PERFORMANCE-60-8500-0.4" in collection


def test_non_CO2Measure_dict_from_dict_raises_error():
    measure_dict = {
        "type": "Not A CO2 Measure",
        "name": "Test Measure",
        "measure_type": "PERFORMANCE",
        "year": 2022,
        "cost": 10000.0,
        "kg_CO2": 500.0,
        "country_name": "USA",
        "labor_fraction": 0.5,
    }

    with pytest.raises(ValueError):
        measure = CO2ReductionMeasure.from_dict(measure_dict)
