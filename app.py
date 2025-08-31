import streamlit as st
import json
import re
import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #FF9B4B;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .recipe-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .ingredient-list {
        background-color: #fff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #FF4B4B;
    }
    .instruction-list {
        background-color: #fff;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #FF9B4B;
        color: white;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# Recipe database with embeddings precomputed
def load_recipe_database():
    recipes = [
        {
            "name": "Summer Berry Salad",
            "cuisine": "American",
            "season": "Summer",
            "mood": "Refreshing",
            "ingredients": ["Mixed greens", "strawberries", "blueberries", "feta cheese", "walnuts", "balsamic vinaigrette"],
            "prep_time": "15 minutes",
            "description": "A light and refreshing salad perfect for hot summer days",
            "instructions": [
                "Wash and dry the mixed greens",
                "Slice strawberries and blueberries",
                "Crumble feta cheese",
                "Chop walnuts",
                "Combine all ingredients in a bowl",
                "Drizzle with balsamic vinaigrette and toss gently"
            ],
            "embedding": [0.8, 0.1, 0.4, 0.2, 0.7, 0.3, 0.1, 0.9]
        },
        {
            "name": "Hearty Winter Stew",
            "cuisine": "American",
            "season": "Winter",
            "mood": "Comforting",
            "ingredients": ["Beef chuck", "potatoes", "carrots", "onions", "beef broth", "herbs"],
            "prep_time": "2 hours",
            "description": "A warm and comforting stew for cold winter nights",
            "instructions": [
                "Cube beef chuck into bite-sized pieces",
                "Dice potatoes, carrots, and onions",
                "Brown beef in a large pot",
                "Add vegetables and cook for 5 minutes",
                "Pour in beef broth and add herbs",
                "Simmer for 1.5-2 hours until meat is tender"
            ],
            "embedding": [0.2, 0.8, 0.7, 0.9, 0.1, 0.4, 0.6, 0.3]
        },
        {
            "name": "Spring Vegetable Pasta",
            "cuisine": "Italian",
            "season": "Spring",
            "mood": "Energizing",
            "ingredients": ["Pasta", "asparagus", "peas", "lemon", "garlic", "parmesan cheese"],
            "prep_time": "30 minutes",
            "description": "A fresh pasta dish with seasonal spring vegetables",
            "instructions": [
                "Cook pasta according to package directions",
                "Chop asparagus and mince garlic",
                "Sauté asparagus and peas in olive oil",
                "Add garlic and cook for 1 minute",
                "Toss with drained pasta",
                "Add lemon zest, juice, and parmesan cheese"
            ],
            "embedding": [0.5, 0.3, 0.2, 0.1, 0.9, 0.7, 0.4, 0.6]
        },
        {
            "name": "Autumn Pumpkin Soup",
            "cuisine": "American",
            "season": "Fall",
            "mood": "Cozy",
            "ingredients": ["Pumpkin", "onions", "vegetable broth", "cream", "spices"],
            "prep_time": "45 minutes",
            "description": "A creamy soup that captures the essence of autumn",
            "instructions": [
                "Dice pumpkin and onions",
                "Sauté onions until translucent",
                "Add pumpkin and cook for 5 minutes",
                "Pour in vegetable broth and simmer until pumpkin is tender",
                "Blend soup until smooth",
                "Stir in cream and season with spices"
            ],
            "embedding": [0.3, 0.6, 0.8, 0.4, 0.2, 0.5, 0.9, 0.7]
        },
        {
            "name": "Spicy Thai Curry",
            "cuisine": "Thai",
            "season": "All",
            "mood": "Adventurous",
            "ingredients": ["Coconut milk", "curry paste", "vegetables", "tofu or chicken", "basil"],
            "prep_time": "40 minutes",
            "description": "A flavorful and aromatic curry with a spicy kick",
            "instructions": [
                "Heat curry paste in a pan until fragrant",
                "Add protein and cook until sealed",
                "Pour in coconut milk and bring to a simmer",
                "Add vegetables and cook until tender",
                "Stir in basil leaves just before serving",
                "Serve with jasmine rice"
            ],
            "embedding": [0.7, 0.4, 0.3, 0.6, 0.8, 0.2, 0.5, 0.1]
        },
        {
            "name": "Mediterranean Mezze Platter",
            "cuisine": "Mediterranean",
            "season": "Summer",
            "mood": "Social",
            "ingredients": ["Hummus", "tabbouleh", "pita bread", "olives", "feta", "vegetables"],
            "prep_time": "25 minutes",
            "description": "A shareable platter perfect for gatherings",
            "instructions": [
                "Arrange hummus and tabbouleh in bowls on a platter",
                "Cut pita bread into wedges and lightly toast",
                "Slice vegetables for dipping",
                "Add olives and cubed feta cheese",
                "Drizzle with olive oil and sprinkle with herbs",
                "Serve immediately"
            ],
            "embedding": [0.9, 0.2, 0.5, 0.7, 0.3, 0.1, 0.8, 0.4]
        }
    ]
    return recipes

# Simple embedding function (in a real app, you'd use a proper model)
def create_text_embedding(text):
    # This is a simplified version - in reality you'd use a proper embedding model
    # But for demonstration, we'll create a simple hash-based embedding
    words = text.lower().split()
    embedding = [0.0] * 8  # 8-dimensional embedding for simplicity
    
    for word in words:
        # Simple hash-based embedding for demonstration
        hash_val = hash(word) % 8
        embedding[hash_val] += 0.1
        
    # Normalize
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = [e/norm for e in embedding]
    
    return embedding

# Find similar recipes using cosine similarity
def find_similar_recipes(user_input, recipes, top_k=3):
    input_text = f"{user_input['mood']} {user_input['cuisine']} {user_input['season']}"
    input_embedding = create_text_embedding(input_text)
    
    similarities = []
    for recipe in recipes:
        # Calculate cosine similarity
        dot_product = np.dot(input_embedding, recipe['embedding'])
        norm_a = np.linalg.norm(input_embedding)
        norm_b = np.linalg.norm(recipe['embedding'])
        
        if norm_a > 0 and norm_b > 0:
            similarity = dot_product / (norm_a * norm_b)
        else:
            similarity = 0
            
        similarities.append((recipe, similarity))
    
    # Sort by similarity and return top matches
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [recipe for recipe, similarity in similarities[:top_k] if similarity > 0.1]

# Function to validate user input
def validate_input(user_input):
    required_fields = ["mood", "cuisine", "season"]
    for field in required_fields:
        if not user_input.get(field):
            st.error(f"Error: {field} is required")
            return False
    return True

# Function to generate recipes using a rule-based approach
def generate_recipe_kit(user_input, similar_recipes):
    # Base recipe templates that we'll customize
    recipe_templates = [
        {
            "name": f"{user_input['cuisine']} Inspired Bowl",
            "ingredients": ["Base grain (rice, quinoa, or couscous)", "Seasonal vegetables", "Protein source", "Signature sauce or dressing"],
            "prep_time": "30-40 minutes",
            "steps": [
                "Cook your chosen grain according to package instructions",
                "Prepare and sauté seasonal vegetables",
                "Cook your protein with herbs and spices",
                "Combine all components in a bowl and drizzle with sauce"
            ]
        },
        {
            "name": f"{user_input['season']} {user_input['cuisine']} Soup",
            "ingredients": ["Seasonal vegetables", "Broth base", "Aromatic herbs", "Protein or legumes"],
            "prep_time": "45-60 minutes",
            "steps": [
                "Sauté aromatics (onions, garlic) in a large pot",
                "Add seasonal vegetables and cook until slightly softened",
                "Pour in broth and bring to a simmer",
                "Add protein/legumes and simmer until cooked through",
                "Season to taste and serve hot"
            ]
        },
        {
            "name": f"{user_input['mood']} {user_input['cuisine']} Platter",
            "ingredients": ["Assorted fresh ingredients", "Dips or spreads", "Bread or crackers", "Garnishes"],
            "prep_time": "20-30 minutes",
            "steps": [
                "Arrange an assortment of fresh ingredients on a large platter",
                "Prepare simple dips or spreads that complement the cuisine",
                "Add bread, crackers, or other accompaniments",
                "Garnish with fresh herbs or spices for visual appeal"
            ]
        }
    ]
    
    # Customize based on user input
    for recipe in recipe_templates:
        # Adjust ingredients based on season
        if user_input['season'] == "Winter":
            recipe['ingredients'].append("Root vegetables, warming spices")
        elif user_input['season'] == "Spring":
            recipe['ingredients'].append("Fresh greens, light herbs")
        elif user_input['season'] == "Summer":
            recipe['ingredients'].append("Fresh fruits, cooling ingredients")
        elif user_input['season'] == "Fall":
            recipe['ingredients'].append("Squash, apples, warming spices")
        
        # Adjust based on mood
        if "comfort" in user_input['mood'].lower():
            recipe['ingredients'].append("Creamy elements, warm spices")
            recipe['name'] = f"Comforting {recipe['name']}"
        elif "refresh" in user_input['mood'].lower():
            recipe['ingredients'].append("Citrus, fresh herbs")
            recipe['name'] = f"Refreshing {recipe['name']}"
        elif "energy" in user_input['mood'].lower():
            recipe['ingredients'].append("Protein-rich ingredients, energizing spices")
            recipe['name'] = f"Energizing {recipe['name']}"
    
    # Format the output
    output = "## Your Personalized Recipe Kit\n\n"
    output += f"Based on your preferences for {user_input['mood']} mood, {user_input['cuisine']} cuisine, and {user_input['season']} season, here are three recipe suggestions:\n\n"
    
    for i, recipe in enumerate(recipe_templates, 1):
        output += f"### Recipe {i}: {recipe['name']}\n\n"
        output += f"**Why it fits your preferences:** This dish combines elements of {user_input['cuisine']} cuisine with {user_input['season']} ingredients to create a {user_input['mood']} dining experience.\n\n"
        
        output += "**Ingredients:**\n"
        for ingredient in recipe['ingredients']:
            output += f"- {ingredient}\n"
        output += "\n"
        
        output += f"**Preparation Time:** {recipe['prep_time']}\n\n"
        
        output += "**Instructions:**\n"
        for j, step in enumerate(recipe['steps'], 1):
            output += f"{j}. {step}\n"
        output += "\n"
        
        output += "**Serving Suggestions:**\n"
        if user_input['season'] in ["Winter", "Fall"]:
            output += "- Serve warm with a side of crusty bread\n"
            output += "- Perfect for a cozy night in\n"
        else:
            output += "- Serve at room temperature or chilled\n"
            output += "- Great for picnics or light meals\n"
        output += "\n" + ("-" * 40) + "\n\n"
    
    # Add inspiration from similar recipes if available
    if similar_recipes:
        output += "### Inspiration From Similar Recipes\n\n"
        output += "These existing recipes inspired your personalized suggestions:\n"
        for recipe in similar_recipes:
            output += f"- {recipe['name']}: {recipe['description']}\n"
    
    return output

# Main app function
def main():
    # Initialize recipe database
    recipes = load_recipe_database()
    
    # App Header
    st.markdown('<h1 class="main-header">🍳 AI Recipe Generator</h1>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem;'>Create personalized recipes based on your mood, cuisine preferences, and the season - no API keys required!</p>",
        unsafe_allow_html=True
    )
    
    # Sidebar for inputs
    with st.sidebar:
        st.markdown("## 🎯 Your Preferences")
        
        mood = st.selectbox(
            "How are you feeling?",
            ["Comforting", "Refreshing", "Energizing", "Cozy", "Adventurous", "Social", "Happy"]
        )
        
        cuisine = st.selectbox(
            "What cuisine are you craving?",
            ["Italian", "Mexican", "Indian", "Thai", "Chinese", "American", "Mediterranean", "Japanese", "French"]
        )
        
        season = st.selectbox(
            "What's the season?",
            ["Winter", "Spring", "Summer", "Fall"]
        )
        
        # Additional options
        st.markdown("### Optional Preferences")
        diet = st.multiselect(
            "Dietary preferences",
            ["Vegetarian", "Vegan", "Gluten-free", "Dairy-free", "Nut-free"]
        )
        
        cooking_time = st.slider(
            "Max cooking time (minutes)",
            min_value=15,
            max_value=120,
            value=60,
            step=15
        )
        
        # Generate button
        generate_btn = st.button("Generate Recipes", type="primary")
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📊 Your Selections")
        st.info(f"""
        - **Mood:** {mood}
        - **Cuisine:** {cuisine}
        - **Season:** {season}
        - **Diet:** {', '.join(diet) if diet else 'None'}
        - **Max Time:** {cooking_time} minutes
        """)
        
        # Display sample recipes from the database
        with st.expander("View Recipe Database"):
            for recipe in recipes:
                st.write(f"**{recipe['name']}** ({recipe['cuisine']}, {recipe['season']})")
                st.caption(recipe['description'])
    
    with col2:
        st.markdown("### 🍽️ Generated Recipes")
        
        if generate_btn:
            with st.spinner("Creating your personalized recipes..."):
                # Prepare user input
                user_input = {
                    "mood": mood,
                    "cuisine": cuisine,
                    "season": season,
                    "diet": diet,
                    "cooking_time": cooking_time
                }

                # Validate input
                if validate_input(user_input):
                    # Find similar recipes
                    similar_recipes = find_similar_recipes(user_input, recipes)

                    # Generate the recipe kit
                    generated_output = generate_recipe_kit(user_input, similar_recipes)

                    # Display the generated recipe suggestions
                    st.markdown(generated_output, unsafe_allow_html=True)
                    
                    # Add option to save recipes
                    st.download_button(
                        label="Download Recipes",
                        data=generated_output,
                        file_name="personalized_recipes.md",
                        mime="text/markdown"
                    )
        else:
            st.info("Select your preferences and click 'Generate Recipes' to get started!")
            
            # Show sample output
            with st.expander("See sample recipe output"):
                st.markdown("""
                ### Recipe 1: Comforting Italian Inspired Bowl
                
                **Why it fits your preferences:** This dish combines elements of Italian cuisine with Winter ingredients to create a Comforting dining experience.
                
                **Ingredients:**
                - Base grain (rice, quinoa, or couscous)
                - Seasonal vegetables
                - Protein source
                - Signature sauce or dressing
                - Root vegetables, warming spices
                - Creamy elements, warm spices
                
                **Preparation Time:** 30-40 minutes
                
                **Instructions:**
                1. Cook your chosen grain according to package instructions
                2. Prepare and sauté seasonal vegetables
                3. Cook your protein with herbs and spices
                4. Combine all components in a bowl and drizzle with sauce
                
                **Serving Suggestions:**
                - Serve warm with a side of crusty bread
                - Perfect for a cozy night in
                """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div class="footer">Powered by Local AI • Made with ❤️ for food lovers</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()