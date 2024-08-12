# LinkedIn-Job-Scraper
This Python script scrapes job postings from LinkedIn for specific companies and locations, and stores the job details in JSON and CSV formats.

## Prerequisites

- Python 3.x
- Selenium
- BeautifulSoup4
- pandas

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/linkedin-job-scraper.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd linkedin-job-scraper
    ```

3. **Install the required Python packages:**

    ```bash
    pip install selenium beautifulsoup4 pandas
    ```

4. **Download the [ChromeDriver](https://sites.google.com/chromium.org/driver/) and place it in your PATH.**

## Usage

1. **Update the `log_file`, `json_file`, and `csv_file` paths in the script to match your desired file locations.**

2. **Run the script:**

    ```bash
    python scraper.py
    ```

## Script Overview

- **WebDriver Configuration:** Configures Selenium WebDriver with Chrome options to avoid detection and mimic a real user.
- **URL List:** Contains LinkedIn job search URLs to scrape.
- **`wait_for_element`:** Waits for elements to appear on the page to ensure that the job listings have loaded.
- **`scrape_linkedin_jobs`:** Navigates to the URL, scrolls through the page, and extracts job details.
- **`parse_date`:** Converts the job posting date to a human-readable format.
- **Output:** Job data is saved to both JSON and CSV files.

## Logging

- **Log File:** All log messages are written to `scraper_log.txt`. This file includes timestamps and details about the scraping process.

## Contributing

Feel free to fork this repository and submit pull requests. Any improvements or bug fixes are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please reach out to (mailto:ayushcaphys@gmail.com)
