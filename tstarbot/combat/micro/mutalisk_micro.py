from pysc2.lib.typeenums import UNIT_TYPEID, ABILITY_ID, UPGRADE_ID
from s2clientprotocol import sc2api_pb2 as sc_pb
from tstarbot.combat.micro.micro_base import MicroBase
from tstarbot.data.queue.combat_command_queue import CombatCmdType
from tstarbot.data.pool.macro_def import COMBAT_ANTI_AIR_UNITS

import numpy as np


class MutaliskMgr(MicroBase):
    """ A zvz Zerg combat manager """
    def __init__(self):
        super(MutaliskMgr, self).__init__()
        self.safe_harass_dist = 20
        self.safe_positions = [
            {'x': 20, 'y': 5},
            {'x': 20, 'y': 140},
            {'x': 180, 'y': 140},
            {'x': 180, 'y': 5},

            {'x': 20, 'y': 75},
            {'x': 100, 'y': 140},
            {'x': 180, 'y': 75},
            {'x': 100, 'y': 5}
        ]

    def act(self, u, pos, mode):
        action = []
        if mode == CombatCmdType.MOVE:
            action = self.move_pos(u, pos)
        elif mode == CombatCmdType.ATTACK:
            closest_combat_enemy_dist = 100000
            enemy_anti_air_units = [e for e in self.enemy_units
                                    if e.int_attr.unit_type in COMBAT_ANTI_AIR_UNITS]
            if len(enemy_anti_air_units) > 0:
                closest_combat_enemy = self.find_closest_enemy(u, enemy_anti_air_units)
                closest_combat_enemy_dist = self.cal_square_dist(u, closest_combat_enemy)
            if closest_combat_enemy_dist < self.safe_harass_dist:
                pos_id = np.argmin([self.cal_coor_dist({'x': u.float_attr.pos_x,
                                                        'y': u.float_attr.pos_y},
                                                       pos) for pos in self.safe_positions])
                action = self.move_pos(u, self.safe_positions[pos_id])
            else:
                action = self.attack_pos(u, pos)
        return action