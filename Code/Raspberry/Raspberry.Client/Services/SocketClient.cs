using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
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
            Image image = Image.FromFile("a1.jpeg");
            using (MemoryStream ms = new MemoryStream())
            {
                image.Save(ms, ImageFormat.Jpeg);
                byte[] arr = new byte[ms.Length];
                ms.Position = 0;
                ms.Read(arr, 0, (int)ms.Length);

                Image image2 = Image.FromStream(ms);
                image2.Save("a2.jpeg", ImageFormat.Jpeg);
            }


            client.Connect(serverIp, serverPort);
            netStream = new NetworkStream(client);

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
            const int ReadBufferSize = 1024 * 1024;

            try
            {
                netStream.ReadTimeout = 5000;
                byte[] readBuffer = new byte[ReadBufferSize];
                while (true)
                {
                    if (netStream.CanRead)
                    {

                        //byte[] data = new byte[ReadBufferSize];

                        //int bytesRead = 0; int chunkSize = 0;

                        //while (netStream.DataAvailable)
                        //{
                        //    bytesRead += chunkSize =
                        //        await netStream.ReadAsync(data, bytesRead, data.Length - bytesRead);
                        //}

                        //Debug.WriteLine($"Read: {bytesRead}");
                        //data = data.Take(bytesRead).ToArray();
                        //if (data.Length > 0)
                        //    Received?.Invoke(this, data);

                        List<byte> data = new List<byte>();
                        int bytesRead = 0; int chunkSize = 0;

                        while (netStream.DataAvailable)
                        {
                            Array.Clear(readBuffer, 0, ReadBufferSize);
                            bytesRead = await netStream.ReadAsync(readBuffer, 0, ReadBufferSize);
                            data.AddRange(readBuffer.Take(bytesRead));
                            Debug.WriteLine($"Read: {bytesRead}");
                        }
                        if (data.Any())
                            Received?.Invoke(this, data.ToArray());
                    }
                    await Task.Delay(0).ConfigureAwait(true);
                }
            }
            catch (OperationCanceledException ex)
            {
                Debug.WriteLine(ex.Message);
            }
        }
    }
}
