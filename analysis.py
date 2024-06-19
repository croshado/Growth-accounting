import pandas as pd

# Load the data
file_path = "C:\\Users\\vinay\\Downloads\\Active Users (4) (1) (1).csv - Active Users.csv"
df = pd.read_csv(file_path)

# Display the first few rows of the dataframe to understand its structure
print(df.head())
print(df.columns)


import numpy as np

# Initialize lists to store the metrics
new_users = []
resurrected_users = []
churned_users = []
retained_users = []
quick_ratios = []

# Convert the dataframe to a list of sets for easier comparison
weekly_active_users = [set(df[week].dropna()) for week in df.columns]

# Calculate metrics for each week
for i in range(1, len(weekly_active_users)):
    current_week = weekly_active_users[i]
    previous_week = weekly_active_users[i - 1]
    
    new = current_week - previous_week
    resurrected = current_week & previous_week
    churned = previous_week - current_week
    retained = current_week & previous_week
    
    new_users.append(len(new))
    resurrected_users.append(len(resurrected))
    churned_users.append(len(churned))
    retained_users.append(len(retained))
    
    if len(churned) > 0:
        quick_ratio = (len(new) + len(resurrected)) / len(churned)
    else:
        quick_ratio = np.inf  # If there are no churned users, set quick ratio to infinity
    quick_ratios.append(quick_ratio)

# Create a dataframe to store the results
metrics_df = pd.DataFrame({
    'Week': df.columns[1:],
    'New Users': new_users,
    'Resurrected Users': resurrected_users,
    'Churned Users': churned_users,
    'Retained Users': retained_users,
    'Quick Ratio': quick_ratios
})

print(metrics_df.head())



import matplotlib.pyplot as plt
import seaborn as sns

# Set the style of the visualization
sns.set(style='whitegrid')

# Create a figure and axis
# Adjust the x-axis labels to create gaps in the week names
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot the metrics
sns.lineplot(data=metrics_df, x='Week', y='New Users', ax=ax1, label='New Users')
sns.lineplot(data=metrics_df, x='Week', y='Resurrected Users', ax=ax1, label='Resurrected Users')
sns.lineplot(data=metrics_df, x='Week', y='Churned Users', ax=ax1, label='Churned Users')
sns.lineplot(data=metrics_df, x='Week', y='Retained Users', ax=ax1, label='Retained Users')

# Create a second y-axis for the quick ratio
ax2 = ax1.twinx()
sns.lineplot(data=metrics_df, x='Week', y='Quick Ratio', ax=ax2, label='Quick Ratio', color='purple')

# Set the labels and title
ax1.set_xlabel('Week')
ax1.set_ylabel('Number of Users')
ax2.set_ylabel('Quick Ratio')
plt.title('Weekly Growth Accounting')

# Adjust the x-axis labels
ax1.set_xticks(ax1.get_xticks()[::2])  # Show every other week label

# Display the legend
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# Show the plot
plt.show()