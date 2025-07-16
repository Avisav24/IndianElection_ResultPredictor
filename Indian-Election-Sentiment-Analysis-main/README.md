# Indian Election Predictor

A sophisticated web application that analyzes Twitter sentiment to predict election outcomes using AI-powered Natural Language Processing.

## Features

- **Sentiment Analysis**: Uses TextBlob NLP to analyze Twitter sentiment for political leaders
- **Interactive Visualizations**: Beautiful charts and graphs using Plotly.js
- **Modern UI**: Responsive design with glassmorphism effects and smooth animations
- **Real-time Analysis**: Dynamic loading and results presentation
- **Professional Dashboard**: Clean, professional interface with Indian flag colors

## Project Structure

```
Indian-Election-Sentiment-Analysis/
├── app.py                    # Flask backend application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── data/                     # Data files
│   ├── modi_reviews.csv      # Modi sentiment data
│   └── rahul_reviews.csv     # Rahul Gandhi sentiment data
├── static/                   # Static files
│   ├── css/                  # Stylesheets
│   │   └── style.css         # Main CSS file
│   ├── js/                   # JavaScript files
│   │   └── script.js         # Main JavaScript file
│   └── images/               # Image files
│       ├── Prime_Minister_Of_Bharat_Shri_Narendra_Damodardas_Modi.jpg
│       └── Rahul_Gandhi.png
└── templates/                # HTML templates
    └── index_clean.html      # Clean template (separate files)
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/indian-election-sentiment-analysis.git
   cd indian-election-sentiment-analysis
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   python app.py
   ```

5. **Open in browser**:
   Navigate to `http://localhost:5000`

## Usage

1. **Homepage**: View the political candidates and their information
2. **Analyze**: Click the "Analyze Sentiment" button to start the analysis
3. **Results**: View sentiment statistics, prediction results, and interactive charts
4. **Charts**: Explore bar charts and pie charts showing sentiment distribution

## Technical Details

### Backend (Flask)

- **Framework**: Flask web framework
- **NLP Library**: TextBlob for sentiment analysis
- **Data Processing**: Pandas and NumPy for data manipulation
- **Visualization**: Plotly for chart generation

### Frontend

- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with gradients, animations, and glassmorphism
- **JavaScript**: Interactive functionality and API calls
- **External Libraries**:
  - Font Awesome for icons
  - Google Fonts (Poppins)
  - Animate.css for animations
  - Plotly.js for interactive charts

### Data

- **Format**: CSV files containing Twitter sentiment data
- **Processing**: Real-time sentiment analysis using TextBlob
- **Visualization**: Multiple chart types for comprehensive analysis

## Features

- 🎨 **Modern UI**: Glassmorphism design with smooth animations
- 📊 **Interactive Charts**: Real-time data visualization
- 🎯 **Accurate Predictions**: AI-powered sentiment analysis
- 📱 **Responsive Design**: Works on all devices
- 🇮🇳 **Indian Theme**: Flag colors and cultural elements
- ⚡ **Fast Performance**: Optimized for speed and efficiency

## API Endpoints

- `GET /`: Homepage
- `GET /analyze`: Perform sentiment analysis and return results
- `GET /static/<path:filename>`: Serve static files

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This prediction is based solely on Twitter sentiment analysis and should not be considered as a definitive election forecast. Actual election results depend on many factors beyond social media sentiment including voter turnout, regional preferences, and ground-level campaign effectiveness.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

**© 2024 Indian Election Predictor | Powered by TextBlob NLP & Plotly**
