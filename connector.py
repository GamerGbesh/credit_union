import psycopg2

conn = psycopg2.connect(
    database="credit_union",
    host="localhost",
    user="postgres",
    password="gbeshko1",
    port="5432"
)

cursor = conn.cursor()

def get_members(status = "all"):
    query = """SELECT m.msisdn, m.status, k.first_name,
               k.last_name, k.dob, k.id_type
               FROM members m
               JOIN kyc_details k ON k.member_msisdn = m.msisdn"""
    
    if status not in ["all", "active", "inactive", "suspended"]:
        return "Invalid status"
    
    if status == "all":
        cursor.execute(query)
        return cursor.fetchall()
    elif status == "active":
        cursor.execute(query + " WHERE status = 'ACTIVE'")
        return cursor.fetchall()
    elif status == "inactive":
        cursor.execute(query + " WHERE status = 'INACTIVE'")
        return cursor.fetchall()
    elif status == "suspended":
        cursor.execute(query + " WHERE status = 'SUSPENDED'")
        return cursor.fetchall()
    
    

def get_contributions(status = "all"):
    query = """SELECT m.msisdn, k.first_name, k.last_name, 
               SUM(c.amount) AS total_contributions
               FROM members m
               JOIN kyc_details k ON m.msisdn = k.member_msisdn
               JOIN contributions c ON m.msisdn = c.member_msisdn
               """
    suffix = " GROUP BY m.msisdn, k.first_name, k.last_name"

    if status not in ["all", "active", "inactive", "suspended"]:
        return "Invalid status"
    
    if status == "all":
        cursor.execute(query + suffix)
        return cursor.fetchall()
    elif status == "active":
        cursor.execute(query + " WHERE m.status = 'ACTIVE'" + suffix)
        return cursor.fetchall()
    elif status == "inactive":
        cursor.execute(query + " WHERE m.status = 'INACTIVE'" + suffix)
        return cursor.fetchall()
    elif status == "suspended":
        cursor.execute(query + " WHERE m.status = 'SUSPENDED'" + suffix)
        return cursor.fetchall()
    
    



def get_loan_requests(status = "all"):
        query = """SELECT lr.request_date, lr.status, lr.member_msisdn,
            k.first_name, k.last_name, lr.amount_requested
            FROM loan_request lr
            JOIN kyc_details k ON lr.member_msisdn = k.member_msisdn"""
        
        if status not in ["all", "pending", "approved", "rejected"]:
            return "Invalid status"
        
        if status == "all":
            cursor.execute(query)
            return cursor.fetchall()
        elif status == "pending":
            cursor.execute(query + " WHERE lr.status = 'PENDING'")
            return cursor.fetchall()
        elif status == "approved":
            cursor.execute(query + " WHERE lr.status = 'ACCEPTED'")
            return cursor.fetchall()
        elif status == "rejected":
            cursor.execute(query + " WHERE lr.status = 'DECLINED'")
            return cursor.fetchall()
        
        
def get_credit_union_balance():
    cursor.execute("SELECT amount FROM credit_union_balance")
    return cursor.fetchone()[0]


def get_transaction_history(member_msisdn:None|int = None, transaction_type:None|str=None):
    query = """SELECT k.first_name, k.last_name, t.transaction_type, t.amount, t.date, t.description
                FROM transactions t
                JOIN kyc_details k ON t.member_msisdn = k.member_msisdn
                """
    suffix = " ORDER BY t.date DESC"
    if transaction_type and transaction_type.upper() not in ["DEPOSIT", "SAVINGS_WITHDRAWAL", "LOAN_REPAYMENT", "LOAN_WITHDRAWAL"]:
        return "Invalid transaction type"
    if member_msisdn:
        query = query + f" WHERE t.member_msisdn = {member_msisdn}"
        if transaction_type:
            query = query + f" AND t.transaction_type = '{transaction_type.upper()}'"
    elif transaction_type:
        query = query + f" WHERE t.transaction_type = '{transaction_type.upper()}'"
    query += suffix
    cursor.execute(query)
    return cursor.fetchall()

def get_total_contributions():
    query = """SELECT SUM(c.amount) AS total_contributions
                FROM contributions c"""
    cursor.execute(query)
    return cursor.fetchone()[0]


def get_loans():
    query = """SELECT k.first_name, k.last_name, al.amount_left, al.monthly_deduction
                FROM approved_loan al
                JOIN kyc_details k ON al.member_msisdn = k.member_msisdn
                WHERE al.amount_left > 0"""
    cursor.execute(query)
    return cursor.fetchall()


def get_member_balance():
    query = """SELECT mb.member_msisdn, k.first_name, k.last_name, mb.balance
                FROM member_balance mb
                JOIN kyc_details k ON mb.member_msisdn = k.member_msisdn
                ORDER BY mb.balance DESC"""
    cursor.execute(query)
    return cursor.fetchall()