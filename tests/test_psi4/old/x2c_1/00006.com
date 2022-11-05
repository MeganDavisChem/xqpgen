#h2o SPECIAL eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5324442879       -0.9645940696
O        0.0000000000       -0.0093518604        0.1195405381
H        0.0000000000        1.5417961482       -0.9712106584

units bohr
}
 
set globals {
 reference rohf
 basis aug-cc-pvtz-dk
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