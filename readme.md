# 🍽️ SkyCity Auckland Restaurant Channel Analytics Dashboard



Interactive Streamlit dashboard for analyzing restaurant order channels, market share, profitability, and dependency risks across SkyCity Auckland Restaurants & Bars.



---



## 📌 Table of Contents

- <a href="#overview">Overview</a>

- <a href="#project-goal">Project Goal</a>

- <a href="#dataset">Dataset</a>

- <a href="#tools--technologies">Tools & Technologies</a>

- <a href="#project-structure">Project Structure</a>

- <a href="#data-cleaning--validation">Data Cleaning & Validation</a>

- <a href="#exploratory-data-analysis-eda">Exploratory Data Analysis (EDA)</a>

- <a href="#key-findings--insights">Key Findings & Insights</a>

- <a href="#streamlit-dashboard">Streamlit Dashboard</a>

- <a href="#how-to-run-this-project">How to Run This Project</a>

- <a href="#live-dashboard">Live Dashboard</a>

- <a href="#future-improvements">Future Improvements</a>

- <a href="#author--contact">Author & Contact</a>



---



<h2><a class="anchor" id="overview"></a>Overview</h2>



This project focuses on analyzing multi-channel restaurant ordering behavior across SkyCity Auckland Restaurants \& Bars. The analysis helps understand how restaurants perform across different ordering channels such as InStore, Uber Eats, DoorDash, and Self Delivery.



The project includes:

- Data cleaning and validation

- KPI engineering

- Market share analysis

- Geographic analysis

- Risk and profitability analysis

- Interactive Streamlit dashboard



---



<h2><a class="anchor" id="project-goal"></a>Project Goal</h2>



The main goal of this project is to help restaurants understand:



- Which ordering channels generate the highest orders

- Which channels are most profitable

- Which restaurants are highly dependent on aggregators

- How customer behavior changes across regions and cuisines

- How restaurants can build balanced and resilient channel strategies



---



<h2><a class="anchor" id="dataset"></a>Dataset</h2>



The dataset contains restaurant-level operational and financial information such as:



- Restaurant details

- Cuisine type

- Business segment

- Subregion

- Monthly orders

- Revenue by channel

- Profit by channel

- Delivery costs

- Commission rates

- Channel share percentages



Main ordering channels analyzed:

- InStore

- Uber Eats

- DoorDash

- Self Delivery



---



<h2><a class="anchor" id="tools--technologies"></a>Tools & Technologies</h2>



- Python

- Pandas

- NumPy

- Matplotlib

- Seaborn

- Plotly

- Streamlit

- GitHub



---



<h2><a class="anchor" id="project-structure"></a>Project Structure</h2>



text

skycity-auckland-channel-analytics/

│

├── app.py

├── final\_cleaned\_skycity\_data.csv

├── requirements.txt

├── README.md

│

├── notebooks/

│   ├── 01\_Data\_Cleaning\_Validation.ipynb

│   ├── 02\_EDA\_Channel\_Analytics.ipynb

│   ├── 03\_Final\_Insights\_Recommendations.docx


---



<h2><a class="anchor" id="data-cleaning--validation"></a>Data Cleaning & Validation</h2>

- The dataset was cleaned and validated before analysis.

Main steps included:

- Checking missing values
- Removing duplicates
- Validating monthly order totals
- Validating revenue calculations
- Checking channel share consistency
- Identifying negative profit scenarios
- Creating business KPIs

Important KPIs created:

- Total Revenue
- Total Net Profit
- Aggregator Dependence
- InStore Reliance
- Diversification Score
- Risk Categories

---

<h2><a class="anchor" id="exploratory-data-analysis-eda"></a>Exploratory Data Analysis (EDA)</h2>

- EDA was performed to understand business behavior and market trends.

Analysis sections included:

- Overall business overview
- Channel performance analysis
- Geographic analysis
- Cuisine analysis
- Segment analysis
- Dependency risk analysis
- Profitability analysis

---

<h2><a class="anchor" id="key-findings--insights"></a>Key Findings & Insights</h2>

### 1. Channel Performance

- Uber Eats generated strong delivery order volumes.
- InStore channels generally produced higher profit margins.

### 2. Geographic Insights

- Central Auckland showed stronger delivery platform usage.
- Some suburban areas demonstrated balanced channel behavior.

### 3. Cuisine Insights

- Pizza and QSR categories showed high aggregator dependence.
- Cafes relied more on in-store customers.

### 4. Risk Analysis

- Several restaurants showed high dependency on third-party aggregators.
- Diversified restaurants demonstrated stronger operational resilience.

### 5. Profitability Insights

- High order volume did not always result in high profitability.
- Commission rates negatively affected delivery profits.

---

<h2><a class="anchor" id="streamlit-dashboard"></a>Streamlit Dashboard</h2>

The project includes an interactive Streamlit dashboard with:

- KPI cards
- Channel performance analytics
- Market share charts
- Geographic heatmaps
- Cuisine and segment analysis
- Dependency risk analysis
- Profitability analysis
- Interactive filters
- Downloadable filtered dataset

---

<h2><a class="anchor" id="how-to-run-this-project"></a>How to Run This Project</h2>

### Clone the repository:

```bash
git clone https://github.com/yourusername/skycity-auckland-channel-analytics.git
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run Streamlit app:

```bash
streamlit run app.py
```

### Open in browser:

```text
http://localhost:8501
```

---

<h2><a class="anchor" id="live-dashboard"></a>Live Dashboard</h2>

Streamlit Dashboard Link:

```text
https://skycity-auckland-channel-analytics-ucq8xzimnv5jy5bttuyxdy.streamlit.app/
```

---

<h2><a class="anchor" id="future-improvements"></a>Future Improvements</h2>

- Add forecasting models for future order prediction
- Add customer sentiment analysis
- Deploy dashboard with database integration
- Add real-time analytics
- Improve dashboard UI further

---

<h2><a class="anchor" id="author--contact"></a>Author & Contact</h2>

Name: Namrata Pokharkar

📧 Email: namratapokharkar20@gmail.com

🔗 LinkedIn: www.linkedin.com/in/namrata-pokharkar-862a55288
