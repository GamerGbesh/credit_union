SELECT m.msisdn, m.status, m.created, m.updated, 
       k.first_name, k.last_name, k.email, k.dob, k.id_type
FROM members m
LEFT JOIN kyc_details k ON m.msisdn = k.member_msisdn;

SELECT m.msisdn, k.first_name, k.last_name, 
       SUM(c.amount) AS total_contributions
FROM members m
JOIN kyc_details k ON m.msisdn = k.member_msisdn
JOIN contributions c ON m.msisdn = c.member_msisdn
WHERE m.status = 'ACTIVE'
GROUP BY m.msisdn, k.first_name, k.last_name;

SELECT lr.request_date, lr.status, lr.member_msisdn,
       k.first_name, k.last_name, k.email
FROM loan_request lr
JOIN kyc_details k ON lr.member_msisdn = k.member_msisdn;

SELECT SUM(balance) AS total_member_balance
FROM member_balance;

SELECT amount AS credit_union_balance
FROM credit_union_balance
ORDER BY id DESC LIMIT 1;

SELECT t.transaction_type, t.amount, t.date, t.description
FROM transactions t
WHERE t.member_msisdn = 10001 -- Replace with specific member's MSISDN
ORDER BY t.date DESC;

SELECT k.first_name, k.last_name, al.amount_left, al.monthly_deduction
FROM approved_loan al
JOIN kyc_details k ON al.member_msisdn = k.member_msisdn
WHERE al.amount_left > 0;

SELECT SUM(c.amount) AS total_contributions
FROM contributions c;

SELECT status, COUNT(*) AS total_requests
FROM loan_request
GROUP BY status;

SELECT mb.member_msisdn, k.first_name, k.last_name, mb.balance
FROM member_balance mb
JOIN kyc_details k ON mb.member_msisdn = k.member_msisdn
WHERE mb.balance < 500;

SELECT t.transaction_type, SUM(t.amount) AS total_amount
FROM transactions t
WHERE t.transaction_type IN ('DEPOSIT', 'LOAN_REPAYMENT')
GROUP BY t.transaction_type;

SELECT k.first_name, k.last_name, al.amount_left, al.status
FROM approved_loan al
JOIN kyc_details k ON al.member_msisdn = k.member_msisdn
WHERE al.status = 'ACTIVE'
ORDER BY al.amount_left DESC;

SELECT m.msisdn, k.first_name, k.last_name
FROM members m
JOIN kyc_details k ON m.msisdn = k.member_msisdn
LEFT JOIN contributions c ON m.msisdn = c.member_msisdn
WHERE m.status = 'ACTIVE' AND c.id IS NULL;

SELECT t.transaction_type, COUNT(*) AS transaction_count, SUM(t.amount) AS total_amount
FROM transactions t
GROUP BY t.transaction_type;
