import os
import random
import numpy as np
import pandas as pd

POP_SIZE = 20  # tamanho da população (20 grupos)
N_GERACOES = 100  # número de gerações
TAM_GRUPO = 100  # cada cromossomo representa 100 candidatos
TAXA_MUT = 0.02  # taxa de mutação
TAXA_CROSS = 0.8  # taxa de crossover
AMOSTRA_MAX = 100000  # máximo de registros(meu pc é fraco, vc pode escolher ou n todos)


def carregar_dados(caminho):
    print("Carregando microdados do ENEM")

    chunksize = 50000
    chunks = []
    total = 0

    colunas = [
        "NU_INSCRICAO",
        "NU_NOTA_MT", "NU_NOTA_CN", "NU_NOTA_LC",
        "NU_NOTA_CH", "NU_NOTA_REDACAO",
        "Q006", "Q002", "TP_COR_RACA", "SG_UF_PROVA"
    ]

    for chunk in pd.read_csv(
        caminho, sep=";", encoding="latin1",
        low_memory=False, chunksize=chunksize,
        usecols=lambda c: c in colunas
    ):
        chunk = chunk.dropna()
        chunks.append(chunk)
        total += len(chunk)

        if total >= AMOSTRA_MAX:
            break

    df = pd.concat(chunks, ignore_index=True)
    return df


def fitness(df, grupo_idx):

    notas = df.loc[grupo_idx, [
        "NU_NOTA_MT", "NU_NOTA_CN",
        "NU_NOTA_LC", "NU_NOTA_CH",
        "NU_NOTA_REDACAO"
    ]].mean(axis=1).mean()

    notas_norm = notas / 1000

    def shannon(col):
        cont = df.loc[grupo_idx, col].value_counts()
        p = cont / cont.sum()
        return -(p * np.log(p)).sum()

    div_raca = shannon("TP_COR_RACA")
    div_renda = shannon("Q006")

    div_total = (div_raca + div_renda) / 2
    div_norm = div_total / 3

    estados = df.loc[grupo_idx, "SG_UF_PROVA"].nunique() / 27

    return 0.5 * notas_norm + 0.3 * div_norm + 0.2 * estados


def crossover(pai, mae):

    # para evitar duplicatas.

    if random.random() > TAXA_CROSS:
        return pai.copy(), mae.copy()

    corte = random.randint(1, TAM_GRUPO - 2)

    filho1 = pai[:corte] + [g for g in mae if g not in pai[:corte]]
    filho2 = mae[:corte] + [g for g in pai if g not in mae[:corte]]

    filho1 = filho1[:TAM_GRUPO]
    filho2 = filho2[:TAM_GRUPO]

    return filho1, filho2


def mutacao(individuo, total_indices):

    # substitui genes com pequena probabilidade.

    for i in range(TAM_GRUPO):
        if random.random() < TAXA_MUT:
            individuo[i] = random.choice(total_indices)
    return individuo


def selecao_torneio(pop, scores):

    # seleção por torneio entre dois indivíduos.

    i, j = random.sample(range(len(pop)), 2)
    return pop[i] if scores[i] > scores[j] else pop[j]


def executar_ga(df, output_dir):
    print("Iniciando Algoritmo Genético")

    total_idx = list(range(len(df)))
    pop = [random.sample(total_idx, TAM_GRUPO) for _ in range(POP_SIZE)]

    for ger in range(N_GERACOES):
        scores = [fitness(df, ind) for ind in pop]

        nova_pop = []
        for _ in range(POP_SIZE // 2):
            pai = selecao_torneio(pop, scores)
            mae = selecao_torneio(pop, scores)

            filho1, filho2 = crossover(pai, mae)
            filho1 = mutacao(filho1, total_idx)
            filho2 = mutacao(filho2, total_idx)

            nova_pop.append(filho1)
            nova_pop.append(filho2)

        pop = nova_pop

        if (ger + 1) % 10 == 0:
            print(f"Geração {ger+1}/{N_GERACOES} concluída.")

    scores = [fitness(df, ind) for ind in pop]
    best = pop[np.argmax(scores)]

    df.loc[best].to_csv(f"{output_dir}/bolsistas.csv", index=False)

    print(f"Arquivo salvo em: {output_dir}/bolsistas.csv")


def main():
    caminho = r"SEU CAMINHO\microdados_enem_2023\DADOS\MICRODADOS_ENEM_2023.csv"

    output_dir = "resultados"
    os.makedirs(output_dir, exist_ok=True)

    df = carregar_dados(caminho)
    executar_ga(df, output_dir)


if __name__ == "__main__":
    main()

