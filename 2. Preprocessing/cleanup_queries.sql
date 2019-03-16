use smart_tourism;

CREATE TABLE Attractions_master AS

    SELECT 
        Attraction AS 'Attraction_name',
        Place,
        Description,
        'Beach' AS 'Category',
        'HolidayIQ' AS 'Website',
        0 AS 'User_rating',
        '' AS 'Review_keywords',
        city,
        district,
        formatted_address,
        lat,
        lng,
        locality,
        pincode,
        SUBSTRING(state, 1, LENGTH(state) - 3) AS 'state'
    FROM
        beachesdescription 
    UNION ALL SELECT 
        Attraction AS 'Attraction_name',
        Place,
        Description,
        'Heritage' AS 'Category',
        'HolidayIQ' AS 'Website',
        0 AS 'User_rating',
        '' AS 'Review_keywords',
        city,
        district,									
        formatted_address,
        lat,
        lng,
        locality,
        pincode,
        SUBSTRING(state, 1, LENGTH(state) - 3) AS 'state'
    FROM
        heritagedescription 
    UNION ALL SELECT 
        Attraction AS 'Attraction_name',
        Place,
        Description,
        'Hill-Station' AS 'Category',
        'HolidayIQ' AS 'Website',
        0 AS 'User_rating',
        '' AS 'Review_keywords',
        city,
        district,
        formatted_address,
        lat,
        lng,
        locality,
        pincode,
        SUBSTRING(state, 1, LENGTH(state) - 3) AS 'state'
    FROM
        hillsdescription 
    UNION ALL SELECT 
        Attraction_name,
        Raw_address as 'Place',
        Description,
        'Beach' AS 'Category',
        'TripAdvisor' AS 'Website',
        User_rating,
        Review_keywords,
        city,
        district,
        formatted_address,
        lat,
        lng,
        locality,
        pincode,
        SUBSTRING(state, 1, LENGTH(state) - 3) AS 'state'
    FROM
        attraction_details_beaches
	UNION ALL SELECT 
        Attraction_name,
        Raw_address as 'Place',
        Description,
        'Heritage' AS 'Category',
        'TripAdvisor' AS 'Website',
        User_rating,
        Review_keywords,
        city,
        district,
        formatted_address,
        lat,
        lng,
        locality,
        pincode,
        SUBSTRING(state, 1, LENGTH(state) - 3) AS 'state'
    FROM
        attraction_details_heritage
    UNION ALL SELECT 
        Attraction_name,
        Raw_address as 'Place',
        Description,
        'Hill-Station' AS 'Category',
        'TripAdvisor' AS 'Website',
        User_rating,
        Review_keywords,
        city,
        district,
        formatted_address,
        lat,
        lng,
        locality,
        pincode,
        SUBSTRING(state, 1, LENGTH(state) - 3) AS 'state'
    FROM
        attraction_details_hill_stations;
        
-- Remove EOL characters and double quotes
Update Attractions_master set Description =  REPLACE(REPLACE(Description, '\r', ''), '\n', '');
Update Attractions_master set Description =  REPLACE(Description,'"','');
        
-- Add an id column for the attractions
alter table Attractions_master add column `attraction_id` int(10) unsigned primary key AUTO_INCREMENT;

   
drop table attraction_reviews;


create table attraction_reviews as 

SELECT 
    'TripAdvisor' AS 'Website',
    Category,
    Attraction_name,
    place,
    '' AS 'Heading',
    Review_text,
    Review_date,
    Review_rating
FROM
    attraction_reviews_hill_station_ta 
UNION ALL SELECT 
    'TripAdvisor' AS 'Website',
    Category,
    Attraction_name,
    place,
    '' AS 'Heading',
    Review_text,
    Review_date,
    Review_rating
FROM
    attraction_reviews_beaches_ta 
UNION ALL SELECT 
    'TripAdvisor' AS 'Website',
    Category,
    Attraction_name,
    place,
    '' AS 'Heading',
    Review_text,
    Review_date,
    Review_rating
FROM
    attraction_reviews_heritage_ta 
UNION ALL SELECT 
    'HolidayIQ' AS 'Website',
    'beaches' AS 'Category',
    Attractions AS 'Attraction_name',
    place,
    Heading,
    Review_comment AS 'Review_text',
    NULL AS Review_date,
    NULL AS Review_rating
FROM
    beachreviewshiq_cleaned 
UNION ALL SELECT 
    'HolidayIQ' AS 'Website',
    'Historical Sites' AS 'Category',
    Attraction AS 'Attraction_name',
    place,
    Heading,
    Review_comment AS 'Review_text',
    NULL AS Review_date,
    Rating AS Review_rating
FROM
    heritagesreviewhiq_cleaned 
UNION ALL SELECT 
    'HolidayIQ' AS 'Website',
    'hill stations' AS 'Category',
    Attracton AS 'Attraction_name',
    place,
    Heading,
    Review_comment AS 'Review_text',
    NULL AS Review_date,
    NULL AS Review_rating
FROM
    hillstationreviewshiq_cleaned;


-- Add a review Id column
alter table attraction_reviews add column `review_id` int(10) unsigned primary key AUTO_INCREMENT;

-- Add an attraction Id column
alter table attraction_reviews add column `attraction_id` int(10);

-- One time Cleanup --------------------------------------------------------------------------------------------------------------------------
-- Add an place column
alter table attraction_reviews_beaches_ta add column `place` varchar(450);
alter table attraction_reviews_heritage_ta add column `place` varchar(450);
alter table attraction_reviews_hill_station_ta add column `place` varchar(450);

select * from _missed_reviews;

delete
FROM
    attraction_reviews_hill_station_ta
WHERE exists
    (SELECT 1 
		FROM
            _missed_reviews
        WHERE
            category = 'hill stations' and
            attraction_name = nearby_attraction);
            

insert into attraction_reviews_hill_station_ta (Category,Attraction_name,Review_text,Review_date,Review_rating,place)
select category,nearby_attraction,review_body,review_date,review_rating,raw_address from _missed_reviews where category = 'hill stations';


update attraction_reviews set category = 'Hill-Station' where category in ('hill_stations','hill stations');
update attraction_reviews set category = 'Beach' where category in ('beaches');
update attraction_reviews set category = 'Heritage' where category in ('Historical sites');

-- One time Cleanup -----------------------------------------------------------------------------------------------------------------------------
select count(distinct(attraction_name)) from attraction_reviews where place is not null and website = 'TripAdvisor';
select count(distinct(nearby_attraction)) from _missed_reviews;


select attraction_name,place from attraction_reviews where place <> ' ' and website = 'TripAdvisor' and attraction_name = 'Church and Monastery of St Augustine';
select * from attractions_master where attraction_name = 'Church and Monastery of St Augustine';

update attractions_master set place = trim(place);
update attraction_reviews set place = replace(place,',',' ');
update attraction_reviews set place = replace(place,',,',',');
update attraction_reviews set place = '' where place is null;
update attraction_reviews set attraction_name = replace(attraction_name,'â€™','');
update attraction_reviews set place = trim(place);
update attractions_master set place = replace(place,'''','');
update attraction_reviews set attraction_name = replace(attraction_name,'"','');
update attractions_master set attraction_name = replace(attraction_name,'"','');
update attraction_reviews set place = replace(place,'â€Ž','');

update attractions_master set place = replace(place,'  ',' ');

select * from attraction_reviews;



-- update attraction_ids for TripAdvisor
UPDATE attraction_reviews r 
SET 
    r.attraction_id = (SELECT 
            m.attraction_id
        FROM
            attractions_master m
        WHERE
            m.Website = 'TripAdvisor'
                AND r.Website = 'TripAdvisor'
                AND m.attraction_name = r.attraction_name
                AND r.category = m.category   
                AND R.place = m.place
                limit 1)
WHERE
    r.website = 'TripAdvisor'
    and r.place is not null
    and r.attraction_id is null;
    
    
    SELECT 
    attraction_name, place, category,website
FROM
    attraction_reviews
WHERE
    attraction_id IS NULL
        AND website = 'TripAdvisor'
GROUP BY attraction_name , place , category,website;

select * from attractions_master where attraction_name like 'Buland%';
-- update attractions_master set place = 'where attraction_name = 'Akshardham Temple' and attraction_id = 8982;

select * from attraction_details_heritage where upper(attraction_name) like '%BU%';
    

select m.attraction_id from attraction_reviews r,attractions_master m where             m.Website = 'TripAdvisor'
                AND r.Website = 'TripAdvisor'
                AND trim(m.attraction_name) = trim(r.attraction_name)
                AND r.category = m.category
                AND r.place = m.place and r.place is not null;
                
             --   AND r.place = m.place;




SELECT 
    attraction_name, place, category
FROM
    attraction_reviews
WHERE
    website = 'TripAdvisor'
        AND attraction_id IS NULL;

select length(place),place,category from attractions_master where attraction_name like 'Lal Tibba%';

                

SHOW PROCESSLIST;

                
			KILL 37;

update attractions_master_tmp set attraction_name = replace(attraction_name,'Overview','') where website = 'HolidayIQ';
                
                
-- Find duplicate locations
SELECT 
    attraction_name,place,category,count(*)
FROM
    attractions_master_tmp
WHERE
    website = 'TripAdvisor'
GROUP BY attraction_name,place,category
HAVING COUNT(*) > 1; 


select distinct attraction_name from attraction_reviews where website = 'TripAdvisor' and attraction_name not in (select attraction_name from attractions_master);



select attraction_name,place from attraction_reviews where attraction_id is null and website = 'TripAdvisor' and attraction_name = 'Mahabaleshwar Hill Station';


select * from _missed_reviews;

select * from attractions_master_tmp where website ='TripAdvisor' and attraction_name = 'Mahabaleshwar Hill Station';

select category from attractions_master group by category;
select category from attraction_reviews group by category;
select website from attractions_master group by website; 
select website from attraction_reviews group by website; 


select count(*) from attraction_details_beaches;