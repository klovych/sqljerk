# SQLJerk 🚨

**SQLJerk** is a tool designed to test web applications for SQL injection vulnerabilities. It checks URL parameters for potential vulnerabilities using various SQL injection payloads and provides feedback if vulnerabilities are detected.

## 🚀 Installation

To install and use SQLJerk, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/sqljerk.git
   cd sqljerk
Install required dependencies:

```pip install -r requirements.txt```

🔧 How to Use

Run the program:


```bash
python sqljerk.py
```

Enter the target URL with query parameters for testing:

Example URLs:

https://example.com?id=1

https://example.com?search=test

The program will attempt to find SQL injection vulnerabilities by sending various payloads to the target URL. If vulnerabilities are detected, the results will be displayed in the terminal and logged in the sqljerk_log.txt file.

Check the results:

✅ If no vulnerabilities are found, you will see a success message.

❌ If potential vulnerabilities are found, you will be notified with the exact query and payload that triggered the vulnerability.
📜 Logs

All requests and responses are logged into a file named sqljerk_log.txt. Each log entry includes:

The test URL

The server's response code

The response length

A snippet of the response content (up to 500 characters)

🛠 Example Output

Enter the target URL (with parameters): https://example.com?id=1

[+] Checking URL: https://example.com?id=1

[!] Possible SQL injection vulnerability detected: https://example.com?id=1' OR 1=1--

    Payload: ' OR 1=1--
    
[+] No SQL injection vulnerabilities found.

🔑 Requirements
You will need Python 3.6+ and the following dependencies:

requests (for sending HTTP requests)

termcolor (for colored output in the terminal)

⚖ License
This project is licensed under the MIT License. See the LICENSE file for more details.

