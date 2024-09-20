# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""This is called during __init__ and extends the base honeybee class Properties with a new ._revive slot"""

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
###### IMPORTANT ######
## ALL HONEYBEE-CORE / HONEYBEE-ENERGY CLASSES MUST BE IMPORTED **FIRST** BEFORE ANY OF THE
## HONEYBEE-REVIVE EXTENSIONS CAN BE LOADED. SEE ISSUE HERE:
## https://discourse.pollination.cloud/t/honeybee-ph-causing-error/
#

import honeybee_energy

# -- Import the Honeybee-Energy Constructions
from honeybee_energy.properties.extension import (
    OpaqueConstructionProperties,
    WindowConstructionProperties,
    WindowConstructionShadeProperties,
    ShadeConstructionProperties,
)

# -- Import the Honeybee-Energy Materials
from honeybee_energy.properties.extension import (
    EnergyMaterialNoMassProperties,
    EnergyMaterialProperties,
    EnergyMaterialVegetationProperties,
    EnergyWindowMaterialGlazingsProperties,
    EnergyWindowMaterialSimpleGlazSysProperties,
    EnergyWindowMaterialShadeProperties,
    EnergyWindowMaterialBlindProperties,
    EnergyWindowFrameProperties,
    EnergyWindowMaterialGasProperties,
    EnergyWindowMaterialGasCustomProperties,
    EnergyWindowMaterialGasMixtureProperties,
)

# -- Import the Honeybee-Energy Program Items
from honeybee_energy.properties.extension import (
    ElectricEquipmentProperties,
    LightingProperties,
    PeopleProperties,
    ServiceHotWaterProperties,
    ProcessProperties,
)
from honeybee_energy.schedule.ruleset import ScheduleRulesetProperties


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# -- Now that Honeybee-Energy is imported, import the relevant HB-REVIVE classes

# -- Constructions
from honeybee_energy_revive.properties.construction.opaque import OpaqueConstructionReviveProperties
from honeybee_energy_revive.properties.construction.window import WindowConstructionReviveProperties
from honeybee_energy_revive.properties.construction.windowshade import WindowConstructionShadeReviveProperties

# -- Materials
from honeybee_energy_revive.properties.materials.opaque import (
    EnergyMaterialNoMassReviveProperties,
    EnergyMaterialReviveProperties,
    EnergyMaterialVegetationReviveProperties,
)
from honeybee_energy_revive.properties.materials.glazing import (
    EnergyWindowMaterialGlazingReviveProperties,
    EnergyWindowMaterialSimpleGlazSysReviveProperties,
)
from honeybee_energy_revive.properties.materials.shade import (
    EnergyWindowMaterialShadeReviveProperties,
    EnergyWindowMaterialBlindReviveProperties,
)
from honeybee_energy_revive.properties.materials.frame import EnergyWindowFrameReviveProperties
from honeybee_energy_revive.properties.materials.gas import (
    EnergyWindowMaterialGasCustomReviveProperties,
    EnergyWindowMaterialGasReviveProperties,
    EnergyWindowMaterialGasMixtureReviveProperties,
)

# -- Program / Load
from honeybee_energy_revive.properties.ruleset import ScheduleRulesetReviveProperties
from honeybee_energy_revive.properties.hot_water.hw_program import ServiceHotWaterReviveProperties
from honeybee_energy_revive.properties.load.equipment import ElectricEquipmentReviveProperties
from honeybee_energy_revive.properties.load.lighting import LightingReviveProperties
from honeybee_energy_revive.properties.load.people import PeopleReviveProperties
from honeybee_energy_revive.properties.construction.shade import ShadeConstructionReviveProperties
from honeybee_energy_revive.properties.load.process import ProcessReviveProperties

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


# Step 1)
# set a private ._revive attribute on each relevant HB-Energy Property class to None

setattr(OpaqueConstructionProperties, "_revive", None)
setattr(WindowConstructionProperties, "_revive", None)
setattr(WindowConstructionShadeProperties, "_revive", None)
setattr(ShadeConstructionProperties, "_revive", None)

setattr(EnergyMaterialProperties, "_revive", None)
setattr(EnergyMaterialNoMassProperties, "_revive", None)
setattr(EnergyMaterialVegetationProperties, "_revive", None)

setattr(EnergyWindowMaterialGlazingsProperties, "_revive", None)
setattr(EnergyWindowMaterialSimpleGlazSysProperties, "_revive", None)
setattr(EnergyWindowMaterialShadeProperties, "_revive", None)
setattr(EnergyWindowMaterialBlindProperties, "_revive", None)
setattr(EnergyWindowFrameProperties, "_revive", None)
setattr(EnergyWindowMaterialGasProperties, "_revive", None)
setattr(EnergyWindowMaterialGasCustomProperties, "_revive", None)
setattr(EnergyWindowMaterialGasMixtureProperties, "_revive", None)

setattr(ScheduleRulesetProperties, "_revive", None)
setattr(ServiceHotWaterProperties, "_revive", None)
setattr(ElectricEquipmentProperties, "_revive", None)
setattr(PeopleProperties, "_revive", None)
setattr(LightingProperties, "_revive", None)
setattr(ProcessProperties, "_revive", None)


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


def energy_no_mass_revive_properties(self):
    if self._revive is None:
        self._revive = EnergyMaterialNoMassReviveProperties(self.host)
    return self._revive


def energy_vegetation_revive_properties(self):
    if self._revive is None:
        self._revive = EnergyMaterialVegetationReviveProperties(self.host)
    return self._revive


def energy_window_glazing_revive_properties(self):
    if self._revive is None:
        self._revive = EnergyWindowMaterialGlazingReviveProperties(self.host)
    return self._revive


def energy_window_simple_glazing_system_revive_properties(self):
    if self._revive is None:
        self._revive = EnergyWindowMaterialSimpleGlazSysReviveProperties(self.host)
    return self._revive


def material_window_shade_revive_properties(self):
    if self._revive is None:
        self._revive = EnergyWindowMaterialShadeReviveProperties(self.host)
    return self._revive


def material_window_blind_revive_properties(self):
    if self._revive is None:
        self._revive = EnergyWindowMaterialBlindReviveProperties(self.host)
    return self._revive


def window_construction_revive_properties(self):
    if self._revive is None:
        self._revive = WindowConstructionReviveProperties(self.host)
    return self._revive


def window_construction_shade_revive_shade(self):
    if self._revive is None:
        self._revive = WindowConstructionShadeReviveProperties(self.host)
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


def window_frame_properties(self):
    if self._revive is None:
        self._revive = EnergyWindowFrameReviveProperties(self.host)
    return self._revive


def material_gas_properties(self):
    if self._revive is None:
        self._revive = EnergyWindowMaterialGasReviveProperties(self.host)
    return self._revive


def material_gas_custom_properties(self):
    if self._revive is None:
        self._revive = EnergyWindowMaterialGasCustomReviveProperties(self.host)
    return self._revive


def material_gas_mixture_properties(self):
    if self._revive is None:
        self._revive = EnergyWindowMaterialGasMixtureReviveProperties(self.host)
    return self._revive


def shade_construction_revive_properties(self):
    if self._revive is None:
        self._revive = ShadeConstructionReviveProperties(self.host)
    return self._revive


def process_load_revive_properties(self):
    if self._revive is None:
        self._revive = ProcessReviveProperties(self.host)
    return self._revive


# -----------------------------------------------------------------------------

# Step 3)
# add public .revive @property methods to the appropriate Properties classes

# -- Constructions
setattr(OpaqueConstructionProperties, "revive", property(opaque_construction_revive_properties))
setattr(WindowConstructionProperties, "revive", property(window_construction_revive_properties))
setattr(WindowConstructionShadeProperties, "revive", property(window_construction_shade_revive_shade))
setattr(ShadeConstructionProperties, "revive", property(shade_construction_revive_properties))

# -- Regular Materials
setattr(EnergyMaterialProperties, "revive", property(energy_material_revive_properties))
setattr(EnergyMaterialNoMassProperties, "revive", property(energy_no_mass_revive_properties))
setattr(EnergyMaterialVegetationProperties, "revive", property(energy_vegetation_revive_properties))
setattr(EnergyWindowMaterialGlazingsProperties, "revive", property(energy_window_glazing_revive_properties))
setattr(
    EnergyWindowMaterialSimpleGlazSysProperties,
    "revive",
    property(energy_window_simple_glazing_system_revive_properties),
)

# -- Window Materials
setattr(EnergyWindowFrameProperties, "revive", property(window_frame_properties))
setattr(EnergyWindowMaterialGasProperties, "revive", property(material_gas_properties))
setattr(EnergyWindowMaterialGasCustomProperties, "revive", property(material_gas_custom_properties))
setattr(EnergyWindowMaterialGasMixtureProperties, "revive", property(material_gas_mixture_properties))
setattr(EnergyWindowMaterialShadeProperties, "revive", property(material_window_shade_revive_properties))
setattr(EnergyWindowMaterialBlindProperties, "revive", property(material_window_blind_revive_properties))

# -- Program
setattr(ServiceHotWaterProperties, "revive", property(hot_water_program_revive_properties))
setattr(ElectricEquipmentProperties, "revive", property(elec_equip_revive_properties))
setattr(PeopleProperties, "revive", property(people_revive_properties))
setattr(LightingProperties, "revive", property(lighting_revive_properties))
setattr(ScheduleRulesetProperties, "revive", property(schedule_ruleset_revive_properties))
setattr(ProcessProperties, "revive", property(process_load_revive_properties))
