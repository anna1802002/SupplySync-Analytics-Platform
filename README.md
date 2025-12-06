# SupplySync Analytics Platform

## 📊 Overview
SupplySync Analytics Platform is a comprehensive supply chain analytics solution that provides real-time insights into inventory management, supplier performance, logistics optimization, and demand forecasting. This platform combines data analysis, visualization, and business intelligence to help organizations make data-driven decisions in their supply chain operations.

## 🎯 Key Features
- **Inventory Analytics**: Track stock levels, turnover rates, and reorder points
- **Supplier Performance Monitoring**: Evaluate supplier reliability, delivery times, and quality metrics
- **Demand Forecasting**: Predict future demand using historical data and trend analysis
- **Logistics Optimization**: Analyze shipping routes, delivery times, and transportation costs
- **Real-time Dashboards**: Interactive Power BI dashboards for visual insights
- **Cost Analysis**: Monitor procurement costs, carrying costs, and total supply chain expenses

## 🏗️ Project Structure
```
SupplySync-Analytics-Platform/
│
├── data/                          # Data files
│   ├── raw/                       # Raw data from various sources
│   ├── processed/                 # Cleaned and transformed data
│   └── sample/                    # Sample datasets for testing
│
├── notebooks/                     # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_inventory_analysis.ipynb
│   ├── 04_supplier_analysis.ipynb
│   └── 05_demand_forecasting.ipynb
│
├── scripts/                       # Python automation scripts
│   ├── data_ingestion.py
│   ├── data_transformation.py
│   ├── etl_pipeline.py
│   └── export_to_powerbi.py
│
├── sql/                           # SQL queries and database scripts
│   ├── schema.sql
│   ├── views.sql
│   └── analytical_queries.sql
│
├── powerbi/                       # Power BI related files
│   ├── reports/
│   └── datasets/
│
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook
- SQL Database (PostgreSQL, MySQL, or SQL Server)
- Power BI Desktop (for local development)
- Power BI Pro or Premium license (for online publishing)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/anna1802002/SupplySync-Analytics-Platform.git
cd SupplySync-Analytics-Platform
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install required packages**
```bash
pip install -r requirements.txt
```

4. **Set up database connection**
   - Update database credentials in `config.py`
   - Run schema creation scripts from `sql/schema.sql`

5. **Run the ETL pipeline**
```bash
python scripts/etl_pipeline.py
```

## 📦 Required Python Packages
```
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
seaborn>=0.12.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0  # For PostgreSQL
jupyter>=1.0.0
scikit-learn>=1.2.0
plotly>=5.11.0
```

## 📊 Data Sources
The platform integrates data from multiple sources:
- **ERP Systems**: Inventory levels, purchase orders, sales data
- **Supplier Data**: Delivery performance, quality metrics, pricing
- **Logistics Data**: Shipping times, routes, transportation costs
- **External Data**: Market trends, economic indicators

## 🔍 Analysis Modules

### 1. Inventory Management
- Current stock levels by product and location
- Inventory turnover ratio
- Stock-out analysis
- ABC analysis for inventory classification

### 2. Supplier Performance
- On-time delivery rate
- Quality acceptance rate
- Lead time analysis
- Supplier scorecards

### 3. Demand Forecasting
- Time series analysis
- Seasonal decomposition
- Moving average predictions
- Machine learning models for forecast accuracy

### 4. Cost Analysis
- Total cost of ownership (TCO)
- Cost per unit analysis
- Freight cost optimization
- Budget vs. actual comparisons

## 📈 Power BI Dashboard

### Dashboard Components
1. **Executive Summary**: High-level KPIs and trends
2. **Inventory Dashboard**: Stock levels, turnover, reorder alerts
3. **Supplier Performance**: Delivery metrics, quality scores
4. **Demand Analysis**: Forecast vs. actual, trend analysis
5. **Cost Analytics**: Spend analysis, cost breakdown

### Key Metrics
- **Inventory Turnover Ratio**: Cost of Goods Sold / Average Inventory
- **Perfect Order Rate**: (Orders Delivered Complete & On Time) / Total Orders
- **Supply Chain Cycle Time**: Average time from order to delivery
- **Forecast Accuracy**: 1 - (|Actual - Forecast| / Actual)
- **Carrying Cost**: Storage + Insurance + Depreciation costs

## 🔧 Configuration

### Database Configuration
Edit `config.py`:
```python
DB_CONFIG = {
    'host': 'your_host',
    'database': 'supplysync_db',
    'user': 'your_username',
    'password': 'your_password',
    'port': 5432
}
```

### Power BI Connection
1. Use DirectQuery or Import mode
2. Configure scheduled refresh (for Import mode)
3. Set up row-level security if needed

## 📝 Usage Examples

### Running Analysis Notebooks
```bash
jupyter notebook notebooks/03_inventory_analysis.ipynb
```

### Executing ETL Pipeline
```bash
python scripts/etl_pipeline.py --source erp --target warehouse
```

### Exporting Data for Power BI
```bash
python scripts/export_to_powerbi.py --format csv --output data/processed/
```

## 🤝 Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors
- **Anna** - *Initial work* - [anna1802002](https://github.com/anna1802002)
