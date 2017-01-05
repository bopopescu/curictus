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
hgt_object_names['Ball.000'] = None
hgt_object_names['Ball.001'] = None
hgt_object_names['Ball.002'] = None
hgt_object_names['Ball.003'] = None
hgt_object_names['Ball.004'] = None
hgt_object_names['Ball.005'] = None
hgt_object_names['Ball.006'] = None
hgt_object_names['Ball.007'] = None
hgt_object_names['Ball.008'] = None
hgt_object_names['Ball.009'] = None
hgt_object_names['Ball.010'] = None
hgt_object_names['Ball.011'] = None
hgt_object_names['Ball.012'] = None
hgt_object_names['Ball.013'] = None
hgt_object_names['Ball.014'] = None
hgt_object_names['Ball.015'] = None
hgt_object_names['Ball.016'] = None
hgt_object_names['Ball.017'] = None
hgt_object_names['Ball.018'] = None
hgt_object_names['Ball.019'] = None
hgt_object_names['Ball.020'] = None
hgt_object_names['Ball.021'] = None
hgt_object_names['Ball.022'] = None
hgt_object_names['Ball.023'] = None
hgt_object_names['Blocker.000'] = None
hgt_object_names['Blocker.001'] = None
hgt_object_names['Blocker.002'] = None
hgt_object_names['Blocker.003'] = None
hgt_object_names['Blocker.004'] = None
hgt_object_names['Cube.000'] = None
hgt_object_names['Cube.001'] = None
hgt_object_names['Cube.002'] = None
hgt_object_names['Cube.003'] = None
hgt_object_names['Cube.004'] = None
hgt_object_names['Cube.005'] = None
hgt_object_names['Cube.006'] = None
hgt_object_names['Cube.007'] = None
hgt_object_names['Diskbank'] = None
hgt_object_names['DiskbankLowerPart'] = None
hgt_object_names['HapticBlocker'] = None
hgt_object_names['Level'] = None
hgt_object_names['LevelLabel'] = None
hgt_object_names['Plane.000'] = None
hgt_object_names['Plane.001'] = None
hgt_object_names['Plane.002'] = None
hgt_object_names['Plane.003'] = None
hgt_object_names['Plane.004'] = None
hgt_object_names['Plane.005'] = None
hgt_object_names['Plane.020'] = None
hgt_object_names['Plane.021'] = None
hgt_object_names['Plane.022'] = None
hgt_object_names['Plate.000'] = None
hgt_object_names['Plate.001'] = None
hgt_object_names['Plate.002'] = None
hgt_object_names['Plate.003'] = None
hgt_object_names['Plate.004'] = None
hgt_object_names['Plate.005'] = None
hgt_object_names['Plate.006'] = None
hgt_object_names['Plate.007'] = None
hgt_object_names['Plate.008'] = None
hgt_object_names['Plate.009'] = None
hgt_object_names['Plate.010'] = None
hgt_object_names['Plate.011'] = None
hgt_object_names['Plate.012'] = None
hgt_object_names['Plate.013'] = None
hgt_object_names['Plate.014'] = None
hgt_object_names['Plate.015'] = None
hgt_object_names['Plate.016'] = None
hgt_object_names['Plate.017'] = None
hgt_object_names['Plate.018'] = None
hgt_object_names['Plate.019'] = None
hgt_object_names['Plate.020'] = None
hgt_object_names['Plate.021'] = None
hgt_object_names['Plate.022'] = None
hgt_object_names['Plate.023'] = None
hgt_object_names['Plate.024'] = None
hgt_object_names['Plate.025'] = None
hgt_object_names['Plate.026'] = None
hgt_object_names['Plate.027'] = None
hgt_object_names['Plate.028'] = None
hgt_object_names['Plate.029'] = None
hgt_object_names['Point'] = None
hgt_object_names['Point.001'] = None
hgt_object_names['Score'] = None
hgt_object_names['ScoreLabel'] = None
hgt_object_names['Wall'] = None

hgt_objects = {}
hgt_objects['Appearance_Ball.000'] = None
hgt_objects['Appearance_Ball.001'] = None
hgt_objects['Appearance_Ball.002'] = None
hgt_objects['Appearance_Ball.003'] = None
hgt_objects['Appearance_Ball.004'] = None
hgt_objects['Appearance_Ball.005'] = None
hgt_objects['Appearance_Ball.006'] = None
hgt_objects['Appearance_Ball.007'] = None
hgt_objects['Appearance_Ball.008'] = None
hgt_objects['Appearance_Ball.009'] = None
hgt_objects['Appearance_Ball.010'] = None
hgt_objects['Appearance_Ball.011'] = None
hgt_objects['Appearance_Ball.012'] = None
hgt_objects['Appearance_Ball.013'] = None
hgt_objects['Appearance_Ball.014'] = None
hgt_objects['Appearance_Ball.015'] = None
hgt_objects['Appearance_Ball.016'] = None
hgt_objects['Appearance_Ball.017'] = None
hgt_objects['Appearance_Ball.018'] = None
hgt_objects['Appearance_Ball.019'] = None
hgt_objects['Appearance_Ball.020'] = None
hgt_objects['Appearance_Ball.021'] = None
hgt_objects['Appearance_Ball.022'] = None
hgt_objects['Appearance_Ball.023'] = None
hgt_objects['Appearance_Blocker.000'] = None
hgt_objects['Appearance_Blocker.001'] = None
hgt_objects['Appearance_Blocker.002'] = None
hgt_objects['Appearance_Blocker.003'] = None
hgt_objects['Appearance_Blocker.004'] = None
hgt_objects['Appearance_Cube.000'] = None
hgt_objects['Appearance_Cube.001'] = None
hgt_objects['Appearance_Cube.002'] = None
hgt_objects['Appearance_Cube.003'] = None
hgt_objects['Appearance_Cube.004'] = None
hgt_objects['Appearance_Cube.005'] = None
hgt_objects['Appearance_Cube.006'] = None
hgt_objects['Appearance_Cube.007'] = None
hgt_objects['Appearance_Diskbank'] = None
hgt_objects['Appearance_DiskbankLowerPart'] = None
hgt_objects['Appearance_Level'] = None
hgt_objects['Appearance_LevelLabel'] = None
hgt_objects['Appearance_Plane.000'] = None
hgt_objects['Appearance_Plane.001'] = None
hgt_objects['Appearance_Plane.002'] = None
hgt_objects['Appearance_Plane.003'] = None
hgt_objects['Appearance_Plane.004'] = None
hgt_objects['Appearance_Plane.005'] = None
hgt_objects['Appearance_Plane.020'] = None
hgt_objects['Appearance_Plane.021'] = None
hgt_objects['Appearance_Plane.022'] = None
hgt_objects['Appearance_Plate.000'] = None
hgt_objects['Appearance_Plate.001'] = None
hgt_objects['Appearance_Plate.002'] = None
hgt_objects['Appearance_Plate.003'] = None
hgt_objects['Appearance_Plate.004'] = None
hgt_objects['Appearance_Plate.005'] = None
hgt_objects['Appearance_Plate.006'] = None
hgt_objects['Appearance_Plate.007'] = None
hgt_objects['Appearance_Plate.008'] = None
hgt_objects['Appearance_Plate.009'] = None
hgt_objects['Appearance_Plate.010'] = None
hgt_objects['Appearance_Plate.011'] = None
hgt_objects['Appearance_Plate.012'] = None
hgt_objects['Appearance_Plate.013'] = None
hgt_objects['Appearance_Plate.014'] = None
hgt_objects['Appearance_Plate.015'] = None
hgt_objects['Appearance_Plate.016'] = None
hgt_objects['Appearance_Plate.017'] = None
hgt_objects['Appearance_Plate.018'] = None
hgt_objects['Appearance_Plate.019'] = None
hgt_objects['Appearance_Plate.020'] = None
hgt_objects['Appearance_Plate.021'] = None
hgt_objects['Appearance_Plate.022'] = None
hgt_objects['Appearance_Plate.023'] = None
hgt_objects['Appearance_Plate.024'] = None
hgt_objects['Appearance_Plate.025'] = None
hgt_objects['Appearance_Plate.026'] = None
hgt_objects['Appearance_Plate.027'] = None
hgt_objects['Appearance_Plate.028'] = None
hgt_objects['Appearance_Plate.029'] = None
hgt_objects['Appearance_Score'] = None
hgt_objects['Appearance_ScoreLabel'] = None
hgt_objects['Appearance_Wall'] = None
hgt_objects['Coord_Ball.000'] = None
hgt_objects['Coord_Cube'] = None
hgt_objects['Coord_Cube.001'] = None
hgt_objects['Coord_Cube.002'] = None
hgt_objects['Coord_Cube.003'] = None
hgt_objects['Coord_Cube.004'] = None
hgt_objects['Coord_Cube.005'] = None
hgt_objects['Coord_Cube.006'] = None
hgt_objects['Coord_Cube.007'] = None
hgt_objects['Coord_Cube.008'] = None
hgt_objects['Coord_Cube.009'] = None
hgt_objects['Coord_Cube.010'] = None
hgt_objects['Coord_Cube.011'] = None
hgt_objects['Coord_Cube.012'] = None
hgt_objects['Coord_Cube.013'] = None
hgt_objects['Coord_Diskbank'] = None
hgt_objects['Coord_Plane'] = None
hgt_objects['Coord_Plane.001'] = None
hgt_objects['Coord_Plane.002'] = None
hgt_objects['Coord_Plane.003'] = None
hgt_objects['Coord_Plane.005'] = None
hgt_objects['Coord_Plane.006'] = None
hgt_objects['Coord_Plane.021'] = None
hgt_objects['Coord_Plane.022'] = None
hgt_objects['Coord_Plane.023'] = None
hgt_objects['Coord_Plate.000'] = None
hgt_objects['Coord_Plate.001'] = None
hgt_objects['Coord_Plate.002'] = None
hgt_objects['Coord_Plate.003'] = None
hgt_objects['Coord_Plate.004'] = None
hgt_objects['Coord_Plate.005'] = None
hgt_objects['Coord_Plate.006'] = None
hgt_objects['Coord_Plate.007'] = None
hgt_objects['Coord_Plate.008'] = None
hgt_objects['Coord_Plate.009'] = None
hgt_objects['Coord_Plate.010'] = None
hgt_objects['Coord_Plate.011'] = None
hgt_objects['Coord_Plate.012'] = None
hgt_objects['Coord_Plate.013'] = None
hgt_objects['Coord_Plate.014'] = None
hgt_objects['Coord_Plate.015'] = None
hgt_objects['Coord_Plate.016'] = None
hgt_objects['Coord_Plate.017'] = None
hgt_objects['Coord_Plate.018'] = None
hgt_objects['Coord_Plate.019'] = None
hgt_objects['Coord_Plate.020'] = None
hgt_objects['Coord_Plate.021'] = None
hgt_objects['Coord_Plate.022'] = None
hgt_objects['Coord_Plate.023'] = None
hgt_objects['Coord_Plate.024'] = None
hgt_objects['Coord_Plate.025'] = None
hgt_objects['Coord_Plate.026'] = None
hgt_objects['Coord_Plate.027'] = None
hgt_objects['Coord_Plate.028'] = None
hgt_objects['Coord_Plate.029'] = None
hgt_objects['Coord_Wall'] = None
hgt_objects['ImageTexture_wallpaper.jpg'] = None
hgt_objects['ImageTexture_wood.jpg'] = None
hgt_objects['Material_Ball.000'] = None
hgt_objects['Material_BlackMaterial'] = None
hgt_objects['Material_Diskbank'] = None
hgt_objects['Material_DiskbankLowerPart'] = None
hgt_objects['Material_Invisible'] = None
hgt_objects['Material_Label'] = None
hgt_objects['Material_Mug0'] = None
hgt_objects['Material_Mug1'] = None
hgt_objects['Material_Mug2'] = None
hgt_objects['Material_Mug3'] = None
hgt_objects['Material_Mug4'] = None
hgt_objects['Material_Mug5'] = None
hgt_objects['Material_Room'] = None
hgt_objects['Material_ScoreBoard'] = None
hgt_objects['Material_Shelf'] = None
hgt_objects['Material_WhiteCeramic'] = None
hgt_objects['Material_WhiteMaterial'] = None
hgt_objects['Mesh_Ball.000'] = None
hgt_objects['Mesh_Cube'] = None
hgt_objects['Mesh_Cube.001'] = None
hgt_objects['Mesh_Cube.002'] = None
hgt_objects['Mesh_Cube.003'] = None
hgt_objects['Mesh_Cube.004'] = None
hgt_objects['Mesh_Cube.005'] = None
hgt_objects['Mesh_Cube.006'] = None
hgt_objects['Mesh_Cube.007'] = None
hgt_objects['Mesh_Cube.008'] = None
hgt_objects['Mesh_Cube.009'] = None
hgt_objects['Mesh_Cube.010'] = None
hgt_objects['Mesh_Cube.011'] = None
hgt_objects['Mesh_Cube.012'] = None
hgt_objects['Mesh_Cube.013'] = None
hgt_objects['Mesh_Diskbank'] = None
hgt_objects['Mesh_Plane'] = None
hgt_objects['Mesh_Plane.001'] = None
hgt_objects['Mesh_Plane.002'] = None
hgt_objects['Mesh_Plane.003'] = None
hgt_objects['Mesh_Plane.005'] = None
hgt_objects['Mesh_Plane.006'] = None
hgt_objects['Mesh_Plane.021'] = None
hgt_objects['Mesh_Plane.022'] = None
hgt_objects['Mesh_Plane.023'] = None
hgt_objects['Mesh_Plate.000'] = None
hgt_objects['Mesh_Plate.001'] = None
hgt_objects['Mesh_Plate.002'] = None
hgt_objects['Mesh_Plate.003'] = None
hgt_objects['Mesh_Plate.004'] = None
hgt_objects['Mesh_Plate.005'] = None
hgt_objects['Mesh_Plate.006'] = None
hgt_objects['Mesh_Plate.007'] = None
hgt_objects['Mesh_Plate.008'] = None
hgt_objects['Mesh_Plate.009'] = None
hgt_objects['Mesh_Plate.010'] = None
hgt_objects['Mesh_Plate.011'] = None
hgt_objects['Mesh_Plate.012'] = None
hgt_objects['Mesh_Plate.013'] = None
hgt_objects['Mesh_Plate.014'] = None
hgt_objects['Mesh_Plate.015'] = None
hgt_objects['Mesh_Plate.016'] = None
hgt_objects['Mesh_Plate.017'] = None
hgt_objects['Mesh_Plate.018'] = None
hgt_objects['Mesh_Plate.019'] = None
hgt_objects['Mesh_Plate.020'] = None
hgt_objects['Mesh_Plate.021'] = None
hgt_objects['Mesh_Plate.022'] = None
hgt_objects['Mesh_Plate.023'] = None
hgt_objects['Mesh_Plate.024'] = None
hgt_objects['Mesh_Plate.025'] = None
hgt_objects['Mesh_Plate.026'] = None
hgt_objects['Mesh_Plate.027'] = None
hgt_objects['Mesh_Plate.028'] = None
hgt_objects['Mesh_Plate.029'] = None
hgt_objects['Mesh_Wall'] = None
hgt_objects['PointLight_Point'] = None
hgt_objects['PointLight_Point.001'] = None
hgt_objects['Text_Level'] = None
hgt_objects['Text_LevelLabel'] = None
hgt_objects['Text_Score'] = None
hgt_objects['Text_ScoreLabel'] = None
hgt_objects['ToggleGroup_Ball.000'] = None
hgt_objects['ToggleGroup_Ball.001'] = None
hgt_objects['ToggleGroup_Ball.002'] = None
hgt_objects['ToggleGroup_Ball.003'] = None
hgt_objects['ToggleGroup_Ball.004'] = None
hgt_objects['ToggleGroup_Ball.005'] = None
hgt_objects['ToggleGroup_Ball.006'] = None
hgt_objects['ToggleGroup_Ball.007'] = None
hgt_objects['ToggleGroup_Ball.008'] = None
hgt_objects['ToggleGroup_Ball.009'] = None
hgt_objects['ToggleGroup_Ball.010'] = None
hgt_objects['ToggleGroup_Ball.011'] = None
hgt_objects['ToggleGroup_Ball.012'] = None
hgt_objects['ToggleGroup_Ball.013'] = None
hgt_objects['ToggleGroup_Ball.014'] = None
hgt_objects['ToggleGroup_Ball.015'] = None
hgt_objects['ToggleGroup_Ball.016'] = None
hgt_objects['ToggleGroup_Ball.017'] = None
hgt_objects['ToggleGroup_Ball.018'] = None
hgt_objects['ToggleGroup_Ball.019'] = None
hgt_objects['ToggleGroup_Ball.020'] = None
hgt_objects['ToggleGroup_Ball.021'] = None
hgt_objects['ToggleGroup_Ball.022'] = None
hgt_objects['ToggleGroup_Ball.023'] = None
hgt_objects['ToggleGroup_Blocker.000'] = None
hgt_objects['ToggleGroup_Blocker.001'] = None
hgt_objects['ToggleGroup_Blocker.002'] = None
hgt_objects['ToggleGroup_Blocker.003'] = None
hgt_objects['ToggleGroup_Blocker.004'] = None
hgt_objects['ToggleGroup_Cube.000'] = None
hgt_objects['ToggleGroup_Cube.001'] = None
hgt_objects['ToggleGroup_Cube.002'] = None
hgt_objects['ToggleGroup_Cube.003'] = None
hgt_objects['ToggleGroup_Cube.004'] = None
hgt_objects['ToggleGroup_Cube.005'] = None
hgt_objects['ToggleGroup_Cube.006'] = None
hgt_objects['ToggleGroup_Cube.007'] = None
hgt_objects['ToggleGroup_Diskbank'] = None
hgt_objects['ToggleGroup_DiskbankLowerPart'] = None
hgt_objects['ToggleGroup_HapticBlocker'] = None
hgt_objects['ToggleGroup_Level'] = None
hgt_objects['ToggleGroup_LevelLabel'] = None
hgt_objects['ToggleGroup_Plane.000'] = None
hgt_objects['ToggleGroup_Plane.001'] = None
hgt_objects['ToggleGroup_Plane.002'] = None
hgt_objects['ToggleGroup_Plane.003'] = None
hgt_objects['ToggleGroup_Plane.004'] = None
hgt_objects['ToggleGroup_Plane.005'] = None
hgt_objects['ToggleGroup_Plane.020'] = None
hgt_objects['ToggleGroup_Plane.021'] = None
hgt_objects['ToggleGroup_Plane.022'] = None
hgt_objects['ToggleGroup_Plate.000'] = None
hgt_objects['ToggleGroup_Plate.001'] = None
hgt_objects['ToggleGroup_Plate.002'] = None
hgt_objects['ToggleGroup_Plate.003'] = None
hgt_objects['ToggleGroup_Plate.004'] = None
hgt_objects['ToggleGroup_Plate.005'] = None
hgt_objects['ToggleGroup_Plate.006'] = None
hgt_objects['ToggleGroup_Plate.007'] = None
hgt_objects['ToggleGroup_Plate.008'] = None
hgt_objects['ToggleGroup_Plate.009'] = None
hgt_objects['ToggleGroup_Plate.010'] = None
hgt_objects['ToggleGroup_Plate.011'] = None
hgt_objects['ToggleGroup_Plate.012'] = None
hgt_objects['ToggleGroup_Plate.013'] = None
hgt_objects['ToggleGroup_Plate.014'] = None
hgt_objects['ToggleGroup_Plate.015'] = None
hgt_objects['ToggleGroup_Plate.016'] = None
hgt_objects['ToggleGroup_Plate.017'] = None
hgt_objects['ToggleGroup_Plate.018'] = None
hgt_objects['ToggleGroup_Plate.019'] = None
hgt_objects['ToggleGroup_Plate.020'] = None
hgt_objects['ToggleGroup_Plate.021'] = None
hgt_objects['ToggleGroup_Plate.022'] = None
hgt_objects['ToggleGroup_Plate.023'] = None
hgt_objects['ToggleGroup_Plate.024'] = None
hgt_objects['ToggleGroup_Plate.025'] = None
hgt_objects['ToggleGroup_Plate.026'] = None
hgt_objects['ToggleGroup_Plate.027'] = None
hgt_objects['ToggleGroup_Plate.028'] = None
hgt_objects['ToggleGroup_Plate.029'] = None
hgt_objects['ToggleGroup_Score'] = None
hgt_objects['ToggleGroup_ScoreLabel'] = None
hgt_objects['ToggleGroup_Wall'] = None
hgt_objects['TransformInfo_Ball.000'] = None
hgt_objects['TransformInfo_Ball.001'] = None
hgt_objects['TransformInfo_Ball.002'] = None
hgt_objects['TransformInfo_Ball.003'] = None
hgt_objects['TransformInfo_Ball.004'] = None
hgt_objects['TransformInfo_Ball.005'] = None
hgt_objects['TransformInfo_Ball.006'] = None
hgt_objects['TransformInfo_Ball.007'] = None
hgt_objects['TransformInfo_Ball.008'] = None
hgt_objects['TransformInfo_Ball.009'] = None
hgt_objects['TransformInfo_Ball.010'] = None
hgt_objects['TransformInfo_Ball.011'] = None
hgt_objects['TransformInfo_Ball.012'] = None
hgt_objects['TransformInfo_Ball.013'] = None
hgt_objects['TransformInfo_Ball.014'] = None
hgt_objects['TransformInfo_Ball.015'] = None
hgt_objects['TransformInfo_Ball.016'] = None
hgt_objects['TransformInfo_Ball.017'] = None
hgt_objects['TransformInfo_Ball.018'] = None
hgt_objects['TransformInfo_Ball.019'] = None
hgt_objects['TransformInfo_Ball.020'] = None
hgt_objects['TransformInfo_Ball.021'] = None
hgt_objects['TransformInfo_Ball.022'] = None
hgt_objects['TransformInfo_Ball.023'] = None
hgt_objects['TransformInfo_Blocker.000'] = None
hgt_objects['TransformInfo_Blocker.001'] = None
hgt_objects['TransformInfo_Blocker.002'] = None
hgt_objects['TransformInfo_Blocker.003'] = None
hgt_objects['TransformInfo_Blocker.004'] = None
hgt_objects['TransformInfo_Cube.000'] = None
hgt_objects['TransformInfo_Cube.001'] = None
hgt_objects['TransformInfo_Cube.002'] = None
hgt_objects['TransformInfo_Cube.003'] = None
hgt_objects['TransformInfo_Cube.004'] = None
hgt_objects['TransformInfo_Cube.005'] = None
hgt_objects['TransformInfo_Cube.006'] = None
hgt_objects['TransformInfo_Cube.007'] = None
hgt_objects['TransformInfo_Diskbank'] = None
hgt_objects['TransformInfo_DiskbankLowerPart'] = None
hgt_objects['TransformInfo_HapticBlocker'] = None
hgt_objects['TransformInfo_Level'] = None
hgt_objects['TransformInfo_LevelLabel'] = None
hgt_objects['TransformInfo_Plane.000'] = None
hgt_objects['TransformInfo_Plane.001'] = None
hgt_objects['TransformInfo_Plane.002'] = None
hgt_objects['TransformInfo_Plane.003'] = None
hgt_objects['TransformInfo_Plane.004'] = None
hgt_objects['TransformInfo_Plane.005'] = None
hgt_objects['TransformInfo_Plane.020'] = None
hgt_objects['TransformInfo_Plane.021'] = None
hgt_objects['TransformInfo_Plane.022'] = None
hgt_objects['TransformInfo_Plate.000'] = None
hgt_objects['TransformInfo_Plate.001'] = None
hgt_objects['TransformInfo_Plate.002'] = None
hgt_objects['TransformInfo_Plate.003'] = None
hgt_objects['TransformInfo_Plate.004'] = None
hgt_objects['TransformInfo_Plate.005'] = None
hgt_objects['TransformInfo_Plate.006'] = None
hgt_objects['TransformInfo_Plate.007'] = None
hgt_objects['TransformInfo_Plate.008'] = None
hgt_objects['TransformInfo_Plate.009'] = None
hgt_objects['TransformInfo_Plate.010'] = None
hgt_objects['TransformInfo_Plate.011'] = None
hgt_objects['TransformInfo_Plate.012'] = None
hgt_objects['TransformInfo_Plate.013'] = None
hgt_objects['TransformInfo_Plate.014'] = None
hgt_objects['TransformInfo_Plate.015'] = None
hgt_objects['TransformInfo_Plate.016'] = None
hgt_objects['TransformInfo_Plate.017'] = None
hgt_objects['TransformInfo_Plate.018'] = None
hgt_objects['TransformInfo_Plate.019'] = None
hgt_objects['TransformInfo_Plate.020'] = None
hgt_objects['TransformInfo_Plate.021'] = None
hgt_objects['TransformInfo_Plate.022'] = None
hgt_objects['TransformInfo_Plate.023'] = None
hgt_objects['TransformInfo_Plate.024'] = None
hgt_objects['TransformInfo_Plate.025'] = None
hgt_objects['TransformInfo_Plate.026'] = None
hgt_objects['TransformInfo_Plate.027'] = None
hgt_objects['TransformInfo_Plate.028'] = None
hgt_objects['TransformInfo_Plate.029'] = None
hgt_objects['TransformInfo_Score'] = None
hgt_objects['TransformInfo_ScoreLabel'] = None
hgt_objects['TransformInfo_Wall'] = None
hgt_objects['Transform_Ball.000'] = None
hgt_objects['Transform_Ball.001'] = None
hgt_objects['Transform_Ball.002'] = None
hgt_objects['Transform_Ball.003'] = None
hgt_objects['Transform_Ball.004'] = None
hgt_objects['Transform_Ball.005'] = None
hgt_objects['Transform_Ball.006'] = None
hgt_objects['Transform_Ball.007'] = None
hgt_objects['Transform_Ball.008'] = None
hgt_objects['Transform_Ball.009'] = None
hgt_objects['Transform_Ball.010'] = None
hgt_objects['Transform_Ball.011'] = None
hgt_objects['Transform_Ball.012'] = None
hgt_objects['Transform_Ball.013'] = None
hgt_objects['Transform_Ball.014'] = None
hgt_objects['Transform_Ball.015'] = None
hgt_objects['Transform_Ball.016'] = None
hgt_objects['Transform_Ball.017'] = None
hgt_objects['Transform_Ball.018'] = None
hgt_objects['Transform_Ball.019'] = None
hgt_objects['Transform_Ball.020'] = None
hgt_objects['Transform_Ball.021'] = None
hgt_objects['Transform_Ball.022'] = None
hgt_objects['Transform_Ball.023'] = None
hgt_objects['Transform_Blocker.000'] = None
hgt_objects['Transform_Blocker.001'] = None
hgt_objects['Transform_Blocker.002'] = None
hgt_objects['Transform_Blocker.003'] = None
hgt_objects['Transform_Blocker.004'] = None
hgt_objects['Transform_Cube.000'] = None
hgt_objects['Transform_Cube.001'] = None
hgt_objects['Transform_Cube.002'] = None
hgt_objects['Transform_Cube.003'] = None
hgt_objects['Transform_Cube.004'] = None
hgt_objects['Transform_Cube.005'] = None
hgt_objects['Transform_Cube.006'] = None
hgt_objects['Transform_Cube.007'] = None
hgt_objects['Transform_Diskbank'] = None
hgt_objects['Transform_DiskbankLowerPart'] = None
hgt_objects['Transform_HapticBlocker'] = None
hgt_objects['Transform_Level'] = None
hgt_objects['Transform_LevelLabel'] = None
hgt_objects['Transform_Plane.000'] = None
hgt_objects['Transform_Plane.001'] = None
hgt_objects['Transform_Plane.002'] = None
hgt_objects['Transform_Plane.003'] = None
hgt_objects['Transform_Plane.004'] = None
hgt_objects['Transform_Plane.005'] = None
hgt_objects['Transform_Plane.020'] = None
hgt_objects['Transform_Plane.021'] = None
hgt_objects['Transform_Plane.022'] = None
hgt_objects['Transform_Plate.000'] = None
hgt_objects['Transform_Plate.001'] = None
hgt_objects['Transform_Plate.002'] = None
hgt_objects['Transform_Plate.003'] = None
hgt_objects['Transform_Plate.004'] = None
hgt_objects['Transform_Plate.005'] = None
hgt_objects['Transform_Plate.006'] = None
hgt_objects['Transform_Plate.007'] = None
hgt_objects['Transform_Plate.008'] = None
hgt_objects['Transform_Plate.009'] = None
hgt_objects['Transform_Plate.010'] = None
hgt_objects['Transform_Plate.011'] = None
hgt_objects['Transform_Plate.012'] = None
hgt_objects['Transform_Plate.013'] = None
hgt_objects['Transform_Plate.014'] = None
hgt_objects['Transform_Plate.015'] = None
hgt_objects['Transform_Plate.016'] = None
hgt_objects['Transform_Plate.017'] = None
hgt_objects['Transform_Plate.018'] = None
hgt_objects['Transform_Plate.019'] = None
hgt_objects['Transform_Plate.020'] = None
hgt_objects['Transform_Plate.021'] = None
hgt_objects['Transform_Plate.022'] = None
hgt_objects['Transform_Plate.023'] = None
hgt_objects['Transform_Plate.024'] = None
hgt_objects['Transform_Plate.025'] = None
hgt_objects['Transform_Plate.026'] = None
hgt_objects['Transform_Plate.027'] = None
hgt_objects['Transform_Plate.028'] = None
hgt_objects['Transform_Plate.029'] = None
hgt_objects['Transform_Score'] = None
hgt_objects['Transform_ScoreLabel'] = None
hgt_objects['Transform_Wall'] = None
(world, nodes) = get_world_and_nodes(hgt_filename, hgt_objects)
