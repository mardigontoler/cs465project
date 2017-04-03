import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;

public class DataHandler {
    public DataHandler(){
        try {
            InetAddress address = InetAddress.getByName("cs465.duckdns.org");
            Socket sock = new Socket(address, 1024);
            byte b;
            b = (byte)0xfe;
            OutputStream outputStream = sock.getOutputStream();
            InputStream inputStream = sock.getInputStream();
            outputStream.write(b);
            outputStream.flush();
            if(inputStream.read() == 0xfe){
                outputStream.write("Hello from java".getBytes());
                outputStream.flush();
                outputStream.write(0xff);
                outputStream.flush();
            }
            inputStream.close();
            outputStream.close();
            sock.close();

        }
        catch(IOException e){
            e.printStackTrace();
        }
    }
}
