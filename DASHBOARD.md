# Finance Tracker Dashboard

A comprehensive web-based financial management application built with Flask and Python.

## 🎯 Features

### Dashboard
- **Visual Analytics**: Interactive charts showing expense categories and investment distribution
- **Real-time Statistics**: Total expenses, investments, and transaction counts
- **Recent Transactions**: View latest expense and investment records

### Expense Management
- **Add Expenses**: Track expenses by category with optional notes
- **View All Expenses**: Organized table view of all expenses
- **Delete Expenses**: Remove outdated or incorrect entries
- **Category Breakdown**: Automatic categorization and analysis

### Investment Tracking
- **Add Investments**: Record investments with expected returns
- **Investment Portfolio**: View all investments in one place
- **Returns Tracking**: Monitor expected returns and performance
- **Delete Investments**: Manage your investment portfolio

### Data Persistence
- **JSON Storage**: All data stored in JSON files for easy backup
- **Automatic Saving**: Changes persist automatically
- **Data Export**: Easy access to raw JSON data

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the Flask app:**
```bash
python app.py
```

3. **Open browser:**
Navigate to `http://localhost:8000`

### Docker Deployment

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

2. **Access the app:**
Open `http://localhost:8000`

### Kubernetes Deployment (Minikube)

1. **Initialize Terraform:**
```bash
cd terraform
terraform init
terraform apply
cd ..
```

2. **Apply Kubernetes manifests:**
```bash
kubectl apply -f k8s-config/
```

3. **Access the service:**
```bash
kubectl port-forward svc/finance-tracker-service 8000:8000 -n finance-tracker
```

## 📊 Dashboard Pages

### Home Page
- Overview of total expenses and investments
- Quick action buttons to manage finances
- Information about the application

### Dashboard
- Visual charts of expense categories
- Investment distribution pie chart
- Recent transactions summary
- Real-time statistics

### Expenses
- Form to add new expenses
- Complete expense list in table format
- Delete functionality for each entry
- Category and amount tracking

### Investments
- Form to add new investments
- Investment portfolio list
- Expected returns tracking
- Investment type breakdown

## 🔌 API Endpoints

### Expenses
- `GET /api/expenses` - Get all expenses
- `POST /api/expenses` - Create new expense
- `PUT /api/expenses/<id>` - Update expense
- `DELETE /api/expenses/<id>` - Delete expense

### Investments
- `GET /api/investments` - Get all investments
- `POST /api/investments` - Create new investment
- `PUT /api/investments/<id>` - Update investment
- `DELETE /api/investments/<id>` - Delete investment

### Statistics
- `GET /api/stats` - Get financial statistics

## 📁 Project Structure

```
finance-tracker/
├── app.py                    # Flask application
├── finance_tracker.py        # Core business logic
├── test_finance_tracker.py   # Unit tests
├── requirements.txt          # Dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── terraform/               # Kubernetes manifests (IaC)
├── scripts/                 # Shell scripts for CI/CD
├── templates/               # HTML templates
│   ├── index.html          # Home page
│   ├── dashboard.html      # Dashboard
│   ├── expenses.html       # Expenses management
│   ├── investments.html    # Investments management
│   ├── 404.html           # 404 error page
│   └── 500.html           # 500 error page
└── static/                 # Static assets
    └── style.css          # Main stylesheet
```

## 🧪 Testing

Run the test suite:
```bash
pytest test_finance_tracker.py -v
```

With coverage:
```bash
pytest test_finance_tracker.py --cov=finance_tracker --cov-report=html
```

## 📈 Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Database**: JSON files
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes (Minikube)
- **Infrastructure**: Terraform
- **CI/CD**: GitHub Actions

## 🔒 Security Features

- Non-root user in Docker
- Input validation
- CSRF protection ready
- Secure headers configured
- Health checks implemented

## 📝 Notes

- All data is stored locally in JSON files
- No external database required
- Perfect for personal finance tracking
- Can be deployed locally or in the cloud

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the application.

## 📄 License

This project is open source and available under the MIT License.
