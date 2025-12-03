import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Parâmetros do circuito
# -------------------------
Vin = 12.0           # V
D = 0.4              # duty cycle
f_sw = 10e3         # Hz
T = 1 / f_sw
L = 200e-6           # H
C = 47e-6            # F
R_load = 50.0        # ohm
Vd = 0.7             # diodo Vf (V)

# Perdas / parasitas
R_L = 0.05           # resistência série do indutor (ohm)
R_d_on = 0.1         # resistência equivalente quando diodo conduz (ohm)
Rds_on = 0.05        # resistência do MOSFET quando ON (ohm)
R_esr = 0.05         # ESR do capacitor (OHMS) -> modelado em série com C

# Tempo de simulação e resolução
t_sim = 5e-3
substeps = 400        # substeps por período (aumente para maior precisão)
dt = T / substeps
t = np.arange(0, t_sim, dt)

# Vetores de estado
iL = np.zeros_like(t)       # corrente do indutor
v_out = np.zeros_like(t)    # tensão no nó de saída (nó do capacitor)
v_sw = np.zeros_like(t)     # tensão no nó de comutação (entre L, MOSFET e diodo)
pwm = ((t % T) < (D * T)).astype(float)

# Condições iniciais
iL[0] = 0.0
v_out[0] = 0.0
v_sw[0] = 0.0

# -------------------------
# Loop de simulação com v_sw explícito
# -------------------------
for n in range(1, len(t)):
    ON = (pwm[n] == 1.0)

    if ON:
        # MOSFET ligado: v_sw ≈ queda no MOSFET (Rds_on * iL)
        v_sw[n-1] = iL[n-1] * Rds_on
        vL = (Vin - v_sw[n-1]) - iL[n-1] * R_L
        diode_conduct = False
        iD = 0.0
    else:
        # MOSFET desligado: diodo pode conduzir se v_sw > v_out + Vd
        v_sw_est = v_sw[n-1]
        if v_sw_est > v_out[n-1] + Vd:
            diode_conduct = True
            v_sw[n-1] = v_out[n-1] + Vd + iL[n-1] * R_d_on
            vL = (Vin - v_sw[n-1]) - iL[n-1] * R_L
            iD = iL[n-1]
        else:
            diode_conduct = False
            # mantém v_sw constante se diodo bloqueado
            v_sw[n-1] = v_sw[n-1]
            vL = (Vin - v_sw[n-1]) - iL[n-1] * R_L
            iD = 0.0

    # Atualiza corrente do indutor
    di = (vL / L) * dt
    iL[n] = iL[n-1] + di
    if iL[n] < 0:
        iL[n] = 0.0

    # Corrente da carga
    i_load = v_out[n-1] / R_load

    # Corrente do capacitor
    iC = iD - i_load

    # Atualiza tensão ideal no capacitor (integra uma vez só)
    vC_ideal = v_out[n-1] + (iC / C) * dt

    # Tensão no nó de saída considerando ESR
    v_out[n] = vC_ideal + iC * R_esr

    # Atualiza v_sw para o próximo passo (usa o valor calculado nesse passo)
    v_sw[n] = v_sw[n-1] if ON == False else iL[n] * Rds_on

# -------------------------
# Resultados e verificação
# -------------------------
v_theoretical = Vin * D
print("Tensão final simulada (v_out): {:.3f} V".format(v_out[-1]))
print("Tensão teórica esperada: {:.3f} V".format(v_theoretical))
print("Erro percentual: {:.3f} %".format(abs((v_out[-1] - v_theoretical) / v_theoretical) * 100))

# -------------------------
# Plots
# -------------------------
plt.figure(figsize=(12,9))
plt.subplot(4,1,1)
plt.plot(t*1e3, pwm, linewidth=0.6); plt.ylabel("PWM"); plt.ylim(-0.2,1.2)

plt.subplot(4,1,2)
plt.plot(t*1e3, iL, linewidth=0.7); plt.ylabel("iL (A)")

plt.subplot(4,1,3)
plt.plot(t*1e3, v_sw, linewidth=0.7); plt.ylabel("v_sw (V)")

plt.subplot(4,1,4)
plt.plot(t*1e3, v_out, linewidth=0.7); plt.ylabel("v_out (V)"); plt.xlabel("tempo (ms)")

plt.tight_layout()
plt.show()
