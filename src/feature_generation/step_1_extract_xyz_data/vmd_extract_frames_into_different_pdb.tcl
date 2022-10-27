proc extract_frames {name} {
    set nf [molinfo top get numframes]

    for { set i 0 } {$i < $nf } { incr i } {
        set sel [atomselect top "all" frame $i]
        $sel writepdb $name-$i.pdb
    }
}
