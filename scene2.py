from utils import get_signal_snippet, draw_ECG, Distr, HtmlLogger, make_arrows


import matplotlib.pyplot as plt
import statistics

class UDistr:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_p_of_event(self, a1, b1):
        all = abs(self.b-self.a)
        event = abs(b1 - a1)
        p = event/all
        return p



class SceneNoInertia:
    def __init__(self, dy_law, neg_end):
        self.full_signal = get_signal_snippet(lead_name='i', start_coord=340, end_coord=435)
        self.pos_start = 11
        self.pos_end = 43
        self.neg_start = 44
        self.neg_end = neg_end

        self.dy_law = dy_law

    def get_pos_vs(self):
        vs = list([self.full_signal[i] for i in range(self.pos_start, self.pos_end+1 )])
        return vs

    def get_neg_vs(self):
        vs = list([self.full_signal[i] for i in range(self.neg_start, self.neg_end+1)])
        return vs

    def get_full_vs(self):
        vs = self.get_pos_vs() + self.get_neg_vs()
        return vs

    def get_dV(self):
        abs_razbros = abs (max (self.get_full_vs()) - min(self.get_full_vs()) )
        #dV = abs_razbros/len(self.get_full_vs())
        return abs_razbros


    def draw(self, log):
        fig, ax = plt.subplots()
        draw_ECG(ax, self.full_signal)
        ax.vlines(x=self.pos_start, ymin=0, ymax=max(self.full_signal), colors='green', lw=2, alpha=0.5)
        ax.vlines(x=self.pos_end, ymin=0, ymax=max(self.full_signal), colors='green', lw=2, alpha=0.5)

        ax.vlines(x=self.neg_start, ymin=0, ymax=max(self.full_signal), colors='red', lw=2, alpha=0.5)
        ax.vlines(x=self.neg_end, ymin=0, ymax=max(self.full_signal), colors='red', lw=2, alpha=0.5)
        log.add_fig(fig)
 

    def measure_r_in_point_pos(self, index_child):
        dV = self.get_dV()
        dv_distr = UDistr(a=-dV, b=dV)
        real_dv = self.full_signal[index_child] - self.full_signal[index_child -1]
        predicted_dv = self.dy_law


        err_naive = abs(real_dv)
        err_of_prediction = abs(predicted_dv - real_dv)

        p_of_so_close = dv_distr.get_p_of_event(real_dv, predicted_dv)

        if err_naive < err_of_prediction: # наше предсказание вредно
            return - p_of_so_close

        # наше предсказание хорошее
        return 1 - p_of_so_close


    def get_r_of_so_good_pos(self):
        r = 0
        for index in range(self.pos_start+1, self.pos_end+1):
           r += self.measure_r_in_point_pos(index_child=index)

        max_r = len(self.get_pos_vs())
        return r/max_r


def ex(log, neg_end):
    scene = SceneNoInertia(dy_law=0, neg_end=neg_end)
    scene.draw(log)
    # scene.draw_v_hists(log)

    # визуальное тестирование всех методов

    r_pos_list = []
    y_low_list = list(range(-15, 15, 1))
    for dy_law in y_low_list:
        scene.dy_law = dy_law
        r_pos = scene.get_r_of_so_good_pos()
        r_pos_list.append(r_pos)

    index = r_pos_list.index(max(r_pos_list))
    y_best = y_low_list[index]

    fig, ax = plt.subplots()
    ax.plot(y_low_list, r_pos_list, 'o-', label='r(dy)')
    ax.grid(which='major', axis='both', linestyle='--', alpha=0.75)
    make_arrows(ax)
    ax.vlines(x=y_best, ymin=0, ymax=max(r_pos_list), colors="green", lw=2, alpha=0.5,
              label='r({}) ={:.2f}'.format(y_best, max(r_pos_list)))
    ax.legend()
    log.add_fig(fig)


if __name__ == '__main__':
    log = HtmlLogger("NO_INERTIA2")
    ex(log, neg_end=90)
    ex(log, neg_end=50)

