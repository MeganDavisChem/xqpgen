#h2o AUG-PCVTZ eom-cc3
memory 31950 mb

molecule h2o{
1 2
H        0.0000000000       -1.5425225611       -0.9653479245
O        0.0000000000        0.0000000000        0.1144316590
H        0.0000000000        1.5425225611       -0.9653479245

units bohr
}
 
set globals {
 reference rohf
 basis aug-cc-pcvtz
 freeze_core OFF
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