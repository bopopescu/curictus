##############################################################################
#
# Copyright (c) 2006-2011 Curictus AB.
#
# This file part of Curictus VRS.
#
# Curictus VRS is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Curictus VRS is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Curictus VRS; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA 02111-1307 USA
#
##############################################################################

# This is an auto-generated file. Do not edit manually.
import hgt
from hgt.blenderhelpers import get_world_and_nodes
hgt_filename = 'space.hgt'

hgt_object_names = {}
hgt_object_names['B3.001'] = None
hgt_object_names['BetButton'] = None
hgt_object_names['BetButtonLabel'] = None
hgt_object_names['Bevel'] = None
hgt_object_names['Bevel.001'] = None
hgt_object_names['Bevel.002'] = None
hgt_object_names['Bevel.003'] = None
hgt_object_names['Bevel.004'] = None
hgt_object_names['Bevel.005'] = None
hgt_object_names['CoinSlot'] = None
hgt_object_names['CoinsBet'] = None
hgt_object_names['Coinstack'] = None
hgt_object_names['Credits'] = None
hgt_object_names['Curtain'] = None
hgt_object_names['Cylinder'] = None
hgt_object_names['Cylinder.001'] = None
hgt_object_names['Cylinder.002'] = None
hgt_object_names['Cylinder.013'] = None
hgt_object_names['Cylinder0'] = None
hgt_object_names['Cylinder1'] = None
hgt_object_names['Cylinder2'] = None
hgt_object_names['Empty'] = None
hgt_object_names['ExitButton'] = None
hgt_object_names['ExitButtonLabel'] = None
hgt_object_names['ExitButtonShape'] = None
hgt_object_names['HoldButton.000'] = None
hgt_object_names['HoldButton.001'] = None
hgt_object_names['HoldButton.002'] = None
hgt_object_names['HoldButtonLabel.000'] = None
hgt_object_names['HoldButtonLabel.001'] = None
hgt_object_names['HoldButtonLabel.002'] = None
hgt_object_names['HoldButtonShape.000'] = None
hgt_object_names['HoldButtonShape.001'] = None
hgt_object_names['HoldButtonShape.002'] = None
hgt_object_names['HoldButtonShape.003'] = None
hgt_object_names['HoldButtonShape.004'] = None
hgt_object_names['Pay'] = None
hgt_object_names['Plane'] = None
hgt_object_names['Plane.001'] = None
hgt_object_names['Plane.002'] = None
hgt_object_names['Plane.003'] = None
hgt_object_names['Plane.004'] = None
hgt_object_names['Point'] = None
hgt_object_names['SpinButton'] = None
hgt_object_names['SpinButtonLabel'] = None
hgt_object_names['TopCoin'] = None

hgt_objects = {}
hgt_objects['Appearance_B3.001'] = None
hgt_objects['Appearance_BetButtonLabel'] = None
hgt_objects['Appearance_Bevel'] = None
hgt_objects['Appearance_Bevel.001'] = None
hgt_objects['Appearance_Bevel.002'] = None
hgt_objects['Appearance_Bevel.003'] = None
hgt_objects['Appearance_Bevel.004'] = None
hgt_objects['Appearance_Bevel.005'] = None
hgt_objects['Appearance_CoinSlot'] = None
hgt_objects['Appearance_CoinsBet'] = None
hgt_objects['Appearance_Coinstack'] = None
hgt_objects['Appearance_Credits'] = None
hgt_objects['Appearance_Curtain'] = None
hgt_objects['Appearance_Cylinder'] = None
hgt_objects['Appearance_Cylinder.001'] = None
hgt_objects['Appearance_Cylinder.002'] = None
hgt_objects['Appearance_Cylinder.013'] = None
hgt_objects['Appearance_ExitButtonLabel'] = None
hgt_objects['Appearance_ExitButtonShape'] = None
hgt_objects['Appearance_HoldButtonLabel.000'] = None
hgt_objects['Appearance_HoldButtonLabel.001'] = None
hgt_objects['Appearance_HoldButtonLabel.002'] = None
hgt_objects['Appearance_HoldButtonShape.000'] = None
hgt_objects['Appearance_HoldButtonShape.001'] = None
hgt_objects['Appearance_HoldButtonShape.002'] = None
hgt_objects['Appearance_HoldButtonShape.003'] = None
hgt_objects['Appearance_HoldButtonShape.004'] = None
hgt_objects['Appearance_Pay'] = None
hgt_objects['Appearance_Plane'] = None
hgt_objects['Appearance_Plane.001'] = None
hgt_objects['Appearance_Plane.002'] = None
hgt_objects['Appearance_Plane.003'] = None
hgt_objects['Appearance_Plane.004'] = None
hgt_objects['Appearance_SpinButtonLabel'] = None
hgt_objects['Appearance_TopCoin'] = None
hgt_objects['Coord_B3.000'] = None
hgt_objects['Coord_B3.001'] = None
hgt_objects['Coord_B3.002'] = None
hgt_objects['Coord_B3.003'] = None
hgt_objects['Coord_B3.004'] = None
hgt_objects['Coord_B3.006'] = None
hgt_objects['Coord_B3.007'] = None
hgt_objects['Coord_BetButton'] = None
hgt_objects['Coord_CoinSlot'] = None
hgt_objects['Coord_Coinstack'] = None
hgt_objects['Coord_Cylinder'] = None
hgt_objects['Coord_Cylinder.001'] = None
hgt_objects['Coord_Cylinder.002'] = None
hgt_objects['Coord_Cylinder.003'] = None
hgt_objects['Coord_ExitButton'] = None
hgt_objects['Coord_HoldButton.000'] = None
hgt_objects['Coord_HoldButton.001'] = None
hgt_objects['Coord_HoldButton.002'] = None
hgt_objects['Coord_Mesh.147'] = None
hgt_objects['Coord_Plane'] = None
hgt_objects['Coord_Plane.001'] = None
hgt_objects['Coord_Plane.002'] = None
hgt_objects['Coord_Plane.003'] = None
hgt_objects['Coord_Plane.004'] = None
hgt_objects['Coord_SpinButton'] = None
hgt_objects['Coord_TopCoin'] = None
hgt_objects['DynamicTransform_Cylinder0'] = None
hgt_objects['DynamicTransform_Cylinder1'] = None
hgt_objects['DynamicTransform_Cylinder2'] = None
hgt_objects['ImageTexture_ReelTexture'] = None
hgt_objects['ImageTexture_slot_machine_plate.pn'] = None
hgt_objects['Material_BetButton'] = None
hgt_objects['Material_BlockerPlane'] = None
hgt_objects['Material_ButtonText'] = None
hgt_objects['Material_CoinSlot'] = None
hgt_objects['Material_Curtain'] = None
hgt_objects['Material_CylinderMaterial'] = None
hgt_objects['Material_ExitButton'] = None
hgt_objects['Material_GlassThing'] = None
hgt_objects['Material_HoldButton.000'] = None
hgt_objects['Material_HoldButton.001'] = None
hgt_objects['Material_HoldButton.002'] = None
hgt_objects['Material_Instructions'] = None
hgt_objects['Material_LedText'] = None
hgt_objects['Material_SlotMachineMaterial'] = None
hgt_objects['Material_SlotMachineMetal'] = None
hgt_objects['Material_SlotMachineMetal.001'] = None
hgt_objects['Material_SpinButton'] = None
hgt_objects['Material_TopCoin'] = None
hgt_objects['Mesh_B3.000'] = None
hgt_objects['Mesh_B3.001'] = None
hgt_objects['Mesh_B3.002'] = None
hgt_objects['Mesh_B3.003'] = None
hgt_objects['Mesh_B3.004'] = None
hgt_objects['Mesh_B3.006'] = None
hgt_objects['Mesh_B3.007'] = None
hgt_objects['Mesh_BetButton'] = None
hgt_objects['Mesh_CoinSlot'] = None
hgt_objects['Mesh_Coinstack'] = None
hgt_objects['Mesh_Cylinder'] = None
hgt_objects['Mesh_Cylinder.001'] = None
hgt_objects['Mesh_Cylinder.002'] = None
hgt_objects['Mesh_Cylinder.003'] = None
hgt_objects['Mesh_ExitButton'] = None
hgt_objects['Mesh_HoldButton.000'] = None
hgt_objects['Mesh_HoldButton.001'] = None
hgt_objects['Mesh_HoldButton.002'] = None
hgt_objects['Mesh_Mesh.147'] = None
hgt_objects['Mesh_Plane'] = None
hgt_objects['Mesh_Plane.001'] = None
hgt_objects['Mesh_Plane.002'] = None
hgt_objects['Mesh_Plane.003'] = None
hgt_objects['Mesh_Plane.004'] = None
hgt_objects['Mesh_SpinButton'] = None
hgt_objects['Mesh_TopCoin'] = None
hgt_objects['PointLight_Point'] = None
hgt_objects['Text_BetButtonLabel'] = None
hgt_objects['Text_CoinsBet'] = None
hgt_objects['Text_Credits'] = None
hgt_objects['Text_ExitButtonLabel'] = None
hgt_objects['Text_HoldButtonLabel.000'] = None
hgt_objects['Text_HoldButtonLabel.001'] = None
hgt_objects['Text_HoldButtonLabel.002'] = None
hgt_objects['Text_Pay'] = None
hgt_objects['Text_SpinButtonLabel'] = None
hgt_objects['ToggleGroup_B3.001'] = None
hgt_objects['ToggleGroup_BetButton'] = None
hgt_objects['ToggleGroup_BetButtonLabel'] = None
hgt_objects['ToggleGroup_Bevel'] = None
hgt_objects['ToggleGroup_Bevel.001'] = None
hgt_objects['ToggleGroup_Bevel.002'] = None
hgt_objects['ToggleGroup_Bevel.003'] = None
hgt_objects['ToggleGroup_Bevel.004'] = None
hgt_objects['ToggleGroup_Bevel.005'] = None
hgt_objects['ToggleGroup_CoinSlot'] = None
hgt_objects['ToggleGroup_CoinsBet'] = None
hgt_objects['ToggleGroup_Coinstack'] = None
hgt_objects['ToggleGroup_Credits'] = None
hgt_objects['ToggleGroup_Curtain'] = None
hgt_objects['ToggleGroup_Cylinder'] = None
hgt_objects['ToggleGroup_Cylinder.001'] = None
hgt_objects['ToggleGroup_Cylinder.002'] = None
hgt_objects['ToggleGroup_Cylinder.013'] = None
hgt_objects['ToggleGroup_Cylinder0'] = None
hgt_objects['ToggleGroup_Cylinder1'] = None
hgt_objects['ToggleGroup_Cylinder2'] = None
hgt_objects['ToggleGroup_Empty'] = None
hgt_objects['ToggleGroup_ExitButton'] = None
hgt_objects['ToggleGroup_ExitButtonLabel'] = None
hgt_objects['ToggleGroup_ExitButtonShape'] = None
hgt_objects['ToggleGroup_HoldButton.000'] = None
hgt_objects['ToggleGroup_HoldButton.001'] = None
hgt_objects['ToggleGroup_HoldButton.002'] = None
hgt_objects['ToggleGroup_HoldButtonLabel.000'] = None
hgt_objects['ToggleGroup_HoldButtonLabel.001'] = None
hgt_objects['ToggleGroup_HoldButtonLabel.002'] = None
hgt_objects['ToggleGroup_HoldButtonShape.000'] = None
hgt_objects['ToggleGroup_HoldButtonShape.001'] = None
hgt_objects['ToggleGroup_HoldButtonShape.002'] = None
hgt_objects['ToggleGroup_HoldButtonShape.003'] = None
hgt_objects['ToggleGroup_HoldButtonShape.004'] = None
hgt_objects['ToggleGroup_Pay'] = None
hgt_objects['ToggleGroup_Plane'] = None
hgt_objects['ToggleGroup_Plane.001'] = None
hgt_objects['ToggleGroup_Plane.002'] = None
hgt_objects['ToggleGroup_Plane.003'] = None
hgt_objects['ToggleGroup_Plane.004'] = None
hgt_objects['ToggleGroup_SpinButton'] = None
hgt_objects['ToggleGroup_SpinButtonLabel'] = None
hgt_objects['ToggleGroup_TopCoin'] = None
hgt_objects['TransformInfo_B3.001'] = None
hgt_objects['TransformInfo_BetButton'] = None
hgt_objects['TransformInfo_BetButtonLabel'] = None
hgt_objects['TransformInfo_Bevel'] = None
hgt_objects['TransformInfo_Bevel.001'] = None
hgt_objects['TransformInfo_Bevel.002'] = None
hgt_objects['TransformInfo_Bevel.003'] = None
hgt_objects['TransformInfo_Bevel.004'] = None
hgt_objects['TransformInfo_Bevel.005'] = None
hgt_objects['TransformInfo_CoinSlot'] = None
hgt_objects['TransformInfo_CoinsBet'] = None
hgt_objects['TransformInfo_Coinstack'] = None
hgt_objects['TransformInfo_Credits'] = None
hgt_objects['TransformInfo_Curtain'] = None
hgt_objects['TransformInfo_Cylinder'] = None
hgt_objects['TransformInfo_Cylinder.001'] = None
hgt_objects['TransformInfo_Cylinder.002'] = None
hgt_objects['TransformInfo_Cylinder.013'] = None
hgt_objects['TransformInfo_Cylinder0'] = None
hgt_objects['TransformInfo_Cylinder1'] = None
hgt_objects['TransformInfo_Cylinder2'] = None
hgt_objects['TransformInfo_Empty'] = None
hgt_objects['TransformInfo_ExitButton'] = None
hgt_objects['TransformInfo_ExitButtonLabel'] = None
hgt_objects['TransformInfo_ExitButtonShape'] = None
hgt_objects['TransformInfo_HoldButton.000'] = None
hgt_objects['TransformInfo_HoldButton.001'] = None
hgt_objects['TransformInfo_HoldButton.002'] = None
hgt_objects['TransformInfo_HoldButtonLabel.000'] = None
hgt_objects['TransformInfo_HoldButtonLabel.001'] = None
hgt_objects['TransformInfo_HoldButtonLabel.002'] = None
hgt_objects['TransformInfo_HoldButtonShape.000'] = None
hgt_objects['TransformInfo_HoldButtonShape.001'] = None
hgt_objects['TransformInfo_HoldButtonShape.002'] = None
hgt_objects['TransformInfo_HoldButtonShape.003'] = None
hgt_objects['TransformInfo_HoldButtonShape.004'] = None
hgt_objects['TransformInfo_Pay'] = None
hgt_objects['TransformInfo_Plane'] = None
hgt_objects['TransformInfo_Plane.001'] = None
hgt_objects['TransformInfo_Plane.002'] = None
hgt_objects['TransformInfo_Plane.003'] = None
hgt_objects['TransformInfo_Plane.004'] = None
hgt_objects['TransformInfo_SpinButton'] = None
hgt_objects['TransformInfo_SpinButtonLabel'] = None
hgt_objects['TransformInfo_TopCoin'] = None
hgt_objects['Transform_B3.001'] = None
hgt_objects['Transform_BetButton'] = None
hgt_objects['Transform_BetButtonLabel'] = None
hgt_objects['Transform_Bevel'] = None
hgt_objects['Transform_Bevel.001'] = None
hgt_objects['Transform_Bevel.002'] = None
hgt_objects['Transform_Bevel.003'] = None
hgt_objects['Transform_Bevel.004'] = None
hgt_objects['Transform_Bevel.005'] = None
hgt_objects['Transform_CoinSlot'] = None
hgt_objects['Transform_CoinsBet'] = None
hgt_objects['Transform_Coinstack'] = None
hgt_objects['Transform_Credits'] = None
hgt_objects['Transform_Curtain'] = None
hgt_objects['Transform_Cylinder'] = None
hgt_objects['Transform_Cylinder.001'] = None
hgt_objects['Transform_Cylinder.002'] = None
hgt_objects['Transform_Cylinder.013'] = None
hgt_objects['Transform_Cylinder0'] = None
hgt_objects['Transform_Cylinder1'] = None
hgt_objects['Transform_Cylinder2'] = None
hgt_objects['Transform_Empty'] = None
hgt_objects['Transform_ExitButton'] = None
hgt_objects['Transform_ExitButtonLabel'] = None
hgt_objects['Transform_ExitButtonShape'] = None
hgt_objects['Transform_HoldButton.000'] = None
hgt_objects['Transform_HoldButton.001'] = None
hgt_objects['Transform_HoldButton.002'] = None
hgt_objects['Transform_HoldButtonLabel.000'] = None
hgt_objects['Transform_HoldButtonLabel.001'] = None
hgt_objects['Transform_HoldButtonLabel.002'] = None
hgt_objects['Transform_HoldButtonShape.000'] = None
hgt_objects['Transform_HoldButtonShape.001'] = None
hgt_objects['Transform_HoldButtonShape.002'] = None
hgt_objects['Transform_HoldButtonShape.003'] = None
hgt_objects['Transform_HoldButtonShape.004'] = None
hgt_objects['Transform_Pay'] = None
hgt_objects['Transform_Plane'] = None
hgt_objects['Transform_Plane.001'] = None
hgt_objects['Transform_Plane.002'] = None
hgt_objects['Transform_Plane.003'] = None
hgt_objects['Transform_Plane.004'] = None
hgt_objects['Transform_SpinButton'] = None
hgt_objects['Transform_SpinButtonLabel'] = None
hgt_objects['Transform_TopCoin'] = None
(world, nodes) = get_world_and_nodes(hgt_filename, hgt_objects)
