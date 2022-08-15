// Author: Walter Dal'Maz Silva
// Date  : Sep 28 2021

mod numerics;
mod diff1d;
mod nitriding;

use std::time::Instant;
use diff1d::BCType;
use nitriding::simulate_nitriding;

fn main() {
    println!("*** NITRIDING MASS INTAKE MODEL ***");

    // -- Nitriding potential [Pa^{-1/2}].
    let kn: f64 = 0.05;
    
    // -- Temperature [°C].
    let temp: f64  = 650.0;
    
    // -- Exposed length [m].
    let length: f64 = 600.0;
    
    // -- Line speed [m/min]
    let speed: f64 = 600.0;
    
    // -- Strip width [mm].
    let width: f64 = 1500.0;
    
    // -- Strip thickness [mm].
    let thick: f64 = 0.3;
    
    // -- Nitrogen content [ppm].
    let y0: f64 = 100.0;
    
    // -- Use this to store results in CSV format.
    let dump: String = String::from("results.csv");

    // -- Characteristic cell size in space [m].
    let dx: f64 = 1.0E-06;

    // -- Characteristic time step [s].
    let dt: f64 = 1.0E-01;

    // -- Test all B.C. types.
    let bcs: [BCType; 2] = [BCType::DirichletDirichlet,
                            BCType::DirichletSymmetry];

    // -- Simulation entry point.
    for bc in bcs {
        let start = Instant::now();
        println!("\n\n* Using B.C. {:#?}", bc);
        simulate_nitriding(&thick, &width, &length, &speed, &temp,
                           &kn, &y0, &dump, &bc, &dx, &dt);
        let duration = start.elapsed();
        println!("* Simulation took is: {:?}", duration);
    }

    println!("\n\n*** NITRIDING MASS INTAKE MODEL ***");
}
