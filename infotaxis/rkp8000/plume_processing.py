"""
Code for creating plume objects.
"""
from infotaxis import get_hit_rate
import numpy as np
from config import xs, ys


class IdealPlume(object):
    def __init__(self, src_pos, w, d, r, a, tau, dt):
        self.src_pos = np.array(src_pos)
        self.w = w
        self.d = d
        self.r = r
        self.tau = tau
        self.a = a
        self.dt = dt

    def sample(self, pos, t):
        xs_src = np.array([self.src_pos[0]])
        ys_src = np.array([self.src_pos[1]])

        hit_rate = get_hit_rate(
            xs_src=xs_src, ys_src=ys_src, pos=pos,
            w=self.w, d=self.d, r=self.r, a=self.a, tau=self.tau)[0, 0]

        mean_hits = hit_rate * self.dt
        sample = int(np.random.poisson(mean_hits) > 0)
        return sample

    def get_profile(self, grid):
        xs_src = np.array([self.src_pos[0]])
        ys_src = np.array([self.src_pos[1]])

        conc = np.nan * np.zeros((len(xs), len(ys)))
        for x_ctr, x in enumerate(xs):
            for y_ctr, y in enumerate(ys):
                hit_rate = get_hit_rate(
                    xs_src=xs_src, ys_src=ys_src, pos=(x, y),
                    w=self.w, d=self.d, r=self.r, a=self.a, tau=self.tau)[0, 0]

                conc[x_ctr, y_ctr] = hit_rate

        dx = np.mean(np.diff(xs))
        dy = np.mean(np.diff(ys))

        x_lim = [xs[0] - dx/2, xs[-1] + dx/2]
        y_lim = [ys[0] - dy/2, ys[-1] + dy/2]

        extent = x_lim + y_lim

        return conc, extent