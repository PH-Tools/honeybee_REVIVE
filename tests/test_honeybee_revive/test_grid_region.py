import pytest
from honeybee_revive.grid_region import GridRegion


def test_grid_region_initialization():
    grid_region = GridRegion("Test Name", "Test Code", "Test Description", "Test/Path")
    assert grid_region.display_name == "Test Name"
    assert grid_region.region_name == "Test Name"
    assert grid_region.region_code == "Test Code"
    assert grid_region.description == "Test Description"
    assert grid_region.filepath == "Test/Path"


def test_grid_region_to_dict():
    grid_region = GridRegion("Test Name", "Test Code", "Test Description", "Test/Path")
    grid_dict = grid_region.to_dict()
    assert grid_dict["region_name"] == "Test Name"
    assert grid_dict["region_code"] == "Test Code"
    assert grid_dict["description"] == "Test Description"
    assert grid_dict["filepath"] == "Test/Path"


def test_grid_region_from_dict():
    grid_dict = {
        "region_name": "Test Name",
        "region_code": "Test Code",
        "description": "Test Description",
        "filepath": "Test/Path",
    }
    grid_region = GridRegion.from_dict(grid_dict)
    assert grid_region.display_name == "Test Name"
    assert grid_region.region_name == "Test Name"
    assert grid_region.region_code == "Test Code"
    assert grid_region.description == "Test Description"
    assert grid_region.filepath == "Test/Path"


def test_grid_region_duplicate():
    grid_region = GridRegion("Test Name", "Test Code", "Test Description", "Test/Path")
    duplicate_region = grid_region.duplicate()
    assert duplicate_region.display_name == "Test Name"
    assert duplicate_region.region_name == "Test Name"
    assert duplicate_region.region_code == "Test Code"
    assert duplicate_region.description == "Test Description"
    assert duplicate_region.filepath == "Test/Path"
    assert duplicate_region is not grid_region


def test_grid_region_str():
    grid_region = GridRegion("Test Name", "Test Code", "Test Description", "Test/Path")
    expected_str = "GridRegion [Test Code]: Test Name | Test Description | Test/Path"
    assert str(grid_region) == expected_str


def test_grid_region_repr():
    grid_region = GridRegion("Test Name", "Test Code", "Test Description", "Test/Path")
    expected_repr = "GridRegion [Test Code]: Test Name | Test Description | Test/Path"
    assert repr(grid_region) == expected_repr


def test_grid_region_ToString():
    grid_region = GridRegion("Test Name", "Test Code", "Test Description", "Test/Path")
    expected_ToString = "GridRegion [Test Code]: Test Name | Test Description | Test/Path"
    assert grid_region.ToString() == expected_ToString
