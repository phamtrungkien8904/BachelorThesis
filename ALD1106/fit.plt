reset
set encoding utf8 


# ============================ Plot Settings ============================
set title "Title"
set ylabel 'Sheet Conductance \sigma (S/sq)'
set xlabel 'Gate Voltage V_{G4} (V)'
# set grid
# set xrange [0:900]
# set yrange [0:180]
# set format x "%.0s%c"
set samples 10000


set fit quiet
f(x) = a*x + b 
fit[1:5] f(x) '.\Data_Mobility_ALD\20262004003.dat' using 1:(-$8) via a,b
V_T = -b/a
print sprintf("Fitted parameters: a = %g, b = %g", a, b)
print sprintf("Threshold voltage: V_T = %g", V_T)


# Styling
# Use valid color syntax and distinct colors per dataset
set style line 1 lw 1.5 pt 7 ps 0.5 lc rgb 'black' dt 4
set style line 2 lw 2 pt 7 ps 0.5 lc rgb 'blue' 
set style line 3 lw 2 pt 7 ps 0.5 lc rgb 'purple'
set style line 4 lw 2 pt 7 lc rgb 'red' 

# V12(V14, V24) = (V14 - V24)
# sigma(I34, V14, V24) = log(2)/pi * I34/V12(V14, V24)

mu(sigma, V_GS) = sigma/(V_GS - V_T)

# Plot
plot \
    '.\Data_Mobility_ALD\20262004003.dat' using 1:(-$8) with lines ls 4 notitle,\
    f(x) with lines ls 2 notitle

# plot \
#     '.\Data_Mobility_ALD\20262004001.dat' using 1:(mu(($8),($1))) with lines ls 4 notitle,\

# set out