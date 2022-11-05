#h2o AUG-PCVTZ eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5526779723       -0.9699150799
O        0.0000000000        0.0093330892        0.1169625279
H        0.0000000000        1.5433448831       -0.9633116380

units bohr
}
 
set globals {
 reference rohf
 basis aug-cc-pcvtz
 freeze_core false
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