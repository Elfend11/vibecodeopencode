PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Loan;
DROP TABLE IF EXISTS Item;

CREATE TABLE Item (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL,
    total_stock     INTEGER NOT NULL DEFAULT 0 CHECK (total_stock >= 0),
    available_stock INTEGER NOT NULL DEFAULT 0 CHECK (available_stock >= 0),
    CHECK (available_stock <= total_stock)
);

CREATE TABLE Loan (
    id          INTEGER   PRIMARY KEY AUTOINCREMENT,
    student_id  TEXT      NOT NULL,
    item_id     INTEGER   NOT NULL,
    quantity    INTEGER   NOT NULL CHECK (quantity > 0),
    status      TEXT      NOT NULL DEFAULT 'BORROWED'
                          CHECK (status IN ('BORROWED', 'RETURNED', 'CANCELLED')),
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES Item (id) ON DELETE RESTRICT
);

CREATE INDEX idx_loan_student_id ON Loan (student_id);
CREATE INDEX idx_loan_item_id ON Loan (item_id);
