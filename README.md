# Análise de algoritmos de ordenação em Java

Projeto acadêmico de Computação Paralela e Concorrente — Ciência da Computação, UNIFOR.

## Abrir no IntelliJ
1. Selecione **Open** e escolha esta pasta (ou `pom.xml`).
2. Selecione um JDK 21 ou superior em **File > Project Structure > Project SDK**. A linguagem alvo é Java 21; este projeto foi validado com JDK 24.
3. Aguarde a importação Maven. O IntelliJ pode usar seu Maven integrado.
4. Abra `src/main/java/br/edu/unifor/cpc/Main.java` e execute `main`.
5. Em **Run > Edit Configurations**, use `--test` para validar ou `--full` para o experimento completo. Configure o diretório de trabalho como a raiz deste projeto.

## Executar pelo terminal (sem instalar Maven)
```sh
sh run.sh --test
sh run.sh
sh run.sh --full
```
Sem argumentos, executa uma amostra rápida de 240 medições, com tamanho 1.000. `--full` gera 720 medições em `results/completo.csv`: quatro algoritmos × três tamanhos (1.000, 5.000, 10.000) × três entradas × quatro configurações × cinco amostras. Uma nova execução substitui o CSV do mesmo perfil; preserve os resultados anteriores antes de repetir.

## Algoritmos e paralelismo
- Quick Sort: partição em três vias e tarefas sobre subvetores disjuntos.
- Merge Sort: ordenação de metades em paralelo e fusão sequencial.
- Insertion Sort e Selection Sort: versões sequenciais tradicionais; versões paralelas híbridas com ordenação de blocos pelo algoritmo correspondente e fusão. Não são versões puras dos algoritmos e a divisão também reduz o trabalho quadrático; o speedup precisa ser interpretado com essa ressalva.

Usamos ForkJoinPool dedicado com paralelismo 2, 4 e 8; o caso sequencial usa uma única thread chamadora. Há limite de subdivisão por orçamento de tarefas e limiar de 256 elementos. O paralelismo configurado não garante uso simultâneo de todas as threads e não fixa afinidade nem altera o número de núcleos físicos.

## Metodologia dos dados
Cada amostra usa seed reproduzível e os mesmos dados para todas as configurações; entradas crescente e decrescente derivam da mesma distribuição uniforme de inteiros em [0, 10n). Há três aquecimentos por configuração; a ordem das configurações é embaralhada a cada amostra. Clonagem, geração, validação e escrita do CSV ficam fora do tempo. O tempo inclui despacho de tarefas, alocações internas e fusões. Pools são reutilizados, com criação e encerramento fora da medição. Cada saída é comparada integralmente com `Arrays.sort` aplicado a uma cópia, fora da medição.

Resultados representam esta máquina e JVM; tamanhos pequenos são sensíveis ao agendamento, JIT e coleta de lixo. Não é um estudo com JMH ou múltiplos processos JVM. Registre hardware e carga do sistema antes de usar os dados no artigo. O arquivo de ambiente registra Java, SO, arquitetura e processadores lógicos visíveis.

O CSV usa ponto decimal e vírgula como separador; ao importar no Excel/Sheets, selecione esses formatos. `resumo.csv` resume a execução inicial completa com média, mediana, desvio padrão amostral, speedup (média sequencial / média da configuração) e eficiência (speedup / threads). Ele não é recalculado automaticamente pelo Java se repetir o benchmark.

## Git e GitHub
O repositório local já foi inicializado. Para publicar pelo IntelliJ, use **Git > GitHub > Share Project on GitHub**, autentique sua conta e escolha a visibilidade. Confirme a URL criada antes de colocá-la no relatório. Nenhum remoto foi criado nesta sessão.

## Documentação
`docs/Modelo-Artigo.docx` é uma cópia do modelo fornecido. `docs/roteiro-relatorio.md` organiza o trabalho restante; o artigo final e os gráficos ainda precisam ser produzidos.
