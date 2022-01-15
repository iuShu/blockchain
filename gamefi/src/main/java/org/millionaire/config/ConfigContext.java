package org.millionaire.config;

import org.apache.commons.io.monitor.FileAlterationListenerAdaptor;
import org.apache.commons.io.monitor.FileAlterationMonitor;
import org.apache.commons.io.monitor.FileAlterationObserver;

import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;

import static org.apache.commons.io.FileUtils.openInputStream;
import static org.apache.commons.io.FilenameUtils.getBaseName;
import static org.apache.commons.io.FilenameUtils.getExtension;

public class ConfigContext {

    private static final String CONFIG_DIR = "config";
    private static final String CONFIG_EXTENSION = "properties";

    private File root;
    private boolean developing;
    private Map<String, Properties> cache = new ConcurrentHashMap<>();
    private FileAlterationMonitor monitor = new FileAlterationMonitor(2000);

    private static final ConfigContext INSTANCE = new ConfigContext();

    private ConfigContext() {
        String path = ConfigContext.class.getClassLoader().getResource("org").getPath();
        developing = !path.contains(".jar");
        root = new File(developing ? path : CONFIG_DIR);
        System.out.println("[crawler] config at " + root.getAbsolutePath());
        loadConfig();
        watchConfig();
    }

    private void loadConfig() {
        try {
            System.out.println("[crawler] loading configurations ...");
            for (File file : root.listFiles()) {
                if (getExtension(file.getName()).equals(CONFIG_EXTENSION))
                    loadConfig(file);
            }
            System.out.println("[crawler] configurations loaded with " + cache.keySet());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void loadConfig(File config) throws IOException {
        Properties properties = new Properties();
        properties.load(openInputStream(config));
        cache.put(getBaseName(config.getName()), properties);
    }

    private void watchConfig() {
        try {
            FileAlterationObserver observer = new FileAlterationObserver(root);
            observer.addListener(new FileAlterationListenerAdaptor() {
                @Override
                public void onFileChange(File file) {
                    System.out.println("[crawler] reload trigger");
                    try {
                        loadConfig(file);
                    } catch (IOException e) {
                        e.printStackTrace();
                        System.out.println("[crawler] reload failed at " + file.getAbsolutePath());
                    }
                    System.out.println("[crawler] reload succeeded");
                }
            });
            monitor.addObserver(observer);
            monitor.start();
            System.out.println("[crawler] watch config monitoring ...");
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("[crawler] watch config error");
        }
    }

    public static void onConfigChange(Consumer<Void> consumer) {
        INSTANCE.monitor.getObservers().forEach(observer -> observer.addListener(new FileAlterationListenerAdaptor() {
            @Override
            public void onFileChange(File file) {
                consumer.accept(null);
            }
        }));
    }

    private static ConfigContext getInstance() {
        return INSTANCE;
    }

    public static Integer getIntValue(String type, String key) {
        return getIntValue(type, key, 0);
    }

    public static Integer getIntValue(String type, String key, Integer defaultValue) {
        Properties properties = INSTANCE.cache.get(type);
        if (properties == null || properties.isEmpty())
            return defaultValue;

        Object value = properties.get(key);
        return value == null ? defaultValue : Integer.parseInt(value.toString());
    }

    public static String getString(String type, String key) {
        return getString(type, key, "");
    }

    public static String getString(String type, String key, String defaultValue) {
        Properties properties = INSTANCE.cache.get(type);
        if (properties == null || properties.isEmpty())
            return defaultValue;

        Object value = properties.get(key);
        return value == null ? defaultValue : value.toString();
    }

    public static Properties getProperties(String type) {
        Properties properties = INSTANCE.cache.get(type);
        if (properties == null)
            return new Properties();
        return new Properties(properties);
    }

    public static void main(String[] args) {

    }

}
