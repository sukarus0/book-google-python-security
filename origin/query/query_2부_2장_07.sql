CREATE TABLE secret_member(
member_id char(20),
member_name char(20),
mobile_number char(20),
email char(30)
)
go
INSERT INTO secret_member VALUES('admin', '홍길동', '010-xxxx-2222', 'test@test.com')
