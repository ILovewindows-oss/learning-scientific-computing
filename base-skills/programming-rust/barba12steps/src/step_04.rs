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

use barba12steps::*;

fn main() {
    lineardiff(41);
}

fn lineardiff(nx: usize) {
    let sigma: f64 = 0.2;
    let nu: f64 = 0.3;
    let l: f64 = 2.0;
    let dx: f64 = l / (nx as f64 - 1.0);
    let nt: usize = 20;
    let dt: f64 = sigma * f64::powf(dx, 2.0) / nu;
    let base: &str = "results/step_04_{name}_nx{nx}.png";

    let alpha: f64 = nu * dt / f64::powf(dx, 2.0);
    let x: Vec<f64> = barba12steps::linspace(0.0, l, nx);
    let mut u: Vec<f64> = vec![1.0; nx];

    for k in (nx / 4)..(nx / 2 + 1) { u[k] = 2.0; }

    let filename: String = make_filename(base, nx, "initial");
    let caption: String = "Initial state".to_string();
    plot_state(&filename, &caption, &x, &u, l);

    for _ in 0..nt {
        let un = u.to_vec();
        for i in 1..(nx-1) {
            u[i] = un[i] + alpha * (un[i+1] - 2.0 * un[i] + un[i-1]);
        }
    }

    let filename: String = make_filename(base, nx, "final");
    let caption: String = "Final state".to_string();
    plot_state(&filename, &caption, &x, &u, l);
}

fn make_filename(base: &str, nx: usize, name: &str) -> String {
    base.replace("{name}", name)
        .replace("{nx}", nx.to_string().as_str())
        .to_string()
}

fn plot_state(filename: &String, caption: &String, 
              x: &Vec<f64>, u: &Vec<f64>, l: f64) {
    let xlabel: String = "Position [m]".to_string();
    let ylabel: String = "Amplitude [-]".to_string();
    plot2d(&filename, &x, &u, &caption, &xlabel, &ylabel, 
           (-1.0e-06, l + 1.0e-06), (0.79, 2.21));
}
