package br.edu.unifor.cpc.algorithms;

import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

public final class Sorts {
    private Sorts() {}
    public enum Algorithm { QUICK, MERGE, INSERTION, SELECTION }
    public static void sequential(int[] a, Algorithm algorithm) {
        serial(a, 0, a.length, algorithm);
    }
    private static void serial(int[] a, int lo, int hi, Algorithm algorithm) {
        switch (algorithm) {
            case QUICK -> quick(a, lo, hi);
            case MERGE -> mergeSort(a, lo, hi);
            case INSERTION -> {
                for (int i = lo + 1; i < hi; i++) {
                    int value = a[i], j = i - 1;
                    while (j >= lo && a[j] > value) { a[j + 1] = a[j]; j--; }
                    a[j + 1] = value;
                }
            }
            case SELECTION -> {
                for (int i = lo; i < hi - 1; i++) {
                    int min = i;
                    for (int j = i + 1; j < hi; j++) if (a[j] < a[min]) min = j;
                    swap(a, i, min);
                }
            }
        }
    }
    private static void swap(int[] a, int i, int j) { int v = a[i]; a[i] = a[j]; a[j] = v; }
    // Partição em três vias evita degeneração em entradas com muitos valores iguais.
    private static int[] partition(int[] a, int lo, int hi) {
        int pivot = a[lo + (hi - lo) / 2], lt = lo, i = lo, gt = hi;
        while (i < gt) {
            if (a[i] < pivot) swap(a, lt++, i++);
            else if (a[i] > pivot) swap(a, i, --gt);
            else i++;
        }
        return new int[]{lt, gt};
    }
    private static void quick(int[] a, int lo, int hi) {
        while (hi - lo > 1) {
            int[] b = partition(a, lo, hi);
            // Recursão apenas no lado menor limita o uso da pilha.
            if (b[0] - lo < hi - b[1]) { quick(a, lo, b[0]); lo = b[1]; }
            else { quick(a, b[1], hi); hi = b[0]; }
        }
    }
    private static void mergeSort(int[] a, int lo, int hi) {
        if (hi - lo < 2) return;
        int mid = lo + (hi - lo) / 2;
        mergeSort(a, lo, mid); mergeSort(a, mid, hi); merge(a, lo, mid, hi);
    }
    private static void merge(int[] a, int lo, int mid, int hi) {
        int[] out = new int[hi - lo]; int i = lo, j = mid, k = 0;
        while (i < mid && j < hi) out[k++] = a[i] <= a[j] ? a[i++] : a[j++];
        while (i < mid) out[k++] = a[i++];
        while (j < hi) out[k++] = a[j++];
        System.arraycopy(out, 0, a, lo, out.length);
    }
    public static void parallel(int[] a, Algorithm algorithm, ForkJoinPool pool) {
        pool.invoke(new Task(a, 0, a.length, algorithm, pool.getParallelism()));
    }
    private static final class Task extends RecursiveAction {
        private final int[] a; private final int lo, hi, budget; private final Algorithm algorithm;
        Task(int[] a, int lo, int hi, Algorithm algorithm, int budget) {
            this.a = a; this.lo = lo; this.hi = hi; this.algorithm = algorithm; this.budget = budget;
        }
        protected void compute() {
            if (budget <= 1 || hi - lo <= 256) { serial(a, lo, hi, algorithm); return; }
            int leftEnd, rightStart;
            if (algorithm == Algorithm.QUICK) {
                int[] b = partition(a, lo, hi); leftEnd = b[0]; rightStart = b[1];
            } else { leftEnd = lo + (hi - lo) / 2; rightStart = leftEnd; }
            invokeAll(new Task(a, lo, leftEnd, algorithm, budget / 2),
                      new Task(a, rightStart, hi, algorithm, budget - budget / 2));
            if (algorithm != Algorithm.QUICK) merge(a, lo, leftEnd, hi);
        }
    }
}
