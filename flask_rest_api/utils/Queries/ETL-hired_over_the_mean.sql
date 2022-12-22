
with joins_and_casts as 
(
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
	on emp.job_id = jb.id
),
mean_hired as( #i get the mean
	select AVG(hired) as hired  from
	(
		select department, job , count(*) as hired
		from joins_and_casts
		where year = '2021'
		group by job, department
	) b
)
select * from 
			(
			select job, department, count(*) as hired
			from joins_and_casts
			group by job, department
			order by job desc, department desc
			) a
having hired > (select * from mean_hired);