import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib.cm import get_cmap
from matplotlib.colors import LinearSegmentedColormap

# Load data
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df.columns = df.columns.str.strip()

# Process skills
skills_series = df["required_skills"].dropna().str.split(', ')
all_skills = skills_series.explode().str.strip()
skill_counts = all_skills.value_counts()

# Frequency bounds
max_freq = skill_counts.max()
min_freq = skill_counts.min()

# Truncate inferno to remove yellow top
def truncate_colormap(cmap, minval=0.0, maxval=0.85, n=256):
    new_cmap = LinearSegmentedColormap.from_list(
        f'trunc({cmap.name},{minval:.2f},{maxval:.2f})',
        cmap(np.linspace(minval, maxval, n))
    )
    return new_cmap

# Create a smoother, darker inferno
original_cmap = get_cmap('inferno')
truncated_inferno = truncate_colormap(original_cmap, 0.0, 0.85)

# Define color function
def gradient_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    freq = skill_counts.get(word, 0)
    norm_freq = (freq - min_freq) / (max_freq - min_freq) if max_freq != min_freq else 0
    r, g, b, _ = truncated_inferno(norm_freq)
    return f"rgb({int(r*255)}, {int(g*255)}, {int(b*255)})"

# Generate word cloud
wordcloud = WordCloud(width=1280,
                      height=1280,
                      background_color='white',
                      max_words=100,
                      color_func=gradient_color_func,
                      font_path = '/Users/tameemsuleiman/Downloads/Montserrat/static/Montserrat-Black.ttf').generate_from_frequencies(skill_counts)

# Plot the word cloud
plt.figure(figsize=(24, 24))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Top Required Skills for AI Jobs in 2025", fontsize=16)
plt.tight_layout()

# Render the visualization
plt.show()