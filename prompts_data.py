PROMPTS = [
    {
        "text": """Ich studiere AI/ML und im modul Data Visualization müssen wir ein Projekt abgeben. Das ist die Projektbeschreibung:

You submit a data story using one or more datasets of your choice. You can think of it as a
popular science article, a blog post, a report with your insights, a data journalism article etc.
Visualizations need to be static, and their main purpose should be explanatory (not exploratory). I want you to focus on storytelling and design, intentional use of annotations and other elements we discussed. You need to include at least 4 charts which constitute a logical story (the minimum requirement increases by +1 chart for each additional team member).
It is possible to get a good grade by applying only basic charts and techniques, but to get an
excellent grade you will need to e.g. create some custom charts or heavily customize the prebuilt charts. Since you are writing an article, you also need to include text that presents the actual story and guides the reader.
As project outcomes, I would like you to submit:
- A short video (max 30s) where you demo your work – can be a simple screen grab with Zoom etc.
- Standalone source code to run the data story / dashboard (including all data and files needed to run it)
- Documentation needed to run the app locally, such as requirements.txt/pyproject.toml files and a readme
- If you did any data preprocessing outside of your app and the app only reaches to a transformed version of the dataset, please submit those scripts as well 
In your code, use human-friendly names of variables and functions and provide a brief
commentary of what the particular parts of the code do.

Die technologien die wir anwenden sollten sind z.B. Pandas, seaborn, matplotlib und sonstige python packages. Ich glaube man darf auch nicht python basierte technologien verwenden wenn es keine passende python packages hat. 
Meine Idee ist es, die Lyrics der Top 100 Songs der letzten Jahrzehnte zu analysieren und relationen zu historischen events oder so zu machen. Ich habe bereits ein passendes Dataset auf kaggle gefunden. Ich hatte die Idee, die lyrics mit einem simplen KI von Hugging Face zu analysieren und herauszufinden, über was über die Jahre am meisten gesungen wurde. Falls du noch andere gute Ideen hast, gib sie mir. Ich weiss noch nicht, wie ich die Daten dann schön präsentieren kann. Ich dachte es wäre cool, wenn ich eine lokale webseite machen könnte, bei der die Daten während dem Scrollen animiert gezeigt werden, doch ich weis nicht ob das zu aufwendig wäre. Ich möchte sehr viel Zeit für das aufwenden, doch ich möchte auch ein gutes produkt haben. Kannst du mir vorschlagen wie ich das projekt angehen sollte?"""
    },
    {
        "text": """was für hugging face modelle kannst du mir empfehlen"""
    },
    {
        "text": """Ich möchte daten von hitparade.ch scrapen. Die URL ist https://hitparade.ch/charts/jahreshitparade/[Jahr]. Ich möchte die Top songs von 1968-2023 von der website scrapen. Kannst du mir einen python script schreiben der das macht"""
    },
    {
        "text": """Wie kann ich die lyrics von den songs von Genius scrapen? Gib mir beispiel Code"""
    },
    {
        "text": """was passiert wenn z.B das api plötzlich keine requests mehr annimmt? Werden die lyrics die schon heruntergeladen wurden trotzdem gespeichert?"""
    },
    {
        "text": """Schreibe einen seperaten python script der die ganze lyrics in eine zeile umwandelt"""
    },
    {
        "text": """ich muss für ein schulprojekt ein kaggle dataset säubern. Es ist ein dataset von den top 100 songs von 1959 bis 2023. Das Dataset hat eine Kolonne names "Rank" bei der die Position im Top 100 angegeben ist. Das Problem ist jedoch, dass nicht angegeben ist, in welchem Jahr. Die Daten sind so angeordnet, dass es bei 1959 platz 1 anfängt und dann bis 100 geht und dann wieder bei 1 anfängt, aber wie gesagt, wenn die liste nicht genau so geordnet wäre, kann man nicht wissen, in welchem jahr es in der top 100 war. Wie kann ich mit python z.B mit pandas, die csv datei um eine Kolonne ergänzen, die das jahr in dem es in den top 100 war angibt?"""
    },
    {
        "text": """Give me a list of mayor historical events from 1970 to 2020 in the USA and Switzerland"""
    },
    {
        "text": """I have the following code to analyze the lyrics in dataset of the top songs of the last decades:

import pandas as pd
import torch
from transformers import pipeline

country = ""
while country.lower() != "ch" and country.lower() != "us":
    print("Which country should be analyzed? (CH/US)")
    country = str(input())

df = pd.read_csv(f'country/songs_processed.csv')

print("Checking for Apple Silicon acceleration...")
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device.upper()}")

print("Downloading models...")

# -- SETUP PIPELINES --
sentiment_pipe = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", truncation=True, max_length=512, device=device)

emotion_pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=2, truncation=True, max_length=512, device=device)

zero_shot_pipe = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)

# Categories for Zero-Shot Classification
categories = [
    "Romantic Love", "Heartbreak and Breakup", 
    "Wealth, Success and Flexing", "Social Issues and Protest", 
    "Escapism and Partying", "Mental Health and Struggles", 
    "Empowerment and Self-Confidence", "Nostalgia and Memories"
]


# -- HELPER METHODS --

def get_sentiment_and_score(text):
    if not text: return pd.Series([None, None])
    
    result = sentiment_pipe(text, truncation=True, max_length=512)
    return pd.Series([result[0]['label'], result[0]['score']])

def get_top2_emotions(text):
    if not text: return pd.Series([None, None, None, None])
    
    result = emotion_pipe(text, truncation=True, max_length=512)
    emotions = result[0] 
    
    # Returns Emotion 1, Score 1, Emotion 2 and Score 2
    if len(emotions) >= 2:
        return pd.Series([
            emotions[0]['label'], emotions[0]['score'], 
            emotions[1]['label'], emotions[1]['score']
        ])
    elif len(emotions) == 1:
         return pd.Series([emotions[0]['label'], emotions[0]['score'], None, None])
    else:
        return pd.Series([None, None, None, None])

def get_topic_and_score(text):
    if not text: return pd.Series([None, None])
    
    text_short = text[:1500] 
    result = zero_shot_pipe(text_short, candidate_labels=categories)
    
    return pd.Series([result['labels'][0], result['scores'][0]])


# -- DATA PROCESSING --
print("Starting analysis...")

print("Analyzing sentiment...")
df[['Sentiment', 'Sentiment_Score']] = df['Lyrics'].apply(get_sentiment_and_score)

print("Analyzing emotions...")
df[['Emotion_1', 'Emotion_1_Score', 'Emotion_2', 'Emotion_2_Score']] = df['Lyrics'].apply(get_top2_emotions)

print("Analyzing theme...")
df[['Topic', 'Topic_Score']] = df['Lyrics'].apply(get_topic_and_score)

print("Analysis done!")

df.to_csv(f'country/songs_analyzed.csv', index=False)

I have two problems. The first problem is that some songs aren't english so i need to either translate them first or use different models that also work with languages other than english. The second problem is that the lyrics, which were scraped from genius with lyricsgenius, aren't always the actual lyrics from the song. Sometimes random comments from users or other things completely unrelated to the actual song were scraped. Deleting the wrong entries manually would take hours because there are over 10000 songs in the two datasets i'm analyzing. Can you propose solutions for the two problems i have?"""
    },
    {
        "text": """I already have the following code for data preprocessing:

import pandas as pd
import numpy as np
import re

def clean_lyrics(text):
    if pd.isna(text):
        return np.nan
        
    text = str(text)
    
    if text.strip().lower() == 'nan': 
        return np.nan
    
    text_cleaned = re.sub(r'\[.*?\]|\(.*?\)', '', text)
    text_cleaned = text_cleaned.replace('♫  ♫', '')
    text_cleaned = text_cleaned.replace('Instrumental', '')
    text_cleaned = text_cleaned.strip()

    if not text_cleaned:
        return np.nan
        
    return text_cleaned


def process_data():

    df = pd.read_csv('songs_original.csv')

    newyear = df['Rank'] < df['Rank'].shift(1)
    df['Year'] = 1959 + newyear.cumsum()

    df['Lyrics'] = df['Lyrics'].apply(clean_lyrics)

    df = df.dropna(subset=['Lyrics'])

    df.to_csv('songs_processed.csv', index=False)



if __name__ == "__main__":
    process_data()

Can you modify it to do additional lyrics cleaning"""
    },
    {
        "text": """Give me code for the first chart"""
    },
    {
        "text": """Refactor and clean up the following code and add simple comments:

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

backgroundColor = "#2A2B2D"
titleColor = "#FFFFFF"
textColor = "#FFFFFF"
usLineColor = "#4797FF"
chLineColor = "#FF0000"
gridLineColor = "#6C757D"

def process_sentiment_data(df):
    df = df.copy()
    
    def calc_net_sentiment(row):
        if row['Sentiment'] == 'positive':
            return row['Sentiment_Score']
        elif row['Sentiment'] == 'negative':
            return -row['Sentiment_Score']
        else:
            return 0 
            
    df['Net_Sentiment'] = df.apply(calc_net_sentiment, axis=1)
    yearly = df.groupby('Year')['Net_Sentiment'].mean().reset_index()
    yearly['smoothed_trend'] = yearly['Net_Sentiment'].rolling(window=3, center=True).mean()
    
    return yearly

def create_comparative_sentiment_chart_sns(df_usa, df_ch):
    yearly_usa = process_sentiment_data(df_usa)
    yearly_ch = process_sentiment_data(df_ch)
    
    merged_data = pd.merge(yearly_usa, yearly_ch, on='Year', suffixes=('_USA', '_CH'), how='inner')

    trend_melted = merged_data.melt(id_vars=['Year'], 
                                    value_vars=['smoothed_trend_USA', 'smoothed_trend_CH'],
                                    var_name='Country', value_name='Smoothed_Trend')
    trend_melted['Country'] = trend_melted['Country'].map({'smoothed_trend_USA': 'USA', 'smoothed_trend_CH': 'Switzerland'})

    scatter_melted = merged_data.melt(id_vars=['Year'], 
                                      value_vars=['Net_Sentiment_USA', 'Net_Sentiment_CH'],
                                      var_name='Country', value_name='Net_Sentiment')
    scatter_melted['Country'] = scatter_melted['Country'].map({'Net_Sentiment_USA': 'USA', 'Net_Sentiment_CH': 'Switzerland'})

    sns.set_theme(style="whitegrid", rc={"axes.facecolor": backgroundColor, "figure.facecolor": backgroundColor})
    fig, ax = plt.subplots(figsize=(14, 7), dpi=150)

    custom_palette = {'USA': usLineColor, 'Switzerland': chLineColor}

    ax.axhline(0, color=gridLineColor, linestyle='--', linewidth=1, zorder=1)

    sns.scatterplot(data=scatter_melted, x='Year', y='Net_Sentiment', hue='Country', 
                    palette=custom_palette, alpha=0.2, s=25, legend=False, ax=ax, zorder=2)

    sns.lineplot(data=trend_melted, x='Year', y='Smoothed_Trend', hue='Country', 
                 palette=custom_palette, linewidth=3, ax=ax, zorder=4)

    ax.fill_between(merged_data['Year'], 
                    merged_data['smoothed_trend_USA'], 
                    merged_data['smoothed_trend_CH'],
                    where=(merged_data['smoothed_trend_USA'] >= merged_data['smoothed_trend_CH']),
                    color=usLineColor, alpha=0.15, interpolate=True, zorder=3)

    ax.fill_between(merged_data['Year'], 
                    merged_data['smoothed_trend_USA'], 
                    merged_data['smoothed_trend_CH'],
                    where=(merged_data['smoothed_trend_CH'] > merged_data['smoothed_trend_USA']),
                    color=chLineColor, alpha=0.15, interpolate=True, zorder=3)

    sns.despine(left=True, top=True, right=True)
    
    ax.grid(color=gridLineColor, linestyle='-', linewidth=0.5, axis='y', alpha=0.7)
    ax.grid(False, axis='x')

    ax.set_title('The Transatlantic Vibe Gap', fontsize=20, fontweight='bold', pad=30, loc='left', color=titleColor)
    ax.text(0, 1.03, 'Comparing the Net Sentiment of Top 100 pop songs: USA vs. Switzerland.', 
            transform=ax.transAxes, fontsize=12, color=textColor, ha='left')
            
    ax.set_xlabel('Release Year', fontsize=12, color=textColor, labelpad=10)
    ax.set_ylabel('Net Sentiment Score\n(-1 = Negative, +1 = Positive)', fontsize=12, color=textColor, labelpad=10)
    ax.set_ylim(-0.5, 0.5)

    ax.tick_params(axis='x', colors=textColor)
    ax.tick_params(axis='y', colors=textColor)

    y_val_usa_2001 = merged_data.loc[merged_data['Year'] == 2001, 'smoothed_trend_USA'].values[0]
    ax.annotate('2001\nPost-9/11 Era', 
                xy=(2001, y_val_usa_2001),
                xytext=(1995, -0.3), 
                fontsize=10, color=textColor, fontweight='bold',
                arrowprops=dict(facecolor=textColor, arrowstyle='->', connectionstyle="arc3,rad=.2", color=textColor))


    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=labels, title='', frameon=False, loc='upper right', fontsize=11, labelcolor=textColor)
    
    plt.tight_layout()
    return fig

df_usa = pd.read_csv('data/US/songs_analyzed.csv')
df_ch = pd.read_csv('data/CH/songs_analyzed.csv') 

sentiment_fig = create_comparative_sentiment_chart_sns(df_usa, df_ch)

plt.show()"""
    },
    {
        "text": """Can you put some parts into separate functions"""
    },
    {
        "text": """does the font path have to be relative to the file i am writing the code in or to the python executer in the venv?"""
    },
    {
        "text": """I have a local font "fonts/akira.otf" i want to use just for the title and a font "fonts/nexaHeavy.ttf" i want to use for everything else. Modify the code to do that"""
    },
    {
        "text": """There is a high peak of net sentiment around 2011 or 2012. What could it be? """
    },
    {
        "text": """What mayor events from 1970 to 2020 could i also annotate?"""
    },
    {
        "text": """I still think that there are too many informations in one chart and that the chart is too confusing. Do you have ideas for how i could improve the chart or do you have ideas for other kind of charts that also analyze the emotions"""
    },
    {
        "text": """Now can you give me code for a heatmap chart visualizing how many times specific cultural marker words have been mentioned in songs. The words should be Dance, Money, War and Phone, but also include similar words. So for example Money should also include Cash and Bills and similar words."""
    },
    {
        "text": """Ich muss nun für all diese charts die ich habe eine lokale webseite machen die wie ein artikel diese charts präsentiert. Wie mach ich das am besten? """
    },
    {
        "text": """Ich möchte das ich die farben und fonts für die charts und den artikel alle in einem file konfigurieren kann, sodass ich es nicht in 5 verschiedenen files anpassen muss. Wenn es mit den fonts zu schwierig ist möchte ich es wenigstens für die farben so haben. Wie mach ich das?"""
    },
    {
        "text": """How can i make that while scrolling the different charts kinda fade and shift into the screen? """
    },
    {
        "text": """I want that when scrolling the different sections slide into the screen like a powerpoint slide with animations. So first only the title and intruduction text is on the screen and then when i scroll the text part slides in."""
    },
    {
        "text": """Kannst du mir Text für den Artikel entsprechend meinen folgenden Beobachtungen geben. Schreibe den Text auf englisch. Ich habe in folgenden Beobachtungen einfach schnell schnell das aufgeschrieben was ich in den Chart sehen kann, also schreibe den Text sicher schöner und ausführlicher und "philosophiere" noch ein bisschen rein.

Der erste Chart "The Shifting Mood of Music" ist sehr interessant. Das Sentiment in der Schweiz und in den USA ist vorallem in der zweiten hälfte recht ähnlich. Man sieht, dass nach kriesen wie die 1973 oil crisis und 2008 financial Crisis das sentiment steigt, vielleicht um sich mit partysongs ablenken. Man sieht auch das nach den 2001 9/11 attacken und nach der wahl von donald trump das Sentiment einen Tiefpunkt erreicht.

Das zweite Chart "From Romance to more Dance" zeigt wie Songs die um Liebe, Nostalgie und Erinnerungen handeln immer mehr verdrängt werden, aber immer noch das beliebteste Thema sind. Party und Flexing songs werden hingegen immer beliebter und erreichen in den 2010er Jahren einen höhenpunkt. Ab 2020 sinkt die anzahl partysongs jedoch drastisch und songs bei denen über mentale gesundheit gesungen werden werden plötzlich sehr beliebt, was wahrscheinlich wegen COVID-19 so ist.

Die dritte Chart zeigt die ratio von einzigartigen Wörtern zu der totalen Anzahl Wörter in songs über die Jahre. Man sieht eine weniger grosse Reduzierung als ich erwartet habe. Die ratio sink von ca. 45% in 1960 langsam und stetig bis zu ca. 35% Mitte 2010er. Nachdem es diesen Tiefpunkt erreicht hat steigt es jedoch recht schnell wieder auf 40%, was ich sehr interessant finde. Vielleicht legen die menschen in den letzten Jahren wieder mehr wert in "intelligentere" songs.

Der letzte Chart untersucht wie viel bestimme "Cultural Marker" Wörter (und ähnliche Wörter) in den songs erwähnt werden. Man sieht wie "Money" immer mehr an Bedeutung gewinnt. Bei "Dance" ist die Veränderung besonders stark, die frequenz steigt um mehr als das zehnfache in den 2000er Jahren doch sinkt dann wieder minimal bis zu den 2020er Jahren. Es hat mich sehr überrascht, dass "Phone" so wenig angestiegen ist. Bis zu den 2000er Jahren veroppelt sich die frequenz und bleibt dann stetig. Die Frequenz von"War" verändert sich am wenigsten. Ich finde es besonders interessant wie wenig über krieg in den 1960er bis 1970er gesungen wurde, obwohl der Vietnam krieg zu dieser zeit am wüten war. Viellecht wollten die menschen lieber etwas anderes hören, um sich abzulenken."""
    },
    {
        "text": """Ich möchte einen teil einfügen im artikel, welcher erläutert was für KI modelle ich für die analysen gebraucht habe und von wo ich die Daten habe. Wo sollte ich das einfügen? Am anfang oder am ende?"""
    },
    {
        "text": """Ich habe die top 100 songs datenset von der USA von diesem link: https://www.kaggle.com/datasets/brianblakely/top-100-songs-and-lyrics-from-1959-to-2019

Die top 100 von der schweiz habe ich von da selbst gescraped: https://hitparade.ch/charts/jahreshitparade

Für alle ai analysen habe ich hugging face modelle gebraucht. Für die sentiment analyse habe ich cardiffnlp/twitter-roberta-base-sentiment-latest gebraucht, für die emotion analyse j-hartmann/emotion-english-distilroberta-base und für die zero-shot Klassifikation facebook/bart-large-mnli

Kannst du den code und text entsprechen anpassen"""
    },
    {
        "text": """I want to also add a section creating transparency over the AI use in the project. A small section where it says that for example ai was used to write the text and help with the code and then a link to another html file where all the used promts are listed"""
    },
    {
        "text": """Give me code for a promts.html that follows the same design and include a few example promts. The promts.html doesn't need fancy animations though"""
    },
    {
        "text": """i have put all style for the article.html into a seperate style.css file:

body {
    line-height: 1.6;
    margin: 0;
    padding: 0;
}

article {
    max-width: 1000px;
    margin: 0 auto;
    padding: 60px 20px;
}

header {
    text-align: left;
    margin-bottom: 80px;
    padding-left: 30px;
}

h1 {
    font-size: 3rem;
    margin-bottom: 10px;
    line-height: 1.1;
    text-transform: uppercase;
    letter-spacing: -1px;
}

.subtitle {
    color: var(--muted-text);
    font-size: 1.3rem;
    margin-top: 10px;
    font-weight: 300;
}

h2 {
    color: var(--text-color);
    margin-top: 60px;
    font-size: 1.8rem;
    font-weight: 700;
}

p {
    font-size: 1.15rem;
    margin-bottom: 25px;
    color: var(--light-text-color);
}

figure {
    margin: 50px 0;
    text-align: center;
}

img {
    max-width: 100%;
    height: auto;
}

figcaption {
    color: var(--muted-text);
    font-size: 0.95rem;
    margin-top: 15px;
    font-style: italic;
}

section {
    margin-bottom: 80px;
}

hr {
    border: 0;
    border-top: 1px solid #444;
    margin: 40px 0;
}

a {
    color: var(--accent-color); 
    text-decoration: none;
}

footer p {
    font-size: 0.9rem; 
    color: var(--muted-text); 
    text-align: center;
}

ul {
    color:  var(--light-text-color); 
    font-size: 1.05rem; 
    margin-top: 20px; 
    padding-left: 20px; 
    line-height: 1.8;
}

ul li strong {
    color:  var(--light-text-color);
}

Modify the promts.html to use this file for the style where possible and only keep the style that isn't in the style.css"""
    }
]