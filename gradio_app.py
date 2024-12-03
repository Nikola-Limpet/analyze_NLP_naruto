import streamlit as st
from theme_classifier import ThemeClassifier
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def get_themes(theme_list_str, subtitles_path, save_path):
    try:
        # Input validation
        if not theme_list_str or not subtitles_path:
            st.error("Please provide themes and subtitles path.")
            return None

        theme_list = [t.strip() for t in theme_list_str.split(',')]
        theme_classifier = ThemeClassifier(theme_list)
        output_df = theme_classifier.get_themes(subtitles_path, save_path)

        # Remove dialogue from the theme list
        theme_list = [theme for theme in theme_list if theme != 'dialogue']
        output_df = output_df[theme_list]

        # Prepare data for plotting
        plot_data = pd.DataFrame({
            'Theme': theme_list,
            'Score': output_df[theme_list].sum().values
        })

        return plot_data
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Streamlit App
def main():
    st.title("Theme Classification (Zero Shot Classifiers)")
    st.markdown("### Analyze Themes in Subtitles or Scripts")

    # Inputs
    theme_list_str = st.text_input(
        label="Themes (comma-separated)",
        value="action,adventure,friendship",
        help="Enter themes separated by commas"
    )
    subtitles_path = st.text_input(
        label="Subtitles or Script Path",
        value="/data/Subtitles",
        help="Path to the subtitles file"
    )
    save_path = st.text_input(
        label="Save Path",
        value="output/themes.csv",
        help="Where to save the results"
    )

    # Button
    if st.button("Analyze Themes"):
        st.info("Processing...")
        plot_data = get_themes(theme_list_str, subtitles_path, save_path)
        if plot_data is not None:
            st.success("Analysis completed successfully!")
            
            # Display Bar Chart
            st.bar_chart(data=plot_data.set_index("Theme"))

            # Display Data
            st.dataframe(plot_data)

if __name__ == '__main__':
    main()
