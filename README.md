# 🌐 Algoritmo Genético aplicado ao ENEM 2023

Este projeto implementa um **Algoritmo Genético (AG)** para selecionar um **grupo ideal de 100 candidatos** do ENEM 2023, equilibrando:

- Desempenho acadêmico  
- Diversidade socioeconômica e racial  
- Cobertura geográfica  

O trabalho faz parte da disciplina de **Sistemas de Apoio à Decisão (SAD)** e cumpre todas as especificações solicitadas pelo professor.

---

## 📌 Objetivo do Projeto

O objetivo é utilizar técnicas de inteligência computacional para simular um processo evolutivo que encontre um grupo de candidatos com:

✔ **Melhores notas médias**  
✔ **Maior diversidade (renda e raça)**  
✔ **Maior representatividade nacional (UFs)**  

A solução final contém **100 estudantes** selecionados pelo algoritmo.

---

## 🧬 Estrutura do Algoritmo Genético

O AG foi configurado da seguinte forma:

### **Cromossomo**
- Representa um grupo contendo **100 candidatos**

### **População Inicial**
- 20 grupos gerados aleatoriamente

### **Função de Aptidão (Fitness)**
Combinação ponderada de:
- 0.5 × Média das notas  
- 0.3 × Diversidade (Índice de Shannon)  
- 0.2 × Cobertura geográfica (UFs representadas)

### **Operadores Genéticos**
- **Seleção:** Torneio  
- **Crossover:** 1 ponto (single-point)  
- **Mutação:** 2% por gene  

### **Critério de parada**
- 100 gerações  

---

## 📁 Dados Utilizados

O algoritmo utiliza os **microdados do ENEM 2023**, disponibilizados pelo INEP.

Para evitar sobrecarga em computadores pessoais, o carregamento é feito em **chunks** e limitado a:

