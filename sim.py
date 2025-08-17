```python
import numpy as np
import pandas as pd
from scipy.stats import entropy

# Set random seed for reproducibility
np.random.seed(42)

# Define parameters for PV simulated data (150 samples: 75 lesional, 75 non-lesional)
n_samples = 150
n_patients = 75
n_asvs = 5  # Staphylococcus, Propionibacterium, Corynebacterium, Streptococcus, Lactobacillus

# Initialize data
data = {
    'SampleID': [f'S{i+1}' for i in range(n_samples)],
    'PatientID': [f'P{(i//2)+1}' for i in range(n_samples)],  # 2 samples per patient
    'Site': ['L' if i % 2 == 0 else 'NL' for i in range(n_samples)]  # Alternate L/NL
}

# Generate ASV abundances (sum to 1 per sample, PV-specific dysbiosis)
asv_names = ['Staphylococcus', 'Propionibacterium', 'Corynebacterium', 'Streptococcus', 'Lactobacillus']
asv_data = []
for i in range(n_samples):
    if data['Site'][i] == 'L':  # Lesional: high Staphylococcus, low Propionibacterium
        staph = np.random.uniform(0.45, 0.60)
        prop = np.random.uniform(0.04, 0.08)
        remaining = 1 - (staph + prop)
        other_asvs = np.random.dirichlet(np.ones(3), 1)[0] * remaining  # Split remaining among 3 ASVs
        asvs = [staph, prop] + list(other_asvs)
    else:  # Non-lesional: lower Staphylococcus, higher Propionibacterium
        staph = np.random.uniform(0.15, 0.25)
        prop = np.random.uniform(0.25, 0.30)
        remaining = 1 - (staph + prop)
        other_asvs = np.random.dirichlet(np.ones(3), 1)[0] * remaining
        asvs = [staph, prop] + list(other_asvs)
    asv_data.append(asvs)

# Add ASVs to data
asv_df = pd.DataFrame(asv_data, columns=asv_names)
for col in asv_names:
    data[col] = asv_df[col].round(2)

# Generate histopathological and clinical features
data['Acantholysis'] = [np.random.randint(3, 6) if site == 'L' else np.random.randint(0, 2) for site in data['Site']]
data['Inflammation'] = [np.random.randint(2, 4) if site == 'L' else np.random.randint(0, 2) for site in data['Site']]
data['PDAI'] = [np.random.randint(18, 26) if site == 'L' else np.random.randint(8, 13) for site in data['Site']]

# Calculate Shannon Index (simplified, based on ASV abundances)
data['ShannonIndex'] = [
    round(entropy(asv_data[i], base=2) * (0.7 if data['Site'][i] == 'L' else 1.0), 1)
    for i in range(n_samples)
]  # Scale for lesional (2.0–2.3) vs. non-lesional (3.2–3.5)

# Create DataFrame
df = pd.DataFrame(data)

# Export to CSV for Excel
df.to_csv('Sample_Simulated_PV_Data_150.csv', index=False)
print("Data saved to Sample_Simulated_PV_Data_150.csv")

# Print summary for PowerPoint slides
print("\nSlide 1: Sample Distribution")
print(f"Lesional Samples: {sum(df['Site'] == 'L')}, Non-Lesional Samples: {sum(df['Site'] == 'NL')}")
print("\nSlide 2: Staphylococcus Abundance")
print(f"Mean Staphylococcus (Lesional): {df[df['Site'] == 'L']['Staphylococcus'].mean():.3f}")
print(f"Mean Staphylococcus (Non-Lesional): {df[df['Site'] == 'NL']['Staphylococcus'].mean():.3f}")
```
