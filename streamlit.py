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
    .tag {
        display: inline-block;
        background-color: #e0e0e0;
        border-radius: 15px;
        padding: 2px 10px;
        margin: 2px;
        font-size: 0.8rem;
    }
    .nutrition-facts {
        background-color: #fff;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Expanded recipe database with more variety
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
            "calories": 320,
            "tags": ["vegetarian", "gluten-free", "quick"],
            "embedding": [0.8, 0.1, 0.4, 0.2, 0.7, 0.3, 0.1, 0.9, 0.5, 0.6]
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
            "calories": 450,
            "tags": ["high-protein", "hearty", "slow-cooked"],
            "embedding": [0.2, 0.8, 0.7, 0.9, 0.1, 0.4, 0.6, 0.3, 0.5, 0.2]
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
            "calories": 380,
            "tags": ["vegetarian", "quick", "fresh"],
            "embedding": [0.5, 0.3, 0.2, 0.1, 0.9, 0.7, 0.4, 0.6, 0.8, 0.3]
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
            "calories": 280,
            "tags": ["vegetarian", "gluten-free", "creamy"],
            "embedding": [0.3, 0.6, 0.8, 0.4, 0.2, 0.5, 0.9, 0.7, 0.1, 0.4]
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
            "calories": 420,
            "tags": ["spicy", "aromatic", "adaptable"],
            "embedding": [0.7, 0.4, 0.3, 0.6, 0.8, 0.2, 0.5, 0.1, 0.9, 0.7]
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
            "calories": 350,
            "tags": ["vegetarian", "shareable", "no-cook"],
            "embedding": [0.9, 0.2, 0.5, 0.7, 0.3, 0.1, 0.8, 0.4, 0.6, 0.2]
        },
        {
            "name": "Cozy Hot Chocolate",
            "cuisine": "International",
            "season": "Winter",
            "mood": "Comforting",
            "ingredients": ["Milk", "dark chocolate", "cocoa powder", "sugar", "vanilla extract", "whipped cream"],
            "prep_time": "10 minutes",
            "description": "A rich and creamy hot chocolate to warm your soul",
            "instructions": [
                "Heat milk in a saucepan over medium heat",
                "Whisk in chopped chocolate, cocoa powder, and sugar",
                "Stir continuously until chocolate is melted and mixture is smooth",
                "Remove from heat and stir in vanilla extract",
                "Pour into mugs and top with whipped cream"
            ],
            "calories": 320,
            "tags": ["vegetarian", "quick", "dessert"],
            "embedding": [0.1, 0.9, 0.8, 0.3, 0.2, 0.4, 0.7, 0.5, 0.6, 0.1]
        },
        {
            "name": "Energizing Green Smoothie",
            "cuisine": "International",
            "season": "All",
            "mood": "Energizing",
            "ingredients": ["Spinach", "banana", "green apple", "almond milk", "chia seeds", "protein powder"],
            "prep_time": "5 minutes",
            "description": "A nutrient-packed smoothie to start your day right",
            "instructions": [
                "Add all ingredients to a blender",
                "Blend until smooth and creamy",
                "Add more liquid if needed to reach desired consistency",
                "Pour into a glass and enjoy immediately"
            ],
            "calories": 280,
            "tags": ["vegan", "gluten-free", "quick", "healthy"],
            "embedding": [0.6, 0.2, 0.1, 0.5, 0.9, 0.7, 0.3, 0.4, 0.8, 0.6]
        }
    ]
    return recipes

# Improved embedding function with better semantic mapping
def create_text_embedding(text):
    # Create a more sophisticated embedding based on semantic categories
    words = text.lower().split()
    embedding = [0.0] * 10  # 10-dimensional embedding
    
    # Define semantic categories for each dimension
    categories = {
        0: ["winter", "cold", "snow", "warm", "hearty", "stew", "soup", "hot"],
        1: ["summer", "warm", "sun", "refreshing", "cool", "salad", "light"],
        2: ["spring", "fresh", "green", "renewal", "light", "vegetable"],
        3: ["fall", "autumn", "cozy", "pumpkin", "spice", "comfort"],
        4: ["comforting", "cozy", "warm", "hearty", "rich", "creamy"],
        5: ["refreshing", "light", "cool", "crisp", "fresh", "zesty"],
        6: ["energizing", "vibrant", "invigorating", "active", "healthy"],
        7: ["adventurous", "spicy", "bold", "exotic", "aromatic"],
        8: ["social", "sharing", "gathering", "party", "platter"],
        9: ["quick", "easy", "fast", "simple", "minimal"]
    }
    
    for word in words:
        for dim, keywords in categories.items():
            if word in keywords:
                embedding[dim] += 0.2
                
    # Add some randomness to differentiate similar inputs
    for i in range(len(embedding)):
        embedding[i] += random.uniform(0, 0.1)
        
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
            
        # Apply dietary filters if specified
        if user_input.get('diet'):
            recipe_tags = [tag.lower() for tag in recipe.get('tags', [])]
            user_diet = [d.lower() for d in user_input['diet']]
            
            # Check if recipe matches all dietary requirements
            matches_diet = all(any(diet_tag in tag for tag in recipe_tags) for diet_tag in user_diet)
            if not matches_diet:
                similarity *= 0.5  # Reduce similarity for non-matching diets
                
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
            recipe['ingredients'].extend(["Root vegetables", "Warming spices like cinnamon or nutmeg", "Hearty greens like kale or collards"])
            recipe['prep_time'] = "40-50 minutes"  # Winter dishes often take longer
        elif user_input['season'] == "Spring":
            recipe['ingredients'].extend(["Fresh greens", "Light herbs like parsley or dill", "Early spring vegetables like asparagus or peas"])
        elif user_input['season'] == "Summer":
            recipe['ingredients'].extend(["Fresh fruits", "Cooling ingredients like cucumber or mint", "Light, fresh vegetables"])
            if "Bowl" in recipe['name']:
                recipe['ingredients'].append("Chilled elements")
        elif user_input['season'] == "Fall":
            recipe['ingredients'].extend(["Squash", "Apples or pears", "Warming spices like cinnamon or cloves"])
        
        # Adjust based on mood
        mood = user_input['mood'].lower()
        if "comfort" in mood:
            recipe['ingredients'].extend(["Creamy elements", "Warm spices", "Rich ingredients"])
            recipe['name'] = f"Comforting {recipe['name']}"
        elif "refresh" in mood:
            recipe['ingredients'].extend(["Citrus", "Fresh herbs", "Crisp vegetables"])
            recipe['name'] = f"Refreshing {recipe['name']}"
        elif "energy" in mood:
            recipe['ingredients'].extend(["Protein-rich ingredients", "Energizing spices like ginger or turmeric", "Whole grains"])
            recipe['name'] = f"Energizing {recipe['name']}"
        elif "adventurous" in mood:
            recipe['ingredients'].extend(["Exotic spices", "Unusual ingredients", "Bold flavors"])
            recipe['name'] = f"Adventurous {recipe['name']}"
        elif "social" in mood:
            recipe['ingredients'].extend(["Shareable components", "Colorful ingredients", "Interactive elements"])
            recipe['name'] = f"Social {recipe['name']}"
            
        # Adjust based on cuisine
        cuisine = user_input['cuisine'].lower()
        if "italian" in cuisine:
            recipe['ingredients'].extend(["Olive oil", "Garlic", "Basil", "Tomatoes"])
        elif "mexican" in cuisine:
            recipe['ingredients'].extend(["Chili peppers", "Cilantro", "Lime", "Beans"])
        elif "indian" in cuisine:
            recipe['ingredients'].extend(["Curry spices", "Ginger", "Yogurt", "Lentils"])
        elif "thai" in cuisine:
            recipe['ingredients'].extend(["Coconut milk", "Lemongrass", "Fish sauce", "Thai basil"])
        elif "mediterranean" in cuisine:
            recipe['ingredients'].extend(["Olives", "Feta cheese", "Lemon", "Olive oil"])
            
        # Adjust based on dietary preferences
        if user_input.get('diet'):
            diet = user_input['diet']
            if "Vegetarian" in diet:
                recipe['ingredients'] = [ing for ing in recipe['ingredients'] if "chicken" not in ing.lower() and "beef" not in ing.lower()]
                recipe['ingredients'].append("Plant-based protein (tofu, tempeh, or legumes)")
            if "Vegan" in diet:
                recipe['ingredients'] = [ing for ing in recipe['ingredients'] if "cheese" not in ing.lower() and "cream" not in ing.lower()]
                recipe['ingredients'].append("Plant-based alternatives")
            if "Gluten-free" in diet:
                recipe['ingredients'] = [ing for ing in recipe['ingredients'] if "pasta" not in ing.lower() and "bread" not in ing.lower()]
                recipe['ingredients'].append("Gluten-free grains (quinoa, rice, or gluten-free pasta)")
                
        # Adjust cooking time based on user preference
        max_time = user_input.get('cooking_time', 60)
        if "Soup" in recipe['name'] and max_time < 45:
            recipe['prep_time'] = "30-40 minutes"
            recipe['steps'] = [step.replace("simmer until cooked through", "simmer for 20-25 minutes") for step in recipe['steps']]
    
    # Format the output with enhanced styling
    output = "## 🍳 Your Personalized Recipe Kit\n\n"
    output += f"Based on your preferences for **{user_input['mood']}** mood, **{user_input['cuisine']}** cuisine, and **{user_input['season']}** season, here are three recipe suggestions:\n\n"
    
    for i, recipe in enumerate(recipe_templates, 1):
        output += f"### Recipe {i}: {recipe['name']}\n\n"
        output += f"**Why it fits your preferences:** This dish combines elements of {user_input['cuisine']} cuisine with {user_input['season']} ingredients to create a {user_input['mood']} dining experience.\n\n"
        
        output += "**Ingredients:**\n"
        output += '<div class="ingredient-list">\n'
        for ingredient in recipe['ingredients']:
            output += f"- {ingredient}\n"
        output += "</div>\n\n"
        
        output += f"**Preparation Time:** {recipe['prep_time']}\n\n"
        
        output += "**Instructions:**\n"
        output += '<div class="instruction-list">\n'
        for j, step in enumerate(recipe['steps'], 1):
            output += f"{j}. {step}\n"
        output += "</div>\n\n"
        
        output += "**Serving Suggestions:**\n"
        if user_input['season'] in ["Winter", "Fall"]:
            output += "- Serve warm with a side of crusty bread\n"
            output += "- Perfect for a cozy night in\n"
            output += "- Pair with a robust red wine or warm cider\n"
        else:
            output += "- Serve at room temperature or chilled\n"
            output += "- Great for picnics or light meals\n"
            output += "- Pair with a crisp white wine or iced tea\n"
            
        # Add wine pairing suggestions
        if user_input['cuisine'] == "Italian":
            output += "- Wine pairing: Chianti or Pinot Grigio\n"
        elif user_input['cuisine'] == "Mexican":
            output += "- Beverage pairing: Margarita or Mexican beer\n"
        elif user_input['cuisine'] == "Indian":
            output += "- Beverage pairing: Mango lassi or Indian beer\n"
        elif user_input['cuisine'] == "Thai":
            output += "- Beverage pairing: Thai iced tea or light lager\n"
            
        output += "\n" + ("-" * 50) + "\n\n"
    
    # Add inspiration from similar recipes if available
    if similar_recipes:
        output += "### Inspiration From Similar Recipes\n\n"
        output += "These existing recipes inspired your personalized suggestions:\n"
        for recipe in similar_recipes:
            tags = " ".join([f'<span class="tag">{tag}</span>' for tag in recipe.get('tags', [])])
            output += f"- **{recipe['name']}**: {recipe['description']} {tags}\n"
    
    # Add nutritional information
    output += "\n### Nutritional Notes\n\n"
    output += "<div class='nutrition-facts'>\n"
    output += "These recipes are designed to be balanced and nutritious. For specific dietary needs:\n"
    output += "- To reduce calories: Use less oil, choose lean proteins, and increase vegetables\n"
    output += "- To increase protein: Add legumes, nuts, seeds, or lean meats\n"
    output += "- To make gluten-free: Use gluten-free grains and verify all sauces are gluten-free\n"
    output += "- To make vegan: Substitute dairy with plant-based alternatives and omit animal products\n"
    output += "</div>\n"
    
    return output

# Function to display recipe in a nice format
def display_recipe(recipe):
    st.markdown(f"### {recipe['name']}")
    st.caption(f"{recipe['cuisine']} • {recipe['season']} • {recipe['mood']} • {recipe['prep_time']}")
    st.write(recipe['description'])
    
    # Display tags
    tags = recipe.get('tags', [])
    if tags:
        tag_html = " ".join([f'<span class="tag">{tag}</span>' for tag in tags])
        st.markdown(tag_html, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Ingredients:**")
        st.markdown('<div class="ingredient-list">', unsafe_allow_html=True)
        for ingredient in recipe['ingredients']:
            st.markdown(f"- {ingredient}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown("**Instructions:**")
        st.markdown('<div class="instruction-list">', unsafe_allow_html=True)
        for i, step in enumerate(recipe['instructions'], 1):
            st.markdown(f"{i}. {step}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"**Calories:** Approximately {recipe.get('calories', 'N/A')} per serving")
    st.markdown("---")

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
            ["Comforting", "Refreshing", "Energizing", "Cozy", "Adventurous", "Social", "Happy", "Relaxed"]
        )
        
        cuisine = st.selectbox(
            "What cuisine are you craving?",
            ["Italian", "Mexican", "Indian", "Thai", "Chinese", "American", "Mediterranean", "Japanese", "French", "Any"]
        )
        
        season = st.selectbox(
            "What's the season?",
            ["Winter", "Spring", "Summer", "Fall", "Any"]
        )
        
        # Additional options
        st.markdown("### Optional Preferences")
        diet = st.multiselect(
            "Dietary preferences",
            ["Vegetarian", "Vegan", "Gluten-free", "Dairy-free", "Nut-free", "Low-carb", "High-protein"]
        )
        
        cooking_time = st.slider(
            "Max cooking time (minutes)",
            min_value=15,
            max_value=120,
            value=60,
            step=15
        )
        
        # Advanced options
        with st.expander("Advanced Options"):
            complexity = st.select_slider(
                "Recipe complexity",
                options=["Very Easy", "Easy", "Medium", "Challenging", "Expert"]
            )
            
            servings = st.number_input(
                "Number of servings",
                min_value=1,
                max_value=10,
                value=4
            )
        
        # Generate button
        generate_btn = st.button("Generate Recipes", type="primary", use_container_width=True)
        
        # Add a button to view all recipes
        view_all = st.button("View All Recipes", use_container_width=True)
    
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
        - **Complexity:** {complexity if 'complexity' in locals() else 'Medium'}
        - **Servings:** {servings if 'servings' in locals() else 4}
        """)
        
        # Display sample recipes from the database
        with st.expander("View Recipe Database"):
            for recipe in recipes:
                st.write(f"**{recipe['name']}** ({recipe['cuisine']}, {recipe['season']})")
                st.caption(recipe['description'])
                if st.button("View Details", key=recipe['name']):
                    display_recipe(recipe)
    
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
                        mime="text/markdown",
                        use_container_width=True
                    )
                    
                    # Add a button to generate again with slight variations
                    if st.button("Generate Different Variations", use_container_width=True):
                        st.experimental_rerun()
        
        elif view_all:
            st.markdown("### All Available Recipes")
            for recipe in recipes:
                display_recipe(recipe)
                
        else:
            st.info("Select your preferences and click 'Generate Recipes' to get started!")
            
            # Show sample output
            with st.expander("See sample recipe output"):
                st.markdown("""
                ### Recipe 1: Comforting Italian Inspired Bowl
                
                **Why it fits your preferences:** This dish combines elements of Italian cuisine with Winter ingredients to create a Comforting dining experience.
                
                **Ingredients:**
                <div class="ingredient-list">
                - Base grain (rice, quinoa, or couscous)
                - Seasonal vegetables
                - Protein source
                - Signature sauce or dressing
                - Root vegetables, warming spices
                - Creamy elements, warm spices
                - Olive oil, Garlic, Basil, Tomatoes
                </div>
                
                **Preparation Time:** 30-40 minutes
                
                **Instructions:**
                <div class="instruction-list">
                1. Cook your chosen grain according to package instructions
                2. Prepare and sauté seasonal vegetables
                3. Cook your protein with herbs and spices
                4. Combine all components in a bowl and drizzle with sauce
                </div>
                
                **Serving Suggestions:**
                - Serve warm with a side of crusty bread
                - Perfect for a cozy night in
                - Pair with a robust red wine or warm cider
                - Wine pairing: Chianti or Pinot Grigio
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div class="footer">Powered by Local AI • Made with ❤️ for food lovers</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()