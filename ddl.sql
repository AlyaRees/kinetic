create table if not exists client (
id integer primary key generated always as identity,
name text not null,
age text not null,
level text not null,
gender text not null
);
