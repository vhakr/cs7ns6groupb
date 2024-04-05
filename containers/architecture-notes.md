Queries that specify the tenant_id do not need to communicate with other nodes.

Let's say the host for `tenant_id = 'eur'` is `neimhin`, and all other nodes have died.
We can still select and insert into this shard:

```
postgres=# insert into family (tenant_id, id) values ('bak', 2);
INSERT 0 1
```

```
postgres=# select * from family where tenant_id = 'bak';
 tenant_id | id | member1_id | member2_id | member3_id | member4_id
-----------+----+------------+------------+------------+------------
 bak       |  0 | neimhin    | cian       |            |
 bak       |  2 |            |            |            |
(2 rows)
```

If the query doesn't restrict the tenant_id it will fail because it will try to communicate with all hosts:

```
# select * from family;
ERROR:  connection to the remote node postgres@172.17.0.3:5432 failed with the following error: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
```

Increasing the replication_factor does not change this. Another approach is needed for high availability.
