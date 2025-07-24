import streamlit as st
from typing import List
import json
import os
from indic_transliteration.sanscript import transliterate
from transformers import pipeline

st.set_page_config(page_title="Indian Recipe Exchange", layout="wide")

st.title("Indian Recipe Exchange 🇮🇳")
st.markdown("""
Share your family's traditional recipes in your native language! This app is multilingual, offline-friendly, and helps build a diverse Indian cooking corpus for AI research.
""")

# Language options (major Indian languages)
languages = [
    "English", "Hindi", "Bengali", "Telugu", "Marathi", "Tamil", "Urdu", "Gujarati", "Kannada", "Odia", "Punjabi", "Malayalam", "Assamese", "Maithili", "Santali", "Kashmiri", "Nepali"
]

RECIPES_FILE = "recipes.json"

def load_recipes():
    if os.path.exists(RECIPES_FILE):
        with open(RECIPES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_recipes(recipes):
    with open(RECIPES_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)

# Initialize translation pipeline (offline/online fallback)
try:
    translation_pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
except Exception:
    translation_pipe = None

# Simple ingredient substitution dictionary (expand as needed)
ingredient_subs = {
    "paneer": {"English": "cottage cheese", "Hindi": "पनीर"},
    "mustard oil": {"English": "mustard oil", "Bengali": "সরিষার তেল"},
    "ghee": {"English": "clarified butter", "Hindi": "घी"}
}

with st.form("recipe_form"):
    recipe_name = st.text_input("Recipe Name")
    language = st.selectbox("Recipe Language", languages)
    region = st.text_input("Region (optional)")
    ingredients = st.text_area("Ingredients (one per line)")
    steps = st.text_area("Step-by-step Instructions")
    suggest = st.form_submit_button("Suggest Ingredient Substitutions/Translations")
    submit = st.form_submit_button("Submit Recipe")

if suggest and ingredients:
    st.markdown("**AI Ingredient Suggestions:**")
    for line in ingredients.split("\n"):
        key = line.strip().lower()
        if key in ingredient_subs and language in ingredient_subs[key]:
            st.write(f"{line} → {ingredient_subs[key][language]}")
        elif translation_pipe and language != "English":
            try:
                translated = translation_pipe(line, src_lang="en", tgt_lang=language[:2].lower())[0]['translation_text']
                st.write(f"{line} → {translated}")
            except Exception:
                st.write(f"{line} (translation unavailable)")
        elif language != "English":
            try:
                # Example: Transliterate ingredient to target script (e.g., Hindi)
                transliterated = transliterate(line, "hk", language[:2].lower())
                st.write(f"{line} → {transliterated}")
            except Exception:
                st.write(f"{line} (transliteration unavailable)")
        else:
            st.write(f"{line} (no suggestion)")

if submit:
    st.success("Recipe submitted! (Corpus collection in progress)")
    new_recipe = {
        "name": recipe_name,
        "language": language,
        "region": region,
        "ingredients": ingredients,
        "steps": steps,
        "upvotes": 0
    }
    recipes = load_recipes()
    recipes.append(new_recipe)
    save_recipes(recipes)
st.markdown("---")
st.header("Browse & Upvote Recipes")

# --- Enhancement: Search/filter recipes ---
search_lang = st.selectbox("Filter by Language", ["All"] + languages, key="search_lang")
search_region = st.text_input("Filter by Region (optional)", key="search_region")

recipes = load_recipes()
if search_lang != "All":
    recipes = [r for r in recipes if r["language"] == search_lang]
if search_region:
    recipes = [r for r in recipes if search_region.lower() in r["region"].lower()]

if recipes:
    for idx, recipe in enumerate(recipes):
        st.subheader(f"{recipe['name']} ({recipe['language']})")
        st.caption(f"Region: {recipe['region']}")
        st.markdown(f"**Ingredients:**\n{recipe['ingredients']}")
        st.markdown(f"**Instructions:**\n{recipe['steps']}")
        cols = st.columns([1, 2])
        with cols[0]:
            if st.button(f"👍 Upvote ({recipe['upvotes']})", key=f"upvote_{idx}"):
                recipes[idx]['upvotes'] += 1
                save_recipes(recipes)
                st.experimental_rerun()
        st.markdown("---")
else:
    st.info("No recipes found for the selected filters.")
    st.info("No recipes submitted yet. Be the first to contribute!")