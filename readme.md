```markdown
# Blocklist Processor

Python скрипт для загрузки и обработки списков блокировки (IP/DNS и т.д.) 
и генерации правил для MikroTik RouterOS.

A Python script for downloading and processing blocklists (IP/DNS etc.) 
and generating MikroTik RouterOS firewall rules.

## Описание

Скрипт выполняет следующие функции:
1. Загружает списки блокировки по URL (поддерживает ZIP архивы и текстовые файлы)
2. Извлекает и валидирует IP-адреса/подсети
3. Генерирует файлы с правилами для MikroTik RouterOS в формате `.rsc`
4. Сохраняет результаты в указанную директорию

Конфигурация задаётся через YAML файл.

## Требования

- Python 3.7 или новее
- Установленные зависимости (см. Установка)

## Установка

1. Клонируйте репозиторий или скачайте файлы
2. Установите зависимости:
```bash
pip install requests pyyaml
```

## Настройка ⚙️

Создайте файл `config.yaml` в корне проекта. Формат конфигурации:
```yaml
blocklists:
  - name: "example_list"        # Название списка
    url: "https://example.com/list.zip"  # URL для загрузки
    format: "zip"               # Опционально: "zip" или "text"
    output_file: "example.rsc"  # Опционально: имя выходного файла
```

## Использование

Запустите скрипт:
```bash
python blacklister.py
```

Параметры запуска:
- `config_path` - путь к конфигурационному файлу (по умолчанию "config.yaml")
- `output_dir` - директория для сохранения результатов (по умолчанию "firewall_rules")

Пример:
```python
processor = BlocklistProcessor(
    config_path="custom_config.yaml",
    output_dir="custom_output_dir"
)
```

## Пример config.yaml
```yaml
blocklists:
  - name: "spamhaus_drop"
    url: "https://www.spamhaus.org/drop/drop.txt"
    format: "text"
    output_file: "spamhaus_drop.rsc"

  - name: "spamhaus_edrop"
    url: "https://www.spamhaus.org/drop/edrop.zip"
    format: "zip"
```

## Логирование

Скрипт ведёт журнал работы с уровнями:
- INFO: основные операции
- WARNING: не критические проблемы
- ERROR: критические ошибки

Логи выводятся в консоль.

## Лицензия

Apache License 2.0

---

## Description

The script performs the following functions:
1. Downloads blocklists from URLs (supports ZIP archives and text files)
2. Extracts and validates IP addresses/subnets
3. Generates MikroTik RouterOS rules in `.rsc` format
4. Saves results to the specified directory

Configuration is set via YAML file.

## Requirements

- Python 3.7+
- Installed dependencies (see Installation)

## Installation

1. Clone the repository or download files
2. Install dependencies:
```bash
pip install requests pyyaml
```

## Configuration

Create `config.yaml` in the project root. Configuration format:
```yaml
blocklists:
  - name: "example_list"        # List name
    url: "https://example.com/list.zip"  # Download URL
    format: "zip"               # Optional: "zip" or "text"
    output_file: "example.rsc"  # Optional: output filename
```

## Usage

Run the script:
```bash
python blacklister.py
```

Parameters:
- `config_path` - path to config file (default "config.yaml")
- `output_dir` - output directory (default "firewall_rules")

Example:
```python
processor = BlocklistProcessor(
    config_path="custom_config.yaml",
    output_dir="custom_output_dir"
)
```

## config.yaml example
```yaml
blocklists:
  - name: "spamhaus_drop"
    url: "https://www.spamhaus.org/drop/drop.txt"
    format: "text"
    output_file: "spamhaus_drop.rsc"

  - name: "spamhaus_edrop"
    url: "https://www.spamhaus.org/drop/edrop.zip"
    format: "zip"
```

## Logging

The script maintains operation logs with levels:
- INFO: main operations
- WARNING: non-critical issues
- ERROR: critical errors

Logs are printed to console.

## License

Apache License 2.0
```