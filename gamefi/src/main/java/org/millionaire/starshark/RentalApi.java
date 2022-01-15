package org.millionaire.starshark;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.millionaire.HttpUtils;

import static org.millionaire.CommonUtils.getHeaders;
import static org.millionaire.starshark.ApiConstants.*;

public class RentalApi {

    static void index() {
        JSONObject jsonObject = HttpUtils.get("https://starsharks.com/", getHeaders(HEADER_STATISTIC), new JSONObject());
        System.out.println(jsonObject);
    }

    static void statMarket() {
        JSONObject result = HttpUtils.get(MARKET_STATISTIC, getHeaders(HEADER_STATISTIC), new JSONObject());
        System.out.println(result);
    }

    static void rentalMarket() {
        String data = "{\"class\":[],\"stage\":[],\"star\":0,\"pureness\":0,\"hp\":[0,200],\"speed\":[0,200],\"skill\":[0,200],\"morale\":[0,200],\"body\":[],\"parts\":[],\"page\":1,\"filter\":\"sell\",\"sort\":\"PriceAsc\",\"page_size\":36}";
        JSONObject jsonObject = JSON.parseObject(data);
        JSONObject result = HttpUtils.post(MARKETPLACE, getHeaders(HEADER_STARSHARK), jsonObject);
        System.out.println(result);
    }

    public static void main(String[] args) {
//        index();
        statMarket();
//        rentalMarket();
    }

}
