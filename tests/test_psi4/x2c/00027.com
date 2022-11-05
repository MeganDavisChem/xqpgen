#h2o SPECIAL eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5445220252       -0.9737845712
O        0.0000000000        0.0093613418        0.1246816196
H        0.0000000000        1.5351606833       -0.9671612384

units bohr
}
 
set globals {
 reference rohf
 basis aug-cc-pvtz-dk
 freeze_core true
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