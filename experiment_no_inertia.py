from utils_r import SceneNoInertia
from utils import HtmlLogger

import matplotlib.pyplot as plt


if __name__ == '__main__':
    log = HtmlLogger("NO_INERTIA")
    scene = SceneNoInertia(dy_law=None)
    scene.draw(log)
    scene.draw_v_hists(log)

    rs = []
    dys = list(range(-6, 6, 3))
    for dy in dys:
        scene.dy_law=dy
        r = scene.get_r()
        rs.append(r)

    fig, ax = plt.subplots()
    ax.plot(dys, rs)
    log.add_fig(fig)
