select o.member_id, s.food_name, o.buy_count, o.buy_date, s.price, 
(s.price * o.buy_count) total_price from order_record o(nolock)
join supermarket s(nolock)
on s.food_no = o.food_no
where o.member_id = ''' order by o.buy_count desc
