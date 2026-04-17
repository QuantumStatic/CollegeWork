DELIMITER //
create trigger create_person_trigger
before insert on person
for each row
begin
	if exists(select * 
			from person
            where person.username = new.username) then
            signal sqlstate '45000' set message_text = 'Username Already Exists!!'; 

	elseif exists(select *
			from person
            where person.email = new.email) then
            signal sqlstate '45000' set message_text = 'Email Already Exists!!';
	end if;
end;
//
DELIMITER ;