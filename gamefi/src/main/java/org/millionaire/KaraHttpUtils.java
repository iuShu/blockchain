package org.millionaire;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.apache.commons.io.IOUtils;
import org.apache.http.Header;
import org.apache.http.HttpResponse;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.Arrays;

import static java.nio.charset.StandardCharsets.UTF_8;
import static org.millionaire.karastar.ApiConstants.HEADER_DEFAULT;
import static org.millionaire.CommonUtils.*;

public class KaraHttpUtils {

    private static JSONObject error(Exception e) {
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("status", "999 kara request error");
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
        addDataSign(data);
        httpPost.setEntity(new UrlEncodedFormEntity(mapToNameValuePairs(data), UTF_8));
        try {
            HttpResponse httpResponse = httpClient.execute(httpPost);
            System.out.println(">> " + httpResponse.getStatusLine());
            return JSON.parseObject(EntityUtils.toString(httpResponse.getEntity()));
        } catch (IOException e) {
            e.printStackTrace();
            return error(e);
        } finally {
            IOUtils.closeQuietly(httpClient);
        }
    }

}
