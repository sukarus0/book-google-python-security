CREATE PROCEDURE Insert_Escape_Text 
    @mytext char(30) 
AS 
   INSERT INTO escape_test
   VALUES (@mytext)
