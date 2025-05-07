import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

def generate_nim_data(num_samples=20000, max_pile_size=10):
    data = []
    for _ in range(num_samples):
        piles = [random.randint(0, max_pile_size) for _ in range(3)]
        nim_sum = piles[0] ^ piles[1] ^ piles[2]
        winner = 1 if nim_sum != 0 else 0  # 1 = Winning position, 0 = Losing
        data.append(piles + [winner])
    return data

# Create dataset
dataset = generate_nim_data()

# Save to CSV
df = pd.DataFrame(dataset, columns=["pile1", "pile2", "pile3", "winner"])
df.to_csv('nim_dataset.csv', index=False)
print("Dataset saved to nim_dataset.csv ✅")

# Train a better Model
X = df[["pile1", "pile2", "pile3"]]
y = df["winner"]

model = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
model.fit(X, y)

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Better model trained and saved as model.pkl ✅")
