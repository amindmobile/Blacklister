# IP Firewall Rule Generator

## English Version

### Description

This script downloads an archive containing a list of IP addresses in CIDR format, filters valid CIDR networks, and generates firewall rules for Mikrotik devices. The generated rules are saved to a file that can be imported into Mikrotik.

### Features

- **Download Archive**: Fetches the archive from a specified URL.
- **Extract Contents**: Extracts the first file from the zip archive and reads its contents.
- **Filter Valid CIDR Networks**: Checks each line to ensure it is a valid CIDR network.
- **Generate Firewall Rules**: Creates firewall rules for Mikrotik using the filtered IP addresses.
- **Logging**: Provides detailed logging of the process, including warnings for invalid IP addresses.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ip-firewall-rule-generator.git
   ```

2. Install required packages:
   ```bash
   pip install requests
   ```

### Usage

1. Configure the `config` dictionary in `main.py` with your desired settings.
   ```python
   config = {
       "archive_url": "https://example.com/path/to/archive.zip",
       "list_name": "blacklisted_ips",
       "export_file": "./firewall_rules.rsc"
   }
   ```

2. Run the script:
   ```bash
   python blacklister.py
   ```

### Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Russian Version

### Описание

Этот скрипт загружает архив, содержащий список IP-адресов в формате CIDR, фильтрует допустимые сети и генерирует правила брандмауэра для устройств Mikrotik. Сгенерированные правила сохраняются в файл, который может быть импортирован в Mikrotik.

### Возможности

- **Загрузка Архива**: Загружает архив с указанного URL.
- **Извлечение Контента**: Извлекает первый файл из zip-архива и читает его содержимое.
- **Фильтрация CIDR Сетей**: Проверяет каждую строку, чтобы убедиться, что она является допустимой CIDR сетью.
- **Генерация Правил Брандмауэра**: Создает правила брандмауэра для Mikrotik на основе отфильтрованных IP-адресов.
- **Логирование**: Ведет подробное логирование процесса, включая предупреждения о недопустимых IP-адресах.

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/amindmobile/blacklister.git
   ```

2. Установите необходимые пакеты:
   ```bash
   pip install requests
   ```

### Использование

1. Настройте словарь `config` в файле `main.py` по вашему усмотрению.
   ```python
   config = {
       "archive_url": "https://example.com/path/to/archive.zip",
       "list_name": "blacklisted_ips",
       "export_file": "./firewall_rules.rsc"
   }
   ```

2. Запустите скрипт:
   ```bash
   python blacklister.py
   ```

### Вклад

Вклады приветствуются! Пожалуйста, откройте проблему или отправьте pull request.