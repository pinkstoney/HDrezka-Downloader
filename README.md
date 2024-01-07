# HDRezka Film Downloader 🎬

## Overview

Welcome to the HDRezka Film Downloader repository! 🎬 This Python script enables you to interact with HDRezka, providing various features for film enthusiasts. Please note that the code is in its early stages and may require significant refactoring.

### Features ✨

1. **Film Search:** Easily search for films by name.
2. **Quality Options:** Download films in different quality settings such as 360p, 480p, 720p, 1080p, and more.
3. **Translation Choices:** Select your preferred translation for the film.
4. **Image Download:** Save film cover images for your collection.

### In Progress 🚧

The project is actively being developed, and upcoming features include:

- **TV Show Download:** An upcoming feature will allow you to download your favorite TV shows.
- **Enhanced User Interface:** Improvements to the user interface for a more user-friendly experience.

### Refactoring Notice 🛠️

Please be aware that the codebase currently requires significant refactoring. As this project started without the intention of becoming large-scale, it is the result of a learning process, especially for someone using these libraries for the first time. Refactoring will be an ongoing process to enhance code quality and maintainability.

## Getting Started 🚀

Before starting, follow these simple steps to set up your environment.

### Setup 

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/hdrezka-film-downloader.git
   ```

2. Navigate to the project directory:

   ```bash
   cd hdrezka-film-downloader
   ```

3. Create a `.env` file in the root directory. Specify the path to the Chrome driver and Chrome binary:

   ```env
   CHROME_BINARY_LOCATION=/path/to/chrome/binary
   CHROMEDRIVER_LOCATION=/path/to/chromedriver
   ```

### Dependencies

Make sure to install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the script by executing the Python code in `main.py`.
2. Enter the film name when prompted.
3. Choose the film from the search results.
4. Select the desired translation.
5. Choose the quality of the video to download.

## Notes 📝

- The script uses Selenium and BeautifulSoup for web scraping.
- It supports downloading films in different qualities and translations.

## Disclaimer ⚠️

This script is for educational purposes only. Please make sure to comply with the terms of service of the website.

Feel free to contribute to the project or report any issues. Enjoy downloading your favorite films! 🍿🎉
