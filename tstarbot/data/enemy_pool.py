from tstarbot.data.data_base import PoolBase

class EnemyPool(PoolBase):
    def __init__(self):
        super(PoolBase, self).__init__()

    def update(self, obs):
        # units = obs['units']
        pass