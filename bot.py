# SPDX-License-Identifier: BSD-3-Clause
from typing import Optional, Tuple

import numpy as np

from cholerama import helpers, Positions

AUTHOR = "YeastieBoys"  # This is your team name


class Bot:
    """
    This is the bot that will be instantiated for the competition.

    The pattern can be either a numpy array or a path to an image.
    """

    def __init__(
        self,
        number: int,
        name: str,
        patch_location: Tuple[int, int],
        patch_size: Tuple[int, int],
    ):
        self.number = number  # Mandatory: this is your number on the board
        self.name = name  # Mandatory: player name
        self.color = None  # Optional

        # empty_patches = helpers.find_empty_patches(board, self.puffer.shape)
        # npatches = len(empty_patches)
        # if npatches == 0:
        #     return None
        # ind = np.random.randint(0, npatches)

        self.puffer = helpers.image_to_array("puffer.png")
        self.cost = self.puffer.sum()

        gap = 50
        ks = [1, 0, 2]
        xx = [128 - gap, 128, 128 + gap, 128]
        yy = [128, 128 - gap, 128, 128 + gap]
        xpos = None
        ypos = None
        for k, ix, iy in zip(ks, xx, yy):
            a = np.rot90(self.puffer, k=k)
            y, x = np.where(a > 0)
            x += ix
            y += iy
            if xpos is None:
                xpos = x
                ypos = y
            else:
                xpos = np.concatenate((xpos, x))
                ypos = np.concatenate((ypos, y))
        self.pattern = Positions(x=xpos, y=ypos)

        # self.pattern = np.zeros(14 * 14, dtype=int)
        # cells = np.random.choice(len(self.pattern), 100, replace=False)
        # self.pattern[cells] = 1
        # self.pattern = self.pattern.reshape(14, 14)
        # # self.pattern = "filler.png"
        # # print(np.where(self.filler > 0))

    def iterate(
        self, iteration: int, board: np.ndarray, patch, tokens: int
    ) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        if tokens >= self.cost:
            # Pick a random empty patch of size 3x3
            empty_patches = helpers.find_empty_regions(patch, self.puffer.shape)
            npatches = len(empty_patches)
            if npatches == 0:
                return None
            ind = np.random.randint(0, npatches)

            k = np.random.randint(0, 4)
            a = np.rot90(self.puffer, k=k)

            y, x = np.where(a > 0)
            x += empty_patches[ind, 1]
            y += empty_patches[ind, 0]
            return Positions(x=x, y=y)
