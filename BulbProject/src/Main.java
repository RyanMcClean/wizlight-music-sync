import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.DataLine;
import javax.sound.sampled.Line;
import javax.sound.sampled.Mixer;
import javax.sound.sampled.Mixer.Info;

/**
 * @author : Ryan Urquhart
 * @studentNumber : 40099112
 * @email : rurquhart@qub.ac.uk
 * @created : Oct 26, 2024 - 12:57:49 PM
 **/
public class Main {

    static List<String> ipAdd = new ArrayList<String>();
    static long waitTime = 1;
    static int repeatNumber = 100;

    public static void main(String[] args) {
        run(38899);

        Mixer.Info[] mixersInfo = AudioSystem.getMixerInfo();

        for (Mixer.Info mixerInfo : mixersInfo) {
            System.out.println("Mixer: " + mixerInfo.getName());

            Mixer mixer = AudioSystem.getMixer(mixerInfo);

            Line.Info[] sourceLineInfo = mixer.getSourceLineInfo();
            for (Line.Info info : sourceLineInfo)
                showLineInfo(info);

            Line.Info[] targetLineInfo = mixer.getTargetLineInfo();
            for (Line.Info info : targetLineInfo)
                showLineInfo(info);
        }
    }

    public static void run(int port) {
        try {
            DatagramSocket serverSocket = new DatagramSocket(port);
            serverSocket.setSoTimeout(5000);

            byte[] receiveData = new byte[256];
            DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);

            String sendStringDiscover = "{\"method\":\"getPilot\",\"params\":{}}";
            byte[] sendDataDiscover = sendStringDiscover.getBytes("UTF-8");

            System.out.printf("Sending to udp:%s:%d%n",
                    InetAddress.getByName("255.255.255.255").toString().substring(1), port);

            DatagramPacket sendPacket = new DatagramPacket(sendDataDiscover, sendDataDiscover.length,
                    InetAddress.getByName("255.255.255.255"), port);
            serverSocket.send(sendPacket);
            System.out.printf("Listening for response on port %d%n", port);
            try {
                serverSocket.receive(receivePacket);
                while (receivePacket.getLength() > 0) {
                    if (!receivePacket.getAddress().toString().substring(1)
                            .equals(InetAddress.getLocalHost().getHostAddress())) {

                        ipAdd.add(receivePacket.getSocketAddress().toString().substring(1).split(":")[0]);
                        String sentence = new String(receivePacket.getData(), 0, receivePacket.getLength());
                        System.out.println(sentence);
                        serverSocket.receive(receivePacket);

                    } else {
                        serverSocket.receive(receivePacket);
                    }
                }
            } catch (Exception e) {
            }

            System.out.println("Ip's found:");
            ipAdd.forEach(x -> System.out.println(x));
            TimeUnit.MILLISECONDS.sleep(waitTime);

            int count = 0;

            while (count < repeatNumber && ipAdd.size() > 0) {

                String sendStringOn = "{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":true}}";
                byte[] sendDataOn = sendStringOn.getBytes("UTF-8");

                String sendStringOff = "{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":false}}";
                byte[] sendDataOff = sendStringOff.getBytes("UTF-8");

                ipAdd.forEach(ip -> {
                    try {
                        DatagramPacket sendPacketOn = new DatagramPacket(sendDataOn, sendDataOn.length,
                                InetAddress.getByName(ip),
                                port);
                        DatagramPacket sendPacketOff = new DatagramPacket(sendDataOff, sendDataOff.length,
                                InetAddress.getByName(ip),
                                port);

                        System.out.printf("Sending ON to udp:%s:%d%n",
                                InetAddress.getByName(ip).toString().substring(1), port);
                        serverSocket.send(sendPacketOn);
                        serverSocket.receive(receivePacket);
                        System.out.printf("Listening for response on udp:%s:%d%n",
                                InetAddress.getByName(ip).toString().substring(
                                        1),
                                port);
                        String sentence = new String(receivePacket.getData(), 0, receivePacket.getLength());
                        System.out.println(sentence);
                        TimeUnit.MILLISECONDS.sleep(waitTime);

                        System.out.printf("Sending OFF to udp:%s:%d%n",
                                InetAddress.getByName(ip).toString().substring(1), port);
                        serverSocket.send(sendPacketOff);
                        serverSocket.receive(receivePacket);
                        System.out.printf("Listening for response on udp:%s:%d%n",
                                InetAddress.getByName(ip).toString().substring(
                                        1),
                                port);
                        sentence = new String(receivePacket.getData(), 0, receivePacket.getLength());
                        System.out.println(sentence);
                        TimeUnit.MILLISECONDS.sleep(waitTime);

                    } catch (Exception e) {
                    }
                });
                count++;
            }
            serverSocket.close();

        } catch (Exception e) {
            System.out.println(e);
        }
        // should close serverSocket in finally block
    }

    private static void showLineInfo(final Line.Info lineInfo) {
        System.out.println("  " + lineInfo.toString());

        if (lineInfo instanceof DataLine.Info) {
            DataLine.Info dataLineInfo = (DataLine.Info) lineInfo;

            AudioFormat[] formats = dataLineInfo.getFormats();
            for (final AudioFormat format : formats)
                System.out.println("    " + format.toString());
        }
    }

}
