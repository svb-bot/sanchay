# Sanchay

<div align="center">
<img src="./frontend/public/logo_title.png" width="400" alt="Sanchay" />
</div>

![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![Mantine](https://img.shields.io/badge/Mantine-UI-339AF0)
![Node.js](https://img.shields.io/badge/Node.js-Express-339933?logo=node.js)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green)

Sanchay is a personal finance management application for recording income and spending while maintaining normalized master data for categories and payment modes. The application follows a modular architecture with a React + Mantine frontend, Express backend, and MySQL database.

---

## Features

* Dynamic form engine built with Mantine
* Income management
* Spending management
* Master data management

  * Payment Categories
  * Payment Modes
  * Bill Categories
  * Bill Payment Modes
* REST API backend
* MySQL persistence
* Responsive UI
* Schema-driven forms
* Reusable components

---

## Technology Stack

### Frontend

* React
* Vite
* Mantine
* Axios
* Tabler Icons

### Backend

* Node.js
* Express.js
* MySQL2
* dotenv
* cors

### Database

* MySQL 8+

---

## Project Structure

```text
sanchay
│
├── backend
│   ├── src
│   │   ├── config
│   │   ├── controllers
│   │   ├── models
│   │   ├── routes
│   │   ├── app.js
│   │   └── server.js
│   └── package.json
│
├── frontend
│   ├── src
│   │   ├── api
│   │   ├── components
│   │   │   ├── Dimension
│   │   │   └── DynamicForm
│   │   ├── forms
│   │   ├── pages
│   │   ├── schemas
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
└── README.md
```

---

## Database Schema

### Fact Tables

* fact_income
* fact_spending

### Dimension Tables

* dim_payment_category
* dim_payment_mode
* dim_bill_category
* dim_bill_payment_mode

The application follows a normalized design where fact tables reference dimension tables through foreign keys.

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd sanchay
```

---

## Backend Setup

```bash
cd backend
```

Install dependencies

```bash
npm install
```

Create a `.env` file

```env
PORT=5000

DB_HOST=localhost
DB_PORT=3306
DB_NAME=sanchay
DB_USER=root
DB_PASSWORD=your_password
```

Run development server

```bash
npm run dev
```

---

## Frontend Setup

```bash
cd frontend
```

Install dependencies

```bash
npm install
```

Run

```bash
npm run dev
```

---

## API Endpoints

### Income

| Method | Endpoint    |
| ------ | ----------- |
| GET    | /api/income |
| POST   | /api/income |

### Spending

| Method | Endpoint      |
| ------ | ------------- |
| GET    | /api/spending |
| POST   | /api/spending |

### Payment Categories

| Method | Endpoint                    |
| ------ | --------------------------- |
| GET    | /api/payment-categories     |
| POST   | /api/payment-categories     |
| PUT    | /api/payment-categories/:id |
| DELETE | /api/payment-categories/:id |

### Payment Modes

| Method | Endpoint               |
| ------ | ---------------------- |
| GET    | /api/payment-modes     |
| POST   | /api/payment-modes     |
| PUT    | /api/payment-modes/:id |
| DELETE | /api/payment-modes/:id |

### Bill Categories

| Method | Endpoint                 |
| ------ | ------------------------ |
| GET    | /api/bill-categories     |
| POST   | /api/bill-categories     |
| PUT    | /api/bill-categories/:id |
| DELETE | /api/bill-categories/:id |

### Bill Payment Modes

| Method | Endpoint                    |
| ------ | --------------------------- |
| GET    | /api/bill-payment-modes     |
| POST   | /api/bill-payment-modes     |
| PUT    | /api/bill-payment-modes/:id |
| DELETE | /api/bill-payment-modes/:id |

---

## Dynamic Form Engine

The application includes a reusable dynamic form engine.

Example schema:

```javascript
const schema = [
    {
        name: "payment_date",
        label: "Payment Date",
        type: "date",
        required: true
    },
    {
        name: "payment_category_id",
        label: "Category",
        type: "select",
        dataSource: "/payment-categories"
    }
];
```

Supported field types:

* text
* number
* currency
* textarea
* date
* select

The engine supports:

* Required validation
* Dynamic dropdowns
* Remote data sources
* Schema-driven rendering
* Reusable form layouts

---

## Master Data Management

The Settings module provides CRUD functionality for all dimension tables.

* Payment Categories
* Payment Modes
* Bill Categories
* Bill Payment Modes

All pages reuse the same generic components.

---

## Future Enhancements

* Dashboard
* Charts and analytics
* Monthly summaries
* Budgets
* Investment tracking
* Recurring transactions
* File attachments
* Authentication
* User profiles
* Multi-user support
* Export to CSV and Excel
* Reports
* Search and filtering
* Pagination
* Audit logs

---

## License

This project is licensed under the MIT License.
