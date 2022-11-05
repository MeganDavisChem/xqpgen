#h2o AUG-PV5Z eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5499689432       -0.9712071212
O        0.0000000000        0.0093424435        0.1195400951
H        0.0000000000        1.5406264997       -0.9645971639

units bohr
}
 
set globals {
 reference rohf
 basis aug-cc-pv5z
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