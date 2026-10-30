package br.edu.unifor.cpc;

import br.edu.unifor.cpc.algorithms.Sorts;
import br.edu.unifor.cpc.algorithms.Sorts.Algorithm;
import br.edu.unifor.cpc.benchmark.Benchmark;
import java.util.*;
import java.util.concurrent.ForkJoinPool;

public final class Main {
    public static void main(String[] args) throws Exception {
        if (args.length > 0 && args[0].equals("--test")) { test(); return; }
        Benchmark.run(args.length > 0 && args[0].equals("--full"));
    }
    private static void test() {
        Random random = new Random(42); int checks = 0;
        for (Algorithm algorithm : Algorithm.values()) {
            for (int size : new int[]{0, 1, 2, 255, 256, 257, 1000, 4096}) {
                for (int kind = 0; kind < 5; kind++) {
                    int[] original = new int[size];
                    for (int i = 0; i < size; i++) original[i] = switch (kind) {
                        case 0 -> random.nextInt(); case 1 -> i; case 2 -> size-i;
                        case 3 -> 7; default -> random.nextInt(7)-3;
                    };
                    int[] expected = original.clone(); Arrays.sort(expected);
                    int[] actual = original.clone(); Sorts.sequential(actual, algorithm);
                    if (!Arrays.equals(actual, expected)) throw new AssertionError(algorithm);
                    checks++;
                    for (int threads : new int[]{1, 2, 3, 4}) {
                        try (ForkJoinPool pool = new ForkJoinPool(threads)) {
                            actual = original.clone(); Sorts.parallel(actual, algorithm, pool);
                            if (!Arrays.equals(actual, expected)) throw new AssertionError(algorithm + "/" + threads);
                            checks++;
                        }
                    }
                }
            }
        }
        System.out.println("Validações aprovadas: " + checks);
    }
}
