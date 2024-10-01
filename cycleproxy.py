import requests
import time
import logging

# Set up logging
logging.basicConfig(filename='proxy_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to load the single proxy from a file
def load_proxy(filename):
    with open(filename, 'r') as file:
        return file.readline().strip()  # Read the first line only

# Function to load queries from a file
def load_queries(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Function to simulate getting proxy info (IP and country)
def get_proxy_info(proxy):
    # Extract IP address (mock country for demonstration)
    ip = proxy.split('@')[-1].split(':')[0]  # Extracting IP
    country = "USA"  # Simulated country; replace with actual lookup if needed
    return ip, country

# Function to make a request using a proxy
def make_request(url, proxy):
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error with proxy {proxy}: {e}")
        return None

# Main function
def main(base_url, query_file, proxy_file):
    proxy = load_proxy(proxy_file)
    if not proxy:
        print("No proxy found.")
        return

    # Get proxy info (IP and country)
    proxy_ip, proxy_country = get_proxy_info(proxy)

    while True:
        queries = load_queries(query_file)  # Reload queries each cycle

        if not queries:
            print("No queries found. Waiting 5 minutes...")
            time.sleep(5 * 60)  # Wait before the next cycle
            continue

        for query in queries:
            print(f"Processing query: {query} using proxy: {proxy}")

            url = f"{base_url}?query={query}"
            response = make_request(url, proxy)

            # Log query and proxy information
            if response and response.status_code == 200:
                print("Success:", response.text[:100])  # Print first 100 characters
                logging.info(f"Query: '{query}' processed successfully using proxy IP: {proxy_ip}, Country: {proxy_country}.")
            else:
                print(f"Failed to retrieve data for query '{query}' with proxy '{proxy}'.")
                logging.warning(f"Query: '{query}' failed with proxy IP: {proxy_ip}, Country: {proxy_country}.")

            # Wait for 5 minutes before the next query
            print("Waiting for 5 minutes before the next query...")
            time.sleep(5 * 60)  # 5 minutes

if __name__ == "__main__":
    base_url = "http://example.com/api"  # Replace with your base URL
    query_file_path = "query.txt"  # Path to your query file
    proxy_file_path = "proxy.txt"  # Path to your proxy file
    main(base_url, query_file_path, proxy_file_path)
