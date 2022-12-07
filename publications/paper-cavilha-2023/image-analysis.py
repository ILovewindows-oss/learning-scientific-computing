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
    "centroid",
    "eccentricity",
    "equivalent_diameter_area",
    "feret_diameter_max",
    "orientation",
    "perimeter",
    "perimeter_crofton"
    )


def _workflow_segment(fname, sigma):
    """ Perform image automated thresholding for segmentation. """
    img0 = imread(fname, as_gray=True)
    img1 = gaussian(img0, sigma=sigma)
    img2 = img1 > threshold_otsu(img1)
    
    porosity = 100 * (1 - img2.sum() / img2.size)
    contours = find_contours(img2, 0.99)

    return img0, img2, contours, porosity


def workflow_porosity(file_n, file_m, sigma):
    """ Compare raw and patched images in terms of porosity level. """
    img_n, _, cont_n, porosity_n = _workflow_segment(file_n, sigma)
    img_m, _, cont_m, porosity_m = _workflow_segment(file_m, sigma)
    
    def add_subplot(ax, img, contours, porosity, name):
        """ Create same format of display for each image. """
        ax.set_title(f"Porosity of {porosity:.1f}% ({name})")
        ax.imshow(img, cmap="gray")
        
        for c in contours:
            ax.plot(c[:, 1], c[:, 0], color="r", linewidth=1)
        
        ax.axis("off")
        
    plt.close("all")
    fig, (ax_n, ax_m) = plt.subplots(1, 2, figsize=(12, 5))
    
    add_subplot(ax_n, img_n, cont_n, porosity_n, "normal")
    add_subplot(ax_m, img_m, cont_m, porosity_m, "manual")
    
    fig.tight_layout()
    return fig


def workflow_regionprops(fname, stem, sigma=10, cutoff=100):
    """ Segment image and retrieve region properties. """
    img0, img2, contours, _ = _workflow_segment(fname, sigma)
    label_img = label(1 - img2)
    regions = regionprops(label_img)

    plt.close("all")
    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(12, 5))
    
    ax_a.imshow(img0, cmap="gray")
    ax_b.imshow(img0, cmap="gray")
    
    for c in contours:
        ax_a.plot(c[:, 1], c[:, 0], color="r", linewidth=1)
    
    ax_a.axis("off")
        
    for props in regions:
        if props.area < cutoff:
            continue

        # Only get those fully inside the image!
        h, w = img0.shape
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

            ax_b.plot((x0, x1), (y0, y1), "-r", linewidth=1)
            ax_b.plot((x0, x2), (y0, y2), "-r", linewidth=1)
            ax_b.plot(x0, y0, ".g", markersize=15)

            bx = (minc, maxc, maxc, minc, minc)
            by = (minr, minr, maxr, maxr, minr)
            ax_b.plot(bx, by, "-b", linewidth=1)

    ax_b.axis("off")
    
    table = regionprops_table(label_img, properties=PROPERTIES)
    table = pd.DataFrame(table)

    fig.tight_layout()
    return fig, table


if __name__ == "__main__":
    files_normal = sorted(Path("media/normal").glob(r"*.jpg"))
    files_manual = sorted(Path("media/manual").glob(r"*.jpg"))
    
    stem_normal = [f.stem for f in files_normal]
    stem_manual = [f.stem for f in files_manual]
    
    if stem_normal != stem_manual:
        raise Exception("Check files in sub-folders, names do not match!")
    
    all_files = list(zip(files_normal, files_manual, stem_normal))
    
    for k, (file_n, file_m, stem) in enumerate(all_files):
        if (result := Path(f"media/porosity-{stem}.png")).exists():
            print(f"Already treated ({k}) {stem}")
            continue
        
        print(f"Processing ({k}) {stem}")
        fig = workflow_porosity(file_n, file_m, sigma=15)
        fig.savefig(result, dpi=300)

    for k, (_, file_m, stem) in enumerate(all_files):
        result = Path(f"media/regions-{stem}.png")
        ftable = Path(f"media/regions-{stem}.xlsx")
        
        if result.exists() and ftable.exists():
            print(f"Already treated ({k}) {stem}")
            continue
        
        print(f"Processing ({k}) {stem}")
        fig, df = workflow_regionprops(file_m, stem, sigma=10, cutoff=100)
        fig.savefig(result, dpi=300)
        df.to_excel(ftable, index=False)
