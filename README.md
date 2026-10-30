# Comparação de algoritmos de ordenação em Java

Trabalho de Computação Paralela e Concorrente da UNIFOR.

**Aluno:** Vitor Vargas Cardoso  
**Professor:** Izequiel  
**Turma:** T296-26

O projeto compara Quick Sort, Merge Sort, Insertion Sort e Selection Sort em execução sequencial e paralela. Os tempos são registrados em CSV para análise e geração dos gráficos apresentados no artigo.

## Como executar

É necessário ter JDK 21 ou superior. Os experimentos incluídos no repositório foram executados com JDK 24.

Na pasta do projeto:

```sh
# Verificar as implementações (800 casos)
sh run.sh --test

# Executar o benchmark completo (720 medições)
sh run.sh --full

# Executar somente o cenário de 1.000 elementos (240 medições)
sh run.sh
```

No IntelliJ, abra o `pom.xml` como projeto Maven e execute a classe `Main`. Informe `--test` ou `--full` em **Program arguments**, mantendo a pasta do projeto como diretório de trabalho.

## Experimento

| Parâmetro | Configurações |
|---|---|
| Algoritmos | Quick, Merge, Insertion e Selection |
| Tamanhos | 1.000, 5.000 e 10.000 elementos |
| Entradas | Aleatória, crescente e decrescente |
| Execução | Sequencial e paralela com 2, 4 e 8 threads |
| Amostras | 5 por configuração, após 3 aquecimentos |

As configurações recebem cópias dos mesmos dados em cada amostra. O tempo é medido com `System.nanoTime()`, incluindo a ordenação, o despacho de tarefas e as fusões. Geração dos dados, clonagem, validação e escrita do CSV ficam fora da medição. As saídas são comparadas com `Arrays.sort`.

Quick e Merge dividem o trabalho em tarefas recursivas com `ForkJoinPool`. Insertion e Selection usam uma adaptação híbrida: ordenam blocos com o algoritmo correspondente e depois fazem a fusão. Nesse caso, a divisão também reduz o trabalho quadrático; o ganho medido não vem apenas das threads. O número de threads configura o paralelismo do pool, sem controlar a afinidade aos núcleos físicos.

## Arquivos

- `src/main/java/br/edu/unifor/cpc/`: implementações, benchmark e testes.
- `results/completo.csv`: medições do experimento completo.
- `results/completo-ambiente.txt`: ambiente da execução.
- `results/resumo.csv`: estatísticas da execução original.
- `docs/graficos/`: gráficos em PNG e SVG.
- `docs/analise-resultados.md`: análise dos resultados.
- `docs/Artigo-Computacao-Paralela.docx`: artigo editável.
- [Artigo em PDF](output/pdf/Artigo-Computacao-Paralela.pdf).

Para gerar novamente a análise e os gráficos, instale `matplotlib` em um ambiente Python e execute:

```sh
python scripts/analisar.py
```

Uma nova execução do benchmark substitui o CSV do mesmo perfil. O Java não atualiza `resumo.csv` automaticamente; esse arquivo corresponde às medições originais. O script de análise lê `completo.csv` e atualiza o texto da análise e as figuras.

Os resultados descrevem uma execução em uma única JVM, com cinco amostras por configuração. A dispersão e as limitações da comparação são discutidas no artigo.
