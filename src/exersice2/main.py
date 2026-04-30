import asyncio
import os
import urllib.request
from urllib.parse import urlparse


async def async_input(prompt):
    return await asyncio.to_thread(input, prompt)


def get_save_path():
    path = input("Введите путь для сохранения изображений: ").strip()
    os.makedirs(path, exist_ok=True)
    return path


def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    if not filename:
        filename = "image.jpg"

    return filename


def make_unique_filename(folder, filename):
    name, extension = os.path.splitext(filename)

    if not extension:
        extension = ".jpg"

    result = filename
    counter = 1

    while os.path.exists(os.path.join(folder, result)):
        result = f"{name}_{counter}{extension}"
        counter += 1

    return result


def download_image_sync(url, folder):
    try:
        filename = get_filename_from_url(url)
        filename = make_unique_filename(folder, filename)
        filepath = os.path.join(folder, filename)

        urllib.request.urlretrieve(url, filepath)

        return url, "Успех"

    except Exception:
        return url, "Ошибка"


async def download_image(url, folder):
    return await asyncio.to_thread(download_image_sync, url, folder)


def print_summary(results):
    print("\nСводка об успешных и неуспешных загрузках")

    max_len = max((len(url) for url, _ in results), default=10)
    max_len = min(max_len, 70)

    border = "+" + "-" * (max_len + 2) + "+" + "-" * 10 + "+"

    print(border)
    print(f"| {'Ссылка'.ljust(max_len)} | {'Статус'.ljust(8)} |")
    print(border)

    for url, status in results:
        short_url = url[:max_len]
        print(f"| {short_url.ljust(max_len)} | {status.ljust(8)} |")

    print(border)


async def main():
    folder = await asyncio.to_thread(get_save_path)

    tasks = []

    while True:
        url = await async_input("Введите ссылку на изображение: ")

        if not url.strip():
            break

        task = asyncio.create_task(download_image(url.strip(), folder))
        tasks.append(task)

    if tasks:
        if any(not task.done() for task in tasks):
            print("Не все изображения загружены. Ожидаем завершения загрузок...")

        results = await asyncio.gather(*tasks)
    else:
        results = []

    print_summary(results)


if __name__ == "__main__":
    asyncio.run(main())
