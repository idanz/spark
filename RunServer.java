import py4j.GatewayServer;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class RunServer {
  public static void main(String[] args) throws UnknownHostException {
        int port;
        port = Integer.parseInt(args[args.length - 1]);
        GatewayServer gatewayServer = new GatewayServer(null, port, port + 1, 0, 0, null);
        gatewayServer.start();
        /* Print out the listening port so that clients can discover it. */
        int listening_port = gatewayServer.getListeningPort();
        System.out.println("" + listening_port);
        /* Exit on EOF or broken pipe.  This ensures that the server dies
         * if its parent program dies. */
        BufferedReader stdin = new BufferedReader(
                               new InputStreamReader(System.in));
        try {
            stdin.readLine();
            System.exit(0);
        } catch (java.io.IOException e) {
            System.exit(1);
        }
  }
}
