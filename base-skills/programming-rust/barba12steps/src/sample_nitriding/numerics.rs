// Author: Walter Dal'Maz Silva
// Date  : Sep 28 2021

pub fn trapz(y: &[f64], dx: &f64) -> f64 {
    let mut acc: f64 = 0.0;

    for val in y { acc += val }

    (2.0 * acc - y[0] - y[y.len() - 1]) * dx / 2.0
}

pub fn linspace(x_start: f64, x_end: f64, num: usize) -> Vec<f64> {
    match num {
        0 => Vec::new(),
        1 => vec![x_start],
        _ => {
            let mut linspaced: Vec<f64> = vec![0.0; num];
            let delta: f64 = (x_end - x_start) / (num as f64 - 1.0);

            for i in 0..num {
                linspaced[i] = x_start + delta * (i as f64);
            }

            linspaced
        }
    }
}

pub fn tdma_destroy(a: &mut Vec<f64>, b: &mut Vec<f64>, 
    c: &mut Vec<f64>, d: &mut Vec<f64>) {
    let n: usize = b.len();

    assert_eq!(a.len(), n);
    assert_eq!(c.len(), n);
    assert_eq!(d.len(), n);

    for i in 1..n {
        let m: f64 = a[i] / b[i - 1];
        b[i] = b[i] - m * c[i - 1];
        d[i] = d[i] - m * d[i - 1];
    }

    d[n - 1] = d[n - 1] / b[n - 1];

    for i in (0..n - 1).rev() {
        d[i] = (d[i] - c[i] * d[i + 1]) / b[i];
    }
}

#[cfg(test)]
mod tests {
    use super::trapz;
    use super::linspace;
    use super::tdma_destroy;

    #[test]
    fn test_trapz_array() {
        let dx: f64 = 1.0;
        let y: [f64; 5] = [0.0, 1.0, 2.0, 3.0, 4.0];

        assert_eq!(trapz(&y, &dx), 8.0);
    }

    #[test]
    fn test_trapz_vector() {
        let dx: f64 = 1.0;
        let y: Vec<f64> = vec![0.0, 1.0, 2.0, 3.0, 4.0];

        assert_eq!(trapz(&y, &dx), 8.0);
    }

    #[test]
    fn test_linspace() {
        let z: Vec<f64> = vec![0.00, 0.25, 0.50, 0.75, 1.00];
        let s: Vec<f64> = linspace(0.0, 1.0, 5);

        let matching: usize = z.iter().zip(&s)
            .filter(|&(a, b)| a == b)
            .count();
        assert_eq!(matching, z.len());
    }

    #[test]
    fn test_tdma() {
        let mut a: Vec<f64> = vec![ 0.0, -1.0, -1.0, -1.0];
        let mut b: Vec<f64> = vec![ 4.0,  4.0,  4.0,  4.0];
        let mut c: Vec<f64> = vec![-1.0, -1.0, -1.0,  0.0];
        let mut d: Vec<f64> = vec![ 5.0,  5.0, 10.0, 23.0];
        let z: Vec<f64> = vec![ 2.0,  3.0,  5.0,  7.0];
        
        tdma_destroy(&mut a, &mut b, &mut c, &mut d);

        let matching: usize = z.iter().zip(&d)
            .filter(|&(a, b)| f64::abs(a - b) < 1.0E-10)
            .count();
        assert_eq!(matching, z.len());
    }
}
