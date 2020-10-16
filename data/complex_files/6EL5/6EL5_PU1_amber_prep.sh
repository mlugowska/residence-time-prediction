#!/bin/bash
echo "
# Minimization performed for relaxing the solute : restraint_wt=500
&cntrl
imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,
ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,ntf=1, ntb=1, dielc=1.0, cut=10.0,
nsnb=25, igb=0,
ntr=1, restraint_wt=500, restraintmask='(:1-208 & !@H= & !@Na= & !@Cl=)',
maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=0.0001,
ntc=1,
/
" >> /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_min-500
sander -O -i /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_min-500 -p /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.prmtop -c /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.inpcrd -ref /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.inpcrd -o /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-500.ou -r /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-500.crd -inf /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-500.log
echo "
# Minimization performed for relaxing the solute : restraint_wt=1
&cntrl
imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,
ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,ntf=1, ntb=1, dielc=1.0, cut=10.0,
nsnb=25, igb=0,
ntr=1, restraint_wt=100, restraintmask='(:1-208 & !@H= & !@Na= & !@Cl=)',
maxcyc=1500, ntmin=1, ncyc=100, dx0=0.01, drms=0.0001,
ntc=1,
/
" >> /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_min-100
sander -O -i /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_min-100 -p /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.prmtop -c /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-500.crd -ref /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-500.crd -o /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-100.ou -r /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-100.crd -inf /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-100.log
echo "
# Minimization performed for relaxing the solute : restraint_wt=1
&cntrl
imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,
ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,ntf=1, ntb=1, dielc=1.0, cut=10.0,
nsnb=25, igb=0,
ntr=1, restraint_wt=5, restraintmask='(:1-208 & !@H= & !@Na= & !@Cl=)',
maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=5,
ntc=1,
/
" >> /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_min-5
sander -O -i /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_min-5 -p /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.prmtop -c /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-100.crd -ref /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-100.crd -o /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-5.ou -r /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-5.crd -inf /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-5.log
echo "
# Minimization performed for relaxing the solute : restraint_wt=1
&cntrl
imin=1, ntx=1, irest=0, ntrx=1, ntxo=1,
ntpr=25, ntwr=500, ntwx=0, ntwv=0, ntwe=0,ntf=1, ntb=1, dielc=1.0, cut=10.0,
nsnb=25, igb=0,
ntr=0,
maxcyc=1500, ntmin=1, ncyc=500, dx0=0.01, drms=0.0001,
ntc=1,
/
" >> /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_min
sander -O -i /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_min -p /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.prmtop -c /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-5.crd -ref /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min-5.crd -o /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min.ou -r /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min.crd -inf /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min.log
echo "
# NVT Heating with restrained heavy atoms 50 kcal/mol*A^2
&cntrl
imin=0, ntx=1, irest=0, ntrx=1, ntxo=1,
ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
ntc=2, ntf=2, ntb=1, dielc=1.0, cut=10.0,
nsnb=100, igb=0,
ntr=1, restraint_wt=50.0, restraintmask=':1-208 & !@H= & !@Na= & !@Cl=',
nstlim=25000,
t=0.0, dt=0.002,
ntt=3, gamma_ln=1.0, tempi=10.0, temp0=300.0,
vlimit=15,
ntp=0,
tol=0.00000001,
 /'
" >> /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_heat
sander -O -i /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1_heat -p /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.prmtop -c /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min.crd -ref /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-min.crd -o /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-heat.ou -r /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-heat.crd -inf /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-heat.log
echo "
# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2
&cntrl
imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,
ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,
nsnb=100, igb=0,
ntr=1, restraint_wt=50.0, restraintmask=':1-208 & !@H= & !@Na= & !@Cl=',
nstlim=10000,
t=0.0, dt=0.002,
ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,
vlimit=15,
ntp=1, taup=1.0, pres0=1.0, comp=44.6,
tol=0.00000001, 
/
" >> /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-50
sander -O -i /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-50 -p /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.prmtop -c /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-heat.crd -ref /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-heat.crd -o /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-50.ou -r /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-50.crd -inf /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-50.log -x /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-50.mdcrd
echo "
# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2
&cntrl
imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,
ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,
nsnb=100, igb=0,
ntr=1, restraint_wt=10.0, restraintmask=':1-208 & !@H= & !@Na= & !@Cl=',
nstlim=10000,
t=0.0, dt=0.002,
ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,
vlimit=15,
ntp=1, taup=1.0, pres0=1.0, comp=44.6,
tol=0.00000001, 
/
" >> /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-10
sander -O -i /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-10 -p /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.prmtop -c /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-50.crd -ref /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-50.crd -o /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-10.ou -r /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-10.crd -inf /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-10.log -x /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-10.mdcrd
echo "
# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2
&cntrl
imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,
ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,
nsnb=100, igb=0,
ntr=1, restraint_wt=2.0, restraintmask=':1-208 & !@H= & !@Na= & !@Cl=',
nstlim=10000,
t=0.0, dt=0.002,
ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,
vlimit=15,
ntp=1, taup=1.0, pres0=1.0, comp=44.6,
tol=0.00000001, 
/
" >> /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-2
sander -O -i /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-2 -p /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.prmtop -c /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-10.crd -ref /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-10.crd -o /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-2.ou -r /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-2.crd -inf /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-2.log -x /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-2.mdcrd
echo "
# NPT equilibration with restrained heavy atoms 50 kcal/mol*A^2
&cntrl
imin=0, ntx=5, irest=1, ntrx=1, ntxo=1,
ntpr=100, ntwx=1000, ntwv=1000, ntwe=1000,
ntc=2, ntf=2, ntb=2, dielc=1.0, cut=10.0,
nsnb=100, igb=0,
nstlim=10000,
t=0.0, dt=0.002,
ntt=3, gamma_ln=1.0, tempi=300.0, temp0=300.0,
vlimit=15,
ntp=1, taup=1.0, pres0=1.0, comp=44.6,
tol=0.00000001, 
/
" >> /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT
sander -O -i /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT -p /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/6EL5_PU1_tip3_ions.prmtop -c /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-2.crd -ref /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT-2.crd -o /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT.ou -r /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT.crd -inf /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT.log -x /Users/mlugowska/PhD/residence-time-prediction/data/complex_files/6EL5/amber/6EL5_PU1-equil-NPT.mdcrd
