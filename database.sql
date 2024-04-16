create table players(username varchar(255) primary key,email varchar(255) not null,password_hash varchar(255) not null);

insert into players(username,email,password_hash) values('admin1','email1@email.com','1234');
insert into players(username,email,password_hash) values('admin2','email2@email.com','1234');
insert into players(username,email,password_hash) values('admin3','email3@email.com','1234');