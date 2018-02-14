#1
SELECT language, percentage, countries.name FROM languages
JOIN countries ON languages.country_id = countries.id
WHERE language = 'Slovene'
order by percentage DESC;
#2
SELECT countries.name, count(cities.name) FROM countries
JOIN cities ON cities.country_id = countries.id
GROUP BY countries.name
order by count(cities.name) desc;
#3
SELECT cities.name, cities.population FROM cities
JOIN countries ON countries.id = cities.country_id
WHERE cities.population > 500000 and countries.name = 'Mexico'
order by cities.population desc;
#4
SELECT countries.name, language, languages.percentage FROM languages
JOIN countries ON languages.country_id = countries.id
WHERE languages.percentage > 89
order by languages.percentage desc;
#5
SELECT countries.name, countries.surface_area, countries.population FROM countries
WHERE countries.surface_area < 501 and countries.population > 100000;
#6
SELECT countries.name, countries.government_form, countries.capital, countries.life_expectancy FROM countries
WHERE countries.government_form = 'Constitutional Monarchy' and countries.capital > 200 and countries.life_expectancy > 75;
#7
SELECT countries.name, cities.name, cities.district, cities.population FROM cities
JOIN countries ON cities.country_id = countries.id
WHERE cities.district = 'Buenos Aires' and cities.population > 500000; 
#8
SELECT countries.region, COUNT(countries.name) FROM countries
GROUP BY countries.region
ORDER BY COUNT(countries.name) desc;
