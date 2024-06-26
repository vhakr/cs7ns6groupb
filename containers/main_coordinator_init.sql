\set ON_ERROR_STOP on

CREATE EXTENSION citus;

CREATE TABLE customer (
    tenant_id VARCHAR(3),
    name VARCHAR(255),
    family_id INT,
    password TEXT,
    PRIMARY KEY (tenant_id, name)
);

CREATE TABLE family (
    tenant_id VARCHAR(3),
    id SERIAL,
    -- m1_tenant_id INT, 
    -- m2_tenant_id INT, 
    -- m3_tenant_id INT, 
    -- m4_tenant_id INT, 
    member1_id VARCHAR(255),
    member2_id VARCHAR(255),
    member3_id VARCHAR(255),
    member4_id VARCHAR(255),
    PRIMARY KEY (tenant_id, id)
);


CREATE TABLE purchase (
    tenant_id VARCHAR(3), id SERIAL,
    family_id INT,
    customer_tenant_id VARCHAR(3), customer_name VARCHAR(255),
    amount_euro_equivalent DECIMAL,
    timestamp BIGINT DEFAULT (EXTRACT (EPOCH FROM NOW())),
    PRIMARY KEY (tenant_id, id)
);

ALTER DATABASE postgres SET citus.shard_count = 3;
ALTER DATABASE postgres SET citus.shard_replication_factor = 3;

SELECT create_distributed_table('family', 'tenant_id');
SELECT create_distributed_table('purchase', 'tenant_id', colocate_with => 'family');
SELECT create_distributed_table('customer', 'tenant_id', colocate_with => 'family');
SELECT update_distributed_table_colocation('family', colocate_with => 'customer');
-- SELECT update_distributed_table_colocation('purchase', colocate_with => 'customer');

ALTER TABLE customer
    ADD CONSTRAINT fk_family
        FOREIGN KEY (tenant_id, family_id)
        REFERENCES family(tenant_id, id);

ALTER TABLE purchase
    ADD CONSTRAINT fk_family
        FOREIGN KEY (tenant_id, family_id) 
        REFERENCES family(tenant_id, id);

ALTER TABLE family      ADD CONSTRAINT fk_member1 FOREIGN KEY (tenant_id, member1_id) REFERENCES customer(tenant_id, name);
ALTER TABLE family      ADD CONSTRAINT fk_member2 FOREIGN KEY (tenant_id, member2_id) REFERENCES customer(tenant_id, name);
ALTER TABLE family      ADD CONSTRAINT fk_member3 FOREIGN KEY (tenant_id, member3_id) REFERENCES customer(tenant_id, name);
ALTER TABLE family      ADD CONSTRAINT fk_member4 FOREIGN KEY (tenant_id, member4_id) REFERENCES customer(tenant_id, name);

-- FIXME: fails because purchase is not colocated with customer
-- ALTER TABLE purchase
--     ADD CONSTRAINT fk_customer
--         FOREIGN KEY (customer_tenant_id, customer_name) 
--         REFERENCES customer(tenant_id, name);

SELECT citus_set_coordinator_host('neimhin');

CREATE OR REPLACE FUNCTION si(c VARCHAR(3))
RETURNS TEXT AS $$
DECLARE
    result TEXT;
BEGIN
    SELECT nodename INTO result
    FROM pg_dist_placement AS placement
    JOIN pg_dist_node AS node ON placement.groupid = node.groupid
    WHERE node.noderole = 'primary'
    AND shardid = (SELECT get_shard_id_for_distribution_column('family', c));

    RETURN result;
END;
$$ LANGUAGE plpgsql;

