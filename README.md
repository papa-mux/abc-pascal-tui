abc-pascal-tui-termux - это IDE для Паскаля, основанная на компиляторе PascalABC.NET, но использующий TUI-интерфейс на Python.


Для использования проекта необходимо сначала установить Python, Mono, Git и библиотеку Textual.

```bash
pkg install mono -y

pkg install python -y

pkg install git -y

pip install textual

#клонируем репозиторий через команду
git clone https://github.com/kuzmak161-creator/abc-pascal-tui-termux

cd abc-pascal-tui-termux
#запускаем 

python tui.py

