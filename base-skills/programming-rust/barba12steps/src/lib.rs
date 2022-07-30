// The MIT License (MIT)
// Copyright (c) 2022 Walter Dal'Maz Silva
//
// Permission is hereby granted, free of charge, to any person obtaining a
// copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense,
// and/or sell copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

use plotters::prelude::*;

pub fn pow(a: f64, n: i32) -> f64 {
    match n {
        -4 => 1.0 / pow(a, 4),
        -3 => 1.0 / pow(a, 3),
        -2 => 1.0 / pow(a, 2),
        -1 => 1.0 / a,
         0 => 1.0,
         1 => a,
         2 => a * a,
         3 => a * a * a,
         4 => a * a * a * a,
        _ => f64::powf(a, n as f64)
    }
}

pub fn exp(n: f64) -> f64 {
    n.exp()
}

pub fn linspace(x0: f64, xend: f64, n: usize) -> Vec<f64> {
    let dx = (xend - x0) / (n as f64 - 1.0);
    (0..n).map(|i| x0 + (i as f64) * dx).collect()
}

pub fn plot2d(filename: &String, x: &Vec<f64>, y: &Vec<f64>,
              caption: &String, xlabel: &String, ylabel: &String,
              xlim: (f64, f64), ylim: (f64, f64)) {
    let (xmin, xmax) = xlim;
    let (ymin, ymax) = ylim;
    let data = x.iter().enumerate().map(|(k, &xk)| (xk, y[k]));

    let shape = (512, 384);
    let root = BitMapBackend::new(filename, shape)
        .into_drawing_area();

    root.fill(&WHITE).unwrap();

    let mut chart = ChartBuilder::on(&root)
        .x_label_area_size(35)
        .y_label_area_size(35)
        .margin(10)
        .caption(caption, ("sans-serif", 24.0).into_font())
        .build_cartesian_2d(xmin..xmax, ymin..ymax)
        .unwrap();

    chart
        .configure_mesh()
        .x_desc(xlabel)
        .y_desc(ylabel)
        .draw()
        .unwrap();

    chart.draw_series(LineSeries::new(data, &BLUE)).unwrap();
}
