using Prism.Commands;
using Prism.Mvvm;
using Raspberry.Client.Services;
using System.Diagnostics;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

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



        public MainViewModel()
        {

        }

        public void Window_Loaded(object sender, RoutedEventArgs e)
        {
            Task.Run(() =>
            {
                socketClient = new SocketClient();
                socketClient.Connect("192.168.0.9", 32769);

                try
                {

                }
                catch (System.Exception ex)
                {
                    Debug.Fail(ex.ToString());
                }
            });
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
