CREATE TABLE escape_test
(
   my_text char(30)
)
go 
-- 괜찮음 
INSERT INTO escape_test VALUES('hey')
-- 에러 남
INSERT INTO escape_test VALUES('hey'')
-- escape 처리됨
INSERT INTO escape_test VALUES('hey''')