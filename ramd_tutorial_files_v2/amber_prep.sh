#!/bin/bash


echo "
# Minimization performed for relaxing the solute : restraint_wt=500
 &cntrl
  imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,
  ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,
  ntf=1, ntb=1, dielc=1.0, cut=10.0,
  nsnb=25, igb=0,
  ntr=1, restraint_wt=500, restraintmask='(:1-236 & !@H= & !@Na= & !@Cl=)',
  maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=0.0001,
  ntc=1,
 /
" >> ref_min-500
sander -O -i ref_min-500 -p ref.prmtop -c ref.inpcrd -ref ref.inpcrd -o ref-min-500.ou -r ref-min-500.crd -inf ref-min-500.log

echo "
# Minimization performed for relaxing the solute : restraint_wt=1
 &cntrl
  imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,
  ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,
  ntf=1, ntb=1, dielc=1.0, cut=10.0,
  nsnb=25, igb=0,
  ntr=1, restraint_wt=100, restraintmask='(:1-236 & !@H= & !@Na= & !@Cl=)',
  maxcyc=1500, ntmin=1, ncyc=100, dx0=0.01, drms=0.0001,
  ntc=1,
 /
" >> ref_min-100
sander -O -i ref_min-100 -p ref.prmtop -c ref-min-500.crd -ref ref-min-500.crd -o ref-min-100.ou -r ref-min-100.crd -inf ref-min-100.log

echo "
# Minimization performed for relaxing the solute : restraint_wt=1
 &cntrl
  imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,
  ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,
  ntf=1, ntb=1, dielc=1.0, cut=10.0,
  nsnb=25, igb=0,
  ntr=1, restraint_wt=5, restraintmask='(:1-236 & !@H= & !@Na= & !@Cl=)',
  maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=5,
  ntc=1,
 /
" >> ref_min-5
sander -O -i ref_min-5 -p ref.prmtop -c ref-min-100.crd -ref ref-min-100.crd -o ref-min-5.ou -r ref-min-5.crd -inf ref-min-5.log

echo "
# Minimization performed for relaxing the solute  : no positional restraints
&cntrl
  imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,
  ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,
  ntf=1, ntb=1, dielc=1.0, cut=10.0,
  nsnb=25, igb=0,
  ntr=0,
  maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=0.0001,
  ntc=1, 
 /
" >> ref_min
sander -O -i ref_min -p ref.prmtop -c ref-min-5.crd -ref ref-min-5.crd -o ref-min.ou -r ref-min.crd -inf ref-min.log


echo "
# NVT Heating with restrained heavy atoms 50 kcal/mol*A^2
 &cntrl
  imin=0, ntx=1, irest=0, ntrx=1, ntxo=1, 
  ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
  ntc=2, ntf=2, ntb=1, dielc=1.0, cut=10.0,
  nsnb=100, igb=0,
  ntr=1, restraint_wt=50.0, restraintmask=':1-236 & !@H= & !@Na= & !@Cl=',
  nstlim=25000,
  t=0.0, dt=0.002,
  ntt=3, gamma_ln=1.0, tempi=10.0, temp0=300.0,
  vlimit=15,
  ntp=0,
  tol=0.00000001,
 /
" > ref_heat
sander -O -i ref_heat -p ref.prmtop -c ref-min.crd -ref ref-min.crd -o ref-heat.ou -r ref-heat.crd -inf ref-heat.log

echo "
# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2
 &cntrl
  imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,
  ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
  ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,
  nsnb=100, igb=0,
  ntr=1, restraint_wt=50.0, restraintmask=':1-236 & !@H= & !@Na= & !@Cl=',
  nstlim=10000,
  t=0.0, dt=0.002,
  ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,
  vlimit=15,
  ntp=1, taup=1.0, pres0=1.0, comp=44.6,
  tol=0.00000001, 
 /
" > ref-equil-NPT-50
sander -O -i ref-equil-NPT-50 -p ref.prmtop -c ref-heat.crd -ref ref-heat.crd -o ref-equil-NPT-50.ou -r ref-equil-NPT-50.crd -inf ref-equil-NPT-50.log -x ref-equil-NPT-50.mdcrd

echo "
# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2
 &cntrl
  imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,
  ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
  ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,
  nsnb=100, igb=0,
  ntr=1, restraint_wt=10.0, restraintmask=':1-236 & !@H= & !@Na= & !@Cl=',
  nstlim=10000,
  t=0.0, dt=0.002,
  ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,
  vlimit=15,
  ntp=1, taup=1.0, pres0=1.0, comp=44.6,
  tol=0.00000001,
 /
" > ref-equil-NPT-10
sander -O -i ref-equil-NPT-10 -p ref.prmtop -c ref-equil-NPT-50.crd -ref ref-equil-NPT-50.crd -o ref-equil-NPT-10.ou -r ref-equil-NPT-10.crd -inf ref-equil-NPT-10.log -x ref-equil-NPT-10.mdcrd

echo "
# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2
 &cntrl
  imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,
  ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
  ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,
  nsnb=100, igb=0,
  ntr=1, restraint_wt=2.0, restraintmask=':1-236 & !@H= & !@Na= & !@Cl=',
  nstlim=10000,
  t=0.0, dt=0.002,
  ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,
  vlimit=15,
  ntp=1, taup=1.0, pres0=1.0, comp=44.6,
  tol=0.00000001,
 /
" > ref-equil-NPT-2
sander  -O -i ref-equil-NPT-2 -p ref.prmtop -c ref-equil-NPT-10.crd -ref ref-equil-NPT-10.crd -o ref-equil-NPT-2.ou -r ref-equil-NPT-2.crd -inf ref-equil-NPT-2.log -x ref-equil-NPT-2.mdcrd


echo "
# NPT equilibration with no restrains
 &cntrl
  imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,
  ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
  ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,
  nsnb=100, igb=0,
  nstlim=100000,
  t=0.0, dt=0.002,
  ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0, ig=-1,
  vlimit=15,
  ntp=1, taup=1.0, pres0=1.0, comp=44.6,
  tol=0.00000001,
 /
" > ref-equil-NPT
sander -O -i ref-equil-NPT -p ref.prmtop -c ref-equil-NPT-2.crd -ref ref-equil-NPT-2.crd -o ref-equil-NPT.ou -r ref-equil-NPT.crd -inf ref-equil-NPT.log -x ref-equil-NPT.mdcrd

