import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 7) # Increased figure size for better visibility

# --- Step 1: Load the Dataset with Robust Settings ---
FILE_NAME = 'ecommerce_customer_data_large.csv'

try:
    # Fix 1 & 2: Use 'latin-1' encoding and 'on_bad_lines=skip' for robust loading
    df = pd.read_csv(FILE_NAME, encoding='latin-1', on_bad_lines='skip')
    print(f"Dataset '{FILE_NAME}' loaded successfully.")
except FileNotFoundError:
    print(f"Error: '{FILE_NAME}' not found. Please ensure the file is in the correct directory.")
    exit()

# Fix 3: Clean up column names by stripping leading/trailing spaces (CRITICAL for multi-word headers)
df.columns = df.columns.str.strip()

# Print initial info
print("\n--- Initial Dataset Info ---")
print(df.head())
print(df.info())

# Identify the correct column names (based on your confirmation)
PAYMENT_COL = 'Payment N'
# Fix 4: Use the precise, correct column name found in your file
TOTAL_PURCHASE_COL = 'Total Purchase Amount' 
CHURN_COL = 'Churn'
GENDER_COL = 'Gender'
AGE_COL = 'Age'
PRODUCT_CAT_COL = 'Product C' 
RETURNS_COL = 'Returns' # Adding Returns for potential future analysis

# --- Step 2: Data Cleaning and Preparation ---

# Convert the Total Purchase column to numeric
# This line now uses the correct column name 'Total Purchase Amount'
df[TOTAL_PURCHASE_COL] = pd.to_numeric(df[TOTAL_PURCHASE_COL], errors='coerce')
df.dropna(subset=[TOTAL_PURCHASE_COL], inplace=True)

# Drop the problematic 'Purchase Date' column (full of '#######' display errors)
if 'Purchase Date' in df.columns:
    df.drop('Purchase Date', axis=1, inplace=True)
elif 'Purchase' in df.columns: # For case where 'Date' part was stripped
    df.drop('Purchase', axis=1, inplace=True)


# --- Step 3: Customer Behavior Analysis and Visualization ---

# 1. Payment Method Preference Analysis
# ... (after df.read_csv and df.columns = df.columns.str.strip()) ...

# Identify the correct column names (Final check on all constants)
# 👇 FIX IS HERE 👇
PAYMENT_COL = 'Payment Name' 
TOTAL_PURCHASE_COL = 'Total Purchase Amount' 
CHURN_COL = 'Churn'
GENDER_COL = 'Gender'
AGE_COL = 'Age'
PRODUCT_CAT_COL = 'Product C' 

# ... (rest of the analysis code which should now work) ...

# 2. Churn Rate by Gender and Age
print("\n--- 2. Churn Rate by Gender and Age Analysis ---")

# Churn Rate by Gender
churn_by_gender = df.groupby(GENDER_COL)[CHURN_COL].mean().mul(100).reset_index(name='Churn_Rate_%')

plt.figure(figsize=(6, 5))
sns.barplot(x=GENDER_COL, y='Churn_Rate_%', data=churn_by_gender, palette='pastel')
plt.title('Churn Rate by Gender')
plt.xlabel('Gender')
plt.ylabel('Churn Rate (%)')
plt.ylim(0, churn_by_gender['Churn_Rate_%'].max() * 1.2)
plt.show()

# Distribution of Age for Churned vs. Non-Churned Customers
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x=AGE_COL, hue=CHURN_COL, multiple="stack", bins=30, kde=True, palette={0: 'skyblue', 1: 'salmon'})
plt.title('Age Distribution of Customers by Churn Status')
plt.xlabel('Age')
plt.ylabel('Count')
plt.legend(title='Churn', labels=['No Churn (0)', 'Churn (1)'])
plt.show()

# 3. Average Purchase Value by Product Category
# Assuming the necessary constants were defined earlier in your script as:
# TOTAL_PURCHASE_COL = 'Total Purchase Amount'
# PRODUCT_CAT_COL = 'Product Category' 

print("\n--- 3. Average Purchase Value by Product Category ---")

# Use the likely correct column name 'Product Category' for grouping
avg_purchase_by_category = df.groupby('Product Category')['Total Purchase Amount'].mean().sort_values(ascending=False).reset_index(name='Avg_Purchase')

plt.figure(figsize=(10, 5))
# Use the correct column name 'Product Category' for the x-axis
sns.barplot(x='Product Category', y='Avg_Purchase', data=avg_purchase_by_category, palette='viridis')
plt.title('Average Purchase Value by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Average Total Purchase Amount')
plt.xticks(rotation=45, ha='right') # Added rotation for better display of long category names
plt.tight_layout()
plt.show()