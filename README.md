# HIVE Data service

## Install
```
docker pull nguyenminh1807/hive-db:v1.0
```

## Run local
```
docker run -it --rm -p 5000:5000 nguyenminh18078/hive-db:v1.0
```

## Examples

### Block APIs


GET: number of block (default 25)
```
http GET localhost:8000/hive-db/v1.0.0/blocks\?size\=3 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: return specific fields
```
http GET localhost:8000/hive-db/v1.0.0/blocks\?size\=3\&fields\=signing\_key\,transaction\_ids\,id\,block\_id\,witness TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by witnesses
```
http GET localhost:8000/hive-db/v1.0.0/blocks\?size\=5\&fields\=signing\_key\,transaction\_ids\,id\,block\_id\,witness\&witnesses\=ausbitbank\,pharesim\,anyx TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by ids
```
http GET localhost:8000/hive-db/v1.0.0/blocks\?size\=3\&fields\=signing\_key\,transaction\_ids\,id\,block\_id\,witness\&ids=51314015,51314016 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by block_ids
```
http GET localhost:8000/hive-db/v1.0.0/blocks\?size\=3\&fields\=signing\_key\,transaction\_ids\,id\,block\_id\,witness\&block_ids=030efd5fe57e5fa7104b1186d7df6f00b39d3777,030efd60d0fbf6cca241f8be3577d3f680819c75 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```


**GET block by time can use both of UTC format and timestamp.**

GET: block since begin_time to end_time
```
http GET localhost:8000/hive-db/v1.0.0/blocks\?size\=3\&fields\=signing\_key\,transaction\_ids\,id\,block\_id\,witness\&before\=2021-02-14T04:40:15\&after\=2021-02-14T04:40:12 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks after a specific date
```
http GET localhost:8000/hive-db/v1.0.0/blocks\?size\=3\&fields\=signing\_key\,transaction\_ids\,id\,block\_id\,witness\&after\=2021-02-14T04:40:15 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks before a specific date
```
http GET localhost:8000/hive-db/v1.0.0/blocks\?size\=3\&fields\=signing\_key\,transaction\_ids\,id\,block\_id\,witness\&before\=1620171391 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```