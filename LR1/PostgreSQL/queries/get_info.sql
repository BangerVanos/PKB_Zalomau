SELECT * FROM vendors;
SELECT * FROM details;
SELECT * FROM projects;
SELECT * FROM details_for_projects;

-- Task 26. Получить номера проектов, для которых среднее количество поставляемых 
-- деталей Д1 больше, чем наибольшее количество любых деталей, поставляемых для проекта ПР1.
SELECT DISTINCT project_id FROM details_for_projects WHERE
(SELECT AVG(amount) FROM details_for_projects WHERE detail_id = 'Д1') >
(SELECT MAX(amount) FROM details_for_projects WHERE project_id = 'ПР1')
ORDER BY project_id;

-- Task 17. Для каждой детали, поставляемой для проекта, получить номер детали, номер проекта и соответствующее общее количество.
SELECT DISTINCT detail_id, project_id, SUM(amount) FROM details_for_projects
GROUP BY detail_id, project_id
ORDER BY detail_id;

-- Task 25. Получить номера проектов, город которых стоит первым в алфавитном списке городов.
SELECT id FROM projects
ORDER BY city
LIMIT 1;

-- Task 8. Получить все такие тройки "номера поставщиков-номера деталей-номера проектов", 
-- для которых никакие из двух выводимых поставщиков, деталей и проектов не размещены в одном городе.
SELECT DISTINCT vendors.id, details.id, projects.id FROM vendors
JOIN details ON vendors.city != details.city
JOIN projects ON vendors.city != projects.city AND details.city != projects.city;

-- Task 2. Получить полную информацию обо всех проектах в Минске.
SELECT * FROM projects WHERE city = 'Минск';

-- Task 7. Получить все такие тройки "номера поставщиков-номера деталей-номера проектов", 
-- для которых выводимые поставщик, деталь и проект не размещены в одном городе.
SELECT dfp.vendor_id, dfp.detail_id, dfp.project_id FROM details_for_projects AS dfp
JOIN vendors ON dfp.vendor_id = vendors.id
JOIN details ON dfp.detail_id = details.id
JOIN projects ON dfp.project_id = projects.id
WHERE vendors.city != details.city AND vendors.city != projects.city AND details.city != projects.city;

-- Task 11. Получить все пары названий городов, для которых поставщик из первого города обеспечивает проект во втором городе.
SELECT DISTINCT vendors.city AS vend_city, projects.city AS pj_city FROM details_for_projects AS dfp
JOIN vendors ON dfp.vendor_id = vendors.id
JOIN projects ON dfp.project_id = projects.id
WHERE vendors.city != projects.city;

-- Task 36. Получить все пары номеров поставщиков, скажем, Пx и Пy, такие, 
-- что оба эти поставщика поставляют в точности одно и то же множество деталей.
WITH NOT_EQ AS
	(SELECT DISTINCT V1.VENDOR_ID AS VEN1,
			V2.VENDOR_ID AS VEN2,
			V1.DETAIL_ID,
			V2.DETAIL_ID
		FROM DETAILS_FOR_PROJECTS AS V1
		JOIN DETAILS_FOR_PROJECTS AS V2 ON V1.DETAIL_ID != V2.DETAIL_ID
		WHERE
				(SELECT COUNT(DISTINCT DETAIL_ID)
					FROM DETAILS_FOR_PROJECTS
					WHERE VENDOR_ID = V1.VENDOR_ID) !=
				(SELECT COUNT(DISTINCT DETAIL_ID)
					FROM DETAILS_FOR_PROJECTS
					WHERE VENDOR_ID = V2.VENDOR_ID)
			OR
				(SELECT COUNT(DETAIL_ID)
					FROM DETAILS_FOR_PROJECTS
					WHERE (DETAIL_ID = V1.DETAIL_ID
												AND VENDOR_ID = V2.VENDOR_ID)
						OR (DETAIL_ID = V2.DETAIL_ID
										AND VENDOR_ID = V1.VENDOR_ID)) = 0 )
SELECT DISTINCT V1.VENDOR_ID,
	V2.VENDOR_ID
FROM DETAILS_FOR_PROJECTS AS V1
JOIN DETAILS_FOR_PROJECTS AS V2 ON V1.VENDOR_ID != V2.VENDOR_ID
WHERE V1.VENDOR_ID NOT IN
		(SELECT VEN1
			FROM NOT_EQ
			WHERE VEN2 = V2.VENDOR_ID)
	AND V2.VENDOR_ID NOT IN
		(SELECT VEN2
			FROM NOT_EQ
			WHERE VEN1 = V1.VENDOR_ID);


-- Task 16. Получить общее количество деталей Д1, поставляемых поставщиком П1.
SELECT SUM(details_for_projects.amount) FROM details_for_projects
WHERE details_for_projects.vendor_id = 'П1' AND details_for_projects.detail_id = 'Д1';

-- Task 31. Получить номера поставщиков, поставляющих одну и ту же деталь для всех проектов.
SELECT vendor_id FROM details_for_projects
GROUP BY vendor_id
HAVING COUNT(DISTINCT detail_id) = 1;