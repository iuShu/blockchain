package org.millionaire;

import com.alibaba.fastjson.JSONObject;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.io.FileUtils;
import org.apache.http.Header;
import org.apache.http.HttpMessage;
import org.apache.http.NameValuePair;
import org.apache.http.message.BasicHeader;
import org.apache.http.message.BasicNameValuePair;

import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.*;

import static java.nio.charset.StandardCharsets.UTF_8;
import static org.apache.commons.lang3.StringUtils.isBlank;
import static org.millionaire.karastar.ApiConstants.HEADER_DEFAULT;

public class CommonUtils {

    public static final Map<String, Map<String, String>> HEADERS;

    static {
        HEADERS = new HashMap<>();
        try {
            String path = CommonUtils.class.getClassLoader().getResource("header").getPath();
            System.out.println("path: " + path);
            File dir = new File(path);
//            File dir = new File("header");
            for (File file : dir.listFiles()) {
                List<String> lines = FileUtils.readLines(file, UTF_8);
                Map<String, String> map = new HashMap<>();
                lines.forEach(line -> {
                    String temp[] = line.contains(": ") ? line.split(": ") : new String[]{line, ""};
                    map.put(temp[0], temp[1]);
                });
                HEADERS.put(file.getName(), map);
            }
        } catch (IOException e) {
            System.err.println("error occurred during reading header files");
            e.printStackTrace();
        }
    }

    public static void printSimpleJson(JSONObject jsonObject) {
        if (jsonObject == null || jsonObject.isEmpty())
            return;

        System.out.println("------------- json -------------");
        jsonObject.forEach((k, v) -> System.out.println(k + ": " + v));
        System.out.println("--------------------------------");
    }

    public static void printHeader(Header... headers) {
        printHeader("", headers);
    }

    public static void printHeader(String title, Header... headers) {
        if (headers == null || headers.length < 1)
            return;

        String t = isBlank(title) ? "headers" : title;
        System.out.println("----------- " + t + " -----------");
        Arrays.stream(headers).forEach(System.out::println);
        System.out.println("-------------------------------");
    }

    /**
     * "petid": "132928012157759725769679660471615006507",
     * "timestamp": 1641456631,
     * "sign": "faca42d1840b6f7dc46d52a746bac475"
     *
     * see also: resources/app~06837ae4.61fb3b7f.js#117
     */
    public static String getDataSign(Map<String, String> data) {
//        data.put("petid", "132928012157759725769679660471615004624");
        if (data.isEmpty())
            return "";

        StringBuffer stb = new StringBuffer();
        data.entrySet().forEach(e -> stb.append(e.toString() + "&"));
        String message = stb.append("secret").toString();
        System.out.println("sign data: " + message);
        return DigestUtils.md5Hex(message);
    }

    public static void addDataSign(Map data) {
        if (data.isEmpty())
            return;

        String timestamp = Long.toString(System.currentTimeMillis() / 1000);
        data.put("timestamp", timestamp);
        StringBuffer stb = new StringBuffer();
        data.entrySet().forEach(e -> stb.append(e.toString() + "&"));
        String message = stb.append("secret").toString();
        data.put("sign", DigestUtils.md5Hex(message));
        data.put("_t", timestamp);

        System.out.println("sign data: " + message);
    }

    public static void fillDefaultHeader(HttpMessage httpMessage) {
        HEADERS.get(HEADER_DEFAULT).forEach(httpMessage::addHeader);
    }

    public static Header[] getHeaders(String type) {
        Map<String, String> headers = HEADERS.get(type);
        List<Header> list = new ArrayList<>(headers.size());
        headers.forEach((k, v) -> list.add(new BasicHeader(k, v)));
        return list.stream().toArray(Header[]::new);
    }

    public static List<NameValuePair> mapToNameValuePairs(Map map) {
        List<NameValuePair> pairs = new ArrayList<>();
        if (map == null || map.isEmpty())
            return pairs;

        map.forEach((k, v) -> pairs.add(new BasicNameValuePair(k.toString(), v.toString())));
        return pairs;
    }

}
