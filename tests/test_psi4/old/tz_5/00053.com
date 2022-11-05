#h2o AUG-PVTZ eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5527044291       -0.9737832496
O        0.0000000000        0.0093518617        0.1246857234
H        0.0000000000        1.5433525674       -0.9671666638

units bohr
}
 
set globals {
 reference rohf
 basis aug-cc-pvtz
 freeze_core ON
 cachelevel=0
 maxiter=500
 dertype none
 ints_tolerance 20
 roots_per_irrep = [0,1]
}

set scf d_convergence 12
set ccenergy r_convergence 12
set cceom r_convergence 8

energy('eom-cc3')