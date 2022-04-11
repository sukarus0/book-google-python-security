CREATE TABLE dbo.test_result(
    seqno int IDENTITY(1,1) NOT NULL,
    name varchar (20) NOT NULL,
    previous_score int NOT NULL,
    current_score int NOT NULL,
    pass_yn char(1) NOT NULL
)
