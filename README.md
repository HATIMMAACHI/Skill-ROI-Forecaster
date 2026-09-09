# 📈 Skill ROI Forecaster

An end-to-end machine learning system that analyzes, predicts, and ranks the market return on investment (ROI) of technical skills across modern tech industries. 

Deployed as an interactive analytical dashboard via Streamlit Community Cloud.

---

## 📌 Overview

Determining which technical skills yield the highest career return is a complex problem influenced by industry demand, compensation trends, and skill co-occurrence. 

**Skill ROI Forecaster** addresses this challenge by combining multiple statistical learning techniques into a unified decision-support engine. The application predicts compensation bands, identifies natural skill clusters, uncovers hidden skill associations, and quantifies market viability through a custom mathematical ROI formulation.

---

## 🚀 Key Features

* **Multi-Model Machine Learning Architecture:**
  * **Supervised Regression & Classification:** Leverages Random Forest algorithms to estimate expected compensation percentiles and classify role seniority tiers based on skill combinations.
  * **Unsupervised Clustering:** Employs K-Means to identify latent clusters of technical skill proficiencies and domain archetypes.
  * **Association Rule Mining:** Implements the Apriori algorithm to discover frequent itemsets and calculate confidence/lift metrics between complementary technologies.
* **Interactive Data Visualization:** Real-time exploration of skill matrices, correlation heatmaps, and ROI rankings powered by Streamlit.

---

## 🧮 Mathematical Formulation

To quantify technical viability fairly, the system balances raw compensation potential with general market liquidity through a normalized weighted metric:

**ROI = (0.6 * Normalized Salary) + (0.4 * Normalized Frequency)**

Where:
* **Normalized Salary** is the min-max normalized median compensation associated with a specific technical skill.
* **Normalized Frequency** is the min-max normalized market occurrence/demand volume of that skill across collected job postings.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Machine Learning:** Scikit-learn (Random Forest, K-Means), MLxtend (Apriori)
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn
* **Deployment:** Streamlit

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
Clone the project directly to your local machine:
```bash
git clone [https://github.com/HATIMMAACHI/Skill-ROI-Forecaster.git](https://github.com/HATIMMAACHI/Skill-ROI-Forecaster.git)
cd Skill-ROI-Forecaster
```

### 2. Create a Virtual Environment
Isolate the project dependencies by creating a virtual environment:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Install all required machine learning and data processing libraries:
```bash
pip install -r requirements.txt
```

---

## 🏃 Running the Application

Once the dependencies are installed, you can launch the Streamlit dashboard locally by running:
```bash
streamlit run app.py
```

The application will automatically launch in your default web browser at `http://localhost:8501`. Any changes made to the `app.py` script will hot-reload in the browser.

---

## 👤 Author
* **Hatim Maachi** — MSc Student in Data Science & Intelligent Systems
* **GitHub:** [@HATIMMAACHI](https://github.com/HATIMMAACHI)
* **Portfolio:** [maachi.me](https://maachi.me)
