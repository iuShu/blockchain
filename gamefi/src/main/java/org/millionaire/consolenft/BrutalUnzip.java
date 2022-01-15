package org.millionaire.consolenft;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

public class BrutalUnzip {

    static final String WORD_LIST = "wordlist.txt";
    static final String ZIP_FILE = "7414.zip";
    static Runtime runtime = Runtime.getRuntime();

    static void brutal() {
        String path = BrutalUnzip.class.getClassLoader().getResource("").getPath();
        System.out.println(path);
        String command = "cmd /c 7z t " + path.substring(1) + ZIP_FILE + " -p";
        try {
            List<String> words = FileUtils.readLines(new File(path + WORD_LIST));
            List<String> combines = new ArrayList<>(words);

            AtomicInteger scope = new AtomicInteger(0);
            int batch = words.size() / 16;
            Runnable task = () -> {
                int begin = scope.getAndIncrement() * batch;
                int end = begin + batch;
                begin = begin == 0 ? 0 : (begin + 1);
                List<String> assign = words.subList(begin, end);
                System.out.println(Thread.currentThread().getName() + " " + begin + " ~ " + end + " = " + assign.size());
                for (String each : assign) {
                    for (String combine : combines) {
                        if (!check(command + each + "_" + combine))
                            continue;

                        System.out.println("correct: " + each + "_" + combine);
                        System.exit(1);
                    }
                    System.out.println(Thread.currentThread().getName() + ": " + each + " checked");
                }
            };

            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < 16; i++)
                threads.add(new Thread(task, "#Thread" + i));
            for (Thread thread : threads)
                thread.start();
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    static boolean check(String command) {
        try {
            Process process = runtime.exec(command);
            List<String> lines = IOUtils.readLines(process.getInputStream());
            return lines.get(lines.size() - 1).contains("Compressed");
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public static void main(String[] args) {
        brutal();
    }

}
