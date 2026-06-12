# The Lyrical Time Capsule
## How AI Reveals the Emotional and Cultural Shifts in Music

The Lyrical Time Capsule is a data storytelling project about how popular music reflects social change over time. It compares hit songs from the United States and Switzerland and uses AI models to measure sentiment, detect topics, and analyze vocabulary trends across multiple decades.

The central question of the project is simple: when society changes, does popular music change with it? The article explores that question through four explanatory charts, scroll-based storytelling, and a transparent methodology section.

## Project Overview

This repository contains everything needed to reproduce the final data story:

- the written article in [article.html](article.html)
- four notebook-based charts in [chart1.ipynb](chart1.ipynb), [chart2.ipynb](chart2.ipynb), [chart3.ipynb](chart3.ipynb), and [chart4.ipynb](chart4.ipynb)
- the data, data cleaning notebooks and AI analysis notebooks under [data/](data)
- prompt logging assets in [prompts_data.py](prompts_data.py), [build_prompts.py](build_prompts.py), and [prompts.html](prompts.html)
- styling and theme generation under [style/](style)

The final article is designed as a scrollytelling page. As the reader moves down the page, the charts and accompanying text explain how the mood, themes, and language of hit songs evolve over time.

## Data Sources

- US charts: [Billboard Top 100 dataset from Kaggle](https://www.kaggle.com/datasets/brianblakely/top-100-songs-and-lyrics-from-1959-to-2019), covering 1959 to 2019.
- Switzerland charts: year-end hit parade data scraped from hitparade.ch, covering 1968 to 2023.
- Lyrics: pulled from Genius using the lyricsgenius package.

The project combines two countries so the article can compare how music reacts to cultural and historical change in different contexts.

## Repository Structure

- [article.html](article.html): Main interactive article with the final narrative and chart images.
- [app.py](app.py): Streamlit main application to view the article interactively.
- [pages/Prompts.py](pages/Prompts.py): Streamlit sub-page to view the AI prompt log.
- [chart1.ipynb](chart1.ipynb): Sentiment comparison chart.
- [chart2.ipynb](chart2.ipynb): Topic evolution chart.
- [chart3.ipynb](chart3.ipynb): Lexical diversity chart.
- [chart4.ipynb](chart4.ipynb): Cultural markers heatmap.
- [data/US/](data/US): US preprocessing and cleaned datasets.
- [data/CH/](data/CH): Swiss scraping, preprocessing, and cleaned datasets.
- [data/data_ai_processing.ipynb](data/data_ai_processing.ipynb): AI analysis notebook that adds sentiment, emotion, and topic labels.
- [build_prompts.py](build_prompts.py): Generates the transparency page from the prompt log.
- [prompts_data.py](prompts_data.py): Stores the prompt log used for the project.
- [prompts.html](prompts.html): Generated prompt log page.
- [config.json](config.json): Theme colors and font configuration.
- [style](style/): Stylesheets for article.
- [style/update_theme.py](style/update_theme.py): Generates [style/theme.css](style/theme.css) from the JSON config.
- [chartsPNG/](chartsPNG): Exported chart images used by the article.
- [requirements.txt](requirements.txt): Python dependencies.

## Workflow

The project was built in the following order:

1. Collect raw chart and lyric data.
2. Clean and normalize the lyrics.
3. Run AI analysis on each song.
4. Build the four chart notebooks and export them to PNG files.
5. Build the article and prompt log pages.
6. Open the final article in a browser.

## Data Processing

The preprocessing notebooks clean the raw datasets before the AI analysis runs.

- [data/US/data_preprocessing.ipynb](data/US/data_preprocessing.ipynb) cleans the US lyrics data and prepares a structured CSV.
- [data/CH/data_preprocessing.ipynb](data/CH/data_preprocessing.ipynb) reconstructs the year for Swiss chart entries, cleans the lyrics, and outputs a processed CSV.
- [data/data_ai_processing.ipynb](data/data_ai_processing.ipynb) applies Hugging Face models for sentiment, emotion, and zero-shot topic classification.

The main analysis uses the following models from [Hugging Face](https://huggingface.co):

- `cardiffnlp/twitter-roberta-base-sentiment-latest` for sentiment
- `j-hartmann/emotion-english-distilroberta-base` for emotion detection
- `facebook/bart-large-mnli` for topic classification

## How To View The Article

### 1. Create a Python environment

Use Python 3.10+ if possible, then install the dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Open the article

There are two ways to view the final project. The method required by the project description is to use a local Streamlit server to provide the full web-app experience, while the fallback method allows you to view the raw HTML.

#### Option 1: Run the Streamlit App (Official Method)
Ensure you have installed the requirements and activated your Python virtual environment. Then, run the following command in your terminal:

```bash
streamlit run app.py
```

This will start a local server and automatically open the interactive scrollytelling article in your default web browser.

##### Troubleshooting (Browser & Security Warnings)
If the page does not load or your browser (especially Safari) blocks the connection, try another browser or manually ensure the URL in your address bar starts with https:// (e.g., https://127.0.0.1:8501).

#### Option 2: Direct HTML (Backup)
If you do not want to set up a Python environment or run a local server, you can simply open the article.html file directly in any modern web browser (e.g., by double-clicking it). The core article, text, and styling will work perfectly as a standalone webpage without Streamlit.

## How To Rebuild The Entire Project

To view the article, just open [article.html](article.html) in a browser. Everything required to view the article should already be present.

To rebuild the whole project (NOT RECOMMENDED, will take several hours), follow these instructions:

### 1. Create a Python environment

Use Python 3.10+ if possible, then install the dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Collect raw Swiss chart and lyric data

Open and run the notebooks in this order:

- [data/CH/hitparade_scrapper.ipynb](data/CH/hitparade_scrapper.ipynb) (Will take a few minutes)
- [data/CH/lyrics_scrapper.ipynb](data/CH/lyrics_scrapper.ipynb) (Will take around 4-6 hours)

This produces the Swiss chart data with the accompanying lyrics for most songs.


### 3. Run the preprocessing and AI analysis notebooks

Open and run the notebooks in this order:

- [data/US/data_preprocessing.ipynb](data/US/data_preprocessing.ipynb)
- [data/CH/data_preprocessing.ipynb](data/CH/data_preprocessing.ipynb)
- [data/data_ai_processing.ipynb](data/data_ai_processing.ipynb) (Runtime heavily depends on device capabilites, could take hours)

This produces the processed CSV files used by the chart notebooks.

### 4. Run the chart notebooks

Execute the chart notebooks to regenerate the PNG files in [chartsPNG/](chartsPNG):

- [chart1.ipynb](chart1.ipynb)
- [chart2.ipynb](chart2.ipynb)
- [chart3.ipynb](chart3.ipynb)
- [chart4.ipynb](chart4.ipynb)

### 5. Regenerate the theme and prompt log

Execute the following scripts to regenerate the theme and prompt log:

- [style/update_theme.py](style/update_theme.py)
- [build_prompts.py](build_prompts.py)

### 6. Open the final article

Run the following command in the terminal:

```bash
streamlit run app.py
```

Or open [article.html](article.html) in a browser to view the completed scrollytelling article.

## Notes

- Several outputs are generated files, especially [prompts.html](prompts.html), [style/theme.css](style/theme.css), and the chart images in [chartsPNG/](chartsPNG).
- If you change the color palette or fonts in [config.json](config.json), rerun [style/update_theme.py](style/update_theme.py) and the chart notebooks.
- If you add or edit prompts in [prompts_data.py](prompts_data.py), rerun [build_prompts.py](build_prompts.py).

## Requirements

The project depends on common data science and NLP packages including pandas, numpy, matplotlib, seaborn, scikit-learn, transformers, torch, requests, beautifulsoup4, and lyricsgenius. A complete list is available in [requirements.txt](requirements.txt).

## Credits

Created by Sven Betschart as a Data Visualization final project.

The article includes a transparency section that documents the use of AI during the development process and links to the generated prompt log.
