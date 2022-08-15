# Relecture of Barba's 12 steps to Navier-Stokes in Rust

This is a self-learning study of Rust based on [CFDPython](https://github.com/barbagroup/CFDPython), previously known as 12 steps to Navier-Stokes as documented [here](https://jose.theoj.org/papers/10.21105/jose.00021).

It is not intended to be a faithful translation, but an adaptation for learning how to implement numerical problems in Rust. Since there is no one-to-one exact relationship, the list below provides the approximate links between the original teaching materials and this relecture. Also notice that I created a fork from original repository so that versions are fixed and always compatible with Rust code presented here. Also notice that pure Python coding notebooks were not recast here since it makes no sense,

## Current implementation

**NOTE:** The numbering in Rust files does not reflect the step number in Barba's series, but simply the order of files to be followed here.

- *Linear convection* is handled in [step_01.rs](src/step_01.rs) adapted from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/01_Step_1.ipynb).

- *Nonlinear convection* is treated in [step_02.rs](src/step_02.rs) adapted from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/02_Step_2.ipynb).

- *CFL criterion* is introduced in [step_03.rs](src/step_03.rs) adapted from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/03_CFL_Condition.ipynb).

- *Linear diffusion* is approached in [step_04.rs](src/step_04.rs) adapted from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/03_CFL_Condition.ipynb).

- *Burguer's equation* is implemented in [step_05.rs](src/step_05.rs) adapted from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/05_Step_4.ipynb).

## To-Do's

- *2-D Linear convection* from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/07_Step_5.ipynb).
- *2-D Nonlinear convection* from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/08_Step_6.ipynb).
- *2-D Linear Diffusion* from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/09_Step_7.ipynb).
- *2-D Burguer's equation* from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/10_Step_8.ipynb).
- *2-D Laplace Equation* from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/12_Step_9.ipynb).
- *2-D Poisson Equation* from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/13_Step_10.ipynb).
- *Cavity flow with Navier-Stokes* from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/14_Step_11.ipynb).
- *Channel flow with Navier-Stokes* from this [notebook](https://github.com/WallyMirrors/CFDPython/blob/master/lessons/15_Step_12.ipynb).

