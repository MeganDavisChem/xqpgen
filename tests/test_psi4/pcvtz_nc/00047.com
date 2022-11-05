#h2o AUG-PCVTZ eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5452699707       -0.9717756628
O        0.0000000000       -0.0000000000        0.1272871356
H        0.0000000000        1.5452699707       -0.9717756628

units bohr
}
 
set globals {
 reference rohf
 basis aug-cc-pcvtz
 freeze_core true
 cachelevel=0
 maxiter=500
 dertype none
 ints_tolerance 20
 roots_per_irrep = [0,0,1,0]
}

set scf d_convergence 12
set ccenergy r_convergence 12
set cceom r_convergence 8

energy('eom-cc3')