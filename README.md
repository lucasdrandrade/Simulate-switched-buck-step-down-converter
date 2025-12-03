# Simulate-switched-buck-step-down-converter
Repo to save Simulation of a switched buck (step-down) converter

# Simulação de Conversor Buck em Python

Este projeto contém um código para simular o comportamento de um conversor DC-DC do tipo Buck (conversor abaixador de tensão). A simulação utiliza métodos numéricos para calcular as variáveis elétricas do circuito (corrente do indutor, tensão de saída, tensão no nó de comutação) ao longo do tempo, considerando elementos parasitas e perdas.

---

## O que o código faz

- Simula um conversor Buck operando em modo contínuo, com um sinal PWM controlando o chaveamento do MOSFET.
- Modela elementos não ideais, como resistências do indutor, MOSFET, diodo e ESR do capacitor.
- Calcula a corrente no indutor (`iL`), tensão no nó de saída (`v_out`) e tensão no nó de comutação (`v_sw`) ao longo do tempo.
- Compara o valor final da tensão de saída com o valor teórico esperado baseado no duty cycle e na tensão de entrada.
- Plota gráficos das principais variáveis em função do tempo para análise visual.

---

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - numpy
  - matplotlib

---

## Instalação das bibliotecas necessárias

Para instalar as bibliotecas necessárias, execute o seguinte comando no terminal:

```bash
pip install numpy matplotlib 
```
Como executar o código

Salve o arquivo Python com o código da simulação, por exemplo, switched-buck-step-down-converter.py.

Abra o terminal ou prompt de comando na pasta onde o arquivo está salvo.

Execute o script Python.
``` bash
python switched-buck-step-down-converter.py
```

ou, se usar Python 3 explicitamente:

``` bash
python3 switched-buck-step-down-converter.py
```

O script irá mostrar no console a tensão final simulada, a tensão teórica e o erro percentual.

Também serão exibidos gráficos com o sinal PWM, corrente do indutor, tensão no nó de comutação e tensão de saída, para visualização do comportamento do conversor.