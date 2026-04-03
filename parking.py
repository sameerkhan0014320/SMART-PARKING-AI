# ============================================
# Project 72: Smart Parking Occupancy Prediction
# Student: [sameer khan]
# Section: 504-A | AI Applications Lab
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

print("=" * 50)
print("  Smart Parking Occupancy Prediction System")
print("=" * 50)

# ---- 1. LOAD DATA ----
df = pd.read_csv('dataset.csv')
print(f"\n✅ Dataset Loaded! Shape: {df.shape}")
print(df.head())

# ---- 2. PREPROCESSING ----
df.dropna(inplace=True)
df['LastUpdated'] = pd.to_datetime(df['LastUpdated'])
df['Hour']    = df['LastUpdated'].dt.hour
df['Minute']  = df['LastUpdated'].dt.minute
df['Day']     = df['LastUpdated'].dt.dayofweek
df['OccupancyRate'] = df['Occupancy'] / df['Capacity']

le = LabelEncoder()
df['Location_enc'] = le.fit_transform(df['SystemCodeNumber'])

print("\n✅ Preprocessing Done!")

# ---- 3. FEATURES & TARGET ----
X = df[['Hour', 'Minute', 'Day', 'Capacity', 'Location_enc']]
y = df['OccupancyRate']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\n✅ Train: {X_train.shape} | Test: {X_test.shape}")

# ---- 4. MODEL TRAINING ----
model = LinearRegression()
model.fit(X_train, y_train)
print("\n✅ Model Trained!")

# ---- 5. EVALUATION ----
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2   = r2_score(y_test, y_pred)

print("\n" + "=" * 40)
print("        MODEL RESULTS")
print("=" * 40)
print(f"  RMSE  : {rmse:.4f}")
print(f"  R²    : {r2:.4f}")
print("=" * 40)

# ---- 6. VISUALIZATIONS ----
plt.style.use('dark_background')
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Smart Parking Occupancy Prediction', 
             fontsize=18, fontweight='bold', color='cyan')

# Plot 1: Actual vs Predicted
axes[0,0].scatter(y_test, y_pred, alpha=0.4, color='cyan', s=10)
axes[0,0].plot([0,1],[0,1], color='red', linestyle='--', linewidth=2)
axes[0,0].set_title('Actual vs Predicted', color='white')
axes[0,0].set_xlabel('Actual')
axes[0,0].set_ylabel('Predicted')

# Plot 2: Hourly Trend
hourly = df.groupby('Hour')['OccupancyRate'].mean()
axes[0,1].plot(hourly.index, hourly.values, 
               marker='o', color='lime', linewidth=2)
axes[0,1].fill_between(hourly.index, hourly.values, alpha=0.3, color='lime')
axes[0,1].set_title('Avg Occupancy by Hour', color='white')
axes[0,1].set_xlabel('Hour of Day')
axes[0,1].set_ylabel('Occupancy Rate')

# Plot 3: Day-wise Trend
days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
daily = df.groupby('Day')['OccupancyRate'].mean()
axes[1,0].bar(days[:len(daily)], daily.values, color='orange', edgecolor='white')
axes[1,0].set_title('Avg Occupancy by Day', color='white')
axes[1,0].set_xlabel('Day')
axes[1,0].set_ylabel('Occupancy Rate')

# Plot 4: Feature Importance
coef_df = pd.DataFrame({
    'Feature': ['Hour','Minute','Day','Capacity','Location'],
    'Importance': np.abs(model.coef_)
}).sort_values('Importance', ascending=True)

axes[1,1].barh(coef_df['Feature'], coef_df['Importance'], 
               color='violet', edgecolor='white')
axes[1,1].set_title('Feature Importance', color='white')

plt.tight_layout()
plt.savefig('parking_results.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Graph saved as parking_results.png")

# ---- 7. LIVE PREDICTION ----
print("\n" + "=" * 40)
print("      LIVE PREDICTION DEMO")
print("=" * 40)

sample = pd.DataFrame({
    'Hour':         [9],
    'Minute':       [30],
    'Day':          [0],
    'Capacity':     [500],
    'Location_enc': [3]
})

pred = model.predict(sample)[0]
print(f"\n  Parking Location : Zone 3")
print(f"  Time             : Monday 9:30 AM")
print(f"  Capacity         : 500 slots")
print(f"  Predicted Fill   : {pred*100:.1f}%")

if pred > 0.8:
    print("  Status           : 🔴 Almost FULL!")
elif pred > 0.5:
    print("  Status           : 🟡 Moderate")
else:
    print("  Status           : 🟢 Plenty of Space")

print("\n" + "=" * 50)
print("  Project Complete! 🎉")
print("=" * 50)