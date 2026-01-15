# Multi-Vendor Marketplace – Full Stack Mini Project

## 1. Project Overview
This project is a Multi-Vendor Marketplace where multiple vendors can sell products,
and an admin manages approvals, commissions, and settlements.

The goal of this project is to demonstrate full-stack development skills including
frontend UI, backend APIs, database design, and business logic implementation.

---

## 2. Tech Stack
Frontend:
- HTML, CSS, JavaScript / React (edit if needed)

Backend:
- Python Flask / Django / Node.js (edit)

Database:
- SQLite / MySQL / PostgreSQL (edit)

---

## 3. User Roles
1. Admin
   - Approves vendors and products
   - Controls product visibility
   - Calculates commission
   - Manages settlements

2. Vendor
   - Registers and waits for admin approval
   - Adds products
   - Views orders and earnings

3. Customer
   - Views approved products
   - Places orders

---

## 4. UI Explanation
- Login & Registration pages are role-based (Admin / Vendor).
- Vendor dashboard shows product management and earnings.
- Admin dashboard provides approval controls and reports.
- UI is responsive and designed for clarity and ease of use.

---

## 5. Backend Logic
- REST APIs handle all operations (no hard-coded data).
- Role-based access control is implemented.
- CRUD operations for vendors, products, and orders.
- Commission is calculated during order processing.
- Validation and error handling are implemented at API level.

---

## 6. Data Flow
1. User interacts with the frontend UI.
2. Frontend sends request to backend APIs.
3. Backend validates data and processes business logic.
4. Database stores and retrieves required data.
5. API sends response back to frontend.
6. UI updates dynamically based on response.

---

## 7. Commission & Settlement Logic
- Each order is split based on vendor commission percentage.
- Admin commission is deducted.
- Vendor earnings are calculated automatically.
- Settlement reports are generated for vendors.

---

## 8. Error Handling & Validation
- Invalid inputs are validated at backend.
- Proper error messages returned via API.
- Unauthorized access is restricted.

---

## 9. Design Decisions
- Modular code structure for scalability.
- API-driven architecture for separation of concerns.
- Role-based system for security.
- Database normalization to avoid redundancy.

---

## 10. Conclusion
This project demonstrates end-to-end full-stack development including UI design,
backend logic, data handling, and real-world business rules.
