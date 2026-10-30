package br.edu.unifor.cpc.benchmark;

import br.edu.unifor.cpc.algorithms.Sorts;
import br.edu.unifor.cpc.algorithms.Sorts.Algorithm;
import java.nio.file.*;
import java.io.*;
import java.util.*;
import java.util.concurrent.ForkJoinPool;

public final class Benchmark {
    private record Job(Algorithm algorithm, int threads) {}
    public static void run(boolean full) throws IOException {
        Files.createDirectories(Path.of("results"));
        int[] sizes = full ? new int[]{1000, 5000, 10000} : new int[]{1000};
        String prefix = full ? "completo" : "smoke";
        Files.writeString(Path.of("results", prefix + "-ambiente.txt"),
            "Data UTC: " + java.time.Instant.now() + "\nJava: " + System.getProperty("java.version") +
            "\nSO: " + System.getProperty("os.name") + " " + System.getProperty("os.arch") +
            "\nProcessadores lógicos disponíveis: " + Runtime.getRuntime().availableProcessors() +
            "\nAquecimentos por configuração: 3; amostras: 5; seed base: 2026\n");
        Map<Integer, ForkJoinPool> pools = new HashMap<>();
        for (int t : new int[]{2,4,8}) pools.put(t, new ForkJoinPool(t));
        try (PrintWriter csv = new PrintWriter(Files.newBufferedWriter(Path.of("results", prefix + ".csv")))) {
            csv.println("algorithm,mode,size,distribution,value_bound,threads,sample,seed,time_ns,time_ms,valid");
            for (int size : sizes) for (String distribution : new String[]{"random", "ascending", "descending"}) {
                List<Job> jobs = new ArrayList<>();
                for (Algorithm algorithm : Algorithm.values()) for (int threads : new int[]{1,2,4,8}) jobs.add(new Job(algorithm, threads));
                for (Job job : jobs) for (int w = 0; w < 3; w++) sort(data(size, distribution, 2026+w), job, pools);
                for (int sample = 1; sample <= 5; sample++) {
                    long seed = 2026 + sample;
                    int[] original = data(size, distribution, seed), expected = original.clone(); Arrays.sort(expected);
                    Collections.shuffle(jobs, new Random(seed));
                    for (Job job : jobs) {
                        int[] values = original.clone();
                        long start = System.nanoTime(); sort(values, job, pools); long elapsed = System.nanoTime()-start;
                        if (!Arrays.equals(values, expected)) throw new IllegalStateException("Ordenação incorreta: " + job);
                        csv.printf(Locale.ROOT, "%s,%s,%d,%s,%d,%d,%d,%d,%d,%.6f,true%n", job.algorithm,
                            job.threads == 1 ? "sequential" : "parallel", size, distribution, size * 10,
                            job.threads, sample, seed, elapsed, elapsed/1_000_000.0);
                    }
                }
                csv.flush();
                System.out.println("Concluído: " + size + " / " + distribution);
            }
            if (csv.checkError()) throw new IOException("Falha ao gravar CSV");
        } finally { pools.values().forEach(ForkJoinPool::close); }
        System.out.println("Resultados: results/" + prefix + ".csv");
    }
    private static void sort(int[] values, Job job, Map<Integer, ForkJoinPool> pools) {
        if (job.threads == 1) Sorts.sequential(values, job.algorithm);
        else Sorts.parallel(values, job.algorithm, pools.get(job.threads));
    }
    private static int[] data(int size, String distribution, long seed) {
        int[] a = new Random(seed).ints(size, 0, size * 10).toArray();
        if (!distribution.equals("random")) {
            Arrays.sort(a);
            if (distribution.equals("descending")) for (int i=0; i<size/2; i++) {
                int v=a[i]; a[i]=a[size-1-i]; a[size-1-i]=v;
            }
        }
        return a;
    }
}
