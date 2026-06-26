import requests
import sys
import time


def measure_speed(url: str, num_requests: int = 10) -> None:
    """Измеряет скорость интернета путем загрузки файла с указанного URL"""
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }

    total_time: float = 0
    total_bytes: int = 0
    successful_requests: int = 0

    print('Начинаем измерение скорости...')
    print(f'URL: {url}')
    print(f'Количество запросов: {num_requests}\n')

    with requests.Session() as session:
        session.headers.update(headers)

        for i in range(num_requests):
            try:
                print(
                    f'Запрос {i + 1}/{num_requests}: загрузка...',
                    end='',
                    flush=True
                )
                start_time = time.time()

                with session.get(url, stream=True, timeout=30) as response:
                    response.raise_for_status()

                    size = 0
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            size += len(chunk)

                elapsed_time = time.time() - start_time
                total_time += elapsed_time
                total_bytes += size
                successful_requests += 1

                speed_mbps = (size * 8 / elapsed_time) / (1024 * 1024)
                print(
                    (
                        f' {speed_mbps:.2f} Мбит/с ({size / 1024 / 1024:.2f} '
                        f'МБ за {elapsed_time:.2f} сек)'
                    )
                )

                time.sleep(0.5)

            except requests.exceptions.Timeout:
                print(' Таймаут!')
            except requests.exceptions.RequestException as e:
                print(f' Ошибка: {e}')
            except KeyboardInterrupt:
                print('\nПрервано пользователем')
                break

    if successful_requests == 0:
        print('\nНе удалось выполнить ни одного успешного запроса')
        return

    avg_time = total_time / successful_requests
    avg_bytes = total_bytes / successful_requests
    avg_speed_mbps = (avg_bytes * 8 / avg_time) / (1024 * 1024)

    print(f'\n{'=' * 50}')
    print(f'Результаты (успешных запросов: {successful_requests}):')
    print(f'Среднее время запроса: {avg_time:.2f} сек')
    print(f'Средний размер данных: {avg_bytes / 1024 / 1024:.2f} МБ')
    print(f'Средняя скорость: {avg_speed_mbps:.2f} Мбит/с')
    print(f'{'=' * 50}')


if __name__ == "__main__":
    url = (
        sys.argv[1]
        if len(sys.argv) > 1
        else 'http://speedtest.tele2.net/10MB.zip'
    )
    if len(sys.argv) == 1:
        print(f'Используется URL по умолчанию: {url}\n')

    measure_speed(url)
