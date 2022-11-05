#h2o AUG-PV5Z eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5363420084       -0.9699243624
O        0.0000000000        0.0093518597        0.1169679445
H        0.0000000000        1.5269901487       -0.9633077721

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