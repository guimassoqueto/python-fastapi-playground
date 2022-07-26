create table posts(
	id serial primary key,
	title varchar(100) not null,
	content text not null,
	published boolean default true,
	created_at timestamp not null default current_timestamp
)