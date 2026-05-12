<div align="center">

# Python Basics — Part 2

**[English](#english) | [Русский](#русский)**

</div>

---

<a name="english"></a>
## 🇬🇧 English

Two tasks exploring OOP, multiprocessing, asynchronous programming, and functional patterns in Python.

### What was done

| Task | What & Why |
|------|-----------|
| Exam Simulation | Built a multiprocessing simulation of an exam session. Students queue up, examiners work in parallel processes, and a monitor updates ASCII tables in real time. Each examiner takes a lunch break 30 seconds after start. Exam duration depends on the examiner's name length. Pass/fail logic combines random mood (good/bad/neutral) with answer correctness. The golden ratio distribution biases word choice by gender: boys pick earlier words, girls pick later ones. |
| Image Downloader | Wrote an asynchronous image downloader. The user enters URLs one by one; downloads happen in the background. The program waits for all pending downloads before exiting and prints a summary table of successes and failures. |

### Key takeaways
- **Multiprocessing** with `Manager` and `Lock` allows safe shared state across processes.
- Real-time terminal UI is possible with careful use of ANSI escape codes and in-place printing.
- **Asynchronous I/O** (`asyncio`) is ideal for network-bound tasks like downloading files.
- Combining probability, timing, and state machines creates surprisingly realistic simulations.

### Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Multiprocessing](https://img.shields.io/badge/Multiprocessing-4EAA25?style=flat-square) ![Asyncio](https://img.shields.io/badge/Asyncio-3776AB?style=flat-square)

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:58a6ff,50:1f6feb,100:0969da&height=2&section=header&text=&fontSize=1"/>
</div>

<a name="русский"></a>
## 🇷🇺 Русский

Две задачи, изучающие ООП, многопроцессность, асинхронное программирование и функциональные паттерны в Python.

### Что было сделано

| Задача | Что и зачем |
|--------|-------------|
| Симуляция экзамена | Многопроцессная симуляция экзаменационной сессии. Студенты стоят в очереди, экзаменаторы работают в параллельных процессах, монитор обновляет ASCII-таблицы в реальном времени. Каждый экзаменатор уходит на обед через 30 секунд. Длительность экзамена зависит от длины имени экзаменатора. Логика сдачи/завала комбинирует случайное настроение (хорошее/плохое/нейтральное) и правильность ответов. Распределение по золотому сечению смещает выбор слова в зависимости от пола: мальчики выбирают слова ближе к началу, девочки — ближе к концу. |
| Загрузчик изображений | Асинхронный загрузчик изображений. Пользователь вводит URL по одному; загрузки происходят в фоне. Программа дожидается завершения всех загрузок перед выходом и выводит итоговую таблицу успехов и ошибок. |

### Ключевые выводы
- **Многопроцессность** с `Manager` и `Lock` позволяет безопасно разделять состояние между процессами.
- Real-time терминальный UI возможен через аккуратное использование ANSI escape-кодов и печати на месте.
- **Асинхронный I/O** (`asyncio`) идеален для сетевых задач вроде скачивания файлов.
- Комбинация вероятности, таймингов и конечных автоматов создаёт удивительно реалистичные симуляции.

### Стек технологий

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Multiprocessing](https://img.shields.io/badge/Multiprocessing-4EAA25?style=flat-square) ![Asyncio](https://img.shields.io/badge/Asyncio-3776AB?style=flat-square)

---

<div align="center">

*Project from portfolio | Проект из портфолио*

</div>
