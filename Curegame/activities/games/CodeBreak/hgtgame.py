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

import hgt
import hgt.game

from hgt.event import Event
from hgt.gameelements import Sound
from hgt.gamemath import DEG2RAD
from hgt.gameutils import Enum, StateManager
from hgt.listeners import MFBoolListener
from hgt.locale import translate as _
from hgt.nodes import X3DFileNode, hgn
from hgt.widgets.grabber import Grabber

import math
import random
import space # space.py generated by Blender exporter

from H3DUtils import *

SPACE_TILT = 65.0
BASE_SHELF_SCORE = 1000
###########################################################################
# CodeBreak Game (Replaces MugMasterMind).
###########################################################################

class Game(hgt.game.Game):
    def build(self):
        random.seed()

        cfg = self.load_config()
        self.level = cfg.settings["codebreak_level"]

        if self.level == 1:
            self.number_of_colors = 3
        elif self.level == 2:
            self.number_of_colors = 4
        elif self.level == 3:
            self.number_of_colors = 5

        self.mug_reenable_time = 1.0
        self.plate_reenable_time = 0.5

        # Blender model variables
        self.number_of_base_plates = 6
        self.number_of_shelves = 8
        self.mugs_per_shelf = 3

        # hgt world
        hgt.world.stereoInfo.focalDistance = 0.55
        hgt.world.tilt(-SPACE_TILT)
        hgt.world.load_stylus('ball')

        # Load Blender scene
        self.add_child(space.world)

        # Grabber
        self.grabber = Grabber()
        self.grabber.correct_tilt(tilt=SPACE_TILT)

        # Build
        self.build_sounds()
        self.build_world()

        # States
        self.states = Enum('beginning', 'not_lifting', 'lifting', 'ending')
        self.state = StateManager(self.states, self.states.beginning)
        self.state.add(self.states.beginning, self.states.not_lifting)
        self.state.add(self.states.not_lifting, self.states.lifting)
        self.state.add(self.states.lifting, self.states.not_lifting)
        self.state.add(self.states.not_lifting, self.states.ending)

    # Initialization
    def start(self):
        self.start_time = hgt.time.now
        self.reset()

    def reset(self):
        self.state.change(self.states.not_lifting)
        self.last_plate_touched = None
        #self.score = 0

        space.nodes["Text_LevelLabel"].string = [_('LEVEL')]
        #space.nodes["Text_ScoreLabel"].string = [_('SCORE')]
        space.nodes["Text_Level"].string = [[_('Easy'), _('Medium'), _('Hard')][self.level - 1]]

        #print "level", self.level
        #print "number_of_colors:", self.number_of_colors

        self.combination = []
        for i in range(self.mugs_per_shelf):
            self.combination.append(random.randint(0, self.number_of_colors - 1))

        #print "Correct combination:", self.combination

    # Ending
    def end_game(self):
        hgt.time.add_timeout(4.0, self.end_game2)
        self.cheer_sound.play()

    def end_game2(self):
        self.log_score(
            level = self.level,
            duration = hgt.time.now - self.start_time,
            win = True,
        )
        self.quit()

    # Updates
    def update(self):
        self.grabber.update()

    # Interactivity
    def touch_mug(self, evt):
        # Bumping into other mugs
        if self.state == self.states.lifting:
            self.mugmug_sound.play()

        # Touching a mug on a plate
        elif self.state == self.states.not_lifting:
            mug_info = evt.mug_info
            if not mug_info["finished"]:
                #print "\n", mug_info

                self.state.change(self.states.lifting)

                plate_info = mug_info["plate_info"]
                plate_info["occupied"] = False
                plate_info["mug_info"] = None

                self.last_plate_lifted = plate_info # Cleared by timeout
                self.last_plate_used = plate_info

                mug_info["plate_info"] = None

                self.grabber.grab(mug_info['grabObject'])
                space.nodes["ToggleGroup_HapticBlocker"].hapticsOn = True
                self.force_field.force = Vec3f(0, 0, -1.0)
                self.mug_sound.play()

                self.current_mug_info = mug_info

                hgt.time.add_timeout(self.plate_reenable_time, self.reenable_last_plate, (plate_info,))

    def touch_plate(self, evt):
        if self.state == self.states.lifting:
            plate_info = evt.plate_info
            #print "\n", plate_info
            if not plate_info["finished"]:
                if self.last_plate_lifted != plate_info and not plate_info['occupied']:
                    plate_info["occupied"] = True

                    self.state.change(self.states.not_lifting)

                    self.force_field.force = Vec3f(0, 0, 0)

                    mug_info = self.current_mug_info
                    self.grabber.release()
                    space.nodes["ToggleGroup_HapticBlocker"].hapticsOn = False
                    mug_info["transform"].translation = plate_info['transform'].translation
                    mug_info["plate_info"] = plate_info
                    plate_info["mug_info"] = mug_info
                    self.current_mug_info = None

                    hgt.time.add_timeout(self.mug_reenable_time, self.reenable_mug, (mug_info,))

                    self.plate_sound.play()

                    # Add a new cup to base plates
                    if not plate_info["base_plate"] and self.last_plate_used["base_plate"]:
                        occupied_plates = sum([p["occupied"] for p in self.base_plates])
                        #print "Occupied:", occupied_plates
                        if occupied_plates < self.number_of_base_plates - 1:
                            color_index = self.find_least_common_color()
                            #self.add_mug(plate_info=self.last_plate_used, color_index=mug_info["color_index"])
                            self.add_mug(plate_info=self.last_plate_used, color_index=color_index)

                    if not plate_info["base_plate"]:
                        self.check_shelf(plate_info["shelf_index"])

    def find_least_common_color(self):
        colors = []
        for i in range(self.number_of_colors):
            colors.append(0)
        for pi in self.base_plates:
            if pi["occupied"]:
                #pass
                colors[pi["mug_info"]["color_index"]] += 1
        #print colors
        #print smallest_index
        smallest_index = colors.index(min(colors))
        return smallest_index

    def check_shelf(self, shelf_index):
        shelf = self.shelves[shelf_index]
        shelf_done = all(plate["occupied"] for plate in shelf)
        if shelf_done:
            self.occupied_shelves += 1
            combination = []
            for plate in shelf:
                plate["finished"] = True
                plate["mug_info"]["finished"] = True
                combination.append(plate["mug_info"]["color_index"])

            if combination == self.combination:
                self.state.change(self.states.ending)

                self.ping_sound.play()

                # cutnpaste
                for i in range(self.mugs_per_shelf):
                    ball_index = shelf_index * self.mugs_per_shelf + i
                    space.nodes["ToggleGroup_Ball.%03d" % ball_index].graphicsOn = True
                    space.nodes["Appearance_Ball.%03d" % ball_index].material = self.white_material.h3dNode

                hgt.time.add_timeout(2.0, self.end_game)

            else:
                white_beads = 0
                black_beads = 0
                tmp_combination = self.combination[:]

                for i in range(self.mugs_per_shelf):
                    if combination[i] == self.combination[i]:
                        white_beads += 1

                    if combination[i] in tmp_combination:
                        black_beads += 1
                        tmp_combination.remove(combination[i])

                self.shelf_scores[shelf_index] = white_beads + black_beads

                balls_to_show = white_beads
                if black_beads > white_beads:
                    balls_to_show += black_beads - white_beads

                """
                print
                print "Combination:", self.combination
                print "Guess:", combination
                print "White beads", white_beads
                print "Black beads", black_beads
                print "Balls to show", balls_to_show
                print
                """

                if balls_to_show > 0:
                    self.ping_sound.play()

                for i in range(balls_to_show):
                    ball_index = shelf_index * self.mugs_per_shelf + i
                    space.nodes["ToggleGroup_Ball.%03d" % ball_index].graphicsOn = True
                    if i < white_beads:
                        space.nodes["Appearance_Ball.%03d" % ball_index].material = self.white_material.h3dNode
                    else:
                        space.nodes["Appearance_Ball.%03d" % ball_index].material = self.black_material.h3dNode

                self.clear_worst_shelf(avoid_shelf_index = shelf_index)

    def clear_worst_shelf(self, avoid_shelf_index):
        worst_shelf_index = 0
        worst_shelf_score = BASE_SHELF_SCORE
        for i in range(self.number_of_shelves):
            if i == avoid_shelf_index:
                continue
            if self.shelf_scores[i] < worst_shelf_score:
                worst_shelf_score = self.shelf_scores[i]
                worst_shelf_index = i

        """
        print "Occupied shelves", self.occupied_shelves
        print "Avoid index", avoid_shelf_index
        print "Worst shelf score", worst_shelf_score
        print "Worst shelf index", worst_shelf_index
        """

        if self.occupied_shelves == self.number_of_shelves:
            #print "Clearing worst shelf"
            shelf = self.shelves[worst_shelf_index]
            for plate in shelf:
                plate["occupied"] = False
                plate["finished"] = False
                plate["mug_info"]["toggle"].graphicsOn = False
                plate["mug_info"]["toggle"].hapticsOn = False

            for i in range(self.mugs_per_shelf):
                ball_index = worst_shelf_index * self.mugs_per_shelf + i
                space.nodes["ToggleGroup_Ball.%03d" % ball_index].graphicsOn = False

            self.shelf_scores[worst_shelf_index] = BASE_SHELF_SCORE
            self.occupied_shelves -= 1

    def reenable_mug(self, mug_info):
        #print "\nReenabling", mug_info
        mug_info["toggle"].hapticsOn = True

    # FIXME: Need to check logic, still possible to place two mugs on the same plate!
    def reenable_last_plate(self, plate_info):
        if self.last_plate_lifted == plate_info:
            self.last_plate_lifted = None

    # Build
    def build_world(self):
        space.nodes["ToggleGroup_HapticBlocker"].graphicsOn = False
        space.nodes["ToggleGroup_HapticBlocker"].hapticsOn = False

        self.white_material = space.nodes["Material_WhiteMaterial"]
        self.black_material = space.nodes["Material_BlackMaterial"]

        self.force_field = hgn.ForceField()
        self.add_child(self.force_field)

        self.base_plates = []
        self.shelves = []
        self.shelf_scores = []
        self.occupied_shelves = 0
        for i in range(self.number_of_shelves):
            self.shelves.append([])
            self.shelf_scores.append(BASE_SHELF_SCORE)
            for j in range(self.mugs_per_shelf):
                foo = i * self.mugs_per_shelf + j
                space.nodes["ToggleGroup_Ball.%03d" % foo].graphicsOn = False

        # Plates
        for i in range(self.number_of_base_plates + self.number_of_shelves * self.mugs_per_shelf):
            transform = space.nodes["Transform_Plate.%03d" % i]

            is_base_plate = i < self.number_of_base_plates
            shelf_index = None
            if not is_base_plate:
                shelf_index = (i - self.number_of_base_plates) / self.mugs_per_shelf

            plate_info = {
                'transform': transform,
                'occupied': False,
                'mug_info': None,
                'base_plate': is_base_plate,
                'shelf_index': shelf_index,
                'finished': False,
            }

            if is_base_plate:
                self.base_plates.append(plate_info)
            else:
                self.shelves[shelf_index].append(plate_info)

            evt = Event()
            evt.plate_info = plate_info
            bl = MFBoolListener(
                onTrue=self.touch_plate,
                callbackObject=evt,
            )
            space.nodes["Mesh_Plate.%03d" % i].h3dNode.isTouched.routeNoEvent(bl)

            if i < self.number_of_base_plates - 1:
                self.add_mug(plate_info=plate_info, color_index = i % self.number_of_colors)

    def add_mug(self, plate_info, color_index):
        assert(plate_info["base_plate"])
        assert(not plate_info["occupied"])
        #print "Adding color mug", color_index

        plate_info["occupied"] = True

        mug = X3DFileNode("mug.hgt")
        self.add_child(mug)

        mug.find("ToggleGroup_HapticMug").graphicsOn = False

        toggle = mug.find("ToggleGroup_MugEmpty")

        transform = mug.find("Transform_MugEmpty")
        transform.translation = plate_info['transform'].translation

        appearance = mug.find("Appearance_MugModel")
        appearance.material = space.nodes["Material_Mug%d" % color_index].h3dNode

        mesh = mug.find("Mesh_HapticMug")

        grabObject = self.grabber.register(
            transform=transform,
            toggle=toggle,
        )

        mug_info = {
            'color_index': color_index,
            'transform': transform,
            'appearance': appearance,
            'grabObject': grabObject,
            'toggle': toggle,
            'plate_info': plate_info,
            'finished': False,
        }
        evt = Event()
        evt.mug_info = mug_info
        bl = MFBoolListener(
            onTrue=self.touch_mug,
            callbackObject=evt,
        )
        mesh.h3dNode.isTouched.routeNoEvent(bl)

        plate_info["mug_info"] = mug_info

    def build_sounds(self):
        self.mug_sound = Sound("sounds/glass1.wav", copies=2, intensity=0.4)
        self.mugmug_sound = Sound("sounds/glass3.wav", copies=2, intensity=0.4)
        self.plate_sound = Sound("sounds/glass2.wav", copies=2, intensity=0.4)
        self.knock_sound = Sound("sounds/knock.wav", copies=5, intensity=0.4)
        self.ping_sound = Sound("sounds/ping.wav", copies=2, intensity=0.4)
        self.cheer_sound = Sound("sounds/cheer.wav", copies=1, intensity=0.5)
