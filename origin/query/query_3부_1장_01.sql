CREATE TABLE sms_cert(
    seqno int IDENTITY(1,1) NOT NULL,
    member_id char(20) NOT NULL,
    cert_yn char(1) NOT NULL,
    cert_date datetime NOT NULL,
)