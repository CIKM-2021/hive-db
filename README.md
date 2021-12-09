# HIVE Data service
[![python](https://img.shields.io/badge/python-3.6.15-green)](https://www.python.org/)
[![slither](https://img.shields.io/badge/falcon-3.0.1-yellowgreen)](https://falcon.readthedocs.io/en/stable/)
[![bigquery](https://img.shields.io/badge/google--cloud--bigquery-2.15.0-red)](https://cloud.google.com/bigquery/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY-SA 4.0][cc-by-sa-shield]](https://creativecommons.org/licenses/by-sa/4.0/)


## Setup Environment

- We provide public APIs via the endpoint *http://sochaindb.com*,  currently authenticated by the key *"TOKEN"* with the value *"WrrXP6szu06wlLQVfAM3b0FD8i4612zc"* in the Request Header.
- The APIs could be requested by the [httpie tool](https://httpie.io/). Depending on your OS, you can quickly install this tool by a command line.

On Linux:
    `apt install httpie`

On Window:
    `choco install httpie`

On macOS:
    `brew install httpie`

## Parameters Usage

- We will separate the APIs into three targets:
  1. **Blocks**: get the blocks from the Hive blockchain, which gets all of the transactions of blocks.
  2. **Posts**: get the posts we filtered from the transactions of the blocks.
  3. **Comments**: get the comments we filtered from the transactions of the blocks.

- The current version APIs would serve data of Hive mainnet from **March 27th, 2020** to **December 6th, 2021**. The duration is after [Steem Hard Fork](https://www.coindesk.com/steem-hard-fork-hive).

- The following parameters in bellow table will help the request be more specific.

| Parameter | Description | Default | Accepted Values | blocks | posts | comments | statistic |
|---|--------|---|---|---|---|---|---|
| size | Limit results of the request. A data sample might be large, especiallythe block samples. Users can set size for reducing runtime. | 25 | Interger |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| fields | Get fields in the schema. Not all fields would be useful, and it dependson individuals’ purposes. Users can add a list of fields for reducing runtime. | "*" | List of strings |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| witness | Filter data by the witnesses, sometimes is essential information for analyzing. | None | List of strings |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| ids | Filter data by the IDs of identified blocks. | None | List of strings |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| block_ids | Filter data by the hash of blocks which is similar to IDs, however, this isused to reference each other blocks in the database. | None | List of strings |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| operations | Filter by type of operations of the transactions in the blocks. | None | List of strings |  :heavy_check_mark: | - | - | - |
| after | Filter data after the time. The available begin time in our databaseis at 16:40:09 UTC on March 27th, 2020 for the early version. | None | UTC format or timestamp |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: | - |
| before | Filter data before the time. The available last time in our databaseis at 17:01:15 UTC on December 6th, 2021 for the early version. | None | UTC format or timestamp |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: | - |
| authors | Filter by the authors. If users are interested in some posts or comments,they can add a list of authors to search for more actions. | None | List of strings | - |  :heavy_check_mark: |  :heavy_check_mark: | - |
| permlink | Filter by "permlink" being a partition of posts or comments’ URL on Hivesocial network. Users can add a list of "permlinks" for reducing runtime. | None | List of strings | - |  :heavy_check_mark: |  :heavy_check_mark: | - |
| post_permlinks | Filter the comments in the posts having the "permlinks". | None | List of strings | - | - |  :heavy_check_mark: | - |
| words | Filter the posts or comments which contain the input words.This would help users catch some social network trends by searchingthe hot trending words. | None | List of strings | - |  :heavy_check_mark: |  :heavy_check_mark: | - |
| tags | Filter the posts which have the hashtags. This might help users search theposts more accurately than the words parameter. | None | List of strings | - |  :heavy_check_mark: | - | - |

## Examples of the API Calls

### Block APIs

<!-- GET: number of block (default 25)
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
``` -->

GET: blocks with specific fields
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by witnesses
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=5&fields=signing_key,transaction_ids,id,block_id,witness&witnesses=ausbitbank,pharesim,anyx" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by ids
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&ids=51314015,51314016" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by block_ids
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&block_ids=030efd5fe57e5fa7104b1186d7df6f00b39d3777,030efd60d0fbf6cca241f8be3577d3f680819c75" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks by operations
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&operations=comment_operation,comment_options_operation,vote_operation" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

**GET block by time can use both of UTC format and timestamp.**

GET: blocks since begin_time to end_time
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=2021-02-14T04:40:15&after=2021-02-14T04:40:12" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks after a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&after=2021-02-14T04:40:15" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: blocks before a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=1620171391" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```


### Comment APIs

<!-- GET: number of comments (default 25)
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
``` -->

GET: comment by witnesses
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&witnesses=ausbitbank,pharesim,anyx" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comment by the authors
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&authors=wilhb81,pl-travelfeed" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comments contain words
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&search=dish,aktywnym" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comments by permlink
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&permlinks=re-ptaku-qoi4z7,qoi4z2" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

**GET comments by time can use both of UTC format and timestamp.**

GET: comments since begin_time to end_time
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=2021-02-14T04:40:15&after=2021-02-14T04:40:12" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comments after a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&after=2021-02-14T04:40:15" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: comments before a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=1620171391" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

### Post APIs

<!-- GET: number of posts (default 25)
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
``` -->

GET: posts by the authors
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&authors=wilhb81,pl-travelfeed" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: posts contain words
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&search=covid" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: posts by permlink
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&permlinks=covid-drove-us-into-digitization-and-crypto-or-freewrite-weekend-16-05-21,qoi4z2" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

**GET posts by time can use both of UTC format and timestamp.**

GET: posts since begin_time to end_time
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=2021-05-24T04:40:15&after=2021-02-14T04:40:12" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: posts after a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&after=2021-02-14T04:40:15" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: posts before a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,witness&before=1620171391" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

### Statistics APIs

We also provide some APIs for statistics. You can modify size parameters on requests to limit the number of items. We limit the 10000 items as a default.

GET: the list of top users based on the number of posts.
```
http GET "sochaindb.com/hive-api/v1.0.0/top_posts?size=1000" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: the list of top users based on the number of comments.
```
http GET "sochaindb.com/hive-api/v1.0.0/top_comments?size=1000" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

GET: the list of contents of top posts.
```
http GET "sochaindb.com/hive-api/v1.0.0/top_words?size=1000" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc
```

## Appendix

You can get operation types from this [list](https://github.com/SOCHAINDB/hive-db/blob/master/assets/summary.org).

# Run a local service

- You also could pull the pre-built Docker image to run the Hive Data service on the local machine.

```
docker pull nguyenminh1807/hive-api:v1.0
```

- Then, you run the docker container.

```
docker run -it --rm -p 5000:5000 nguyenminh1807/hive-api:v1.0
```

- When you have run the local service by the docker image, you can request these APIs by replacing the endpoint *sochaindb.com* with *localhost:5000*.


# LICENSE

Shield: [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

The source code for the data service is licensed under the [MIT License](https://github.com/SOCHAINDB/hive-db/blob/master/LICENSE).

The dataset is licensed under the
[Creative Commons Attribution-ShareAlike 4.0 International License](https://github.com/SOCHAINDB/hive-db/blob/master/LICENSE-CC-BY-SA).

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

