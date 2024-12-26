CREATE TYPE "member_status" AS ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED');
CREATE TABLE IF NOT EXISTS "members"(
"msisdn" INT PRIMARY KEY,
"deleted" CHAR(1) DEFAULT '0' NOT NULL,
"status" "member_status",
"created" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
"updated" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dob, name, email, msisdn, id type, id number, member id -- For a table containing the member information(KYC details)
-- Admin table: name, email, password
-- Table for loan request, member id, status of the request, date of the request, amount requested


CREATE TABLE IF NOT EXISTS "kyc_details"(
"member_msisdn" INT REFERENCES "members"("msisdn"),
"first_name" VARCHAR(50) NOT NULL,
"last_name" VARCHAR(50) NOT NULL,
"email" VARCHAR(50) UNIQUE,
"dob" DATE,
"id_type" VARCHAR(20),
"created" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
"updated" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS "contributions"(
"id" SERIAL PRIMARY KEY,
"member_msisdn" INT REFERENCES "members"("msisdn"),
"transaction_date" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
"amount" DECIMAL(10, 2) NOT NULL CHECK("amount" >= 0),
"created" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
"updated" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE "loan_status" AS ENUM('ACCEPTED', 'DECLINED');
CREATE TABLE "loan_request"(
"member_msisdn" INT REFERENCES "members"("msisdn"),
"status" "loan_status" NOT NULL,
"request_date" DATE NOT NULL DEFAULT CURRENT_DATE,
"amount_requested" DECIMAL(10, 2) NOT NULL CHECK("amount_requested" > 0),
"created" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
"updated" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TYPE "status_enum" AS ENUM ('ACTIVE', 'PAID', 'OVERDUE');
CREATE TABLE IF NOT EXISTS "approved_loan"(
"id" SERIAL PRIMARY KEY,
"member_msisdn" INT REFERENCES "members"("msisdn"),
"amount_of_loan" DECIMAL(10, 2) NOT NULL CHECK("amount_of_loan" >= 0),
"interest" DECIMAL(10, 2) NOT NULL CHECK("interest" >= 0),
"end_of_loan_date" DATE NOT NULL, --CHECK("end_of_loan_date" > "date_of_loan"),
"monthly_deduction" DECIMAL(10, 2) NOT NULL CHECK("monthly_deduction" >= 0),
"status" "status_enum" NOT NULL,
"amount_left" DECIMAL(10, 2) NOT NULL,
"created" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
"updated" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS "member_balance"(
"id" SERIAL PRIMARY KEY,
"member_msisdn" INT REFERENCES "members"("msisdn"),
"balance" DECIMAL(10, 2) NOT NULL CHECK("balance" >= 0),
"created" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
"updated" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "credit_union_balance"(
"id" SERIAL PRIMARY KEY,
"amount" DECIMAL(10, 2) NOT NULL CHECK("amount" >= 0),
"created" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
"updated" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE "transaction_enum" AS ENUM ('DEPOSIT', 'SAVINGS_WITHDRAWAL', 'LOAN_REPAYMENT', 'LOAN_WITHDRAWAL');
CREATE TABLE "transactions"(
"id" SERIAL PRIMARY KEY,
"member_msisdn" INT REFERENCES "members"("msisdn"),
"transaction_type" "transaction_enum" NOT NULL,
"amount" DECIMAL(10, 2) NOT NULL,
"date" DATE DEFAULT CURRENT_DATE,
"description" TEXT,
"created" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);