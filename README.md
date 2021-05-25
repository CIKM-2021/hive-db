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
Origin URL: 
- Local: `localhost:8000/`
- Public: `https://nguyenminh-1807-hive-db-ynzyw.ondigitalocean.app/`

### Block APIs

GET: number of block (default 25)
```
http GET localhost:8000/hive-db/v1.0.0/blocks?size=3 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: return specific fields
```
http GET localhost:8000/hive-db/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by witnesses
```
http GET localhost:8000/hive-db/v1.0.0/blocks?size=5&fields=signing_key,transaction_ids,id,block_id,witness&witnesses=ausbitbank,pharesim,anyx TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by ids
```
http GET localhost:8000/hive-db/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&ids=51314015,51314016 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by block_ids
```
http GET localhost:8000/hive-db/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&block_ids=030efd5fe57e5fa7104b1186d7df6f00b39d3777,030efd60d0fbf6cca241f8be3577d3f680819c75 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by operations
```
http GET localhost:8000/hive-db/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&operations=comment_operation,comment_options_operation,vote_operation TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

**GET block by time can use both of UTC format and timestamp.**

GET: blocks since begin_time to end_time
```
http GET localhost:8000/hive-db/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=2021-02-14T04:40:15&after=2021-02-14T04:40:12 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks after a specific date
```
http GET localhost:8000/hive-db/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&after=2021-02-14T04:40:15 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks before a specific date
```
http GET localhost:8000/hive-db/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=1620171391 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```


### Comment APIs

GET: number of comments (default 25)
```
http GET localhost:8000/hive-db/v1.0.0/comments?size=3 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comment by the authors
```
http GET localhost:8000/hive-db/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&authors=wilhb81,pl-travelfeed TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comments contain words
```
http GET localhost:8000/hive-db/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&search=dish,aktywnym TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comments by permlinhk
```
http GET localhost:8000/hive-db/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&permlinks=re-ptaku-qoi4z7,qoi4z2 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

**GET comments by time can use both of UTC format and timestamp.**

GET: comments since begin_time to end_time
```
http GET localhost:8000/hive-db/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=2021-02-14T04:40:15&after=2021-02-14T04:40:12 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comments after a specific date
```
http GET localhost:8000/hive-db/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&after=2021-02-14T04:40:15 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comments before a specific date
```
http GET localhost:8000/hive-db/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=1620171391 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

### Post APIs

GET: number of posts (default 25)
```
http GET localhost:8000/hive-db/v1.0.0/posts?size=3 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: posts by the authors
```
http GET localhost:8000/hive-db/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&authors=wilhb81,pl-travelfeed TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: posts contain words
```
http GET localhost:8000/hive-db/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&search=covid TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: posts by permlinhk
```
http GET localhost:8000/hive-db/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&permlinks=covid-drove-us-into-digitization-and-crypto-or-freewrite-weekend-16-05-21,qoi4z2 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

**GET posts by time can use both of UTC format and timestamp.**

GET: posts since begin_time to end_time
```
http GET localhost:8000/hive-db/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=2021-05-24T04:40:15&after=2021-02-14T04:40:12 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: posts after a specific date
```
http GET localhost:8000/hive-db/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&after=2021-02-14T04:40:15 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: posts before a specific date
```
http GET localhost:8000/hive-db/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=1620171391 TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```
