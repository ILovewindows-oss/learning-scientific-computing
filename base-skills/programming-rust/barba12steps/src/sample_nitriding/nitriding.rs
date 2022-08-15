// Author: Walter Dal'Maz Silva
// Date  : Sep 28 2021

use crate::diff1d::solve_diffusion;
use crate::diff1d::BCType;

const RGAS: f64 = 8.31446261815324;

const RHO: f64 = 7890.0;

pub fn simulate_nitriding(thick: &f64, width: &f64, length: &f64,
    speed: &f64, temp: &f64, kn: &f64, y0: &f64, dump: &String,
    bc: &BCType, dx: &f64, dt: &f64) {
    // -- Scaler for B.C. management.
    let mut scale: f64 = 1.0;

    // -- Convert [mm] to [m].
    let mut thick: f64 = thick / 1000.0;

    // -- Convert [mm] to [m].
    let width: f64 = width / 1000.0;
    
    // -- Convert [m/min] to [m/s].
    let speed: f64 = speed / 60.0;

    // -- Convert [°C] to [K].
    let temp: f64 = temp + 273.15;
    
    // -- Convert [ppm] to [-].
    let y0: f64 = y0 * 1.0E-06;
  
    // -- Manage B.C. types.
    set_boundary(&bc, &mut thick, &mut scale);

    // -- Evaluate computed quantities.
    let ys: f64 = nitrogen_surface_fraction(*kn, temp);
    let dn: f64 = diffusion_coefficient_bcc(temp);
    let endtm: f64 = length / speed;

    // -- Solve problem.
    let sdot: f64 = solve_diffusion(*dx, *dt, thick, endtm, dn,
                                    y0, ys, *bc, dump.to_string());
    let mdot: f64 = scale * RHO * sdot * width * 3600.0;

    // Display results.
    println!("* The following concerns the full exposed length");
    println!("* Mass intake by material {:.2} kg/h", mdot);
}

fn diffusion_coefficient_bcc(temp: f64) -> f64 {
    6.6E-07 * f64::exp(-77900.0 / (RGAS * temp))
}

fn nitrogen_surface_fraction(kn: f64, temp: f64) -> f64 {
    kn * f64::powf(10.0, 0.5 * (12.392 - 5886.0 / temp)) / 53176.0
}

fn set_boundary(bc: &BCType, thick: &mut f64, scale: &mut f64) {
    match bc {
        BCType::DirichletSymmetry => {
            *thick /= 2.0;
            *scale *= 2.0;
        }
        BCType::DirichletDirichlet => {}
    }
}
