
# LinkedIn Sentiment Analysis

## Introduction
Welcome to the LinkedIn Sentiment Analysis project! This repository aims to perform sentiment analysis on LinkedIn data, extracting insights from user posts and interactions.

## Features

- Profile metrics dashboard
  - Shows summary stats for your profile: likes, appreciations, impressions etc. 
  - Top posts ranked by engagement 
  - Historical trends over time
- Post analysis 
  - Sentiment analysis of comments using AI
  - Visualizations of reactions and engagement  
- Competitor benchmarking
  - Extract comments, profiles from competitor pages 
  - Analysis to compare performance vs competitors

## Prerequisites

You need to install:

- Python 3.7+ 
- Streamlit 
- Pandas, Numpy etc for data analysis
- Selenium for web scraping LinkedIn pages

Register for these APIs:

- LinkedIn data API to extract profile/post metrics
- AI text analysis API for sentiment analysis 
## Installation
To use this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Venkateeshh/LinkedIn-Sentiment-Analysis.git
   ```

2. Navigate to the project directory:
   ```bash
   cd LinkedIn-Sentiment-Analysis
   ```

3. Install dependencies:
   ```bash
   # Add installation commands if any
   ```

## Usage
The sidebar menu allows choosing different analysis options:

**My Info:** Enter your LinkedIn URL. Fetches profile metrics and top posts ranked by engagement.

**Post Analysis:** Enter any LinkedIn post URL. Fetches comments and analyzes sentiment.

**Competitor Analysis:** Enter competitor profile username and login creds. Extracts comments, profiles and analyzes to benchmark vs your profile.
### Run Locally

```bash
streamlit run app.py
```

It will open a browser window at `localhost:8501` with the dashboard.

## Features
Highlight the key features of your project.

- Sentiment analysis on LinkedIn posts.
- Automated post scheduling
- Job search integration
- Lead generation tracking
- Multiple profile comparison

## Contributing
If you'd like to contribute to this project, follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature_branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature_branch`.
5. Open a pull request.

