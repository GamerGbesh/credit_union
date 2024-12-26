INSERT INTO members (msisdn, status) VALUES
(10001, 'ACTIVE'),
(10002, 'INACTIVE'),
(10003, 'ACTIVE'),
(10005, 'ACTIVE');

INSERT INTO members (msisdn, status, updated) VALUES
(10004, 'SUSPENDED', '2024-12-28 12:30:00');

INSERT INTO kyc_details (member_msisdn, first_name, last_name, email, dob, id_type) VALUES
(10001, 'John', 'Doe', 'john.doe@example.com', '1990-01-15', 'Passport'),
(10002, 'Jane', 'Smith', 'jane.smith@example.com', '1985-03-20', 'Driver License'),
(10003, 'Robert', 'Brown', 'robert.brown@example.com', '1995-07-25', 'National ID'),
(10004, 'Emily', 'Davis', 'emily.davis@example.com', '1992-10-05', 'Passport'),
(10005, 'Michael', 'Johnson', 'michael.johnson@example.com', '1988-12-12', 'Voter ID');

INSERT INTO contributions (member_msisdn, amount) VALUES
(10001, 1000.50),
(10002, 1500.00),
(10002, 500.00),
(10003, 2000.00),
(10005, 300.00),
(10004, 4000.00);

INSERT INTO loan_request (member_msisdn, status, request_date, amount_requested) VALUES
(10001, 'ACCEPTED', '2024-01-01', 5000.00),
(10002, 'DECLINED', '2024-01-05', 1500.50),
(10003, 'ACCEPTED', '2024-01-10', 3000.00),
(10004, 'DECLINED', '2024-01-12', 2000.50),
(10005, 'ACCEPTED', '2024-01-15', 4000.00);

INSERT INTO approved_loan (member_msisdn, amount_of_loan, interest, end_of_loan_date, monthly_deduction, status, amount_left, updated) VALUES
(10001, 5000.00, 250.00, '2025-01-01', 450.00, 'ACTIVE', 4800.00, '2024-12-27 12:30:00'),
(10003, 3000.00, 180.00, '2025-06-01', 300.00, 'ACTIVE', 3180.00, '2024-01-10 12:30:00'),
(10005, 4000.00, 200.00, '2025-12-01', 400.00, 'PAID', 0.00, '2025-12-01 00:00:00');

INSERT INTO member_balance (member_msisdn, balance) VALUES
(10002, 1500.00),
(10003, 3000.00),
(10001, 1000.50),
(10005, 100.00);


INSERT INTO member_balance (member_msisdn, balance, updated) VALUES
(10004, 0, '2024-12-28 12:30:00');




INSERT INTO credit_union_balance (amount, updated) VALUES
(500000.00, '2025-12-01 00:00:00');

INSERT INTO transactions (member_msisdn, transaction_type, amount, description) VALUES
(10001, 'DEPOSIT', 1000.50, 'Initial deposit'),
(10002, 'DEPOSIT', 1500.00, 'Initial deposit'),
(10003, 'DEPOSIT', 2000.00, 'Initial deposit'),
(10005, 'DEPOSIT', 300.00, 'Savings deposit'),
(10004, 'DEPOSIT', 4000.00, 'Savings deposit');


INSERT INTO transactions (member_msisdn, transaction_type, amount, description, created, date) VALUES
(10003, 'LOAN_WITHDRAWAL', 3000.00, 'Loan disbursement', '2024-01-10 12:30:00','2024-01-10'),
(10001, 'LOAN_REPAYMENT', 450.00, 'Monthly loan repayment', '2024-12-27 12:30:00', '2024-12-27'),
(10004, 'SAVINGS_WITHDRAWAL', 4000.00, 'Member suspended', '2024-12-28 12:30:00', '2024-12-28'),
(10005, 'LOAN_REPAYMENT', 4200.00, 'Full loan payment', '2025-12-01 00:00:00', '2025-12-01');

