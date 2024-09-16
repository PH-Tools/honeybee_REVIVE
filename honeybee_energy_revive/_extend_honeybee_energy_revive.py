# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""This is called during __init__ and extends the base honeybee class Properties with a new ._revive slot"""

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
###### IMPORTANT ######
## ALL HONEYBEE-CORE / HONEYBEE-ENERGY CLASSES MUST BE IMPORTED **FIRST** BEFORE ANY OF THE
## HONEYBEE-REVIVE EXTENSIONS CAN BE LOADED. SEE ISSUE HERE:
## https://discourse.pollination.cloud/t/honeybee-ph-causing-error/


import honeybee_energy
from honeybee_energy.properties.extension import (
    ElectricEquipmentProperties,
    EnergyMaterialNoMassProperties,
    EnergyMaterialProperties,
    EnergyMaterialVegetationProperties,
    LightingProperties,
    OpaqueConstructionProperties,
    PeopleProperties,
    ServiceHotWaterProperties,
    WindowConstructionProperties,
    WindowConstructionShadeProperties,
)
from honeybee_energy.schedule.ruleset import ScheduleRulesetProperties

from honeybee_energy_revive.properties.construction.opaque import OpaqueConstructionReviveProperties
from honeybee_energy_revive.properties.construction.window import WindowConstructionReviveProperties
from honeybee_energy_revive.properties.construction.windowshade import ShadeConstructionReviveProperties
from honeybee_energy_revive.properties.hot_water.hw_program import ServiceHotWaterReviveProperties
from honeybee_energy_revive.properties.load.equipment import ElectricEquipmentReviveProperties
from honeybee_energy_revive.properties.load.lighting import LightingReviveProperties
from honeybee_energy_revive.properties.load.people import PeopleReviveProperties
from honeybee_energy_revive.properties.materials.opaque import (
    EnergyMaterialNoMassReviveProperties,
    EnergyMaterialReviveProperties,
    EnergyMaterialVegetationReviveProperties,
)
from honeybee_energy_revive.properties.ruleset import ScheduleRulesetReviveProperties

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# -- Now import the relevant HB-PH classes


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# Step 1)
# set a private ._revive attribute on each relevant HB-Energy Property class to None
setattr(ScheduleRulesetProperties, "_revive", None)
setattr(OpaqueConstructionProperties, "_revive", None)
setattr(EnergyMaterialProperties, "_revive", None)
setattr(EnergyMaterialNoMassProperties, "_revive", None)
setattr(EnergyMaterialVegetationProperties, "_revive", None)
setattr(WindowConstructionProperties, "_revive", None)
setattr(WindowConstructionShadeProperties, "_revive", None)
setattr(ServiceHotWaterProperties, "_revive", None)
setattr(ElectricEquipmentProperties, "_revive", None)
setattr(PeopleProperties, "_revive", None)
setattr(LightingProperties, "_revive", None)


# -----------------------------------------------------------------------------

# Step 2)
# create methods to define the public .property.<extension> @property instances on each obj.properties container


def schedule_ruleset_revive_properties(self):
    if self._revive is None:
        self._revive = ScheduleRulesetReviveProperties(self.host)
    return self._revive


def opaque_construction_revive_properties(self):
    if self._revive is None:
        self._revive = OpaqueConstructionReviveProperties(self.host)
    return self._revive


def energy_material_revive_properties(self):
    if self._revive is None:
        self._revive = EnergyMaterialReviveProperties(self.host)
    return self._revive


def energy_material_no_mass_revive_properties(self):
    if self._revive is None:
        self._revive = EnergyMaterialNoMassReviveProperties(self.host)
    return self._revive


def energy_material_vegetation_revive_properties(self):
    if self._revive is None:
        self._revive = EnergyMaterialVegetationReviveProperties(self.host)
    return self._revive


def window_construction_revive_properties(self):
    if self._revive is None:
        self._revive = WindowConstructionReviveProperties(self.host)
    return self._revive


def window_construction_shade_revive_properties(self):
    if self._revive is None:
        self._revive = ShadeConstructionReviveProperties(self.host)
    return self._revive


def hot_water_program_revive_properties(self):
    if self._revive is None:
        self._revive = ServiceHotWaterReviveProperties(self.host)
    return self._revive


def elec_equip_revive_properties(self):
    if self._revive is None:
        self._revive = ElectricEquipmentReviveProperties(self.host)
    return self._revive


def people_revive_properties(self):
    if self._revive is None:
        self._revive = PeopleReviveProperties(self.host)
    return self._revive


def lighting_revive_properties(self):
    if self._revive is None:
        self._revive = LightingReviveProperties(self.host)
    return self._revive


# -----------------------------------------------------------------------------

# Step 3)
# add public .revive @property methods to the appropriate Properties classes
setattr(ScheduleRulesetProperties, "revive", property(schedule_ruleset_revive_properties))
setattr(OpaqueConstructionProperties, "revive", property(opaque_construction_revive_properties))
setattr(WindowConstructionProperties, "revive", property(window_construction_revive_properties))
setattr(
    WindowConstructionShadeProperties,
    "revive",
    property(window_construction_shade_revive_properties),
)
setattr(EnergyMaterialProperties, "revive", property(energy_material_revive_properties))
setattr(EnergyMaterialNoMassProperties, "revive", property(energy_material_no_mass_revive_properties))
setattr(
    EnergyMaterialVegetationProperties,
    "revive",
    property(energy_material_vegetation_revive_properties),
)
setattr(ServiceHotWaterProperties, "revive", property(hot_water_program_revive_properties))
setattr(ElectricEquipmentProperties, "revive", property(elec_equip_revive_properties))
setattr(PeopleProperties, "revive", property(people_revive_properties))
setattr(LightingProperties, "revive", property(lighting_revive_properties))
