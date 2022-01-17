package org.millionaire.karastar;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.apache.http.HttpEntity;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpOptions;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.millionaire.HttpUtils;
import org.millionaire.KaraHttpUtils;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import static java.nio.charset.StandardCharsets.UTF_8;
import static org.millionaire.karastar.ApiConstants.*;
import static org.millionaire.CommonUtils.*;

public class ApiConnection {

    static void options() throws IOException {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpOptions options = new HttpOptions(INFO_BY_PET_ID);
        CloseableHttpResponse response = httpClient.execute(options);
        System.out.println(response.getStatusLine());
        printHeader(response.getAllHeaders());
        Set<String> allowedMethods = options.getAllowedMethods(response);
        System.out.println(allowedMethods);
        httpClient.close();
    }

    static void index() throws IOException {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpPost httpPost = new HttpPost(INDEX);
        Map<String, String> params = new HashMap<>();
        String timestamp = Long.toString(System.currentTimeMillis() / 1000);
        params.put("page", "1");
        params.put("row", "12");
        params.put("timestamp", timestamp);
        params.put("sign", getDataSign(params));
        params.put("_t", timestamp);
        UrlEncodedFormEntity entity = new UrlEncodedFormEntity(mapToNameValuePairs(params), UTF_8);

        httpPost.setEntity(entity);
        fillDefaultHeader(httpPost);

        System.out.println(EntityUtils.toString(entity));
        printHeader("request", httpPost.getAllHeaders());

        try {
            CloseableHttpResponse response = httpClient.execute(httpPost);
            System.out.println(response.getStatusLine());
            printHeader("response", response.getAllHeaders());
            HttpEntity responseEntity = response.getEntity();
            JSONObject result = JSON.parseObject(EntityUtils.toString(responseEntity));
            System.out.println(result);
        } catch (IOException e) {
            throw e;
        } finally {
            httpClient.close();
        }
    }

    static void infoByPetId() {
        JSONObject data = new JSONObject();
        data.put("petid", "132928012157759725769679660471615004624");
        JSONObject result = KaraHttpUtils.post(INFO_BY_PET_ID, data);
        printSimpleJson(result);
    }

    /**
     * @see LeaseCrawler#handle(JSONObject)
     */
    public static JSONObject loanList(int page, int row) {
        JSONObject data = new JSONObject();
        data.put("page", page);
        data.put("row", row);
        data.put("timestamp", System.currentTimeMillis() / 1000);
        return KaraHttpUtils.post(LOAN_LIST, data);
    }

    static void getBalance() {
//        String data = "{\"jsonrpc\":\"2.0\",\"id\":11,\"method\":\"eth_call\",\"params\":[{\"data\":\"0xb9186d7d000000000000000000000000000000006401010000000000000000000000aa35\",\"to\":\"0xc8e024a7eac00be9223ca73d1bb00e855153b0a4\"},\"latest\"]}";
        String data = "{\"jsonrpc\":\"2.0\",\"id\":12,\"method\":\"eth_getBalance\",\"params\":[\"0xe3899e1c3020f63ec1da9f1a6a0049aed80fbc72\",\"latest\"]}";
        JSONObject result = HttpUtils.post(RPC_GET_BALANCE, getHeaders(HEADER_BSC), data);
        printSimpleJson(result);
    }

    /**
     * TODO
     */
    public static void main(String[] args) throws Exception {
//        options();
//        index();
//        infoByPetId();
//        loanList();
//        getBalance();
    }

}
