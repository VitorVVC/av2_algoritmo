# Análise dos resultados experimentais

Fonte: `results/completo.csv`, execução original de 30/10/2026. Foram conferidas 720 medições válidas, 144 configurações e cinco amostras por configuração. Nenhuma observação foi removida.

Ambiente registrado: Java 24, macOS aarch64, dez processadores lógicos disponíveis. Os valores abaixo são descritivos desta execução; não demonstram significância estatística nem garantem comportamento em outras máquinas.

## Resultados para 10.000 elementos

| Algoritmo | Entrada | Serial (ms) | 2 threads (ms) | 4 threads (ms) | 8 threads (ms) | Melhor configuração pela média | Speedup correspondente |
|---|---|---:|---:|---:|---:|---|---:|
| Quick | Aleatória | 0.5798 | 0.4644 | 0.4211 | 0.3909 | 8 threads | 1.48× |
| Quick | Crescente | 0.2074 | 0.1852 | 0.2489 | 0.2432 | 2 threads | 1.12× |
| Quick | Decrescente | 0.2310 | 0.2017 | 0.2878 | 0.2559 | 2 threads | 1.15× |
| Merge | Aleatória | 0.7937 | 0.4438 | 0.4040 | 0.3817 | 8 threads | 2.08× |
| Merge | Crescente | 0.3471 | 0.2584 | 0.2884 | 0.2622 | 2 threads | 1.34× |
| Merge | Decrescente | 0.3414 | 0.4196 | 0.3773 | 0.3697 | Sequencial | 1.00× |
| Insertion | Aleatória | 15.7692 | 4.1327 | 1.6787 | 0.9320 | 8 threads | 16.92× |
| Insertion | Crescente | 0.0131 | 0.0649 | 0.0822 | 0.1110 | Sequencial | 1.00× |
| Insertion | Decrescente | 34.3838 | 9.0871 | 3.2862 | 1.6973 | 8 threads | 20.26× |
| Selection | Aleatória | 19.7679 | 5.8939 | 2.1402 | 0.9923 | 8 threads | 19.92× |
| Selection | Crescente | 19.5142 | 5.5814 | 1.9256 | 1.0208 | 8 threads | 19.12× |
| Selection | Decrescente | 28.9341 | 8.8208 | 3.0481 | 1.5592 | 8 threads | 18.56× |

## Discussão dos resultados para o artigo

Para entradas aleatórias com 10.000 elementos, Quick Sort passou de 0,5798 ms na versão sequencial para 0,3909 ms com oito threads (speedup de 1,48). Merge Sort passou de 0,7937 ms para 0,3817 ms (speedup de 2,08). A diferença absoluta entre os dois resultados paralelos é pequena e não sustenta uma afirmação geral de superioridade sem avaliar a dispersão e repetir o experimento.

O efeito da quantidade de threads depende da entrada. Em Quick Sort, duas threads produziram a menor média para entradas crescente e decrescente; quatro e oito threads não melhoraram esses casos. Em Merge Sort decrescente, todas as médias paralelas ficaram acima da sequencial. Portanto, esta execução não indica aceleração monotônica com o aumento do paralelismo.

Insertion Sort apresentou comportamento especialmente dependente da distribuição. Na entrada crescente de 10.000 elementos, o sequencial teve média de 0,0131 ms, contra 0,1110 ms com oito threads, aproximadamente 8,47 vezes mais tempo. A versão serial aproveita a entrada já ordenada, enquanto a versão híbrida acrescenta tarefas e fusões. Na entrada decrescente, as médias foram 34,3838 ms e 1,6973 ms, respectivamente, gerando speedup de 20,26.

Selection Sort com entrada aleatória passou de 19,7679 ms para 0,9923 ms com oito threads (speedup de 19,92). Esse ganho e os ganhos de Insertion precisam ser atribuídos à estratégia híbrida como um todo: menor trabalho dentro de blocos, execução concorrente e fusão. Não se trata de comparação com trabalho computacional idêntico.

Os ganhos relativos elevados dos métodos híbridos também não significam menor tempo absoluto. Para a entrada aleatória de 10.000 elementos, as médias com oito threads foram 0,3817 ms para Merge, 0,3909 ms para Quick, 0,9320 ms para Insertion híbrido e 0,9923 ms para Selection híbrido. As conclusões se restringem às implementações, tamanhos e ambiente utilizados.

## Variação entre as amostras

CV = desvio padrão amostral / média. Um CV alto indica dispersão em relação ao tempo médio; não é um teste de significância. As dez configurações com maior CV estão abaixo.

| Algoritmo | Tamanho | Entrada | Threads | Média (ms) | Mediana (ms) | Desvio padrão (ms) | CV |
|---|---:|---|---:|---:|---:|---:|---:|
| INSERTION | 1000 | ascending | 8 | 0.75199 | 0.12796 | 1.42501 | 189.5% |
| INSERTION | 1000 | ascending | 4 | 0.97315 | 0.23963 | 1.56458 | 160.8% |
| QUICK | 1000 | descending | 2 | 0.22073 | 0.08129 | 0.32088 | 145.4% |
| MERGE | 5000 | descending | 8 | 0.46266 | 0.19917 | 0.60997 | 131.8% |
| MERGE | 1000 | descending | 4 | 0.19511 | 0.10158 | 0.23326 | 119.6% |
| INSERTION | 1000 | random | 8 | 0.46374 | 0.21871 | 0.52965 | 114.2% |
| MERGE | 1000 | random | 4 | 0.69349 | 0.41650 | 0.77222 | 111.4% |
| QUICK | 5000 | descending | 4 | 0.34385 | 0.23438 | 0.35123 | 102.1% |
| MERGE | 1000 | ascending | 8 | 0.49747 | 0.25517 | 0.49999 | 100.5% |
| INSERTION | 1000 | descending | 8 | 0.40128 | 0.23362 | 0.35047 | 87.3% |

## Como interpretar

- Os gráficos de tempo mostram média ± um desvio padrão amostral. Essas barras não são intervalos de confiança. O gráfico de speedup mostra razões entre médias e não contém barras de incerteza.
- A linha de speedup igual a 1 é a referência serial. O gráfico compara razões, portanto um grande ganho relativo não significa que um algoritmo tenha o menor tempo absoluto.
- Insertion e Selection paralelos são híbridos: cada bloco usa o algoritmo indicado, mas os blocos são combinados por fusão. Dividir um problema quadrático em blocos pode reduzir o trabalho total, além de permitir execução simultânea. Ganhos acima do número de threads não comprovam eficiência de hardware superior a 100%.
- O caso serial de Insertion não realiza deslocamentos em uma entrada crescente, enquanto a versão híbrida ainda tem despacho e fusões. Isso ajuda a interpretar por que paralelizar pode custar mais.
- Não é possível atribuir uma medição isolada a JIT, coleta de lixo ou agendamento sem instrumentação adicional. A dispersão observada deve ser apresentada como limitação.
- Três aquecimentos e cinco amostras em uma única JVM são uma primeira avaliação. Uma validação mais robusta deve usar processos JVM independentes, mais aquecimentos e amostras, e tamanhos maiores para Quick/Merge.
- O intervalo de valores varia com o tamanho: [0, 10n). Assim, tamanho e intervalo não foram isolados como fatores independentes.
- O limite de tarefas e o limiar de 256 elementos limitam a concorrência. Configurar oito threads não garante oito trabalhadores ocupados; o experimento controla paralelismo do pool, sem fixar núcleos físicos.

## Figuras

1. `graficos/comparacao_10000.png`: tempos absolutos dos quatro métodos, escala logarítmica.
2. `graficos/speedup_10000.png`: razões entre médias sequenciais e paralelas.
3. `graficos/tempo_quick.png`, `tempo_merge.png`, `tempo_insertion.png`, `tempo_selection.png`: efeito de tamanho, distribuição e threads.

As mesmas figuras estão disponíveis em SVG vetorial. Para reproduzir: instalar matplotlib em um ambiente Python e executar `python scripts/analisar.py` da raiz do projeto.
