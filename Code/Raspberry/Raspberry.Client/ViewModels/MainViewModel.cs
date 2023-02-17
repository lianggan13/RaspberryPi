using Prism.Commands;
using Prism.Mvvm;
using Raspberry.Client.Services;
using Raspberry.Client.Utils;
using System;
using System.Diagnostics;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;

namespace Raspberry.Client.ViewModels
{
    public class MainViewModel : BindableBase
    {
        private string _title = "Raspberry Application";
        private SocketClient socketClient;

        public string Title
        {
            get { return _title; }
            set { SetProperty(ref _title, value); }
        }
        public DelegateCommand<object> PressKeyCommand => new DelegateCommand<object>(PressKey);


        private ImageSource img;

        public ImageSource Img
        {
            get { return img; }
            set { SetProperty(ref img, value); }
        }

        public MainViewModel()
        {

        }

        public void Window_Loaded(object sender, RoutedEventArgs e)
        {
            Task.Run(() =>
            {
                try
                {
                    socketClient = new SocketClient();
                    socketClient.Connect("192.168.0.9", 32769);
                    socketClient.Received += SocketClient_Received;
                }
                catch (System.Exception ex)
                {
                    Debug.Fail(ex.ToString());
                }
            });
        }
        int index = 0;
        private void SocketClient_Received(object arg1, byte[] data)
        {
            try
            {
                //Bitmap bitmap = ImageHelper.Buffer2Bitmap(data.ToArray());
                //System.Drawing.Image t_img = ImageHelper.AddTextToImg(bitmap, $"{DateTime.Now:HH:mm:ss}", 12.0f, bitmap.Width - 10, bitmap.Height - 10, 120, ImageFormat.Jpeg);
                //t_img.Save($"{++index}.jpeg", ImageFormat.Jpeg);

                Application.Current.Dispatcher.Invoke(() =>
                {
                    Img = ImageHelper.ConvertByteArrayToBitmapImage(data);
                    //Img = ImageHelper.BitmapToBitmapImage(new Bitmap(t_img));
                });

            }
            catch (Exception ex)
            {

            }


            //MemoryStream stream = new MemoryStream(data.ToArray());
            //System.Drawing.Image image = System.Drawing.Image.FromStream(stream);
            //image.Save("a3.jpeg", ImageFormat.Jpeg);
        }


        private void PressKey(object para)
        {
            Button btn = para as Button;
            if (!btn.IsFocused)
                btn.Focus();

            Debug.WriteLine($"{nameof(PressKey)}:{btn.Content}");
            socketClient.Send($"{btn.Content}");
        }


        public void Btn_KeyUp(object sender, KeyEventArgs e)
        {
            if (sender is Button btn)
            {
                if ((Key)btn.Content == e.Key)
                {
                    Debug.WriteLine($"{nameof(Btn_KeyUp)}:{e.Key}");
                    socketClient.Send($"P");
                }
            }
            e.Handled = true;
        }
    }
}
