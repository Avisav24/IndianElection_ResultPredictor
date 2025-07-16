from flask import Flask, render_template, jsonify, request, send_file
import pandas as pd
import numpy as np
from textblob import TextBlob
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import plotly
import os

app = Flask(__name__)

# Global variables to store analysis results
analysis_results = {}
analysis_cache = {}  # Cache for processed results

def find_polarity(review):
    """Calculate sentiment polarity using TextBlob"""
    try:
        if pd.isna(review) or review == '' or review == 'nan':
            return 0.0
        blob = TextBlob(str(review))
        return float(blob.sentiment.polarity)
    except Exception as e:
        return 0.0

def perform_sentiment_analysis():
    """Perform the complete sentiment analysis"""
    global analysis_results, analysis_cache
    
    # Check if results are already cached
    if analysis_cache:
        analysis_results = analysis_cache
        return True
    
    try:
        # Get the directory where this script is located
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load data using absolute paths
        modi_path = os.path.join(script_dir, "data", "modi_reviews.csv")
        rahul_path = os.path.join(script_dir, "data", "rahul_reviews.csv")
        
        # Check if files exist
        if not os.path.exists(modi_path):
            raise FileNotFoundError(f"Modi CSV file not found at: {modi_path}")
        if not os.path.exists(rahul_path):
            raise FileNotFoundError(f"Rahul CSV file not found at: {rahul_path}")
        
        modi = pd.read_csv(modi_path)
        rahul = pd.read_csv(rahul_path)
        
        print(f"Loaded {len(modi)} Modi tweets and {len(rahul)} Rahul tweets")
        
        # Convert to string
        modi['Tweet'] = modi['Tweet'].astype(str)
        rahul['Tweet'] = rahul['Tweet'].astype(str)
        
        print("Starting sentiment analysis...")
        # Calculate polarity
        modi['Polarity'] = modi['Tweet'].apply(find_polarity)
        rahul['Polarity'] = rahul['Tweet'].apply(find_polarity)
        
        print("Sentiment analysis completed")
        
        # Create labels
        modi['Label'] = np.where(modi['Polarity'] > 0, 'positive', 'negative')
        modi['Label'][modi['Polarity'] == 0] = 'Neutral'
        
        rahul['Label'] = np.where(rahul['Polarity'] > 0, 'positive', 'negative')
        rahul['Label'][rahul['Polarity'] == 0] = 'Neutral'
        
        # Remove neutral tweets
        modi = modi[modi['Polarity'] != 0.0]
        rahul = rahul[rahul['Polarity'] != 0.0]
        
        # Balance datasets (reduced for faster processing)
        np.random.seed(10)
        if len(modi) > 2000:
            modi = modi.sample(n=2000, random_state=10)
        if len(rahul) > 2000:
            rahul = rahul.sample(n=2000, random_state=10)
        
        # Calculate sentiment percentages
        modi_count = modi.groupby('Label').size()
        rahul_count = rahul.groupby('Label').size()
        
        # Calculate total counts for proper percentage calculation
        modi_total = len(modi)
        rahul_total = len(rahul)
        
        neg_modi = (modi_count.get('negative', 0) / modi_total) * 100
        pos_modi = (modi_count.get('positive', 0) / modi_total) * 100
        neg_rahul = (rahul_count.get('negative', 0) / rahul_total) * 100
        pos_rahul = (rahul_count.get('positive', 0) / rahul_total) * 100
        
        # Calculate metrics
        modi_total_sentiment = pos_modi - neg_modi
        rahul_total_sentiment = pos_rahul - neg_rahul
        
        # Avoid division by zero
        if (pos_modi + neg_modi) > 0:
            modi_sentiment_score = pos_modi / (pos_modi + neg_modi) * 100
        else:
            modi_sentiment_score = 0
            
        if (pos_rahul + neg_rahul) > 0:
            rahul_sentiment_score = pos_rahul / (pos_rahul + neg_rahul) * 100
        else:
            rahul_sentiment_score = 0
        
        # Determine winner
        winner = "Narendra Modi" if modi_sentiment_score > rahul_sentiment_score else "Rahul Gandhi"
        confidence = abs(modi_sentiment_score - rahul_sentiment_score)
        
        print(f"Modi: {pos_modi:.1f}% positive, {neg_modi:.1f}% negative")
        print(f"Rahul: {pos_rahul:.1f}% positive, {neg_rahul:.1f}% negative")
        print(f"Winner: {winner} with {confidence:.1f}% confidence")
        
        analysis_results = {
            'pos_modi': pos_modi,
            'neg_modi': neg_modi,
            'pos_rahul': pos_rahul,
            'neg_rahul': neg_rahul,
            'modi_sentiment_score': modi_sentiment_score,
            'rahul_sentiment_score': rahul_sentiment_score,
            'winner': winner,
            'confidence': confidence,
            'sentiment_lead': abs(modi_total_sentiment - rahul_total_sentiment)
        }
        
        # Cache the results
        analysis_cache = analysis_results.copy()
        
        return True
    except Exception as e:
        print(f"Error in analysis: {e}")
        return False

@app.route('/')
def index():
    return render_template('index_clean.html')

@app.route('/analyze')
def analyze():
    """Perform sentiment analysis and return results"""
    global analysis_cache
    # Clear cache to force fresh analysis
    analysis_cache = {}
    
    success = perform_sentiment_analysis()
    if success:
        # Include chart data in the response
        bar_chart = {
            'data': [
                {
                    'x': ['Modi', 'Rahul Gandhi'],
                    'y': [analysis_results['neg_modi'], analysis_results['neg_rahul']],
                    'name': 'Negative Sentiment',
                    'type': 'bar',
                    'marker': {'color': '#FF6B6B'}
                },
                {
                    'x': ['Modi', 'Rahul Gandhi'],
                    'y': [analysis_results['pos_modi'], analysis_results['pos_rahul']],
                    'name': 'Positive Sentiment',
                    'type': 'bar',
                    'marker': {'color': '#4ECDC4'}
                }
            ],
            'layout': {
                'title': 'Sentiment Analysis Comparison',
                'xaxis': {'title': 'Politicians'},
                'yaxis': {'title': 'Sentiment Percentage (%)'},
                'barmode': 'group'
            }
        }
        
        # Pie chart data
        pie_data = {
            'modi': {
                'values': [analysis_results['neg_modi'], analysis_results['pos_modi']],
                'labels': ['Negative', 'Positive'],
                'colors': ['#FF6B6B', '#4ECDC4']
            },
            'rahul': {
                'values': [analysis_results['neg_rahul'], analysis_results['pos_rahul']],
                'labels': ['Negative', 'Positive'],
                'colors': ['#FF6B6B', '#4ECDC4']
            }
        }
        
        # Combine analysis results with chart data
        response_data = analysis_results.copy()
        response_data['bar_chart'] = bar_chart
        response_data['pie_data'] = pie_data
        
        return jsonify(response_data)
    else:
        return jsonify({'error': 'Analysis failed'}), 500

@app.route('/charts')
def get_charts():
    """Generate and return chart data"""
    if not analysis_results:
        return jsonify({'error': 'No analysis data available'}), 400
    
    # Bar chart
    bar_chart = {
        'data': [
            {
                'x': ['Modi', 'Rahul Gandhi'],
                'y': [analysis_results['neg_modi'], analysis_results['neg_rahul']],
                'name': 'Negative Sentiment',
                'type': 'bar',
                'marker': {'color': '#FF6B6B'}
            },
            {
                'x': ['Modi', 'Rahul Gandhi'],
                'y': [analysis_results['pos_modi'], analysis_results['pos_rahul']],
                'name': 'Positive Sentiment',
                'type': 'bar',
                'marker': {'color': '#4ECDC4'}
            }
        ],
        'layout': {
            'title': 'Sentiment Analysis Comparison',
            'xaxis': {'title': 'Politicians'},
            'yaxis': {'title': 'Sentiment Percentage (%)'},
            'barmode': 'group'
        }
    }
    
    # Pie chart data
    pie_data = {
        'modi': {
            'values': [analysis_results['neg_modi'], analysis_results['pos_modi']],
            'labels': ['Negative', 'Positive'],
            'colors': ['#FF6B6B', '#4ECDC4']
        },
        'rahul': {
            'values': [analysis_results['neg_rahul'], analysis_results['pos_rahul']],
            'labels': ['Negative', 'Positive'],
            'colors': ['#FF6B6B', '#4ECDC4']
        }
    }
    
    return jsonify({
        'bar_chart': bar_chart,
        'pie_data': pie_data
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
