// Author: Walter Dal'Maz Silva
// Date  : Sep 28 2021

use std::fs::File;
use std::io::Write;
use std::path::Path;

use crate::numerics::trapz;
use crate::numerics::linspace;
use crate::numerics::tdma_destroy;

#[derive(Debug, Clone, Copy)]
pub enum BCType { DirichletDirichlet, DirichletSymmetry }

pub fn solve_diffusion(dx: f64, dt: f64, thick: f64, endtm: f64, dn: f64,
                       y0: f64, ys: f64, bc: BCType, dump: String) -> f64 {
    let nt: usize = (endtm / dt).ceil() as usize;
    let nx: usize = (thick / dx).ceil() as usize;
  
    let t = linspace(0.0, endtm, nt);
    let x = linspace(0.0, thick, nx);
  
    let mut a: Vec<f64> = vec![0.0; nx];
    let mut b: Vec<f64> = vec![0.0; nx];
    let mut c: Vec<f64> = vec![0.0; nx];
    let mut y: Vec<f64> = vec![0.0; nx];
  
    for i in 0..nx { y[i] = y0; }
  
    let alpha = dt * dn / (dx * dx);
    let m0 = trapz(&y, &dx);

    match bc {
        BCType::DirichletDirichlet => {
            y[0] = ys;
            y[nx-1] = ys;
        },
        BCType::DirichletSymmetry => {
            y[0] = ys;
        }
    }

    let path = Path::new(&dump);
    let display = path.display();
    let mut file: File = match File::create(&path) {
        Err(why) => panic!("couldn't create {}: {}", display, why),
        Ok(file) => file,
    };

    write_line(&mut file, &x[0], &x);
    write_line(&mut file, &t[0], &y);
  
    for tk in 1..nt {
        for i in 0..nx {
            b[i] = 1.0 + 2.0 * alpha;
            a[i] = -alpha;
            c[i] = -alpha;
        }

        match bc {
            BCType::DirichletDirichlet => {
                b[0]    = 1.0;
                b[nx-1] = 1.0;
                c[0]    = 0.0;
                a[nx-1] = 0.0;
            },
            BCType::DirichletSymmetry => {
                b[0]    = 1.0;
                c[0]    = 0.0;
                b[nx-1] = 1.0 + alpha;
                a[nx-1] = -alpha;
            }
        }

        tdma_destroy(&mut a, &mut b, &mut c, &mut y);

        write_line(&mut file, &t[tk], &y);
    }

    trapz(&y, &dx) - m0
}

fn write_line(fp: &mut File, t: &f64, y: &Vec<f64>) {
    let mut line: String = format!("{:.12},", t);

    for yk in y {
        line = format!("{}{:.12},", line, *yk);
    }

    if let Err(e) = writeln!(fp, "{}", line) {
        eprintln!("Couldn't write to file: {}", e);
    }
}
