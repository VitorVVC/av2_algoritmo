"""Gera análise e figuras a partir das medições, sem alterar o CSV original.

Requer Python 3 e matplotlib. Execute da raiz: python scripts/analisar.py
"""
from pathlib import Path
import csv
import statistics as st
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'graficos'
OUT.mkdir(parents=True, exist_ok=True)
groups = defaultdict(list)
with (ROOT / 'results/completo.csv').open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 720
for r in rows:
    assert r['valid'] == 'true'
    assert abs(float(r['time_ms']) - int(r['time_ns']) / 1e6) < 0.000001
    groups[(r['algorithm'], int(r['size']), r['distribution'], int(r['threads']))].append(float(r['time_ms']))
assert len(groups) == 144 and all(len(v) == 5 for v in groups.values())
ALGS = ['QUICK', 'MERGE', 'INSERTION', 'SELECTION']
NAMES = ['Quick Sort', 'Merge Sort', 'Insertion Sort (blocos + fusão)', 'Selection Sort (blocos + fusão)']
DISTS = ['random', 'ascending', 'descending']
LABELS = ['Aleatória', 'Crescente', 'Decrescente']
THREADS = [1, 2, 4, 8]
SIZES = [1000, 5000, 10000]
COLORS = ['#263648', '#007f86', '#cf6b1b', '#7953a5']
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False,
                     'figure.facecolor': 'white', 'savefig.facecolor': 'white'})

def values(a, n, d, t):
    return groups[(a, n, d, t)]

def save(fig, name):
    fig.savefig(OUT / (name + '.png'), dpi=240, bbox_inches='tight')
    fig.savefig(OUT / (name + '.svg'), bbox_inches='tight')
    plt.close(fig)

# Painéis com escalas próprias: evita esconder Quick/Merge pelos tempos quadráticos.
for a, title in zip(ALGS, NAMES):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.4), layout='constrained')
    for ax, d, label in zip(axes, DISTS, LABELS):
        for t, color in zip(THREADS, COLORS):
            data = [values(a, n, d, t) for n in SIZES]
            ax.errorbar(SIZES, [st.mean(v) for v in data], yerr=[st.stdev(v) for v in data],
                        marker='o', capsize=3, color=color, label='Sequencial' if t == 1 else f'{t} threads')
        ax.set(title=label, xlabel='Quantidade de elementos', ylabel='Tempo médio (ms)')
        ax.set_xticks(SIZES, ['1.000', '5.000', '10.000'])
        ax.set_ylim(bottom=0); ax.grid(alpha=.2)
    axes[-1].legend(fontsize=8)
    fig.suptitle(f'{title} — tempo por tamanho da entrada\nBarras: ±1 desvio padrão amostral; cinco medições por ponto', fontsize=12)
    save(fig, 'tempo_' + a.lower())

fig, axes = plt.subplots(2, 2, figsize=(11, 8), layout='constrained')
for ax, a, title in zip(axes.flat, ALGS, NAMES):
    for d, label, color in zip(DISTS, LABELS, COLORS):
        base = st.mean(values(a, 10000, d, 1))
        ax.plot(THREADS, [base / st.mean(values(a, 10000, d, t)) for t in THREADS],
                marker='o', label=label, color=color)
    ax.axhline(1, color='gray', linestyle='--', linewidth=1)
    ax.set(title=title, xlabel='Threads configuradas (1 = sequencial)', ylabel='Speedup = média serial / média medida')
    ax.set_xticks(THREADS); ax.grid(alpha=.2); ax.legend(fontsize=8)
fig.suptitle('Ganho relativo para 10.000 elementos\nAcima de 1: menor tempo que o sequencial; abaixo de 1: maior tempo', fontsize=13)
save(fig, 'speedup_10000')

fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), layout='constrained')
for ax, d, label in zip(axes, DISTS, LABELS):
    for a, name, color in zip(ALGS, ['Quick', 'Merge', 'Insertion', 'Selection'], COLORS):
        ax.plot(THREADS, [st.mean(values(a, 10000, d, t)) for t in THREADS], marker='o', label=name, color=color)
    ax.set_yscale('log')
    ax.set(title=label, xlabel='Threads (1 = sequencial)', ylabel='Tempo médio (ms, escala logarítmica)')
    ax.set_xticks(THREADS); ax.grid(alpha=.2, which='both')
axes[-1].legend(fontsize=8)
fig.suptitle('Comparação dos quatro algoritmos — 10.000 elementos\nCada passo no eixo vertical representa uma razão de tempos', fontsize=12)
save(fig, 'comparacao_10000')

lines = ['# Análise dos resultados experimentais', '',
         'Fonte: `results/completo.csv`, execução original de 30/10/2026. Foram conferidas 720 medições válidas, 144 configurações e cinco amostras por configuração. Nenhuma observação foi removida.', '',
         'Ambiente registrado: Java 24, macOS aarch64, dez processadores lógicos disponíveis. Os valores abaixo são descritivos desta execução; não demonstram significância estatística nem garantem comportamento em outras máquinas.', '',
         '## Resultados para 10.000 elementos', '',
         '| Algoritmo | Entrada | Serial (ms) | 2 threads (ms) | 4 threads (ms) | 8 threads (ms) | Melhor configuração pela média | Speedup correspondente |',
         '|---|---|---:|---:|---:|---:|---|---:|']
for a in ALGS:
    for d, label in zip(DISTS, LABELS):
        means = [st.mean(values(a, 10000, d, t)) for t in THREADS]
        best = min(range(4), key=lambda i: means[i])
        lines.append('| ' + ' | '.join([a.title(), label, *[f'{v:.4f}' for v in means],
                    'Sequencial' if best == 0 else f'{THREADS[best]} threads', f'{means[0]/means[best]:.2f}×']) + ' |')
lines += ['', '## Discussão dos resultados para o artigo', '',
          'Para entradas aleatórias com 10.000 elementos, Quick Sort passou de 0,5798 ms na versão sequencial para 0,3909 ms com oito threads (speedup de 1,48). Merge Sort passou de 0,7937 ms para 0,3817 ms (speedup de 2,08). A diferença absoluta entre os dois resultados paralelos é pequena e não sustenta uma afirmação geral de superioridade sem avaliar a dispersão e repetir o experimento.', '',
          'O efeito da quantidade de threads depende da entrada. Em Quick Sort, duas threads produziram a menor média para entradas crescente e decrescente; quatro e oito threads não melhoraram esses casos. Em Merge Sort decrescente, todas as médias paralelas ficaram acima da sequencial. Portanto, esta execução não indica aceleração monotônica com o aumento do paralelismo.', '',
          'Insertion Sort apresentou comportamento especialmente dependente da distribuição. Na entrada crescente de 10.000 elementos, o sequencial teve média de 0,0131 ms, contra 0,1110 ms com oito threads, aproximadamente 8,47 vezes mais tempo. A versão serial aproveita a entrada já ordenada, enquanto a versão híbrida acrescenta tarefas e fusões. Na entrada decrescente, as médias foram 34,3838 ms e 1,6973 ms, respectivamente, gerando speedup de 20,26.', '',
          'Selection Sort com entrada aleatória passou de 19,7679 ms para 0,9923 ms com oito threads (speedup de 19,92). Esse ganho e os ganhos de Insertion precisam ser atribuídos à estratégia híbrida como um todo: menor trabalho dentro de blocos, execução concorrente e fusão. Não se trata de comparação com trabalho computacional idêntico.', '',
          'Os ganhos relativos elevados dos métodos híbridos também não significam menor tempo absoluto. Para a entrada aleatória de 10.000 elementos, as médias com oito threads foram 0,3817 ms para Merge, 0,3909 ms para Quick, 0,9320 ms para Insertion híbrido e 0,9923 ms para Selection híbrido. As conclusões se restringem às implementações, tamanhos e ambiente utilizados.', '',
          '## Variação entre as amostras', '',
          'CV = desvio padrão amostral / média. Um CV alto indica dispersão em relação ao tempo médio; não é um teste de significância. As dez configurações com maior CV estão abaixo.', '',
          '| Algoritmo | Tamanho | Entrada | Threads | Média (ms) | Mediana (ms) | Desvio padrão (ms) | CV |',
          '|---|---:|---|---:|---:|---:|---:|---:|']
ranked = sorted(groups, key=lambda k: st.stdev(groups[k])/st.mean(groups[k]), reverse=True)
for k in ranked[:10]:
    v = groups[k]
    lines.append(f'| {k[0]} | {k[1]} | {k[2]} | {k[3]} | {st.mean(v):.5f} | {st.median(v):.5f} | {st.stdev(v):.5f} | {st.stdev(v)/st.mean(v):.1%} |')
lines += ['', '## Como interpretar', '',
          '- Os gráficos de tempo mostram média ± um desvio padrão amostral. Essas barras não são intervalos de confiança. O gráfico de speedup mostra razões entre médias e não contém barras de incerteza.',
          '- A linha de speedup igual a 1 é a referência serial. O gráfico compara razões, portanto um grande ganho relativo não significa que um algoritmo tenha o menor tempo absoluto.',
          '- Insertion e Selection paralelos são híbridos: cada bloco usa o algoritmo indicado, mas os blocos são combinados por fusão. Dividir um problema quadrático em blocos pode reduzir o trabalho total, além de permitir execução simultânea. Ganhos acima do número de threads não comprovam eficiência de hardware superior a 100%.',
          '- O caso serial de Insertion não realiza deslocamentos em uma entrada crescente, enquanto a versão híbrida ainda tem despacho e fusões. Isso ajuda a interpretar por que paralelizar pode custar mais.',
          '- Não é possível atribuir uma medição isolada a JIT, coleta de lixo ou agendamento sem instrumentação adicional. A dispersão observada deve ser apresentada como limitação.',
          '- Três aquecimentos e cinco amostras em uma única JVM são uma primeira avaliação. Uma validação mais robusta deve usar processos JVM independentes, mais aquecimentos e amostras, e tamanhos maiores para Quick/Merge.',
          '- O intervalo de valores varia com o tamanho: [0, 10n). Assim, tamanho e intervalo não foram isolados como fatores independentes.',
          '- O limite de tarefas e o limiar de 256 elementos limitam a concorrência. Configurar oito threads não garante oito trabalhadores ocupados; o experimento controla paralelismo do pool, sem fixar núcleos físicos.', '',
          '## Figuras', '',
          '1. `graficos/comparacao_10000.png`: tempos absolutos dos quatro métodos, escala logarítmica.',
          '2. `graficos/speedup_10000.png`: razões entre médias sequenciais e paralelas.',
          '3. `graficos/tempo_quick.png`, `tempo_merge.png`, `tempo_insertion.png`, `tempo_selection.png`: efeito de tamanho, distribuição e threads.', '',
          'As mesmas figuras estão disponíveis em SVG vetorial. Para reproduzir: instalar matplotlib em um ambiente Python e executar `python scripts/analisar.py` da raiz do projeto.']
(ROOT / 'docs/analise-resultados.md').write_text('\n'.join(lines) + '\n')
print('\n'.join(lines[:24]))
print(f'\nFiguras salvas em {OUT}')
