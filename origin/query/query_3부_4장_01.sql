CREATE TABLE Secret_A
(
    MemberNo int,
    MobileTel varchar(20),
)
go

CREATE TABLE Secret_B
(
    MemoNo int,
    Memo varchar(100),
)
go

INSERT INTO Secret_A
values (10, '010-1111-2222')
go
INSERT INTO Secret_A
values (20, '010-3333-4444')
go
INSERT INTO Secret_B
values (2000, '전화번호는 011-1234-5678입니다')
go
INSERT INTO Secret_B
values (2001, '개인정보가 아니예요 010-2222')
