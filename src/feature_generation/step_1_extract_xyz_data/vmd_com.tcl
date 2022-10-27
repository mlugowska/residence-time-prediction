proc calculate_com {ligand_name output_filename} {
    set numframes [molinfo top get numframes]

    # Loop over frames
    set ref [atomselect top "resname $ligand_name"]
    set outfile [open $output_filename w]
        for {set frame 0} {${frame} < ${numframes}} {incr frame} {
        #Change the frame inside the loop
        $ref frame $frame
        set com_ref [measure center ${ref} weight mass]
        puts $outfile "Frame $frame com $com_ref"
        }
    close $outfile
}
