import honeybee_energy._extend_honeybee
import honeybee_revive._extend_honeybee_revive
import honeybee_energy_revive._extend_honeybee_energy_revive

import pytest
from honeybee.face import Face, Face3D
from honeybee.model import Model
from honeybee.room import Room
from ladybug_geometry.geometry3d import Point3D

# --- Create the actual model


@pytest.fixture
def test_hb_model():
    """A Basic Box Model for testing."""
    hb_floor = Face(
        identifier="hb_floor",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(0, 10, 0), Point3D(0, 10, 10), Point3D(0, 0, 10)]),
    )
    hb_roof = Face(
        identifier="hb_roof",
        geometry=Face3D(boundary=[Point3D(10, 0, 0), Point3D(10, 10, 0), Point3D(10, 10, 10), Point3D(10, 0, 10)]),
    )
    hb_wall_north = Face(
        identifier="hb_wall_north",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(10, 0, 0), Point3D(10, 0, 10), Point3D(0, 0, 10)]),
    )
    hb_wall_south = Face(
        identifier="hb_wall_south",
        geometry=Face3D(boundary=[Point3D(0, 10, 0), Point3D(10, 10, 0), Point3D(10, 10, 10), Point3D(0, 10, 10)]),
    )
    hb_wall_east = Face(
        identifier="hb_wall_east",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(0, 10, 0), Point3D(0, 10, 10), Point3D(0, 0, 10)]),
    )
    hb_wall_west = Face(
        identifier="hb_wall_west",
        geometry=Face3D(boundary=[Point3D(10, 0, 0), Point3D(10, 10, 0), Point3D(10, 10, 10), Point3D(10, 0, 10)]),
    )
    hb_faces = [hb_floor, hb_roof, hb_wall_north, hb_wall_south, hb_wall_east, hb_wall_west]
    room_1 = Room(identifier="hb_room_1", faces=hb_faces)
    return Model(identifier="hb_model", rooms=[room_1])
