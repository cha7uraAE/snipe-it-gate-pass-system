# Gate Pass Generator

A Streamlit application for generating gate passes based on hardware data from a Snipe-IT API.

## Features

- Connect to a Snipe-IT instance using an API key and URL.
- Search for hardware using Asset Tag or Serial Number.
- Generate a PDF gate pass for the selected hardware.

## Installation

### Option 1: Local Setup

1. Clone the repository:
  ```sh
  git clone https://github.com/cha7uraAE/snipe-it-gate-pass-system.git
  cd snipe-it-gate-pass-system
  ```
2. Create and activate a virtual environment:
  ```sh
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```
3. Install the required packages:
  ```sh
  pip install -r requirements.txt
  ```
4. Run the Streamlit application:
  ```sh
  streamlit run app/app.py
  ```
5. Open your web browser and go to http://localhost:8501.

### Option 2: Using Docker

1. Clone the repository:

  ```sh
  git clone https://github.com/cha7uraAE/snipe-it-gate-pass-system.git
  cd snipe-it-gate-pass-system
  ```
2. Build the Docker image:
  ```sh
  docker build -t snipe-it-gate-pass-system .
  ```
3. Run the Docker container:
  ```sh
  docker run -p 8501:8501 snipe-it-gate-pass-system
  ```
4. Open your web browser and go to http://localhost:8501.


## Usage
1. In the sidebar, enter your Snipe-IT API key and URL, then click "Connect".

2. Use the main interface to search for hardware, select a company, and generate a gate pass PDF.

## Project Structure
  ```graphql
.
├── app/
│   ├── pdf_generator.py           # Module to generate PDF gate passes
│   ├── snipe_it_data_generation.py # Module to fetch hardware data from Snipe-IT API
│   ├── helper.py                  # Helper functions
│   ├── app.py                     # Main Streamlit app
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt               # Python package requirements
└── README.md                      # This README file
```
## Configuration
* API Key: Your Snipe-IT API key.
* API URL: The URL of your Snipe-IT instance (e.g., develop.snipeitapp.com).
## Example
### Here is an example of how to use the application:

1. Enter your API key and URL in the sidebar and click "Connect".
2. Enter an asset tag or serial number to search for hardware.
3. Select a company from the dropdown menu.
4. Click "Search" to display the search results.
5. Click "Generate Gate Pass PDF" to create and download the gate pass.
## Error Handling
The application handles various types of errors, such as invalid API keys, incorrect URLs, and connection issues. Appropriate error messages are displayed to guide the user.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## Acknowledgements
* Streamlit for providing an easy-to-use framework for creating web applications.
* Snipe-IT for their powerful asset management tool and API.
