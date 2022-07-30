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
    // Number of FD nodes in space (experiment with both).
    let nx: usize = 41;
    // let nx: usize = 81;

    // Number of time-steps to advance solution.
    let nt: usize = 20;

    // Size of time-step [s].
    let dt: f64 = 0.025;

    // Space length [m].
    let l: f64 = 2.0;

    // Compute space step [m].
    let dx: f64 = l / (nx as f64 - 1.0);

    // Compute problem coefficient.
    let alpha: f64 = dt / dx;

    // Allocate space coordinates [m].
    let x: Vec<f64> = barba12steps::linspace(0.0, l, nx);

    // Allocate solution memory.
    let mut u: Vec<f64> = vec![1.0; nx];

    // Apply step initial condition.
    for k in (nx / 4)..(nx / 2 + 1) { u[k] = 2.0; }

    // Create a plot of initial state.
    plot_initial(&x, &u, l);

    // Loop over time and space to compute solution.
    for _ in 0..nt {
        let un = u.to_vec();
        for i in 1..nx {
            u[i] = un[i] * (1.0 - alpha * (un[i] - un[i - 1]));
        }
    }

    // Create a plot of final state.
    plot_final(&x, &u, l);
}

fn plot_initial(x: &Vec<f64>, u: &Vec<f64>, l: f64) {
    let filename: String = "results/step_02_initial.png".to_string();
    let caption: String = "Initial state".to_string();
    let xlabel: String = "Position [m]".to_string();
    let ylabel: String = "Amplitude [-]".to_string();
    plot2d(&filename, &x, &u, &caption, &xlabel, &ylabel, 
           (-1.0e-06, l + 1.0e-06), (0.79, 2.21));
}

fn plot_final(x: &Vec<f64>, u: &Vec<f64>, l: f64) {
    let filename: String = "results/step_02_final.png".to_string();
    let caption: String = "Final state".to_string();
    let xlabel: String = "Position [m]".to_string();
    let ylabel: String = "Amplitude [-]".to_string();
    plot2d(&filename, &x, &u, &caption, &xlabel, &ylabel, 
           (-1.0e-06, l + 1.0e-06), (0.79, 2.21));
}
