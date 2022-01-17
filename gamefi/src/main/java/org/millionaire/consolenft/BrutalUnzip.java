package org.millionaire.consolenft;

import net.lingala.zip4j.ZipFile;
import net.lingala.zip4j.crypto.StandardDecrypter;
import net.lingala.zip4j.crypto.engine.ZipCryptoEngine;
import net.lingala.zip4j.exception.ZipException;
import net.lingala.zip4j.headers.HeaderReader;
import net.lingala.zip4j.io.inputstream.NumberedSplitRandomAccessFile;
import net.lingala.zip4j.io.inputstream.SplitInputStream;
import net.lingala.zip4j.io.inputstream.ZipInputStream;
import net.lingala.zip4j.model.FileHeader;
import net.lingala.zip4j.model.LocalFileHeader;
import net.lingala.zip4j.model.Zip4jConfig;
import net.lingala.zip4j.model.ZipModel;
import net.lingala.zip4j.model.enums.CompressionMethod;
import net.lingala.zip4j.model.enums.EncryptionMethod;
import net.lingala.zip4j.model.enums.RandomAccessFileMode;
import net.lingala.zip4j.util.InternalZipConstants;
import net.lingala.zip4j.util.UnzipUtil;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.IOUtils;
import org.millionaire.ThreadUtils;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.ConcurrentSkipListSet;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicInteger;

import static net.lingala.zip4j.util.FileUtils.isNumberedSplitFile;
import static net.lingala.zip4j.util.InternalZipConstants.STD_DEC_HDR_SIZE;
import static net.lingala.zip4j.util.Zip4jUtil.getCompressionMethod;

public class BrutalUnzip {

    static final String WORD_LIST = "wordlist.txt";
    static final String ZIP_FILE = "7414.zip";
    static Runtime runtime = Runtime.getRuntime();

    static void brutal() {
        String path = BrutalUnzip.class.getClassLoader().getResource("").getPath();
        System.out.println(path);
        String command = "cmd /c 7z t " + path.substring(1) + ZIP_FILE + " -p";
        try {
            List<String> words = FileUtils.readLines(new File(path + WORD_LIST));
            List<String> combines = new ArrayList<>(words);

            AtomicInteger scope = new AtomicInteger(0);
            int batch = words.size() / 16;
            Runnable task = () -> {
                int begin = scope.getAndIncrement() * batch;
                int end = begin + batch;
                begin = begin == 0 ? 0 : (begin + 1);
                List<String> assign = words.subList(begin, end);
                System.out.println(Thread.currentThread().getName() + " " + begin + " ~ " + end + " = " + assign.size());
                for (String each : assign) {
                    for (String combine : combines) {
                        if (!check(command + each + "_" + combine))
                            continue;

                        System.out.println("correct: " + each + "_" + combine);
                        System.exit(1);
                    }
                    System.out.println(Thread.currentThread().getName() + ": " + each + " checked");
                }
            };

            List<Thread> threads = new ArrayList<>();
            for (int i = 0; i < 16; i++)
                threads.add(new Thread(task, "#Thread" + i));
            for (Thread thread : threads)
                thread.start();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    static boolean check(String command) {
        try {
            Process process = runtime.exec(command);
            List<String> lines = IOUtils.readLines(process.getInputStream());
            return lines.get(lines.size() - 1).contains("Compressed");
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    static void brutalUnzip() throws Exception {
        String path = BrutalUnzip.class.getClassLoader().getResource("").getPath();
        System.out.println(path);
        File file = new File(path + "brutal.zip");
        char[] password = "abuse_above".toCharArray();
        new ZipFile(file, password).extractAll(path);
    }

    static void efficient() {
        char[] password = "zoo_zo".toCharArray();
        long crc = 626819695;
        long lastModifiedTime = 0L; // 1412268920
        byte[] headerBytes = new byte[]{-89, -121, 93, 105, 9, 44, 61, -40, 108, -88, 91, -4};
        try {
            new StandardDecrypter(password, crc, lastModifiedTime, headerBytes);
            System.out.println("correct password");
        } catch (ZipException e) {
            e.printStackTrace();
        }
    }

    static void generateSecretKey() throws IOException {
        String path = BrutalUnzip.class.getClassLoader().getResource("").getPath();
        File word1 = new File(path + "wordlist.txt");
        File word2 = new File(path + "wordlist.txt");
        File key = new File(path + "key.txt");
        if (!key.exists())
            key.createNewFile();

        List<String> words1 = FileUtils.readLines(word1);
        List<String> words2 = FileUtils.readLines(word2);
        List<String> lines = new ArrayList<>(words1.size());
        for (String b : words1) {
            for (String e : words2)
                lines.add(b + "_" + e);

            FileUtils.writeLines(key, lines, true);
            lines.clear();
        }
    }

    static String zip = "5968.zip";
    static void brutalUnzipConsoleNFT() throws Exception {
        String path = BrutalUnzip.class.getClassLoader().getResource("").getPath();
        File file = new File(path + zip);
        BrutalInfo brutalInfo = efficientBrutalUnzip(file);
        byte[] headerBytes = brutalInfo.headerBytes;
        long lastModifiedTime = brutalInfo.localFileHeader.getLastModifiedTime();
        long crc = brutalInfo.localFileHeader.getCrc();

        File key = new File(path + "key.txt");
        List<String> keys = FileUtils.readLines(key);

        AtomicInteger scope = new AtomicInteger(0);
        int threadCnt = 16;
        int batch = keys.size() / threadCnt;
        Runnable task = () -> {
            int s = scope.getAndIncrement();
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
            File collision = new File(path + "collision_" + s + ".txt");
            int begin = s * batch;
            int end = begin + batch;
            begin = begin == 0 ? 0 : (begin + 1);
            List<String> assign = keys.subList(begin, end);
            List<String> collisionKeys = new ArrayList<>();
            System.out.println(ThreadUtils.name() + " " + begin + " ~ " + end + " = " + assign.size() + " at " + dateFormat.format(new Date()));
            for (String each : assign) {
                if (checkPassword(headerBytes, each.toCharArray(), lastModifiedTime, crc))
                    collisionKeys.add(each);
            }
            try {
                if (!collision.exists())
                    collision.createNewFile();
                FileUtils.writeLines(collision, collisionKeys, true);
            } catch (Exception e) {
                e.printStackTrace();
            }
            System.out.println(ThreadUtils.name() + " with " + collisionKeys.size() + " end at " + dateFormat.format(new Date()));
        };

        ThreadUtils.startThread(threadCnt, task);
    }

    static void accurateBrutalUnzipConsoleNFT() {
        AtomicInteger i = new AtomicInteger(0);
        String path = BrutalUnzip.class.getClassLoader().getResource("").getPath();
        Runnable task = () -> {
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
            System.out.println(ThreadUtils.name() + " start at " + dateFormat.format(new Date()));
            File file = new File(path + "collision_" + i.getAndIncrement() + ".txt");
            List<String> lines = null;
            try {
                lines = FileUtils.readLines(file);
            } catch (IOException e) {
                e.printStackTrace();
            }
            for (String password : lines) {
                try {
                    new ZipFile(path + zip, password.toCharArray()).extractAll(path);
                    System.out.println("correct: " + password);
                    System.exit(1);
                } catch (Exception e) {
                    // do nothing
                }
            }
            System.out.println(ThreadUtils.name() + " end at " + dateFormat.format(new Date()));
        };

        ThreadUtils.startThread(16, task);
    }

    static void simpleBrutalForceUnzip() throws IOException {
        String path = BrutalUnzip.class.getClassLoader().getResource("").getPath();
        File key = new File(path + "key.txt");
        List<String> keys = FileUtils.readLines(key);

        AtomicInteger scope = new AtomicInteger(0);
        int threadCnt = 20;
        int batch = keys.size() / threadCnt;
        Runnable task = () -> {
            SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
            System.out.println(ThreadUtils.name() + " start at " + dateFormat.format(new Date()));
            int begin = scope.getAndIncrement() * batch;
            int end = begin + batch;
            begin = begin == 0 ? 0 : (begin + 1);
            List<String> assign = keys.subList(begin, end);
            for (String password : assign) {
                try {
                    new ZipFile(path + zip, password.toCharArray()).extractAll(path);
                    System.out.println("correct: " + password);
                    System.exit(1);
                } catch (Exception e) {
                    // do nothing
                }
            }
            System.out.println(ThreadUtils.name() + " end at " + dateFormat.format(new Date()));
        };

        ThreadUtils.startThread(threadCnt, task);
    }

    static BrutalInfo efficientBrutalUnzip(File file) throws Exception {
        HeaderReader headerReader = new HeaderReader();
        Zip4jConfig config = new Zip4jConfig(null, 4096);
        ZipModel zipModel = headerReader.readAllHeaders(initRandomAccessFileFromHeaderReading(file), config);
        zipModel.setZipFile(file);
        List<FileHeader> fileHeaders = zipModel.getCentralDirectory().getFileHeaders();
        SplitInputStream splitInputStream = prepareZipInputStream(zipModel);
        LocalFileHeader localFileHeader = obtainLocalFileHeader(headerReader, splitInputStream, fileHeaders.get(0));
        ZipInputStream zipInputStream = new ZipInputStream(splitInputStream, "".toCharArray(), config);
        ZipEntryInputStream zipEntryInputStream = new ZipEntryInputStream(splitInputStream, getCompressedSize(localFileHeader));
        byte[] headerBytes = new byte[STD_DEC_HDR_SIZE];
        zipEntryInputStream.readRawFully(headerBytes);
        return new BrutalInfo(headerBytes, localFileHeader, zipEntryInputStream);
    }

    static RandomAccessFile initRandomAccessFileFromHeaderReading(File zipFile) throws Exception {
        if (isNumberedSplitFile(zipFile)) {
            File[] allSplitFiles = net.lingala.zip4j.util.FileUtils.getAllSortedNumberedSplitFiles(zipFile);
            NumberedSplitRandomAccessFile numberedSplitRandomAccessFile = new NumberedSplitRandomAccessFile(zipFile,
                    RandomAccessFileMode.READ.getValue(), allSplitFiles);
            numberedSplitRandomAccessFile.openLastSplitFileForReading();
            return numberedSplitRandomAccessFile;
        }

        return new RandomAccessFile(zipFile, RandomAccessFileMode.READ.getValue());
    }

    static SplitInputStream prepareZipInputStream(ZipModel zipModel) throws IOException {
        SplitInputStream splitInputStream = UnzipUtil.createSplitInputStream(zipModel);

        FileHeader fileHeader = getFirstFileHeader(zipModel);
        if (fileHeader != null) {
            splitInputStream.prepareExtractionForFileHeader(fileHeader);
        }
        return splitInputStream;
    }

    static FileHeader getFirstFileHeader(ZipModel zipModel) {
        if (zipModel.getCentralDirectory() == null
                || zipModel.getCentralDirectory().getFileHeaders() == null
                || zipModel.getCentralDirectory().getFileHeaders().size() == 0) {
            return null;
        }

        return zipModel.getCentralDirectory().getFileHeaders().get(0);
    }

    static long getCompressedSize(LocalFileHeader localFileHeader) {
        if (getCompressionMethod(localFileHeader).equals(CompressionMethod.STORE)) {
            return localFileHeader.getUncompressedSize();
        }

        return localFileHeader.getCompressedSize() - getEncryptionHeaderSize(localFileHeader);
    }

    static int getEncryptionHeaderSize(LocalFileHeader localFileHeader) {
        if (!localFileHeader.isEncrypted()) {
            return 0;
        }

        if (localFileHeader.getEncryptionMethod().equals(EncryptionMethod.AES)) {
            return InternalZipConstants.AES_AUTH_LENGTH + InternalZipConstants.AES_PASSWORD_VERIFIER_LENGTH
                    + localFileHeader.getAesExtraDataRecord().getAesKeyStrength().getSaltLength();
        } else if (localFileHeader.getEncryptionMethod().equals(EncryptionMethod.ZIP_STANDARD)) {
            return InternalZipConstants.STD_DEC_HDR_SIZE;
        } else {
            return 0;
        }
    }

    static LocalFileHeader obtainLocalFileHeader(HeaderReader headerReader, InputStream inputStream, FileHeader fileHeader) throws IOException {
        LocalFileHeader localFileHeader = headerReader.readLocalFileHeader(inputStream, null);
        if (fileHeader != null) {
            localFileHeader.setCrc(fileHeader.getCrc());
            localFileHeader.setCompressedSize(fileHeader.getCompressedSize());
            localFileHeader.setUncompressedSize(fileHeader.getUncompressedSize());
            localFileHeader.setDirectory(fileHeader.isDirectory());
        }
        return localFileHeader;
    }

    static boolean checkPassword(byte[] headerBytes, char[] password, long lastModifiedFileTime, long crc) {
        ZipCryptoEngine zipCryptoEngine = new ZipCryptoEngine();
        zipCryptoEngine.initKeys(password);

        int result = headerBytes[0];
        for (int i = 0; i < STD_DEC_HDR_SIZE; i++) {
            if (i + 1 == InternalZipConstants.STD_DEC_HDR_SIZE) {
                byte verificationByte = (byte) (result ^ zipCryptoEngine.decryptByte());
                if (verificationByte != (byte) (crc >> 24) && verificationByte != (byte) (lastModifiedFileTime >> 8)) {
//                    throw new ZipException("Wrong password!", ZipException.Type.WRONG_PASSWORD);
                    return false;
                }
            }

            zipCryptoEngine.updateKeys((byte) (result ^ zipCryptoEngine.decryptByte()));
            if (i + 1 != STD_DEC_HDR_SIZE)
                result = headerBytes[i + 1];
        }
        return true;
    }

    public static void main(String[] args) throws Exception {
//        brutal();
//        brutalUnzip();
//        efficient();
//        generateSecretKey();
//        brutalUnzipConsoleNFT();
//        accurateBrutalUnzipConsoleNFT();
        simpleBrutalForceUnzip();
    }

}

class BrutalInfo {

    byte[] headerBytes;
    LocalFileHeader localFileHeader;
    ZipEntryInputStream zipEntryInputStream;

    public BrutalInfo(byte[] headerBytes, LocalFileHeader localFileHeader, ZipEntryInputStream zipEntryInputStream) {
        this.headerBytes = headerBytes;
        this.localFileHeader = localFileHeader;
        this.zipEntryInputStream = zipEntryInputStream;
    }
}
