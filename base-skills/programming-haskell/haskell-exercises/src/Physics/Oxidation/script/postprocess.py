# -*- coding: utf-8 -*-
from IPython import embed
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    names = ['time', 'thickness', 'temperature']
    df = pd.read_csv('../results.csv', names=names)
    t = df['time'].to_numpy()
    T = df['temperature'].to_numpy()
    l = df['thickness'].to_numpy() * 1_000_000_000

    plt.close('all')
    plt.style.use('seaborn-white')
    fig, ax1 = plt.subplots(figsize=(6, 6))
    ax2 = ax1.twinx()

    ax1.plot(t, T, 'r', label='Strip temperature')
    ax2.plot(t, l, 'b', label='Oxide thickness')

    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature [K]')
    ax2.set_ylabel('Thickness [nm]')
    ax1.grid(linestyle=':')
    ax2.set_ylim(0, 600)
    ax1.legend(loc='upper left')
    ax2.legend(loc='lower right')

    fig.tight_layout()
    fig.savefig('postprocess.png', dpi=300)

    # embed(using=False)