#!/bin/bash

. /opt/isce2/isce_env.sh
. $slcp2cor_root/set_env_variable.sh

$slcp2cor_root/script/look.py -i geom_masa ter/lat.rdr.full -o geom_master/lat.rdr.7r2a -r 7 -a 2
$slcp2cor_root/script/look.py -i geom_master/lon.rdr.full -o geom_master/lon.rdr.7r2a -r 7 -a 2

$slcp2cor_root/script/slcstk2gamp.py -i SLC/ -o GAMP -lat geom_master/lat.rdr.7r2a -lon geom_master/lon.rdr.7r2a -r 7 -a 2 -bbox "34.6002832,34.6502392,-79.0801608,-78.9705888" -ssize 0.5
