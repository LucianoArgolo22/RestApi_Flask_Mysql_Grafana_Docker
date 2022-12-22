create database if not exists challenge;

create table if not exists challenge.employes(
id 				integer,
name 			varchar(100),
`datetime`  	varchar(30),
department_id 	int,
job_id 			int
);


create table if not exists challenge.departments(
id 					integer,
department 			varchar(200)
);

create table if not exists challenge.jobs(
id 					integer,
job		 			varchar(100)
);




