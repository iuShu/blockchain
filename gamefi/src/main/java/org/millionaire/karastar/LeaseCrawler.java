package org.millionaire.karastar;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.apache.commons.collections.MapUtils;
import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.StringUtils;
import org.apache.http.HttpResponse;
import org.apache.http.StatusLine;
import org.apache.http.client.entity.UrlEncodedFormEntity;
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
import java.util.function.Consumer;

import static java.lang.String.format;
import static java.nio.charset.StandardCharsets.UTF_8;
import static org.apache.commons.lang3.StringUtils.isNotBlank;
import static org.millionaire.CommonUtils.*;
import static org.millionaire.karastar.ApiConstants.INDEX;
import static org.millionaire.starshark.ApiConstants.HEADER_STARSHARK;
import static org.millionaire.starshark.ApiConstants.MARKETPLACE;

public class LeaseCrawler {

    private static final Map<String, String> PARAMS = new HashMap<>();
    private UrlEncodedFormEntity entity;
    int max_open = 10;
    int interval = 2000;
    Set<String> handled = new HashSet<>();
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
            HttpPost httpPost = new HttpPost(INDEX);
            fillDefaultHeader(httpPost);
            httpPost.setEntity(entity);
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
    }

    private boolean handle(JSONObject jsonObject) throws IOException {
        JSONObject data = jsonObject.getJSONObject("data");
        Integer count = data.getInteger("count");
        System.out.println("[crawler] get " + count + " kara");
        if (count == 0)
            return false;

        JSONArray karas = data.getJSONArray("data");
        Scanner scanner = new Scanner(System.in);
        scanner.useDelimiter("\n");
        for (int i = 0, j = 0; i < karas.size(); i++) {
            String karaHash = karas.getJSONObject(i).getString("pet_hash");
            if (!handled.add(karaHash))
                continue;

            desktop.browse(URI.create("https://www.karastar.com/kara/" + karaHash));
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
        while (!pause.compareAndSet(false, true));

        max_open = ConfigContext.getIntValue("karastar", "max-open", 10);
        interval = ConfigContext.getIntValue("karastar", "interval", 2000);

        String timestamp = Long.toString(System.currentTimeMillis() / 1000);
        PARAMS.put("page", ConfigContext.getString("karastar", "page", "1"));
        PARAMS.put("row", ConfigContext.getString("karastar", "page", "12"));
        PARAMS.put("timestamp", timestamp);
        PARAMS.put("sign", getDataSign(PARAMS));
        PARAMS.put("_t", timestamp);

        String type = ConfigContext.getString("karastar", "class");
        if (isNotBlank(type)) {
            String[] arr = type.split(",");
            for (int i = 0; i < arr.length; i++)
                PARAMS.put("pet_type_id[" + i + "]", arr[i]);
        }
        else if (PARAMS.containsKey("pet_type_id[0]")) {
            for (int i = 0; i < 8; i++)
                PARAMS.remove("pet_type_id[" + i + "]");
        }
        entity = new UrlEncodedFormEntity(mapToNameValuePairs(PARAMS), UTF_8);

        while (!pause.compareAndSet(true, false));
    }

    private void prepare() {
        try {
            desktop.browse(URI.create("https://www.karastar.com"));
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("[crawler] can not open the browser, program exit");
            System.exit(1);
        }
    }

    public static void main(String[] args) {
        new LeaseCrawler().run();
    }

}
