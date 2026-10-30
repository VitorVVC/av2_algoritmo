# Roteiro do artigo — pendente de redação final

Título sugerido: Análise de desempenho de algoritmos de ordenação em ambientes sequenciais e paralelos: um estudo comparativo em Java.
O enunciado usa “busca”, mas os métodos exigidos são de ordenação. Confirmar o título de entrega com o professor.

Autores: preencher os dois nomes e demais dados acadêmicos.

Seguir o modelo original: título Arial 14, negrito, caixa alta e centralizado; corpo Arial 11 e espaçamento 1,5; até cinco palavras-chave; referências conforme ABNT.

## Resumo
Redigir após a análise: objetivo, quatro métodos, configurações, principais resultados e conclusão sustentada nos dados.

## Introdução
Contextualizar ordenação e processamento paralelo; apresentar objetivo e diferenças entre os quatro algoritmos.

## Metodologia
Usar a metodologia do README. Acrescentar modelo de CPU, RAM, sistema e condições de execução. Explicar explicitamente as versões híbridas de Insertion e Selection. Threads configuradas não equivalem a núcleos físicos controlados. Dados coletados em results/completo.csv; ambiente em results/completo-ambiente.txt.

## Resultados e Discussão
Usar results/resumo.csv como apoio à execução inicial. Produzir gráficos de tempo por tamanho e distribuição e de speedup por threads. Apresentar dispersão e discutir custos de coordenação, fusão, limitações do aquecimento e a alteração do trabalho nas versões híbridas. Não afirmar que mais threads sempre melhoram o tempo. Cinco amostras não garantem significância estatística.

## Conclusão
Responder ao objetivo com base nos dados e apresentar limitações e melhorias futuras.

## Referências
Adicionar fontes efetivamente consultadas para algoritmos, ForkJoinPool e metodologia de medição; conferir dados bibliográficos e formatação ABNT antes de entregar.

## Anexos
Inserir link real do GitHub após publicação e indicar os arquivos de código e os CSVs.
