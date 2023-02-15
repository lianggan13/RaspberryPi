using System;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace Raspberry.Client.Services
{
    public class SocketClient
    {
        private readonly Socket client;
        private NetworkStream netStream;
        public event Action<object, string> Received = null;
        public SocketClient()
        {
            client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        }

        public void Connect(string serverIp, int serverPort)
        {
            client.Connect(serverIp, serverPort);
            netStream = new NetworkStream(client);

            Task.Factory.StartNew(() =>
                Receiver(),
                TaskCreationOptions.LongRunning);
        }

        public void Send(string data)
        {
            if (netStream.CanWrite)
            {
                //data = $"{data} {DateTime.Now:yyyy MM dd HH:mm:ss}";
                byte[] buffer = Encoding.UTF8.GetBytes($"{data}");
                netStream.Write(buffer, 0, buffer.Length);
            }

            netStream.Flush();
        }

        private async void Receiver()
        {
            const int ReadBufferSize = 4096;

            try
            {
                netStream.ReadTimeout = 5000;
                byte[] readBuffer = new byte[ReadBufferSize];
                while (true)
                {
                    Array.Clear(readBuffer, 0, ReadBufferSize);
                    if (netStream.CanRead)
                    {
                        int read = await netStream.ReadAsync(readBuffer, 0, ReadBufferSize);
                        string receivedLine = Encoding.UTF8.GetString(readBuffer, 0, read);
                        Received?.Invoke(this, receivedLine);
                    }
                }
            }
            catch (OperationCanceledException ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

    }
}
