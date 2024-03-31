CREATE TABLE customer (
    region INT,
    id INT,
    family_region INT, family_id INT,
    password TEXT,
    PRIMARY KEY (region, id)
);

CREATE TABLE family (
    region INT,
    id INT,
    m1_region INT, member1_id INT,
    m2_region INT, member2_id INT,
    m3_region INT, member3_id INT,
    m4_region INT, member4_id INT,
    PRIMARY KEY (region, id),
    FOREIGN KEY (m1_region, member1_id) REFERENCES customer(region, id),
    FOREIGN KEY (m2_region, member2_id) REFERENCES customer(region, id),
    FOREIGN KEY (m3_region, member3_id) REFERENCES customer(region, id),
    FOREIGN KEY (m4_region, member4_id) REFERENCES customer(region, id)
);

ALTER TABLE customer
ADD CONSTRAINT fk_family
FOREIGN KEY (family_region, family_id)
REFERENCES family(region, id);

SELECT
    constraint_name,
    table_name,
    column_name,
    foreign_table_name,
    foreign_column_name
FROM
    information_schema.key_column_usage
WHERE
    constraint_name LIKE 'fk_%'; -- assuming your foreign key constraints start with 'fk_'

CREATE TABLE purchases (
    region INT, id INT,
    family_region INT, family_id INT,
    customer_region INT, customer_id INT,
    amount_euro_equivalent DECIMAL,
    FOREIGN KEY (customer_region, customer_id) REFERENCES customer(region, id),
    FOREIGN KEY (family_region, family_id) REFERENCES family(region, id),
    PRIMARY KEY (region, id)
);
