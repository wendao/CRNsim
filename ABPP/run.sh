python scan_k0.py | grep k0= > dat
rm -rf tmp*
gnuplot << __EOF__
set term png
set output "out.png"
plot [:][0:14] "dat" u 2:3 w lp lw 2 pt 4 ps 2 t "fast", "" u 2:4 w lp lw 2 pt 4 ps 2 t "slow", "" u 2:5 w lp lw 2 pt 4 ps 2 t "median"
__EOF__
