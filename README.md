<br/>
<p align="center">
    <a href="http://sochaindb.com" target="blank_">
        <img  height="100" alt="HTTPie" src="./assets/cover.png" />
    </a>
 </p>
<br/>

<p align="center">
    <a href="https://www.python.org/" target="blank_"><img alt="python" src="https://img.shields.io/badge/python-3.6.15-green" /></a>
    <a href="https://img.shields.io/badge/falcon-3.0.1-yellowgreen" target="blank_"><img alt="falcon" src="https://img.shields.io/badge/falcon-3.0.1-yellowgreen" /></a>
    <a href="https://cloud.google.com/bigquery/" target="blank_"><img alt="bigquery" src="https://img.shields.io/badge/python-3.6.15-green" /></a>
    <a href="https://opensource.org/licenses/MIT" target="blank_"><img alt="mit" src="https://img.shields.io/badge/License-MIT-blue.svg" /></a>
    <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="blank_"><img alt="cc-by-sa" src="https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg" /></a>
</p>

# HIVE Data service
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

| Parameter | &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Descriptions&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Default | Accepted Values | blocks | posts | comments | statistic |
|---|--------|---|---|---|---|---|---|
| size | Limit the results size of a request. A data sample might be large, especially the block samples. Users can set size for reducing runtime. | 25 | Interger |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| [fields](https://github.com/SOCHAINDB/hive-db/blob/master/assets/fields.md) | Get fields in the schema. Not all fields are useful, and it depends on individuals' purposes. Users can add a list of fields for reducing runtime. | "*" | List of strings separated by comma |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| witnesses | Filter data by "witnesses." It sometimes is essential information for analyzing. | None | List of strings separated by comma |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| ids | Filter data by the identified blocks IDs. | None | List of strings separated by comma |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| block_ids | Filter data by the blocks hash, which is similar to IDs, however, this is used to reference each block in the database. | None | List of strings separated by comma |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: |
| [operations](https://github.com/SOCHAINDB/hive-db/blob/master/assets/summary.org#operation-types) | Filter by the operations type of the transactions in the blocks. | None | List of strings separated by comma |  :heavy_check_mark: | - | - | - |
| after | Filter data after a specified time. The first available time in our database is at 16:40:09 UTC on 27th March 2020 for the current version. | None | UTC format or timestamp |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: | - |
| before | Filter data before a specified time. The last available time in our database is at 23:59:57 UTC on January 31st, 2022 for the current version. | None | UTC format or timestamp |  :heavy_check_mark: |  :heavy_check_mark: |  :heavy_check_mark: | - |
| authors | Filter by the authors. If users are interested in some posts or comments, they can add a list of authors to search for more actions. | None | List of strings separated by comma | - |  :heavy_check_mark: |  :heavy_check_mark: | - |
| permlinks | Filter by "permlink" being a partition of posts or comments' URL on Hive social network. Users can add a list of "permlinks" for reducing runtime. | None | List of strings separated by comma | - |  :heavy_check_mark: |  :heavy_check_mark: | - |
| post_permlinks | Filter the comments in the posts having the "permlinks." | None | List of strings separated by comma | - | - |  :heavy_check_mark: | - |
| words | Filter the posts or comments which contain the specified input words. This could help users catch some social network trends by searching the hot trending words. | None | List of strings separated by comma | - |  :heavy_check_mark: |  :heavy_check_mark: | - |
| tags | Filter the posts which contain the specified hashtags. This might help users search the posts more accurately than the words parameter. | None | List of strings separated by comma | - |  :heavy_check_mark: | - | - |

## Examples of the API Calls

### Block APIs


GET: blocks with specific fields. You can get list of supported fields in this [list](https://github.com/SOCHAINDB/hive-db/blob/master/assets/fields.md).
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: blocks by witnesses
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=5&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&witnesses=ausbitbank,pharesim,anyx" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: blocks by ids
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&ids=51314015,51314016" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: blocks by block_ids
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&block_ids=030efd5fe57e5fa7104b1186d7df6f00b39d3777,030efd60d0fbf6cca241f8be3577d3f680819c75" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: blocks by operations
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&operations=comment_operation,comment_options_operation,vote_operation" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

**GET block by time can use both of UTC format and timestamp.**

GET: blocks since begin_time to end_time
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&before=2021-02-14T04:40:15&after=2021-02-14T04:40:12" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: blocks after a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&after=2021-02-14T04:40:15" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: blocks before a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/blocks?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&before=1620171391" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```


### Comment APIs


GET: comment by witnesses
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&witnesses=ausbitbank,pharesim,anyx" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: comment by the authors
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&authors=wilhb81,pl-travelfeed" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: comments contain words
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&search=dish,covid" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: comments by permlink
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&permlinks=re-ptaku-qoi4z7,qoi4z2" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

**GET comments by time can use both of UTC format and timestamp.**

GET: comments since begin_time to end_time
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&before=2021-02-14T04:40:15&after=2021-02-14T04:40:12" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: comments after a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&after=2021-02-14T04:40:15" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: comments before a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/comments?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&before=1620171391" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

### Post APIs


GET: posts by the authors
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&authors=wilhb81,pl-travelfeed" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: posts contain words
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&search=covid" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: posts by permlink
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&permlinks=covid-drove-us-into-digitization-and-crypto-or-freewrite-weekend-16-05-21,qoi4z2" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

**GET posts by time can use both of UTC format and timestamp.**

GET: posts since begin_time to end_time
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&before=2021-05-24T04:40:15&after=2021-02-14T04:40:12" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: posts after a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&after=2021-02-14T04:40:15" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: posts before a specific date
```
http GET "sochaindb.com/hive-api/v1.0.0/posts?size=3&fields=signing_key,transaction_ids,id,block_id,operations.value.author,operations.value.expiration,operations.value.parent_permlink,operations.value.body&before=1620171391" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

### Statistics APIs

We also provide some APIs for statistics. You can modify size parameters on requests to limit the number of items. We limit the 10000 items as a default.

GET: the list of top users based on the number of posts.
```
http GET "sochaindb.com/hive-api/v1.0.0/top_posts?size=1000" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: the list of top users based on the number of comments.
```
http GET "sochaindb.com/hive-api/v1.0.0/top_comments?size=1000" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

GET: the list of contents of top posts.
```
http GET "sochaindb.com/hive-api/v1.0.0/top_words?size=1000" TOKEN:WrrXP6szu06wlLQVfAM3b0FD8i4612zc --timeout 540
```

## Appendix

- You can get operation types from this [list](https://github.com/SOCHAINDB/hive-db/blob/master/assets/summary.org#operation-types).
- [List of supported fields](https://github.com/SOCHAINDB/hive-db/blob/master/assets/fields.md).


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

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

