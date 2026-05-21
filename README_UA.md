[![English](https://img.shields.io/badge/Language-English-red?style=for-the-badge)](README.md) [![Русский](https://img.shields.io/badge/Language-Русский-blue?style=for-the-badge)](README_RU.md)

## опис 
abc-pascal-tui-termux - це IDE для Паскаля, зароблений на компіляторі PascalABC.NET, але використовує TUI-інтерфейс на Python.
## завантаження 
Для завантаження IDE необхідно встановить Python, Mono, Git и библіотеку Textual.

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/232156828/593718056-91439cd7-21ef-4997-a877-8c6254119bff.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwMzI0MDAsIm5iZiI6MTc3OTAzMjEwMCwicGF0aCI6Ii8yMzIxNTY4MjgvNTkzNzE4MDU2LTkxNDM5Y2Q3LTIxZWYtNDk5Ny1hODc3LThjNjI1NDExOWJmZi5qcGc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNTE3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDUxN1QxNTM1MDBaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0xNmVkYjNiMzllMGUxMjUxOTBmYTA3MGUwODVkNzI3ZTNhYmFlMTVjMjY1ZDY3ZmI5NmI4ODhhZGEyOTZmYzgzJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZqcGVnIn0.ER3_n_s3n6cGYBrZGDrQiCPqI1N_WV4zc9BWYUv5B3k" alt="Интерфейс Pascal TUI" width="400">
</p>

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/285278862/593754255-de2eea2e-cbe2-4556-8149-7508e17753b7.jpg?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwNTEyNTQsIm5iZiI6MTc3OTA1MDk1NCwicGF0aCI6Ii8yODUyNzg4NjIvNTkzNzU0MjU1LWRlMmVlYTJlLWNiZTItNDU1Ni04MTQ5LTc1MDhlMTc3NTNiNy5qcGc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjYwNTE3JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI2MDUxN1QyMDQ5MTRaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1iMTY5NDZmYWIzNTVjZmJkNzdlMDc0YzQ3OTZiYTZlNGE0ZjA2NWQ5OTE0N2NmYjc5MDU1MTZlNTM1MGRhZWUwJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZyZXNwb25zZS1jb250ZW50LXR5cGU9aW1hZ2UlMkZqcGVnIn0.1SIcbI-UnMthAN7KT2s_euBF8jmwKXsZxAO5Mwr5ZSU" alt="Интерфейс в граф окружении" width="400">
</p> 

команди для встановлення у termux:


```bash
pkg install mono -y
```

```bash
pkg install python -y
```

```bash
pkg install git -y
```

```bash
pip install textual
```
```bash
git clone https://github.com/kuzmak161-creator/abc-pascal-tui-termux
```

```bash
cd abc-pascal-tui-termux
```

запуск 
```bash
python tui.py
```

команди для встановлення у Debian (перевірено тільки на arm версії)

```bash
sudo apt install mono-complete 
```
```bash
sudo apt install git -y
```
```bash
sudo apt install python3 -y
```
```bash
pip3 install textual
```
```bash
git clone https://github.com/kuzmak161-creator/abc-pascal-tui.git
```
```bash
cd abc-pascal-tui
```
запуск
```bash
python3 tui.py
```

### в релизах більш рідко виходять оновлення.

## ліцензія 

- **компілятор PascalABC.NET** - GNU Lesser General Public License v3 (LGPL v3) https://github.com/pascalabcnet/pascalabcnet

Код інтерфейсу (tui.py) поширюється на умовах MIT License.
