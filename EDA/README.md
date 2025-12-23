# Exploratory Data Analysis (EDA) Pipeline

A comprehensive, automated EDA pipeline for tabular data that streamlines data exploration, feature selection, feature extraction, and feature importance analysis.

## Overview

This notebook automates the exploratory data analysis lifecycle to provide quick insights and intuitions about datasets. It's designed to reduce manual work and accelerate the data understanding phase of machine learning projects.

## Features

- **Automated EDA Reports**: Generate comprehensive statistical reports with minimal code
- **Feature Selection**: Multiple methods to identify the most relevant features
- **Dimensionality Reduction**: Various techniques for feature extraction and visualization
- **Feature Importance**: Tree-based and permutation methods to rank feature significance
- **Smart Detection**: Automatically detects whether your target variable is continuous (regression) or categorical (classification) and applies appropriate methods

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Notebook Structure](#notebook-structure)
  - [Part 0: Data Loading](#part-0-data-loading--setup)
  - [Part I: EDA](#part-i-exploratory-data-analysis)
  - [Part II: Feature Selection](#part-ii-feature-selection)
  - [Part III: Feature Extraction](#part-iii-feature-extraction)
  - [Part IV: Feature Importance](#part-iv-feature-importance)
- [Usage Examples](#usage-examples)
- [Dependencies](#dependencies)

## Requirements

### Python Version

**Recommended: Python 3.8-3.11** for full compatibility with all features.

- **Python 3.8-3.11**: ✅ Full support, all packages work
- **Python 3.12+**: ⚠️ Partial support - `dataprep` and `rfpimp` won't install
- **Python 3.13-3.14**: ⚠️ Same as 3.12, some packages incompatible

### Installation

#### For Python 3.8-3.11 (Full Compatibility - Recommended)

```bash
pip install -r requirements-py312.txt
```

#### For Python 3.12+ (Limited Support - dataprep excluded)

```bash
pip install -r requirements-py313.txt
```

**Note**: Python 3.12+ cannot install these packages:
- `dataprep` → ❌ **Cannot install** (dependency `levenshtein` uses removed Python C API)
  - Alternative: Use `ydata-profiling`, `sweetviz`, or `seaborn` for visualizations
- `rfpimp` → ❌ **Cannot install** (compatibility issues)
  - Alternative: Use `sklearn.inspection.permutation_importance` (built-in)
- `pandas-profiling` → ⚠️ Deprecated, use `ydata-profiling` instead

### Creating a Compatible Environment

If you're having installation issues, create a Python 3.11 environment for full compatibility:

**Using Conda (Recommended):**
```bash
conda create -n eda_env python=3.11 -y
conda activate eda_env
pip install -r requirements-py312.txt
```

**Using venv:**
```bash
python3.11 -m venv eda_env
source eda_env/bin/activate  # On Windows: eda_env\Scripts\activate
pip install -r requirements-py312.txt
```

**Quick Install for Python 3.12+ Users (Skip incompatible packages):**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn tensorflow
pip install ydata-profiling sweetviz eli5 jupyter ipywidgets notebook
```

## Quick Start

1. Load your dataset into a pandas DataFrame
2. Identify your target variable
3. Run the cells sequentially to explore your data
4. The notebook will automatically detect if you have a regression or classification problem

```python
import pandas as pd

# Load your data
df = pd.read_csv("your_data.csv")

# Set your target variable name
TARGET = "target_column_name"

# Run the notebook cells
```

## Notebook Structure

### Part 0: Data Loading & Setup

**Location**: Cells 6-12

- Sandbox area for loading and cleaning your data
- Includes example using Boston Housing dataset
- Install dependencies and import libraries

**Key Libraries**:
- `pandas`, `numpy`, `matplotlib`
- `pandas_profiling`, `dataprep`, `sweetviz`
- `sklearn`, `tensorflow`

### Part I: Exploratory Data Analysis

Three powerful automated EDA tools:

#### I-1: pandas-profiling
**Location**: Cells 17-19

Generates comprehensive dataset reports including:
- Statistical summaries
- Variable distributions
- Correlations
- Missing values
- Duplicate rows

```python
from pandas_profiling import ProfileReport

profile = ProfileReport(df, title='Pandas Profiling Report', explorative=True)
profile.to_widgets()  # Interactive widget
profile.to_notebook_iframe()  # HTML in notebook
```

#### I-2: dataprep.eda
**Location**: Cells 23-25

Interactive visualizations for:
- Overall data distribution
- Correlation matrices
- Missing value patterns

```python
from dataprep.eda import plot, plot_correlation, plot_missing

plot(df)  # Overall analysis
plot_correlation(df)  # Correlation heatmaps
plot_missing(df)  # Missing value analysis
```

#### I-3: sweetviz
**Location**: Cells 30-32

Compare train/test datasets:
- Side-by-side comparisons
- Target variable analysis
- Association graphs
- HTML report generation

```python
import sweetviz

my_report = sweetviz.compare([train, "Train"], [test, "Test"], "target")
my_report.show_html("Report.html")
```

#### I-4: Target Identification
**Location**: Cells 36-41

Automatically detects problem type:
- **Continuous target** → Regression problem
- **Categorical target** → Classification problem

### Part II: Feature Selection

Methods to identify the most relevant features:

#### II-1: Removing Features with Low Variance
**Location**: Cells 47-49

Removes features with >80% missing data or low variance.

```python
from sklearn.feature_selection import VarianceThreshold

sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
X_variance = sel.fit_transform(X)
```

**Use Case**: Remove quasi-constant features

#### II-2: Univariate Selection
**Location**: Cell 54

Uses chi-square test to select features with strongest relationships to target (classification only).

```python
from sklearn.feature_selection import SelectKBest, chi2

select_best_features = SelectKBest(score_func=chi2, k=10)
fit = select_best_features.fit(X, y)
```

**Use Case**: Quick statistical feature ranking

#### II-3: Recursive Feature Elimination (RFE)
**Location**: Cells 60-63

Uses machine learning models to recursively remove features:
- **SVM-based RFE**: Cross-validation to find optimal feature count
- **Logistic Regression RFE**: Ranks features by importance

```python
from sklearn.feature_selection import RFECV
from sklearn.svm import SVC

rfecv = RFECV(estimator=SVC(kernel="linear"), step=1, cv=StratifiedKFold(2))
rfecv.fit(X, y)
```

**Use Case**: Model-based feature selection with performance metrics

#### II-4: SelectFromModel
**Location**: Cells 68-69

Uses L1 regularization to select features:

```python
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel

lsvc = LinearSVC(C=0.01, penalty="l1", dual=False)
model = SelectFromModel(lsvc, prefit=True)
X_new = model.transform(X)
```

**Use Case**: Automatic feature selection via regularization

### Part III: Feature Extraction

Dimensionality reduction techniques (all reduce to 2 components for visualization):

#### III-1: Principal Component Analysis (PCA)
**Location**: Cells 76-79

Linear dimensionality reduction maximizing variance.

```python
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
```

**Best For**: Linear relationships, variance-based reduction

#### III-2: Independent Component Analysis (ICA)
**Location**: Cells 84-86

Separates multivariate signal into independent components.

```python
from sklearn.decomposition import FastICA

ica = FastICA(n_components=2)
X_ica = ica.fit_transform(X)
```

**Best For**: Signal separation, non-Gaussian data

#### III-3: Linear Discriminant Analysis (LDA)
**Location**: Cell 91

Supervised dimensionality reduction maximizing class separation (classification only).

```python
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

lda = LinearDiscriminantAnalysis(n_components=2)
X_lda = lda.fit(X, y).transform(X)
```

**Best For**: Classification, maximizing separability

#### III-4: Locally Linear Embedding (LLE)
**Location**: Cells 96-98

Non-linear dimensionality reduction preserving local structure.

```python
from sklearn.manifold import locally_linear_embedding

lle, error = locally_linear_embedding(X, n_neighbors=5, n_components=2)
```

**Best For**: Manifold learning, non-linear relationships

#### III-5: t-SNE
**Location**: Cells 103-104

Non-linear dimensionality reduction for visualization.

```python
from sklearn.manifold import TSNE

X_embedded = TSNE(n_components=2).fit_transform(X)
```

**Best For**: Visualization, discovering clusters

### Part IV: Feature Importance

#### IV-1: Tree-based Methods
**Location**: Cells 111-113

Uses ensemble tree models to calculate feature importance:

**Classification**:
```python
from sklearn.ensemble import ExtraTreesClassifier

forest = ExtraTreesClassifier(n_estimators=250)
forest.fit(X, y)
importances = forest.feature_importances_
```

**Regression**:
```python
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=100, oob_score=True)
rf.fit(X, y)
importances = rf.feature_importances_
```

**Pros**: Fast, built-in to tree models
**Cons**: Can be biased toward high-cardinality features

#### IV-2: Permutation Importance
**Location**: Cells 117-119

More robust method by permuting feature values:

**Using rfpimp**:
```python
from rfpimp import permutation_importances

perm_imp_rfpimp = permutation_importances(rf, X, y, r2)
```

**Using eli5**:
```python
from eli5.sklearn import PermutationImportance

perm = PermutationImportance(rf, n_iter=50).fit(X, y)
```

**Using sklearn**:
```python
from sklearn.inspection import permutation_importance

r = permutation_importance(model, X_val, y_val, n_repeats=30)
```

**Pros**: More reliable, model-agnostic
**Cons**: Slower computation

## Usage Examples

### Example 1: Quick EDA on CSV File

```python
import pandas as pd
from pandas_profiling import ProfileReport

# Load data
df = pd.read_csv("data.csv")

# Generate report
profile = ProfileReport(df, title='My Dataset Report', explorative=True)
profile.to_file("report.html")
```

### Example 2: Feature Selection for Classification

```python
from sklearn.feature_selection import SelectKBest, chi2

# Separate features and target
TARGET = "label"
X = df.drop(columns=[TARGET])
y = df[TARGET]

# Select top 10 features
selector = SelectKBest(score_func=chi2, k=10)
X_selected = selector.fit_transform(X, y)

# Get feature names
selected_features = X.columns[selector.get_support()]
print(f"Selected features: {list(selected_features)}")
```

### Example 3: Dimensionality Reduction Visualization

```python
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Apply PCA
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

# Visualize
plt.figure(figsize=(10, 8))
plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=y, cmap='viridis')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('PCA Visualization')
plt.colorbar()
plt.show()
```

## Dependencies

### Core Libraries

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | >=1.3.0 | Data manipulation and analysis |
| numpy | >=1.21.0 | Numerical operations and arrays |
| matplotlib | >=3.4.0 | Data visualization and plotting |

### Machine Learning

| Package | Version | Purpose |
|---------|---------|---------|
| scikit-learn | >=1.0.0 | Feature selection, extraction, ML algorithms |
| tensorflow | >=2.6.0 | Dataset loading (Boston Housing example) |

### EDA Tools

| Package | Version | Purpose | Python 3.13+ |
|---------|---------|---------|--------------|
| pandas-profiling / ydata-profiling | >=3.6.0 / >=4.6.0 | Automated comprehensive EDA reports | Use ydata-profiling |
| dataprep | >=0.4.5 | Interactive EDA visualizations | ⚠️ Not compatible |
| sweetviz | >=2.3.0 | Train/test dataset comparison | ✅ Compatible |

### Feature Importance

| Package | Version | Purpose | Python 3.13+ |
|---------|---------|---------|--------------|
| rfpimp | >=1.3.7 | Random Forest permutation importance | ⚠️ May not work |
| eli5 | >=0.11.0 | Model interpretation and explanation | ✅ Compatible |

**Note**: For Python 3.13+, use `sklearn.inspection.permutation_importance` instead of `rfpimp`.

### Jupyter Environment

| Package | Version | Purpose |
|---------|---------|---------|
| jupyter | >=1.0.0 | Jupyter notebook environment |
| ipywidgets | >=7.6.0 | Interactive widgets for notebooks |

## Tips & Best Practices

1. **Start with automated reports**: Use pandas-profiling or sweetviz first to get an overview
2. **Check data quality**: Look for missing values, outliers, and data types
3. **Compare multiple methods**: Different feature selection methods may give different results
4. **Visualize dimensionality reduction**: Always plot the results to understand the data structure
5. **Use permutation importance**: More reliable than tree-based importance for critical decisions
6. **Adjust parameters**: The default parameters are starting points; tune them for your specific dataset

## Known Issues & Troubleshooting

### Python 3.13+ Compatibility Issues

**Error: `ModuleNotFoundError: No module named 'cgi'`**

The `cgi` module was removed in Python 3.13. This affects:
- `pandas-profiling` (use `ydata-profiling` instead)
- `dataprep` (dependency `htmlmin` fails)
- `rfpimp` (may have issues)

**Solution**: Use Python 3.12 or earlier, or use the Python 3.13 compatible requirements file.

### Package-Specific Issues

1. **pandas-profiling vs ydata-profiling**
   - `pandas-profiling` was renamed to `ydata-profiling`
   - Update notebook imports: `from ydata_profiling import ProfileReport`

2. **dataprep Installation Fails**
   - Not compatible with Python 3.13+
   - Use Python 3.12 or skip this package
   - Alternative: Use `ydata-profiling` for EDA

3. **rfpimp Not Installing**
   - Has compatibility issues with newer Python versions
   - Alternative: Use `sklearn.inspection.permutation_importance` (built into scikit-learn)

4. **LDA and Univariate Selection**
   - Only work for classification problems (categorical targets)
   - Will be skipped automatically for regression problems

5. **t-SNE Performance**
   - Can be slow on large datasets (>10,000 samples)
   - Consider using PCA first to reduce dimensions

6. **TensorFlow Boston Housing Dataset**
   - Deprecated in TensorFlow 2.6+
   - Replace with: `sklearn.datasets.load_boston()` or use your own CSV data

## Contributing

Feel free to extend this notebook with:
- Additional EDA visualization libraries
- New feature selection methods
- More dimensionality reduction techniques
- Automated hyperparameter tuning for feature selection

## License

This notebook is provided as-is for educational and research purposes.

## References

- [scikit-learn Feature Selection](https://scikit-learn.org/stable/modules/feature_selection.html)
- [pandas-profiling Documentation](https://pandas-profiling.ydata.ai/)
- [dataprep Documentation](https://dataprep.ai/)
- [sweetviz Documentation](https://github.com/fbdesignpro/sweetviz)
