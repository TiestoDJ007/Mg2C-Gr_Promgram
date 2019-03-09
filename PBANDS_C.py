#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from collections import defaultdict
from copy import deepcopy
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun


# 变量保存
def save_variable(Vars, filename):
    f = open(filename, 'wb')
    pickle.dump(Vars, f)
    f.close()
    return filename


def rgbline(ax, k, e, red, green, blue, alpha=1.):
    # creation of segments based on
    # http://nbviewer.ipython.org/urls/raw.github.com/dpsanders/matplotlib-examples/master/colorline.ipynb
    pts = np.array([k, e]).T.reshape(-1, 1, 2) #生成一个没有用的维度，以便下一步的计算
    seg = np.concatenate([pts[:-1], pts[1:]], axis=1)

    nseg = len(k) - 1
    r = [0.5 * (red[i] + red[i + 1]) for i in range(nseg)]
    g = [0.5 * (green[i] + green[i + 1]) for i in range(nseg)]
    b = [0.5 * (blue[i] + blue[i + 1]) for i in range(nseg)]
    a = np.ones(nseg, np.float) * alpha
    lc = LineCollection(seg, colors=list(zip(r, g, b, a)), linewidth=2)
    ax.add_collection(lc)


if __name__ == "__main__":
    # Only Bands
    vasprun = Vasprun("C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Color_Bands/Bands/vasprun.xml",
                      parse_projected_eigen=True)
    bands = vasprun.get_band_structure("C:/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Color_Bands/Bands/KPOINTS",
                                       line_mode=True,
                                       efermi=vasprun.efermi)
    # 将bands.projections转化成n维数组
    tmp_pbands = list(bands.projections.values())
    pbands_ndarray = deepcopy(tmp_pbands[0])
    # 分别投影到原子和轨道
    pbands_s_C = np.sum(deepcopy(pbands_ndarray[:, :, 0, 8:30]), axis=2)
    pbands_p_C = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 1:4, 8:30]), axis=2), axis=2)
    pbands_d_C = np.sum(np.sum(deepcopy(pbands_ndarray[:, :, 4:9, 8:30]), axis=2), axis=2)

    # 输出投影原子，轨道的贡献率
    contrib_Origin = np.zeros((bands.nb_bands, len(bands.kpoints), 3))
    contrib_C = deepcopy(contrib_Origin)
    for b in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            sc = pbands_s_C[b][k] ** 2
            pc = pbands_p_C[b][k] ** 2
            dc = pbands_d_C[b][k] ** 2
            tot = sc + pc + dc
            if tot != 0.0:
                contrib_C[b, k, 0] = sc / tot
                contrib_C[b, k, 1] = pc / tot
                contrib_C[b, k, 2] = dc / tot

    # 设置绘图参数
    labels = [r"$M$", r"$\Gamma$", r"$K$", r"$M$"]
    font = {'family': 'sans-serif', 'size': 24}
    fig, ax1 = plt.subplots()
    ax1.set_ylim(-1,1)
    for b in range(bands.nb_bands):
        rgbline(ax1,
                range(len(bands.kpoints)),
                [e - bands.efermi for e in bands.bands[Spin.up][b]],
                contrib_C[b, :, 0],
                contrib_C[b, :, 1],
                contrib_C[b, :, 2])
    ax1.set_xlabel("k-points")
    ax1.set_ylabel(r"$E - E_f$   /   eV")
    ax1.grid()
    ax1.hlines(y=0, xmin=0, xmax=len(bands.kpoints), color="k", lw=2)
    nlabs = len(labels)
    step = len(bands.kpoints) / (nlabs - 1)
    for i, lab in enumerate(labels):
        ax1.vlines(i * step, -1, 1, "k")
    ax1.set_xticks([i * step for i in range(nlabs)])
    ax1.set_xticklabels(labels)
    ax1.set_xlim(0, len(bands.kpoints))
    plt.show()
    plt.savefig(sys.argv[0].strip(".py") + ".png", format="png")