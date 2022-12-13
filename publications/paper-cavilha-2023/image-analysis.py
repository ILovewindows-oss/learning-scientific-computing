# -*- coding: utf-8 -*-
from pathlib import Path
from skimage.filters import gaussian
from skimage.filters import threshold_otsu
from skimage.io import imread
from skimage.measure import find_contours
from skimage.measure import label
from skimage.measure import regionprops
from skimage.measure import regionprops_table
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


PROPERTIES = (
    "area",
    "axis_major_length",
    "axis_minor_length",
    "eccentricity",
    "equivalent_diameter_area",
    "feret_diameter_max",
    "perimeter",
    "perimeter_crofton"
    
    # Used for drawing only.
    # "centroid",
    # "orientation",
    )


def _workflow_segment(fname, sigma):
    """ Perform image automated thresholding for segmentation. """
    img0 = imread(fname, as_gray=True)
    img1 = gaussian(img0, sigma=sigma)
    img2 = img1 > threshold_otsu(img1)
    
    porosity = 100 * (1 - img2.sum() / img2.size)
    contours = find_contours(img2, 0.99)

    return img0, img2, contours, porosity


def _draw_regions(img, regions, ax):
    """ Draw regions over image on given axis. """
    for props in regions:
        # Only get those fully inside the image!
        h, w = img.shape
        minr, minc, maxr, maxc = props.bbox
        lower_bounds = minr > 0 and minc > 0
        upper_bounds = maxr < h and maxc < w
        
        if lower_bounds and upper_bounds:
            y0, x0 = props.centroid
            orientation = props.orientation

            x1 = x0 + np.cos(orientation) * 0.5 * props.axis_minor_length
            y1 = y0 - np.sin(orientation) * 0.5 * props.axis_minor_length
            x2 = x0 - np.sin(orientation) * 0.5 * props.axis_major_length
            y2 = y0 - np.cos(orientation) * 0.5 * props.axis_major_length

            ax.plot((x0, x1), (y0, y1), "-r", linewidth=1)
            ax.plot((x0, x2), (y0, y2), "-r", linewidth=1)
            ax.plot(x0, y0, ".g", markersize=10)

            bx = (minc, maxc, maxc, minc, minc)
            by = (minr, minr, maxr, maxr, minr)
            ax.plot(bx, by, "-b", linewidth=1)


def workflow_porosity(file_n, file_m, sigma):
    """ Compare raw and patched images in terms of porosity level. """
    img_n, _, cont_n, porosity_n = _workflow_segment(file_n, sigma)
    img_m, _, cont_m, porosity_m = _workflow_segment(file_m, sigma)
    
    def add_subplot(ax, img, contours, porosity, name=None, lw=1):
        """ Create same format of display for each image. """
        if name is not None:
            ax.set_title(f"Porosity of {porosity:.1f}% ({name})")
        else:
            ax.set_title(f"Porosity of {porosity:.1f}%")

        ax.imshow(img, cmap="gray")
        
        for c in contours:
            ax.plot(c[:, 1], c[:, 0], color="r", linewidth=lw)
        
        ax.axis("off")
        
    plt.close("all")
    fig1, (ax_n, ax_m) = plt.subplots(1, 2, figsize=(12, 5))
    add_subplot(ax_n, img_n, cont_n, porosity_n, name="normal")
    add_subplot(ax_m, img_m, cont_m, porosity_m, name="manual")
    fig1.tight_layout()

    plt.close("all")
    fig2, ax_n = plt.subplots(1, 1, figsize=(6, 5))
    add_subplot(ax_n, img_n, cont_m, porosity_n, lw=2)
    fig2.tight_layout()

    return fig1, fig2


def _get_props_comp_fig(img, contours, regions):
    """ Get figure to compare quality of image properties assignment. """
    plt.close("all")
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 5))
    ax_a.imshow(img, cmap="gray")
    ax_b.imshow(img, cmap="gray")
    
    for c in contours:
        ax_a.plot(c[:, 1], c[:, 0], color="r", linewidth=1)
    
    ax_a.axis("off")

    _draw_regions(img, regions, ax_b)
    ax_b.axis("off")

    fig.tight_layout()
    return fig


def _get_props_publ_fig(img, contours, regions):
    """ Get figure to publish of image properties assignment. """
    plt.close("all")
    fig, ax = plt.subplots(1, 1, figsize=(6, 5))
    ax.imshow(img, cmap="gray")
    
    # for c in contours:
    #     ax.plot(c[:, 1], c[:, 0], color="y", linewidth=1)
    
    _draw_regions(img, regions, ax)
    ax.axis("off")

    fig.tight_layout()
    return fig


def workflow_regionprops(file_n, file_m, sigma, cutoff, pct=[10, 100]):
    """ Segment image and retrieve region properties. """
    img0 = imread(file_n, as_gray=True)

    img1, img2, contours, _ = _workflow_segment(file_m, sigma)
    label_img = label(1 - img2)
    regions = regionprops(label_img)

    # Ensure (if not already) regions are sorted by area.
    regions = sorted(regions, key=lambda r: r.area)

    # Get 95% confidence interval.
    sm, lg = np.percentile([r.area for r in regions], pct)

    def func_cutoff(r):
        """ Function to eliminate extreme regions. """
        return sm < r.area < lg and r.area > cutoff

    # Remove those regions outside the confidence interval.
    regions = list(filter(func_cutoff, regions))

    fig1 = _get_props_comp_fig(img1, contours, regions)
    fig2 = _get_props_publ_fig(img0, contours, regions)

    table = regionprops_table(label_img, properties=PROPERTIES)
    table = pd.DataFrame(table)

    return (fig1, fig2), table


def get_all_files():
    """ Retrive file pairs to be treated. """
    files_normal = sorted(Path("media/inputs/normal").glob(r"*.jpg"))
    files_manual = sorted(Path("media/inputs/manual").glob(r"*.jpg"))
    
    stem_normal = [f.stem for f in files_normal]
    stem_manual = [f.stem for f in files_manual]
    
    if stem_normal != stem_manual:
        raise Exception("Check files in sub-folders, names do not match!")
    
    return list(zip(files_normal, files_manual, stem_normal))


def run_porosity(all_files):
    """ Manage quantification of porosity in samples. """
    path_porosity = Path("media/outputs/porosity")
    path_porosity.mkdir(exist_ok=True, parents=True)

    for k, (file_n, file_m, stem) in enumerate(all_files):
        result1 = path_porosity / f"porosity-{stem}-compare.png"
        result2 = path_porosity / f"porosity-{stem}-publish.png"

        if result1.exists() and result2.exists():
            print(f"Already treated ({k:03d}) {stem}")
            continue
        
        print(f"Processing ({k:03d}) {stem}")
        figs = workflow_porosity(file_n, file_m, sigma=15)
        figs[0].savefig(result1, dpi=300)
        figs[1].savefig(result2, dpi=300)
    

def run_regions(all_files, sigma=10, cutoff=200):
    """ Manage quantification of region properties in samples. """
    path_regions = Path("media/outputs/regions")
    path_regions.mkdir(exist_ok=True, parents=True)

    for k, (file_n, file_m, stem) in enumerate(all_files):
        result1 = path_regions /f"regions-{stem}-compare.png"
        result2 = path_regions /f"regions-{stem}-publish.png"
        ftable = path_regions /f"regions-{stem}.xlsx"
        
        if result1.exists() and result2.exists() and ftable.exists():
            print(f"Already treated ({k:03d}) {stem}")
            continue
        
        print(f"Processing ({k}) {stem}")
        figs, df = workflow_regionprops(file_n, file_m, sigma, cutoff)
        figs[0].savefig(result1, dpi=300)
        figs[1].savefig(result2, dpi=300)
        df.to_excel(ftable, index=False)


def generate_summary(regex, saveas):
    """ Concatenate all data matching one sample. """
    all_tables = []

    for f in Path("media/outputs/regions").glob(regex):
        df = pd.read_excel(f)
        df["source"] = f.stem
        all_tables.append(df)

    df = pd.concat(all_tables, ignore_index=True)
    df.to_excel(saveas, index=False)


if __name__ == "__main__":
    all_files = get_all_files()
    run_porosity(all_files)
    run_regions(all_files)

    for sh in [50, 70, 80]:
        regex = f"*Ti_pure*{sh:0d}.*.xlsx"
        saveas = f"media/outputs/summary-regions-{sh:0d}.xlsx"
        generate_summary(regex, saveas)
