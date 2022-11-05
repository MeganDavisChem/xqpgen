#h2o AUG-PV5Z eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5533946651       -0.9640405749
O        0.0000000000       -0.0000000000        0.1118169598
H        0.0000000000        1.5533946651       -0.9640405749

units bohr
}
 
set globals {
 reference rohf
 basis aug-cc-pv5z
 freeze_core ON
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