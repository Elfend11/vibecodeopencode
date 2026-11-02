import pypandoc

content = r"""# Task Plan — Lab Equipment Loan System

## Project Overview

**Project:** Lab Equipment Loan System  
**Backend:** Python 3.x + Flask  
**Database:** SQLite  
**API format:** JSON  
**Reference documents:** `requirement.md` / SRS, `prd.md`, and `architecture.md`

## Task Checklist

### 1. Project Setup

- [ ] Create the project directory.
- [ ] Create and activate a Python virtual environment.
- [ ] Install Flask and required dependencies.
- [ ] Create `requirements.txt`.
- [ ] Create the initial application entry point (`run.py`).
- [ ] Configure the Flask application.
- [ ] Verify that the Flask development server starts successfully.

**Expected result:** A working Flask application that can receive HTTP requests.

### 2. Database Setup

- [ ] Create the SQLite database file.
- [ ] Create the `Item` table.
- [ ] Create the `Loan` table.
- [ ] Define primary keys and the foreign key from `Loan.item_id` to `Item.id`.
- [ ] Enable SQLite foreign key enforcement for database connections.
- [ ] Add database connection and transaction helper functions.
- [ ] Verify that the tables are created correctly.

**Expected result:** SQLite database is ready to store item and loan records.

### 3. Item Management

- [ ] Implement the item repository or database queries.
- [ ] Implement `GET /items`.
- [ ] Return item data with `total_stock` and the latest `available_stock`.
- [ ] Implement `POST /items`.
- [ ] Validate that the item name is not empty.
- [ ] Validate that the initial stock is a non-negative integer.
- [ ] Set `available_stock` equal to the initial `total_stock` when a new item is created.
- [ ] Return `201 Created` when an item is successfully created.
- [ ] Test item creation and item listing.

**Expected result:** Petugas Lab can add equipment and retrieve current stock information.

### 4. Loan Management

- [ ] Implement the loan repository or database queries.
- [ ] Implement `POST /loans`.
- [ ] Validate that `student_id` is provided.
- [ ] Validate that `item_id` exists.
- [ ] Validate that `quantity` is a positive integer.
- [ ] Check that `available_stock` is sufficient.
- [ ] Reject the request with `404 Not Found` when the item does not exist.
- [ ] Reject the request with `400 Bad Request` when the requested quantity exceeds available stock.
- [ ] Reduce `available_stock` after a valid loan is recorded.
- [ ] Create the loan record with status `BORROWED`.
- [ ] Save the stock update and loan record in one database transaction.
- [ ] Roll back the transaction if any operation fails.
- [ ] Return `201 Created` when the loan is successfully recorded.
- [ ] Test successful and rejected loan requests.

**Expected result:** A valid loan is recorded and stock is reduced without allowing negative available stock.

### 5. Loan Return

- [ ] Implement `PUT /loans/{id}/return`.
- [ ] Find the loan transaction by its ID.
- [ ] Return `404 Not Found` when the loan transaction does not exist.
- [ ] Reject a return request with `400 Bad Request` if the status is already `RETURNED`.
- [ ] Change the loan status to `RETURNED`.
- [ ] Restore `available_stock` by the loan quantity.
- [ ] Save the status update and stock restoration in one database transaction.
- [ ] Roll back the transaction if any operation fails.
- [ ] Return `200 OK` when the return is successful.
- [ ] Test successful return and repeated return attempts.

**Expected result:** Returned equipment is restored to available stock exactly once.

### 6. Student Loan History

- [ ] Implement `GET /loans/student/{student_id}`.
- [ ] Retrieve loan records using the supplied student NIM.
- [ ] Return the loan history in JSON format.
- [ ] Define a consistent response for a student with no loan records.
- [ ] Test history retrieval for students with and without transactions.

**Expected result:** Loan history can be retrieved by student NIM.

### 7. API Response and Error Handling

- [ ] Use JSON for all API responses.
- [ ] Apply consistent response structures for successful requests.
- [ ] Apply consistent response structures for errors.
- [ ] Handle invalid JSON or missing request fields.
- [ ] Handle unexpected internal errors without exposing stack traces to clients.
- [ ] Use the required HTTP status codes.

| Scenario | Expected status |
|---|---|
| Successful data retrieval | `200 OK` |
| Successful item or loan creation | `201 Created` |
| Invalid input or insufficient stock | `400 Bad Request` |
| Item or loan not found | `404 Not Found` |
| Unexpected server error | `500 Internal Server Error` |

**Expected result:** Clients receive predictable JSON responses and appropriate HTTP status codes.

### 8. Automated Testing

- [ ] Prepare a separate test database or isolated test setup.
- [ ] Test `GET /items`.
- [ ] Test `POST /items` with valid data.
- [ ] Test `POST /items` with invalid data.
- [ ] Test `POST /loans` with sufficient stock.
- [ ] Test `POST /loans` when requested quantity exceeds available stock.
- [ ] Test `POST /loans` with an unknown `item_id`.
- [ ] Verify that available stock decreases after a successful loan.
- [ ] Test a successful loan return.
- [ ] Test returning the same loan twice.
- [ ] Verify that available stock is restored exactly once.
- [ ] Test `GET /loans/student/{student_id}`.
- [ ] Test database rollback when a transaction fails.

**Expected result:** Core business rules and API acceptance criteria are covered by tests.

### 9. Documentation

- [ ] Complete `README.md` with project overview and setup instructions.
- [ ] Document how to install dependencies.
- [ ] Document how to initialize the database.
- [ ] Document how to run the Flask application.
- [ ] Document all API endpoints and request examples.
- [ ] Document example JSON responses and error responses.
- [ ] Keep `architecture.md` aligned with the implemented design.
- [ ] Record any known limitations or assumptions.

**Expected result:** Another developer can install, run, and test the backend using the documentation.

### 10. Final Review

- [ ] Confirm that Flask is the only backend framework used.
- [ ] Confirm that all required endpoints are implemented.
- [ ] Confirm that the database schema matches the SRS.
- [ ] Confirm that business rules match the PRD.
- [ ] Confirm that stock cannot become negative.
- [ ] Confirm that a returned loan cannot be returned again.
- [ ] Confirm that stock and loan status updates are atomic.
- [ ] Run the complete test suite.
- [ ] Review code organization and remove unused code.
- [ ] Verify that the project can be started from a clean setup.

**Expected result:** A tested backend that satisfies the current SRS and PRD.

## Definition of Done

The project is considered complete when:

1. All five required API endpoints work as specified.
2. Item and loan data are stored in SQLite with the required relationship.
3. Loan creation reduces available stock only when sufficient stock exists.
4. Returning a loan restores stock and changes its status to `RETURNED`.
5. A loan with status `RETURNED` cannot be returned again.
6. API responses use JSON and the required HTTP status codes.
7. Automated tests cover the main success and failure scenarios.
8. Setup and API usage are documented.

## Scope Notes and Assumptions

- This task list covers the backend REST API only.
- User authentication and role-based authorization are not included because they are not specified in the current SRS and PRD.
- A cancellation endpoint is not included, although `CANCELLED` is listed as a possible loan status.
- Partial returns, due dates, fines, and approval workflows are not included in the current requirements.
- The implementation should not introduce additional business rules without confirming them first.
"""

output_path = "/mnt/data/task.md"
pypandoc.convert_text(content, "md", format="md", outputfile=output_path, extra_args=["--standalone"])
print(f"Created: {output_path}")
