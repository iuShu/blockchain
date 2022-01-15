package org.millionaire;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.apache.commons.io.IOUtils;
import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.Arrays;

import static java.nio.charset.StandardCharsets.UTF_8;
import static org.millionaire.karastar.ApiConstants.HEADER_DEFAULT;
import static org.millionaire.CommonUtils.*;

public class HttpUtils {

    private static JSONObject error(Exception e) {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("status", "999 http request error");
        jsonObject.put("trace", e.toString());
        jsonObject.put("data", null);
        return jsonObject;
    }

    public static JSONObject post(String api) {
        return post(api, getHeaders(HEADER_DEFAULT), new JSONObject());
    }

    public static JSONObject post(String api, Header[] headers) {
        return post(api, headers, new JSONObject());
    }

    public static JSONObject post(String api, JSONObject data) {
        return post(api, getHeaders(HEADER_DEFAULT), data);
    }

    public static JSONObject post(String api, Header[] headers, JSONObject data) {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost(api);
        Arrays.stream(headers).forEach(httpPost::addHeader);
        httpPost.setEntity(new UrlEncodedFormEntity(mapToNameValuePairs(data), UTF_8));
        try {
            HttpResponse httpResponse = httpClient.execute(httpPost);
            StatusLine statusLine = httpResponse.getStatusLine();
            String text = EntityUtils.toString(httpResponse.getEntity());
            System.out.println(">> " + statusLine);
            return JSON.parseObject(text);
        } catch (IOException e) {
            e.printStackTrace();
            return error(e);
        } finally {
            IOUtils.closeQuietly(httpClient);
        }
    }

    public static String _post(String api, Header[] headers, JSONObject data) {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost(api);
        Arrays.stream(headers).forEach(httpPost::addHeader);
        httpPost.setEntity(new UrlEncodedFormEntity(mapToNameValuePairs(data), UTF_8));
        try {
            HttpResponse httpResponse = httpClient.execute(httpPost);
            StatusLine statusLine = httpResponse.getStatusLine();
            System.out.println(">> " + statusLine);
            return EntityUtils.toString(httpResponse.getEntity());
        } catch (IOException e) {
            e.printStackTrace();
            return e.getMessage();
        } finally {
            IOUtils.closeQuietly(httpClient);
        }
    }

    public static JSONObject post(String api, Header[] headers, String data) {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost(api);
        Arrays.stream(headers).forEach(httpPost::addHeader);
        httpPost.setEntity(new StringEntity(data, UTF_8));
        try {
            HttpResponse httpResponse = httpClient.execute(httpPost);
            StatusLine statusLine = httpResponse.getStatusLine();
            String text = EntityUtils.toString(httpResponse.getEntity());
            System.out.println(">> " + statusLine);
            return JSON.parseObject(text);
        } catch (IOException e) {
            e.printStackTrace();
            return error(e);
        } finally {
            IOUtils.closeQuietly(httpClient);
        }
    }

    public static String _post(String api, Header[] headers, String data) {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost(api);
        Arrays.stream(headers).forEach(httpPost::addHeader);
        httpPost.setEntity(new StringEntity(data, UTF_8));
        try {
            HttpResponse httpResponse = httpClient.execute(httpPost);
            StatusLine statusLine = httpResponse.getStatusLine();
            String text = EntityUtils.toString(httpResponse.getEntity());
            System.out.println(">> " + statusLine);
            return text;
        } catch (IOException e) {
            e.printStackTrace();
            return e.getMessage();
        } finally {
            IOUtils.closeQuietly(httpClient);
        }
    }

    public static JSONObject get(String api, Header[] headers, JSONObject data) {
        try {
            CloseableHttpClient httpClient = HttpClients.createDefault();
            URIBuilder builder = new URIBuilder(api);
            data.forEach((param, value) -> builder.addParameter(param, value.toString()));
            HttpGet httpGet = new HttpGet(builder.build());
            Arrays.stream(headers).forEach(httpGet::addHeader);
            CloseableHttpResponse httpResponse = httpClient.execute(httpGet);
            StatusLine statusLine = httpResponse.getStatusLine();
            String text = EntityUtils.toString(httpResponse.getEntity(), UTF_8);
            System.out.println(">> " + statusLine);
            return JSON.parseObject(text);
        } catch (Exception e) {
            e.printStackTrace();
            return error(e);
        }
    }

}
