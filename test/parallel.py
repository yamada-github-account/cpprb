import time
import random
import unittest
import multiprocessing

import numpy as np
import gym
from cpprb import ReplayBuffer, PrioritizedReplayBuffer

@unittest.skipIf(multiprocessing.cpu_count() < 2,
                 "Requires multiple cpu")
class TestPerallelExplore(unittest.TestCase):
    def test_explore(self):

        env_func = lambda : gym.make("FrozenLake-v0")
        policy = lambda o: np.random.randint(0,4,size=o.shape)
        post = lambda args: {"next_obs": args[0],
                             "rew": args[1],
                             "done": args[2]}
        buffer_size = 256

        rb = ReplayBuffer(buffer_size,
                          {"obs": {"dtype": np.int},
                           "act": {"dtype": np.int},
                           "next_obs": {"dtype": np.int},
                           "rew": {},
                           "done": {}},
                          enable_shared = True)

        self.assertEqual(rb.terminate(),False)
        self.assertEqual(rb.get_next_index(),0)
        self.assertEqual(rb.get_stored_size(),0)
        self.assertEqual(rb.explore(env_func,policy,post,
                                    n_env = 16,
                                    n_parallel = 8),True)
        print(f"start waiting: {rb.get_stored_size()}")
        while not rb.get_stored_size():
            pass
        print(f"finish waiting: {rb.get_stored_size()}")
        s = rb.sample(64)
        time.sleep(20)
        self.assertNotEqual(rb.get_stored_size(),0)

        s = rb.sample(128)
        self.assertEqual(rb.terminate(),0)

if __name__ == "__main__":
    unittest.main()
