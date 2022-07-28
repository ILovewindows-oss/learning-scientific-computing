# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt


def plot_history(data_history, metric):
    """ Plot trainning history data for Tensorflow. """
    plt.close('all')
    plt.style.use('seaborn-white')
    plt.figure(figsize=(12, 6))

    plt.subplot(121)
    plt.plot(data_history[metric])
    plt.plot(data_history[F'val_{metric}'])
    plt.title('Metric over epochs')
    plt.ylabel('Metric')
    plt.xlabel('Epoch')
    plt.grid(linestyle=':')
    plt.legend(['train', 'test'], loc='upper left')

    plt.subplot(122)
    plt.plot(data_history['loss'])
    plt.plot(data_history['val_loss'])
    plt.title('Loss over epochs')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.grid(linestyle=':')
    plt.legend(['train', 'test'], loc='upper left')

    plt.tight_layout()
    plt.savefig('plot_history.png', dpi=200)
