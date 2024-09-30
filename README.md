# Cookie Scanner

This Python script is designed to send requests to the Cookie Doctor API to process a list of hostnames. The script reads a single hostname, a list of hostnames, or a `.txt` file containing hostnames, sends them to the Cookie Doctor API for processing, and saves the response in JSON or text format.

## Features

- **Multi-threaded execution** using Python's `ThreadPoolExecutor` for concurrent processing.
- **Input flexibility**: Accepts a single hostname, a list of hostnames, or a `.txt` file containing hostnames.
- **Saves output**: Responses are saved as JSON or plain text in an organized folder structure.
- **Error handling**: Captures and logs errors during the request.

## Requirements

- **Python 3.6+** is required to run this script.
- **Required Python libraries**:
  - `requests`

You can install the required dependencies using:

```bash
pip install requests
```

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/edgewatch/cookie.doctor.git
   cd cookie.doctor
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the API endpoint for Cookie Doctor is configured correctly:

   ```python
   API_COOKIE_DOCTOR='https://api.cookie.doctor/api/v1/process_host/'
   ```

## Usage

The script can process a single hostname, a list of hostnames, or a `.txt` file containing multiple hostnames.

### Command Line Usage:

```bash
python cookie_scanner.py <hostname|hostnames.txt|["hostname1", "hostname2", ...]>
```

- **Single Hostname**:
  ```bash
  python cookie_scanner.py https://example.com
  ```

- **List of Hostnames (as a string)**:
  ```bash
  python cookie_scanner.py '["https://example.com", "http://test.com"]'
  ```

- **Hostnames from a `.txt` file**:
  ```bash
  python cookie_scanner.py hostnames.txt
  ```

### Output

- The responses from the Cookie Doctor API are saved in the `output/` directory.
- For each hostname, a corresponding folder is created. The response is saved as a `.json` file if it's valid JSON or as a `.txt` file if not.
- The filenames are timestamped to differentiate between scans.

#### Example File Structure:
```
output/
└── example.com/
    └── example.com_2023-09-30_15_23_45.json
```

### Concurrency

The script processes hostnames concurrently using Python's `ThreadPoolExecutor`, with 4 worker threads by default. This can be adjusted inside the script if necessary.

## Contributing

Contributions are welcome! If you find a bug or want to improve this script, feel free to submit a pull request or create an issue.

## License

This project is licensed under the MIT License.
