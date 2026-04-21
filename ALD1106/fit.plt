reset
set encoding utf8 

# set terminal postscript eps enhanced color font 'Arial,12' size 6.5,4.5
# set output 'fit.eps' 

# ============================ Plot Settings ============================
set title "Title"
set ylabel 'Sheet Conductance \sigma (S/sq)'
set xlabel 'Gate Voltage V_{G4} (V)'
# set grid
# set xrange [0:900]
# set yrange [0:180]
# set format x "%.0s%c"
set samples 10000

Ci = 1e-2 # F/m^2, capacitance per unit area of the gate oxide
# sigma2D = n2D * mu = Ci*(V_GS - V_T) * mu # 2D sheet conductance
# V_T = -b/a # Threshold voltage from fit
# mu = a/Ci # Mobility from fit
n2D(V_GS) = Ci*(V_GS - V_T) # 2D carrier density per charge


set fit quiet
f(x) = a*x + b 
fit[2:6] f(x) '.\Mobility\20262004004.dat' using 1:8 via a,b

# R^2 = 1 - SS_res / SS_tot, evaluated on the same fit range [2:5]
stats '.\Mobility\20262004004.dat' using (($1>=2 && $1<=5) ? $8 : 1/0) nooutput
SST = STATS_sumsq - (STATS_sum**2)/STATS_records
r2 = 1.0 - FIT_WSSR/SST

V_T = -b/a
mu = a/Ci
mu_err = a_err/Ci
print sprintf("Fitted parameters: a = (%.4f +- %.4f), b = (%.4f +- %.4f), r^2 = %.4f", a, a_err, b, b_err, r2)
print sprintf("Threshold voltage: V_T = (%.4f +- %.4f)", V_T, sqrt((b/a**2)**2 * (a_err)**2 + (1/a)**2 * (b_err)**2))
print sprintf("Mobility: mu = (%.4f +- %.4f) cm^2/Vs (%.2f%%)", mu*1e4, mu_err*1e4, mu_err/mu*100) # Convert from m^2/Vs to cm^2/Vs



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
    '.\Mobility\20262004004.dat' using 1:8 with lines ls 4 notitle,\
    f(x) with lines ls 2 notitle

# plot \
#     '.\Mobility\20262004004.dat' using 1:($8/(Ci*($1 - V_T))*1e4) with lines ls 4 notitle,\

# set output