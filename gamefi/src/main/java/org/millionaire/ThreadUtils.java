package org.millionaire;

public class ThreadUtils {

    public static void startThread(int count, Runnable task) {
        if (count < 1)
            throw new IllegalArgumentException("count must be a positive integer");

        for (int i = 0; i < count; i++) {
            new Thread(task, "#Thread" + i).start();
        }
    }

    public static String name() {
        return Thread.currentThread().getName();
    }

}
