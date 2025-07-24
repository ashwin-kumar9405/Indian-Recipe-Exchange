# Indian Recipe Exchange 🇮🇳

A multilingual, offline-first web application for sharing and collecting traditional Indian recipes in native languages. Designed as a corpus collection engine for inclusive, culturally aware AI models.

## Features
- 🔤 **Multilingual Input:** Supports major Indian languages for recipe entry
- 🤖 **AI Integration:** Open-source AI for translation and ingredient suggestions
- 📶 **Offline-First:** Works in low-bandwidth or intermittent internet areas
- 🗃️ **Corpus Storage:** Collects and stores recipes tagged by region and language
- 🚀 **Deployable on Hugging Face Spaces**
- 📝 **Corpus Generation:** Usable dataset for Indian cultural/linguistic AI training

## Usage
1. Enter recipe name, ingredients, and instructions in your preferred language
2. Choose the language and (optionally) region
3. Submit your recipe to contribute to the corpus
4. Browse, upvote, and save recipes from others

## Tech Stack
- [Streamlit](https://streamlit.io/) for UI
- [Transformers](https://huggingface.co/transformers/) and [Indic NLP](https://github.com/anoopkunchukuttan/indic_nlp_library) for AI/translation
- Offline-first storage (to be implemented)

## Deployment
- Clone this repo
- Install dependencies: `pip install -r requirements.txt`
- Run locally: `streamlit run app.py`
- Deploy on [Hugging Face Spaces](https://huggingface.co/spaces)

## Contributing
Pull requests and suggestions welcome! Please help us build a diverse, inclusive recipe corpus for India.

## License
MIT