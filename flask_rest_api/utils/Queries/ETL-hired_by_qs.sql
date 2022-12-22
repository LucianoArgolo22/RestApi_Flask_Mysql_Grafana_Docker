with joins_and_casts as (
select 
	emp.id,
	emp.name,
	substring(emp.datetime, 1, 4) as year,
	cast(substring(emp.datetime, 6, 2) as unsigned) as month,
	jb.job, dp.department
	from challenge.employes emp
inner join challenge.departments dp
on emp.department_id = dp.id
inner join challenge.jobs jb 
on emp.job_id = jb.id),
quarters_generated as (
	select 
		*,
		CASE 
			WHEN month < 3 then 1
			else 0
			END as 'Q1',
		CASE 
			WHEN  month > 3 and month < 6 then 1
			else 0
			END as 'Q2',
		CASE 
			WHEN month > 6 and month < 9  then 1
			else 0
			END as 'Q3',
		CASE 
			WHEN month > 9 and month < 12  then 1
			else 0
			END as 'Q4'
	from joins_and_casts)
select department,
	   job,
	   sum(Q1) as 'Q1',
	   sum(Q2) as 'Q2',
	   sum(Q3) as 'Q3',
	   sum(Q4) as 'Q4'
from quarters_generated
group by department , job
order by department desc, job desc;	