drop table if exists users;
create table users (
    id integer primary key autoincrement,
    username text not null unique,
    password text not null,
    role integer default 0
);

insert into users (username, password, role) values ("admin", 
  "$2a$06$b109f3bbbc244eb824419u4FoK2HbzJY.e/IxMvHwPlLYQYLk4ysG"
 , 1);