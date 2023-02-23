using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace Raspberry.Client.Services
{
    public class SocketClient
    {
        private readonly Socket client;
        private NetworkStream netStream;
        public event Action<object, byte[]> Received = null;
        public SocketClient()
        {
            client = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        }

        public void Connect(string serverIp, int serverPort)
        {
            try
            {
                client.Connect(serverIp, serverPort);
            }
            catch (SocketException ex)
            {
                Debug.Fail(ex.Message);
            }

            if (!client.Connected)
                return;

            netStream = new NetworkStream(client, ownsSocket: true);
            netStream.ReadTimeout = 5000;

            Task.Factory.StartNew(() =>
                Receiver(),
                TaskCreationOptions.LongRunning);
        }

        public void Send(string data)
        {
            if (netStream?.CanWrite == true)
            {
                //data = $"{data} {DateTime.Now:yyyy MM dd HH:mm:ss}";
                byte[] buffer = Encoding.UTF8.GetBytes($"{data}");
                netStream.Write(buffer, 0, buffer.Length);
                netStream.Flush();
            }
        }

        private async void Receiver()
        {
            const int ReadBufferSize = 1024 * 512;
            byte[] readBuffer = new byte[ReadBufferSize];

            try
            {
                while (netStream.CanRead)
                {
                    var data = new List<byte>();
                    int bytesRead = 0;
                    //while (netStream.DataAvailable)
                    while (true)
                    {
                        bytesRead = await netStream.ReadAsync(readBuffer, 0, readBuffer.Length);
                        Debug.WriteLine($"Read: {bytesRead}");

                        var head = readBuffer.AsSpan(0, 4).ToArray();
                        if (BitConverter.IsLittleEndian)
                            Array.Reverse(head);

                        int len = BitConverter.ToInt32(head, 0);
                        data.AddRange(readBuffer.Skip(4).Take(bytesRead - 4));

                        int l = len;
                        while ((bytesRead = await netStream.ReadAsync(readBuffer, 0, readBuffer.Length)) > 0)
                        {
                            l -= bytesRead;
                            if (l == 0)
                            {
                                data.AddRange(readBuffer.Take(bytesRead));
                                break;
                            }
                            else if (l < 0)
                            {
                                data.AddRange(readBuffer.Take(len - data.Count()));
                                break;
                            }
                            else
                            {
                                data.AddRange(readBuffer.Take(bytesRead));
                            }
                        }

                        if (data.Count > 0)
                        {
                            //Debug.WriteLine(Encoding.UTF8.GetString(data.ToArray()));
                            Received?.Invoke(this, data.ToArray());
                        }
                    }
                }
            }
            catch (OperationCanceledException ex)
            {
                Debug.WriteLine(ex.Message);
            }
            finally
            {
                Array.Clear(readBuffer, 0, ReadBufferSize);
            }
        }
    }
}
