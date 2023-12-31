import math

from utils import get_signal_snippet, draw_ECG, Distr, HtmlLogger, make_arrows


import matplotlib.pyplot as plt
import statistics


class AlphaUniformDistr:
    def __init__(self):
        self.a = -90
        self.b = 90

    def get_p_of_event(self, a1, b1):
        all = abs(self.b-self.a)
        event = abs(b1 - a1)
        p = event/all
        return p


def get_alpha_from_k(k):
    tg = k
    angle_radians = math.atan(tg)
    graduses = angle_radians * 180/math.pi
    return graduses


class Region:
    def __init__(self, vals):
        self.vals = vals

    def get_mean_k(self):
        ks = self._get_ks()
        k_mean = statistics.mean(ks)
        return k_mean

    def get_mean_alpha(self):
        alphas = self._get_alphas()
        return statistics.mean(alphas)

    def _get_alphas(self):
        alphas = []
        ks = self._get_ks()
        for k in ks:
            alpha = get_alpha_from_k(k)
            alphas.append(alpha)
        return alphas

    def _get_ks(self):
        ks = []
        for i in range(len(self.vals) - 1):
            v = self.vals[i]
            v_next = self.vals[i + 1]
            k = v_next - v
            ks.append(k)
        return ks



class SceneNoInertia:
    def __init__(self, neg_end, predicted_k):
        self.full_signal = get_signal_snippet(lead_name='i', start_coord=340, end_coord=435)
        self.pos_start = 11
        self.pos_end = 43
        self.neg_start = 44
        self.neg_end = neg_end

        self.region_pos = Region()
        self.region_neg = Region
        self.region_full = Region

        self.predicted_k = predicted_k

    def compare_predicted_to_best(self):
        pass

    def get_best(self):
        pass

    def eval_best_profit(self):
        pass

    def get_r(self):
        pass

    def draw(self, log):
        pass



def ex(log, neg_end):
    scene = SceneNoInertia(predicted_k=0, neg_end=neg_end)
    scene.draw(log)

    r_list = []
    predicted_k_list = list(range(-15, 15, 4))
    for predicted_k in predicted_k_list:
        scene.predicted_k = predicted_k
        r = scene.get_r()
        r_list.append(r)

    index = r_list.index(max(r_list))
    y_best = predicted_k_list[index]

    fig, ax = plt.subplots()
    ax.plot(predicted_k_list, r_list, 'o-', label='r(dy)')
    ax.grid(which='major', axis='both', linestyle='--', alpha=0.75)
    make_arrows(ax)
    ax.vlines(x=y_best, ymin=0, ymax=max(r_list), colors="green", lw=2, alpha=0.5,
              label='r({}) ={:.2f}'.format(y_best, max(r_list)))
    ax.legend()
    log.add_fig(fig)


if __name__ == '__main__':
    log = HtmlLogger("SQUARE_BASED")
    ex(log, neg_end=90)
    ex(log, neg_end=50)
