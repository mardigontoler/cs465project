import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;

public class DataHandler {

    private Socket sock;
    OutputStream outputStream;
    InputStream inputStream;
    InetSocketAddress address;

    public DataHandler() throws IOException{
        try {
            address = new InetSocketAddress(InetAddress.getByName("cs465.duckdns.org"), 1024);
        }
        catch(IOException e){
            throw new IOException(e);
        }

    }

    public void transmit(String data) throws IOException{
        sock = new Socket();
        sock.connect(address, 10000);
        inputStream = sock.getInputStream();
        outputStream = sock.getOutputStream();
        outputStream.write(0xfe);
        if(inputStream.read() == 0xfe){
            outputStream.write(data.getBytes());
            outputStream.write(0xff);
            outputStream.flush();
        }
        inputStream.close();
        outputStream.close();
        sock.close();
    }

}
