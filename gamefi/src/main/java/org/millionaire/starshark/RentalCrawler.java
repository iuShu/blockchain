package org.millionaire.starshark;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.apache.commons.collections.MapUtils;
import org.apache.commons.io.IOUtils;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.millionaire.config.ConfigContext;

import java.awt.*;
import java.io.IOException;
import java.net.URI;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

import static java.lang.String.format;
import static java.nio.charset.StandardCharsets.UTF_8;
import static org.millionaire.CommonUtils.getHeaders;
import static org.millionaire.starshark.ApiConstants.HEADER_STARSHARK;
import static org.millionaire.starshark.ApiConstants.MARKETPLACE;

public class RentalCrawler {

//    private static final String DATA = "{\"class\":[],\"stage\":[],\"star\":3,\"pureness\":0,\"hp\":[0,200],\"speed\":[0,200],\"skill\":[0,200],\"morale\":[0,200],\"body\":[],\"parts\":[],\"page\":1,\"filter\":\"rent\",\"sort\":\"PriceAsc\",\"page_size\":36}";
    private static final JSONObject PARAMS = JSON.parseObject("{\"class\":[],\"stage\":[],\"star\":3,\"pureness\":0,\"hp\":[0,200],\"speed\":[0,200],\"skill\":[0,200],\"morale\":[0,200],\"body\":[],\"parts\":[],\"page\":1,\"filter\":\"rent\",\"sort\":\"PriceAsc\",\"page_size\":36}");
    int max_open = 10;
    int interval = 2000;
    Set<Integer> handled = new HashSet<>();
    Desktop desktop = Desktop.getDesktop();
    AtomicBoolean pause = new AtomicBoolean(false);

    void run() {
        config();
        ConfigContext.onConfigChange(v -> config());

        prepare();

        int loop = 1;
        int err = 0;
        long start = System.currentTimeMillis();
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        System.out.println("[crawler] program start at " + dateFormat.format(new Date()));
        CloseableHttpClient httpClient = HttpClients.createDefault();
        Random random = new Random();
        while (true) {
            while (pause.get());
            HttpPost httpPost = new HttpPost(MARKETPLACE);
            Arrays.stream(getHeaders(HEADER_STARSHARK)).forEach(httpPost::addHeader);
            httpPost.setEntity(new StringEntity(PARAMS.toJSONString(), UTF_8));
            try {
                HttpResponse httpResponse = httpClient.execute(httpPost);
                StatusLine statusLine = httpResponse.getStatusLine();
                System.out.println(format("[%d] %s", loop, statusLine));
                if (statusLine.getStatusCode() == 200) {
                    String text = EntityUtils.toString(httpResponse.getEntity());
                    JSONObject jsonObject = JSON.parseObject(text);
                    handle(jsonObject);
                }
                else if (statusLine.getStatusCode() == 403) {
                    System.out.println("Tips: You may not running the VPN software.");
                    break;
                }

                long diff = System.currentTimeMillis() - start;
                if (diff < interval)
                    TimeUnit.MILLISECONDS.sleep(interval - diff);
                if (loop % 100 == 0)
                    TimeUnit.SECONDS.sleep(Math.max(5, random.nextInt(10)));
            } catch (Exception e) {
                e.printStackTrace();
                err++;
                if (err >= 10) {
                    System.out.println(format("[%d] too much error occurred", loop));
                    break;
                }
            }
            loop++;
            start = System.currentTimeMillis();
        }
        IOUtils.closeQuietly(httpClient);
        System.out.println("[crawler] program ended at " + dateFormat.format(new Date()));
        System.exit(1);
    }

    private boolean handle(JSONObject jsonObject) throws IOException {
        JSONObject data = jsonObject.getJSONObject("data");
        Integer count = data.getInteger("total_count");
        System.out.println("[crawler] get " + count + " sharks");
        if (count == 0)
            return false;

        JSONArray sharks = data.getJSONArray("sharks");
        Scanner scanner = new Scanner(System.in);
        scanner.useDelimiter("\n");
        for (int i = 0, j = 0; i < sharks.size(); i++) {
            int sharkId = sharks.getJSONObject(i).getJSONObject("sheet").getInteger("shark_id");
            if (!handled.add(sharkId))
                continue;

            desktop.browse(URI.create("https://starsharks.com/market/sharks/" + sharkId));
            j++;
            if (j != 0 && j % max_open == 0 && pause(scanner) == 2)
                break;
        }
        return true;
    }

    private int pause(Scanner scanner) {
        System.out.println("please select next step: ");
        System.out.println("\t1. open remaining pages.");
        System.out.println("\t2. continue program.");
        if (scanner.hasNext())
            return scanner.nextInt();
        return 2;
    }

    private void config() {
        while(!pause.compareAndSet(false, true));

        max_open = ConfigContext.getIntValue("starshark", "max_open", 10);
        interval = ConfigContext.getIntValue("starshark", "interval", 2000);
        Properties properties = ConfigContext.getProperties("starshark");
        properties.remove("max_open");
        properties.remove("interval");
        properties.forEach((k, v) -> PARAMS.put(k.toString(), v));
        PARAMS.forEach((k,v) -> System.out.println(k + ": " + v));

        while(!pause.compareAndSet(true, false));
    }

    private void prepare() {
        try {
            desktop.browse(URI.create("https://starsharks.com"));
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("[crawler] can not open the browser, program exit");
            System.exit(1);
        }
    }

    public static void main(String[] args) {
        new RentalCrawler().run();
    }

    /*

    cluster
    5R1k22
    white_screen
    accurate

    /hacker_part_5_cluster_5R1k22_white_screen_accurate

    industry
    5R1k22
    red_strawberries
    detective
    /hacker_part_5_industry_5R1k22_red_strawberries_detective
     */
}
