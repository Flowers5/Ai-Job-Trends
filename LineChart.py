import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import get_cmap
from matplotlib.colors import LinearSegmentedColormap
from sns_style import first_viz_style as styles

styles()

# Load dataset
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# Data cleaning and preprocessing
df.rename(columns={"job_title": "Title", "salary_usd": "Salary",
                   "company_name": "Company", "experience_level": "Level",
                   "education_required": "Education", "years_experience": "Experience"}, inplace=True)

df["Experience"] = df["Experience"].replace({"SE": "Senior", "MI": "Mid", "EN": "Entry"})

df.drop(columns=["job_id", "salary_currency", "job_description_length", "benefits_score",
                 "application_deadline", "posting_date"], inplace=True)

# Start index count at 1
df.index = range(1, len(df) + 1)

# Display the first 10 rows of the DataFrame (For reference)
print(df.head(10))

### Visualizing the data ###
# Count occurrences of each industry and find the most common one
count = df["industry"].value_counts()
most_common = count.idxmax()

# Group by job title and calculate average salary
df = df.groupby("Title")["Salary"].mean().reset_index()
df = df.sort_values(by="Salary", ascending=False)

# Truncate the colormap to remove bright yellow
def truncate_colormap(cmap, minval=0.0, maxval=0.85, n=256):
    new_cmap = LinearSegmentedColormap.from_list(
        f'trunc({cmap.name},{minval:.2f},{maxval:.2f})',
        cmap(np.linspace(minval, maxval, n))
    )
    return new_cmap

# Create a darker version of Inferno
cmap = truncate_colormap(get_cmap("inferno"), 0.0, 0.85)

# Create gradient line plot
fig, ax = plt.subplots(figsize=(14, 7))

norm = plt.Normalize(df["Salary"].min(), df["Salary"].max())
x = np.arange(len(df))
y = df["Salary"].values

for i in range(len(x) - 1):
    ax.plot(x[i:i + 2], y[i:i + 2], color=cmap(norm(y[i])), linewidth=3)

# Labeling
ax.set_xticks(x)
ax.set_xticklabels(df["Title"], rotation=90, ha="right")
ax.set_title(f"Average Salary by Job Title (Most Common Industry: {most_common})", fontsize=16, fontweight="bold")
ax.set_ylabel("Average Salary")

plt.tight_layout()
plt.show()
