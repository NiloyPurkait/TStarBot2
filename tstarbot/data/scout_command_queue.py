from tstarbot.data.data_base import CommandQueueBase

class ScoutCommandQueue(CommandQueueBase):
    def __init__(self):
        super(CommandQueueBase, self).__init__()

    def update(self, obs):
        # units = obs['units']
        pass

