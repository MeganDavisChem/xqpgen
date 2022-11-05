#h2o SPECIAL eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5417841703       -0.9750699649
O        0.0000000000        0.0093708857        0.1272455447
H        0.0000000000        1.5324132846       -0.9684397698

units bohr
}
 
set globals {
 reference rohf
 basis aug-cc-pvtz-dk
 freeze_core true
 cachelevel=0
 relativistic x2c
 maxiter=500
 dertype none
 ints_tolerance 20
 roots_per_irrep = [0,1]
}

set scf d_convergence 12
set ccenergy r_convergence 12
set cceom r_convergence 8

energy('eom-cc3')