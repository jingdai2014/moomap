drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	uid integer not null,
	time text not null,
	color text not null,
	valence integer not null
);