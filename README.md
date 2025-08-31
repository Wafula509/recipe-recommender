# AI Driven Recipe Generator
An AI-driven recipe generator that recommends personalized recipes based on your mood, cuisine preference, and season, leveraging Pinecone and Claude AI.

## Project Overview
This project integrates various AI services to deliver a smooth and efficient personalized recipe generation experience:
- **Streamlit** is used to build an intuitive user interface that allows users to input their recipe preferences (mood, cuisine, and season).
- **Anthropic's Claude** generates personalized recipe kits, including mood-based recipe recommendations, ingredients, and preparation steps based on user input and seasonal preferences.
- **Pinecone**  is used to find similar recipes through vector similarity search, offering suggestions based on mood, cuisine, and season preferences.

The tool outputs:
- **Recipe suggestions** tailored to your mood, cuisine, and season.
- A list of **essential ingredients** with seasonal and mood-based explanations.
- Estimated **preparation time** for each recipe.
- A detailed, step-by-step **cooking method** with optional tips and serving suggestions.

## How It Works
1. **User Inputs**: The user provides details such as their mood, preferred cuisine, and season.

3. **Recipe Similarity Search**: Pinecone is used to find and display similar recipes using vector similarity, helping the user explore options that fit their mood and preferences.
4. **Detailed Recipe Kit**: The tool outputs detailed recipes with ingredient lists, preparation time estimates, and mood-based explanations for each dish.

### Features
- **Personalized Recipe Generation**: Automatically generate recipes based on your mood, preferred cuisine, and season using Anthropic's Claude AI.
- **Recipe Kit Creation**: Get detailed recommendations for ingredients, preparation steps, and cooking methods tailored to your input.
- **Recipe Similarity Search**: Discover similar recipes using Pinecone's vector search, offering suggestions based on mood, cuisine, and season preferences.
- **Intuitive UI**: A clean, user-friendly interface built with Streamlit makes the recipe generation process simple and interactive.

## Installation
1. **Clone the repository**:
rkdown
# AI Recipe Generator

A Streamlit application that generates personalized recipes based on your mood, cuisine preferences, and season.

## Features

- Personalized recipe recommendations
- No API keys required
- Local vector similarity search
- Dietary preference filtering
- Beautiful UI with custom styling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/recipe-app.git
cd recipe-app
   ```

4. **Run the Application**:
   To start the Streamlit app, run the following command:
   ```bash
   streamlit run app.py

This will launch the application in your browser, where you can input your mood, cuisine, and season to generate personalized recipes.

## Usage
- Input Your Preferences: Fill out the form in the Streamlit app with details about your mood, preferred cuisine, and the current season.
- Generate a Recipe Kit: Click the "Generate Recipe Kit" button, and the app will generate personalized recipes based on your input.
- View Recipe Details: You can view recipe recommendations, ingredients, and preparation steps in a user-friendly interface.

## Screenshots
<img width="804" alt="Screenshot 2024-09-13 at 4 32 23 PM" src="https://github.com/user-attachments/assets/9df142d9-bc23-4e43-b3e1-562153efaae9">


