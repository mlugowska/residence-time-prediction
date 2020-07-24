# name of an input dcd file  
set dcd_name  [lindex $argv 0]
set out_name  [lindex $argv 1]
# name of ligand residues in PDB file
set ligand  INH
#  residue number of Lys that is placed is the ligand exis passway
#set residue  [lindex $argv 1]
#puts "========================= $number"
set name $dcd_name
mol load  parm7 ../ref.prmtop dcd $name.dcd
set mol1 [molinfo top get id]
put "END INI"

package require pbctools
pbc set [pbc get -all] -all
pbc wrap -center bb -centersel protein -compound res -all

# use use frame 0 for the refereince
set reference [atomselect $mol1 "protein and noh" frame 0]
#set reflys [atomselect $mol1 "residue $residue" frame 0]
set reflig [atomselect $mol1 "resname $ligand and noh"  frame 0]
#compute number of atoms in the ligand 
set atomnumber  0
  foreach a [$reflig get name]  {
  set atomnumber [expr $atomnumber+ 1]
 }
puts "Atoms in ligand: $atomnumber"
# the frame being compared
set sel [atomselect $mol1 "protein and noh"]
set sel1 [atomselect $mol1 "all"]
set n [molinfo $mol1  get numframes]
# all ligand atoms
set ligatoms [atomselect $mol1 "resname $ligand and noh"]
# selected residue
#set lys    [atomselect $mol1 "residue $residue"]
#output files
#set outfile1 [open $name-lys_rmsd.dat w]
set outfile2 [open $out_name-prot_rmsd.dat w]
set outfile3 [open $out_name-lig_rmsd.dat w]


# loop over frames
for { set frame 0 } {$frame < $n } { incr frame } {
 # get correct frame
 $sel frame $frame
 $ligatoms frame $frame
 $sel1 frame $frame
# $lys  frame $frame
 #compute the transformation
 set trans_mat [measure fit $sel $reference]
 #do the  alignment
# $ligatoms move $trans_mat
# $sel move $trans_mat
  $sel1 move $trans_mat
 # compute RMSD
# rmsd of a complete protein
 set rmsd [measure rmsd $sel $reference]
# RMSD of ligand 
 set rmsd2 [measure rmsd $ligatoms $reflig]
 puts $outfile3  "$frame $rmsd2"
 puts $outfile2 "$frame $rmsd"
 }
#close $outfile1
close $outfile2
close $outfile3
set scale [expr $n-1]
puts $scale
set sel1 [atomselect $mol1 "all" frame $scale]
set sel2 [atomselect $mol1 "all" frame 0]
#animate write pdb $outpdbfile $sel1 beg $scale end $scale
$sel1 writepdb $out_name-last.pdb
$sel2 writepdb $out_name-first.pdb
close $outpdbfile
quit

