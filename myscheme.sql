drop table customer cascade;
drop table family cascade;
CREATE TABLE IF NOT EXISTS family (
    family_id SERIAL PRIMARY KEY,
    shard_id INT
);

CREATE TABLE IF NOT EXISTS customer (
    customer_name varchar(255) not null PRIMARY KEY,
    family_id INT REFERENCES family(family_id),
    password varchar(255) not null
);

ALTER TABLE family
ADD column if not exists member1_id varchar(255) REFERENCES customer(customer_name),
ADD column if not exists member2_id varchar(255) REFERENCES customer(customer_name),
ADD column if not exists member3_id varchar(255) REFERENCES customer(customer_name),
ADD column if not exists member4_id varchar(255) REFERENCES customer(customer_name);
