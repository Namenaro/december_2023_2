from utils import get_signal_snippet, draw_ECG, Distr, HtmlLogger

import matplotlib.pyplot as plt

class SceneNoInertia:
    def __init__(self, dy_law):
        self.full_signal = get_signal_snippet(lead_name='i', start_coord=340, end_coord=435)
        self.pos_start = 11
        self.pos_end = 43
        self.neg_start = 44
        self.neg_end = len(self.full_signal) -1

        self.dy_law = dy_law

    def get_pos_vs(self):
        vs = list([self.full_signal[i] for i in range(self.pos_start, self.pos_end+1 )])
        return vs

    def get_neg_vs(self):
        vs = list([self.full_signal[i] for i in range(self.neg_start, self.neg_end+1)])
        return vs

    def get_full_vs(self):
        vs = list([self.full_signal[i] for i in range(self.pos_start, self.neg_end + 1)])
        return vs

    def draw_v_hists(self, log):
        fig, ax = plt.subplots()
        pos = self.get_pos_vs()
        negs = self.get_neg_vs()
        ax.hist(pos, label="v+", color='green', alpha=0.5)
        ax.hist(negs, label="v-", color='red', alpha=0.5)
        ax.hist(negs+pos, color='gray', alpha=0.3)
        ax.legend()
        log.add_fig(fig)

    def draw(self, log):
        fig, ax = plt.subplots()
        draw_ECG(ax, self.full_signal)
        ax.vlines(x=self.pos_start, ymin=0, ymax=max(self.full_signal), colors='green', lw=2, alpha=0.5)
        ax.vlines(x=self.pos_end, ymin=0, ymax=max(self.full_signal), colors='green', lw=2, alpha=0.5)

        ax.vlines(x=self.neg_start, ymin=0, ymax=max(self.full_signal), colors='red', lw=2, alpha=0.5)
        ax.vlines(x=self.neg_end, ymin=0, ymax=max(self.full_signal), colors='red', lw=2, alpha=0.5)
        log.add_fig(fig)


    def get_err_distr_for_1_point(self, v_real):
        vs = self.get_full_vs()
        errs = list([abs(v_real - v) for v in vs])
        return errs


    def create_prediction_for_next_point(self, v_real):
        return v_real + self.dy_law


    def check_prediction_err_in_point(self, index):
        pass


    def measure_p_of_so_good_in_point(self, index):
        pass


    def get_p_of_so_good_in_region_pointwise(self):
        pass

    def get_r(self):
        pass


if __name__ == '__main__':
    log = HtmlLogger("NO_INERTIA")
    scene = SceneNoInertia(dy_law=-6)
    scene.draw(log)
    scene.draw_v_hists(log)

    # визуальное тестирование всех методов:
    v_real = 200
    errs_for_some_point = scene.get_err_distr_for_1_point(v_real)
    log.add_text(" abs err для v_real = {:.2f}".format(v_real))
    fig, ax = plt.subplots()
    ax.hist(errs_for_some_point)
    log.add_fig(fig)

    v_real = 10
    errs_for_some_point = scene.get_err_distr_for_1_point(v_real)
    log.add_text(" abs err для v_real = {:.2f}".format(v_real))
    fig, ax = plt.subplots()
    ax.hist(errs_for_some_point)
    log.add_fig(fig)
