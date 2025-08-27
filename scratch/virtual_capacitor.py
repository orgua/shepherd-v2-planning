from cmath import sqrt

V_in = 200e-3  # data-file
I_in = 5e-3  # data-file
I_leak = 0  # model-parameter
dt = 1 / 1e3  # parameter
C = 1000e-6  # model-parameter
V_cap = 3  # start-parameter -> DAC-write
V_cap_max = 4.2  # model-parameter
V_cap_min = 0  # model-parameter
V_upper_thres = 3.5  # model-parameter
V_lower_thres = 3.2  # model-parameter
eta_in = 0.8  # LUT-parameter, f(V_in,I_in)
eta_out = 0.9  # LUT-parameter, f(V_out,I_out)
V_out = 2.3  # parameter
I_out = 0e-3  # ADC-measurement

for _ in range(20):
    P_in = V_in * I_in
    I_cIn = eta_in * P_in / V_cap
    P_out = V_out * I_out
    I_cOut = P_out / (V_cap * eta_out)
    dI = I_cIn - I_cOut - I_leak
    dV_cap = (dI * dt) / C
    V_cap = V_cap + dV_cap
    V_cap = min(V_cap, V_cap_max)
    V_cap = max(V_cap, V_cap_min)
    print(f"V = {V_cap} incl \t dV = {dV_cap}")

# switching on supply with output capacitor -> try to model a more correct approach
# E_new = E_old - E_output
# E = C*V^2 / 2
# C_cap * V_cap_new^2 / 2 = C_cap * V_cap_old^2 / 2 - C_out * V_out^2 / 2
# V_cap_new^2 = V_cap_old^2 - (C_out / C_cap) * V_out^2

C_cap = 200e-6
C_out = 22e-6
V_upper_thres = 3.5
V_out = 2.3
V_cCode = V_upper_thres * sqrt((C_cap - C_out) / C_cap)  # = 3.302 V
V_thesis = V_upper_thres * sqrt(C_cap / (C_cap + C_out))  # = 3.322 V
V_ingmar = sqrt(pow(V_upper_thres, 2) - C_out * pow(V_out, 2) / C_cap)  # = 3.416 V
print(V_cCode)
print(V_thesis)
print(V_ingmar)

# TODO: ask Boris about it
# maxima-code:
# CC: C_cap * V_cap_new^2 / 2 = C_cap * V_cap_old^2 / 2 - C_out * V_out^2 / 2;
# ft : solve(CC, V_cap_new)[2];


# TestBench PreTest

vss = {}
# keep in sync with "example_virtsource_settings.yml"
vss["C_storage_F"] = 1 * (10**-3)
vss["V_storage_V"] = 3.5
vss["t_sample_s"] = 10 * (10**-6)
vss["eta_in"] = 0.5
vss["eta_out"] = 0.8
vss["I_storage_leak_A"] = 9 * (10**-9)
vss["V_storage_disable_threshold_V"] = 2.3
vss["V_out_V"] = 2.0


# set desired end-voltage of storage-cap:
V_cap_V = 4.000
dt_s = 0.100
V_inp_V = 1.0
dV_cap_V = V_cap_V - vss["V_storage_V"]
I_cIn = dV_cap_V * vss["C_storage_F"] / dt_s
P_inp_W = I_cIn * vss["V_storage_V"] / vss["eta_in"]
n_samples = dt_s / vss["t_sample_s"]
I_inp = P_inp_W / V_inp_V

# set desired end-voltage of storage-cap - low enough to disable output
V_cap_V = 2.200
dt_s = 1.00
dV_cap_V = V_cap_V - vss["V_storage_V"]
I_cOut = -dV_cap_V * vss["C_storage_F"] / dt_s - vss["I_storage_leak_A"]
P_out_W = I_cOut * vss["V_storage_V"] * vss["eta_out"]
n_samples = dt_s / vss["t_sample_s"]
I_out = P_out_W / vss["V_out_V"]
Ps = P_out_W / n_samples

print("VCap goal)")
