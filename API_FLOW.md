## API Data Flow

Frontend → Backend → Database → Backend → Frontend

Example:
1. Vendor adds a product
2. Frontend sends POST request
3. Backend validates vendor status
4. Product stored with status = PENDING
5. Admin approves product
6. Product becomes visible to customers
