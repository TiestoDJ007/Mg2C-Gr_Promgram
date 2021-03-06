#!/usr/bin/env python
# -*- coding=utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from pymatgen.electronic_structure.core import Spin
from pymatgen.io.vasp.outputs import Vasprun, Procar

if __name__ == "__main__":
    # 原子选择
    Plot_Atom = 'C'
    vasprun_dirctory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Paper_results/Bands_dos/Strain_0%/'
    vasprun_file = 'vasprun.xml'
    kpoints_file = 'KPOINTS'
    procar_file = 'PROCAR'
    saving_dictory = '/mnt/c/Users/a/OneDrive/Calculation_Data/Mg2C_Graphene/Paper_results/Picture/'
    saving_file = '{}'.format('dos_band_strain_0%')
    # vasprun.xml位置
    vasprun = Vasprun("{}".format(vasprun_dirctory + vasprun_file),
                      parse_projected_eigen=True)
    # 生成独立的band数据
    bands = vasprun.get_band_structure(
        "{}".format(vasprun_dirctory + kpoints_file),
        line_mode=True, efermi=vasprun.efermi)
    # 读取投影数据
    procar = Procar("{}".format(vasprun_dirctory + procar_file))
    Atom_symbol = vasprun.atomic_symbols
    dot_size = np.zeros(((3, bands.nb_bands, len(bands.kpoints))))
    for n in range(bands.nb_bands):
        for k in range(len(bands.kpoints)):
            # 挑选出投影原子的点大小数据
            for atom_nb in range(len(Atom_symbol)):
                if Atom_symbol[atom_nb] == Plot_Atom:
                    dot_size[0][n][k] += procar.data[Spin.up][k][n][atom_nb][
                                             3] * 300
                    dot_size[1][n][k] += procar.data[Spin.up][k][n][atom_nb][
                                             1] * 300
                    dot_size[2][n][k] += procar.data[Spin.up][k][n][atom_nb][
                                             2] * 300
        #    for nb_p in range(3):
        # 选定能量区间
    energy_min = -1
    energy_max = 1
    # 高对称点设置
    labels = [r"$M$", r"$\Gamma$", r"$K$", r"$M$"]
    labels_position = list()
    font = {'family': 'sans-serif', 'size': 24}
    # 开始画图
    fig, ax1 = plt.subplots(figsize=(16, 10))
    # 设置刻度向内
    ax1.tick_params(direction='in')
    # 设置能量区间
    ax1.set_ylim(energy_min, energy_max)
    # 设置x轴区间
    ax1.set_xlim(bands.distance[0], bands.distance[-1])
    ax1.set_xlabel("k-points")
    ax1.set_ylabel(r"$E - E_f$   /   eV")
    # 寻找高对称点
    for i in range(len(bands.distance)):
        if i == 0:
            labels_position.append(bands.distance[i])
        elif i < len(bands.distance) - 2:
            if bands.distance[i] == bands.distance[i + 1]:
                labels_position.append(bands.distance[i])
                # 设置垂直线
                ax1.vlines(bands.distance[i], energy_min, energy_max,
                           colors='gray', linestyles='dashed')
        elif i == len(bands.distance) - 1:
            labels_position.append(bands.distance[i])
    # 展示高对称点
    ax1.set_xticks(labels_position)
    ax1.set_xticklabels(labels)
    # 设置刻度间隔
    # xminorLocator = MultipleLocator(5)
    # ax1.xaxis.set_major_locator(xminorLocator)
    # 画散点图
    #        if nb_p == 0:
    ax1.set_title('{}'.format('Carbon p Orbit Bands'))
    ax1.hlines(0, labels_position[0], labels_position[-1])

    for n in range(len(bands.bands[Spin.up])):
        ax1.scatter(bands.distance, bands.bands[Spin.up][n] - vasprun.efermi, s=dot_size[0][n]*3, color='g', marker='.',
                    alpha=0.5)
        ax1.scatter(bands.distance, bands.bands[Spin.up][n] - vasprun.efermi, s=dot_size[1][n]*3, color='orangered', marker='.',
                    alpha=0.5)
        ax1.scatter(bands.distance, bands.bands[Spin.up][n] - vasprun.efermi, s=dot_size[2][n]*3, color='b', marker='.',
                    alpha=0.5)

    ax1.hlines(0, labels_position[0], labels_position[-1])
    plt.savefig('{}'.format(saving_dictory + saving_file + '_pz.png'),
                dpi=300)
    plt.show()
