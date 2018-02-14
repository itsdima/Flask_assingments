#1
SELECT customer.first_name, customer.last_name, customer.email, address.address FROM address
JOIN customer ON customer.address_id = address.address_id
JOIN city ON city.city_id = address.city_id
WHERE city.city_id = 312;
#2 
SELECT film.title, film.description, film.release_year, film.rating, film.special_features, category.name FROM film
JOIN film_category ON film_category.film_id = film.film_id
JOIN category ON film_category.category_id = category.category_id
WHERE category.name = 'comedy';
#3
SELECT actor.actor_id, actor.first_name, actor.last_name, film.title, film.description, film.release_year FROM film
JOIN film_actor ON film_actor.film_id = film.film_id
JOIN actor ON actor.actor_id = film_actor.actor_id
WHERE actor.actor_id = 5;
#4
SELECT customer.store_id, city.city_id, customer.first_name, customer.last_name, customer.email, address.address FROM address
JOIN city ON city.city_id = address.city_id
JOIN customer ON customer.address_id = address.address_id
WHERE customer.store_id = 1 and (city.city_id = 1 or city.city_id = 42 or city.city_id = 312 or city.city_id = 459); 
#5
SELECT film.title, film.description, film.release_year, film.rating, film.special_features FROM film
JOIN film_actor ON film_actor.film_id = film.film_id
WHERE film.rating = 'G' and film.special_features LIKE '%Behind the Scenes%' and film_actor.actor_id = 15;
#6
SELECT film_actor.film_id, CONCAT(actor.first_name, ' ', actor.last_name) AS Actor_Name, actor.actor_id, actor.last_update FROM actor
JOIN film_actor ON film_actor.actor_id = actor.actor_id
WHERE film_actor.film_id = 369;
#7
SELECT film.film_id, film.title, film.description, film.release_year, film.rating, film.special_features, category.name AS Genre, film.rental_rate FROM film
JOIN film_category ON film_category.film_id = film.film_id
JOIN category ON category.category_id = film_category.category_id
WHERE category.name = 'Drama' and film.rental_rate = '2.99';
#8
SELECT actor.actor_id, CONCAT(actor.first_name, ' ', actor.last_name) AS Actor_Name, film.title, film.description, film.release_year, film.rating, film.special_features, category.name AS Genre FROM film
JOIN film_category ON film_category.film_id = film.film_id
JOIN category ON category.category_id = film_category.category_id
JOIN film_actor ON film_actor.film_id = film.film_id
JOIN actor ON actor.actor_id = film_actor.actor_id
WHERE category.name = 'Action' and actor.first_name = 'Sandra' and actor.last_name = 'Kilmer';