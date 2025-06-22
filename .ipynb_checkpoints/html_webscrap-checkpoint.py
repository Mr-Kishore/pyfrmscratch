import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

# Function to fetch and parse HTML using Selenium
def fetch_bus_data_html(url, retries=3):
    # Set up Selenium with Chrome (non-headless for debugging)
    chrome_options = Options()
    # Comment out headless mode to see the browser (remove if you prefer headless)
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    attempt = 0
    while attempt < retries:
        try:
            attempt += 1
            print(f"Attempt {attempt} of {retries} to load the page...")
            driver.get(url)
            
            # Wait for the initial result section to load
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "result-section"))
            )
            
            # Scroll repeatedly until all bus items are loaded
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scroll_attempts = 20  # Prevent infinite loop
            
            while scroll_attempts < max_scroll_attempts:
                # Scroll to the bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for new content to load
                
                # Check new height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    # No new content loaded, assume all buses are visible
                    print("No more new content loaded. Stopping scroll.")
                    break
                
                last_height = new_height
                scroll_attempts += 1
                print(f"Scroll attempt {scroll_attempts}: Page height increased to {new_height}")
            
            # Get the fully rendered HTML
            html = driver.page_source
            
            # Save HTML for debugging
            with open("debug_page.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("Saved raw HTML to debug_page.html for inspection.")
            
            soup = BeautifulSoup(html, "html.parser")
            
            # Find bus items
            result_section = soup.find("div", id="result-section")
            if not result_section:
                print("No result-section found. Check debug_page.html.")
                return []
            
            bus_items = result_section.find("ul", class_="bus-items")
            if not bus_items:
                print("No bus-items found. Check debug_page.html for structure changes.")
                return []

            # Extract bus entries
            bus_entries = bus_items.find_all("li", class_="row-sec")
            if not bus_entries:
                print("No bus entries found in bus-items.")
                return []

            # Parse bus details
            bus_data = []
            for entry in bus_entries:
                row_one = entry.find("div", class_="clearfix row-one")
                if not row_one:
                    continue

                bus_name_elem = row_one.find("div", class_="travels")
                bus_name = bus_name_elem.text.strip() if bus_name_elem else "N/A"
                bus_name = bus_name.replace("Ad", "").strip()

                dep_time_elem = row_one.find("div", class_="dp-time")
                dep_time = dep_time_elem.text.strip() if dep_time_elem else "N/A"

                arr_time_elem = row_one.find("div", class_="bp-time")
                arr_time = arr_time_elem.text.strip() if arr_time_elem else "N/A"

                bus_data.append({
                    "Bus Name": bus_name,
                    "Departure Time": dep_time,
                    "Arrival Time": arr_time
                })

            return bus_data

        except Exception as e:
            print(f"Error on attempt {attempt}: {str(e)}")
            if attempt < retries:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                print("All retries failed. Check debug_page.html for the last loaded content.")
                with open("debug_page.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                return []

        finally:
            driver.quit()

# Function to save data to CSV
def save_to_csv(bus_data, from_city_name, to_city_name, travel_date):
    filename = f"bus_schedule_{from_city_name}_to_{to_city_name}_{travel_date}.csv"
    headers = ["Bus Name", "Departure Time", "Arrival Time"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(bus_data)

    print(f"Data saved to {filename}")

# Main execution
if __name__ == "__main__":
    url = "https://www.redbus.in/bus-tickets/coimbatore-to-chennai?fromCityName=Coimbatore&fromCityId=141&srcCountry=IND&toCityName=Chennai&toCityId=123&destCountry=IND&onward=4-Mar-2025&opId=0&busType=Any"
    from_city_name = "Coimbatore"
    to_city_name = "Chennai"
    travel_date = "04-03-2025"

    try:
        bus_data = fetch_bus_data_html(url)
        
        if not bus_data:
            print("No bus data extracted. Check the URL or debug_page.html.")
        else:
            save_to_csv(bus_data, from_city_name, to_city_name, travel_date)
            print(f"Found {len(bus_data)} buses for {from_city_name} to {to_city_name} on {travel_date}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")