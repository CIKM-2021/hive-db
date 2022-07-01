# Dataset SQL Queries

## Social media Queries

### Growth of active users per month
``` sql
WITH
  first_account_transactions AS (
  SELECT
    IFNULL(o.value.required_auths[SAFE_OFFSET(0)],
      o.value.required_posting_auths[SAFE_OFFSET(0)]) AS account_name,
    MIN(timestamp) AS transaction_time
  FROM
    `steemit-307308.hive_zurich.block_data_*`
  CROSS JOIN
    UNNEST(transactions) AS t
  CROSS JOIN
    UNNEST(t.operations) AS o
  GROUP BY
    account_name),
  transacting_counts AS (
  SELECT
    DATE_TRUNC(transaction_time, MONTH) AS month,
    COUNT(account_name) AS new_first_transacting
  FROM
    first_account_transactions
  GROUP BY
    month)
SELECT
  month,
  new_first_transacting,
  SUM(new_first_transacting) OVER (ORDER BY month ASC) AS new_transacting_count
FROM
  transacting_counts
ORDER BY
  month ASC
```

### Amount of users created per month

``` sql
SELECT DATE_TRUNC(timestamp, MONTH) AS signup_month, COUNT(o) AS amount
FROM `steemit-307308.hive_zurich.block_data_*`
CROSS JOIN UNNEST(transactions) as t
CROSS JOIN UNNEST(t.operations) as o
WHERE (o.type = "account_create_operation" OR o.type = "account_create_with_delegation_operation" OR o.type = "create_claimed_account_operation")
  AND NOT REGEXP_CONTAINS(o.value.new_account_name, "^hive-")
GROUP BY signup_month
ORDER BY signup_month ASC
```

### Accounts that are active after fork

``` sql
SELECT
  DISTINCT IFNULL(o.value.required_auths[SAFE_OFFSET(0)],
    o.value.required_posting_auths[SAFE_OFFSET(0)]) AS account
FROM
  `steemit-307308.hive_zurich.block_data_*`
CROSS JOIN
  UNNEST(transactions) AS t
CROSS JOIN
  UNNEST(t.operations) AS o
WHERE
  timestamp > TIMESTAMP("2020-03-20 14:00:00")
```

### User profiles

``` sql
WITH
  account_updates AS (
  SELECT
    o.value.json_metadata_dict.profile_dict AS profile,
    o.value.account AS account,
    timestamp AS datetime
  FROM
    `steemit-307308.hive_zurich.block_data_*`
  CROSS JOIN
    UNNEST(transactions) AS t
  CROSS JOIN
    UNNEST(t.operations) AS o
  WHERE
    o.type = "account_update_operation"
    AND o.value.json_metadata_dict.profile_dict IS NOT NULL)
SELECT
  latest.profile.about_str AS about,
  latest.profile.cover_image_str AS cover_image,
  latest.profile.dtube_pub_str AS dtube_pub,
  latest.profile.location_str AS location,
  latest.profile.name_str AS name,
  latest.profile.profile_image_str AS profile_image,
  latest.profile.website_str AS website,
  latest.account AS account
FROM (
  SELECT
    ARRAY_AGG(account_updates
    ORDER BY
      datetime DESC
    LIMIT
      1)[
  OFFSET
    (0)] AS latest
  FROM
    account_updates
  GROUP BY
    account)
```

### Current user subscriptions

``` sql
WITH
  subs AS (
  SELECT
    o.value.json_list_dict[
  OFFSET
    (1)].value_dict.community_str AS community,
    IFNULL(o.value.required_posting_auths[SAFE_OFFSET(0)],
      o.value.required_auths[SAFE_OFFSET(0)]) AS auth,
    timestamp AS datetime
  FROM
    `steemit-307308.hive_zurich.block_data_*`
  CROSS JOIN
    UNNEST(transactions) AS t
  CROSS JOIN
    UNNEST(t.operations) AS o
  WHERE
    o.type = "custom_json_operation"
    AND o.value.id = "community"
    AND o.value.json_list_dict[SAFE_OFFSET(0)].value_str = "subscribe"),
  unsubs AS (
  SELECT
    o.value.json_list_dict[
  OFFSET
    (1)].value_dict.community_str AS community,
    IFNULL(o.value.required_posting_auths[SAFE_OFFSET(0)],
      o.value.required_auths[SAFE_OFFSET(0)]) AS auth,
    timestamp AS datetime
  FROM
    `steemit-307308.hive_zurich.block_data_*`
  CROSS JOIN
    UNNEST(transactions) AS t
  CROSS JOIN
    UNNEST(t.operations) AS o
  WHERE
    o.type = "custom_json_operation"
    AND o.value.id = "community"
    AND o.value.json_list_dict[SAFE_OFFSET(0)].value_str = "unsubscribe")
SELECT
  subs.community,
  subs.auth,
  subs.datetime
FROM
  subs
LEFT JOIN
  unsubs
ON
  subs.community = unsubs.community
  AND subs.auth = unsubs.auth
  AND unsubs.datetime > subs.datetime
WHERE
  unsubs.auth IS NULL
```

### Current user follow state

``` sql
WITH
  # follow operations of users
  follow_operations AS (
  SELECT
    o.value.json_list_dict[
  OFFSET
    (1)].value_dict.follower_str AS follower,
    o.value.json_list_dict[
  OFFSET
    (1)].value_dict.following_str AS follow,
    w AS follow_type,
    timestamp
  FROM
    `steemit-307308.hive_zurich.block_data_*`
  CROSS JOIN
    UNNEST(transactions) AS t
  CROSS JOIN
    UNNEST(t.operations) AS o
  CROSS JOIN
    UNNEST(o.value.json_list_dict) AS j
  CROSS JOIN
    UNNEST(j.value_dict.what_list_str) AS w
  WHERE
    o.type = "custom_json_operation"
    AND o.value.id = "follow"
    AND o.value.json_list_dict[SAFE_OFFSET(0)].value_str = "follow"
    AND w IN UNNEST(["blog", "blacklist", "unblacklist", "follow_blacklist", "unfollow_blacklist", "reset_follow_blacklist", "reset_blacklist", "ignore", "follow_muted", "follow_muted_list", "unfollow_muted", "unfollow_muted_list", "reset_mute_list", "reset_follow_muted_list", "reset_all_lists", "[]"])),
  follow_latest AS (
  SELECT
    latest.*
  FROM (
    SELECT
      ARRAY_AGG(follow_operations
      ORDER BY
        timestamp DESC
      LIMIT
        1)[
    OFFSET
      (0)] AS latest
    FROM
      follow_operations
    WHERE
      follow_type = "blog"
      OR follow_type = "ignore"
    GROUP BY
      follower,
      follow,
      follow_type)),
  # unfollows and unmutes
  follow_operations_split AS (
  SELECT
    fo.follower,
    fo.follow,
  IF
    (fl.follow_type = "blog",
      "unfollow",
      "unmute") AS follow_type,
    fo.timestamp
  FROM
    follow_operations AS fo
  JOIN
    follow_latest AS fl
  ON
    fo.follower = fl.follower
    AND fo.follow = fl.follow
    AND fo.timestamp > fl.timestamp
  WHERE
    fo.follow_type = "[]"),
  # unfollow operations of users
  separate_unfollow_operations AS (
  SELECT
    o.value.json_list_dict[
  OFFSET
    (1)].value_dict.follower_str AS follower,
    o.value.json_list_dict[
  OFFSET
    (1)].value_dict.following_str AS follow,
    "unfollow" AS follow_type,
    timestamp
  FROM
    `steemit-307308.hive_zurich.block_data_*`
  CROSS JOIN
    UNNEST(transactions) AS t
  CROSS JOIN
    UNNEST(t.operations) AS o
  CROSS JOIN
    UNNEST(o.value.json_list_dict) AS j
  CROSS JOIN
    UNNEST(j.value_dict.what_list_str) AS w
  WHERE
    o.type = "custom_json_operation"
    AND o.value.id = "unfollow"
    AND w = "blog"),
  # all operations
  processed_follow_operations AS (
  SELECT
    follower,
    follow,
    timestamp,
    follow_type
  FROM ((
      SELECT
        *
      FROM
        separate_unfollow_operations)
    UNION ALL ((
        SELECT
          *
        FROM
          follow_operations_split)
      UNION ALL (
        SELECT
          *
        FROM
          follow_operations
        WHERE
          follow_type != "[]")))),
  # blacklist resets
  follow_reset_blacklist AS (
  SELECT
    follower,
    follow,
    timestamp
  FROM
    processed_follow_operations
  WHERE
    follow_type = "reset_blacklist"
    OR follow_type = "reset_all_lists"
  ORDER BY
    timestamp
  LIMIT
    1),
  # mute list resets
  follow_reset_mute_list AS (
  SELECT
    follower,
    follow,
    timestamp
  FROM
    processed_follow_operations
  WHERE
    follow_type = "reset_mute_list"
    OR follow_type = "reset_all_lists"
  ORDER BY
    timestamp
  LIMIT
    1),
  # follow blacklist resets
  follow_reset_follow_blacklist AS (
  SELECT
    follower,
    follow,
    timestamp
  FROM
    processed_follow_operations
  WHERE
    follow_type = "reset_follow_blacklist"
    OR follow_type = "reset_all_lists"
  ORDER BY
    timestamp
  LIMIT
    1),
  # follow mute list resets
  follow_reset_follow_mute_list AS (
  SELECT
    follower,
    follow,
    timestamp
  FROM
    processed_follow_operations
  WHERE
    follow_type = "reset_follow_muted_list"
    OR follow_type = "reset_all_lists"
  ORDER BY
    timestamp
  LIMIT
    1),
  # remove reset operations
  follow_operations_remove_reset AS (
  SELECT
    follower,
    follow,
    timestamp,
    follow_type
  FROM
    processed_follow_operations
  WHERE
    NOT REGEXP_CONTAINS(follow_type, "^reset") ),
  # remove blacklist operations before reset
  follow_operations_blacklist_reset AS (
  SELECT
    fo.follower,
    fo.follow,
    fo.timestamp,
    fo.follow_type
  FROM
    follow_operations_remove_reset AS fo
  LEFT JOIN
    follow_reset_blacklist AS frb
  ON
    fo.follow = frb.follow
    AND fo.follower = frb.follower
  WHERE
    NOT (fo.timestamp < frb.timestamp
      AND fo.follow_type IN UNNEST(["blacklist", "unblacklist"])) ),
  # remove ignore operations before reset
  follow_operations_mute_reset AS (
  SELECT
    fo.follower,
    fo.follow,
    fo.timestamp,
    fo.follow_type
  FROM
    follow_operations_remove_reset AS fo
  LEFT JOIN
    follow_reset_mute_list AS frml
  ON
    fo.follow = frml.follow
    AND fo.follower = frml.follower
  WHERE
    NOT (fo.timestamp < frml.timestamp
      AND fo.follow_type IN UNNEST(["ignore", "unmute"])) ),
  # remove follow blacklist operations before reset
  follow_operations_follow_blacklist_reset AS (
  SELECT
    fo.follower,
    fo.follow,
    fo.timestamp,
    fo.follow_type
  FROM
    follow_operations_mute_reset AS fo
  LEFT JOIN
    follow_reset_follow_blacklist AS frfb
  ON
    fo.follow = frfb.follow
    AND fo.follower = frfb.follower
  WHERE
    NOT (fo.timestamp < frfb.timestamp
      AND fo.follow_type IN UNNEST(["follow_blacklist", "unfollow_blacklist"])) ),
  # remove follow mutelist operations before reset
  follow_operations_follow_mutelist_reset AS (
  SELECT
    fo.follower,
    fo.follow,
    fo.timestamp,
    fo.follow_type
  FROM
    follow_operations_follow_blacklist_reset AS fo
  LEFT JOIN
    follow_reset_follow_mute_list AS frfml
  ON
    fo.follow = frfml.follow
    AND fo.follower = frfml.follower
  WHERE
    NOT (fo.timestamp < frfml.timestamp
      AND fo.follow_type IN UNNEST(["follow_muted_list", "unfollow_muted_list"])) ),
  opposite_types AS (
  SELECT
    types,
    opposites
  FROM (
    SELECT
      types,
      off
    FROM
      UNNEST(["blog", "blacklist", "unblacklist", "follow_blacklist", "unfollow_blacklist", "ignore", "follow_muted", "follow_muted_list", "unfollow_muted", "unfollow_muted_list", "unfollow", "unmute"]) AS types
    WITH
    OFFSET
      AS off ) AS a
  JOIN (
    SELECT
      opposites,
      off
    FROM
      UNNEST(["unfollow", "unblacklist", "blacklist", "unfollow_blacklist", "follow_blacklist", "unmute", "unfollow_muted", "unfollow_muted_list", "follow_muted", "follow_muted_list", "blog", "ignore"]) AS opposites
    WITH
    OFFSET
      AS off ) AS b
  ON
    a. off = b. off ),
  head_operations AS (
  SELECT
    fi.follow,
    fi.follower,
    fi.follow_type,
    fi.timestamp
  FROM
    follow_operations_follow_mutelist_reset AS fi
  LEFT JOIN
    opposite_types
  ON
    fi.follow_type = types
  LEFT JOIN
    follow_operations_follow_mutelist_reset AS fo
  ON
    fi.follow = fo.follow
    AND fi.follower = fo.follower
    AND fo.follow_type = opposites
    AND fo.timestamp > fi.timestamp
  WHERE
    fo.follow IS NULL)
SELECT
  follow,
  follower,
  follow_type,
  timestamp
FROM
  head_operations
JOIN
  UNNEST(["blog", "blacklist", "follow_blacklist", "ignore", "follow_muted", "follow_muted_list"]) AS types
ON
  follow_type = types
```

### Comment and comment edit amount

``` sql
WITH
  comments AS (
  SELECT
    o,
    timestamp
  FROM
    `steemit-307308.hive_zurich.block_data_*`
  CROSS JOIN
    UNNEST(transactions) AS t
  CROSS JOIN
    UNNEST(t.operations) AS o
  WHERE
    (o.value.title = ""
      OR o.value.title IS NULL)
    AND o.value.parent_author IS NOT NULL
    AND o.value.parent_permlink IS NOT NULL
    AND timestamp > TIMESTAMP("2020-03-20 14:00:00")),
  unique_comment_dates AS (
  SELECT
    MIN(comments.timestamp) AS comment_timestamp,
    comments.o.value.author AS author,
    comments.o.value.permlink AS permlink
  FROM
    comments
  GROUP BY
    author,
    permlink),
  unique_comment_count AS (
  SELECT
    COUNT(unique_comment_dates.permlink) AS unique_comment_amount,
    DATE_TRUNC(unique_comment_dates.comment_timestamp, MONTH) AS unique_comment_month
  FROM
    unique_comment_dates
  GROUP BY
    unique_comment_month),
  comment_count AS (
  SELECT
    COUNT(comments.o.value.permlink) AS comment_amount,
    DATE_TRUNC(comments.timestamp, MONTH) AS comment_month
  FROM
    comments
  GROUP BY
    comment_month)
SELECT
  unique_comment_count.unique_comment_amount AS comment_amount,
  comment_count.comment_amount - unique_comment_count.unique_comment_amount AS comment_edit_amount,
  comment_count.comment_month AS month
FROM
  comment_count
JOIN
  unique_comment_count
ON
  comment_count.comment_month = unique_comment_count.unique_comment_month
ORDER BY month ASC
```

### Posts

``` sql
SELECT DATE_TRUNC(timestamp, MONTH) AS signup_month, COUNT(o.value.body) AS post_amount
FROM `steemit-307308.hive_zurich.block_data_*`
CROSS JOIN UNNEST(transactions) as t
CROSS JOIN UNNEST(t.operations) as o
WHERE o.value.body IS NOT NULL AND o.value.title != "" AND o.value.title IS NOT NULL AND timestamp > TIMESTAMP("2020-03-20 14:00:00")
GROUP BY signup_month
ORDER BY signup_month ASC
```

### Tag count

``` sql
SELECT COUNT(t) AS tag_count
FROM `steemit-307308.hive_zurich.block_data_*`,
    UNNEST (transactions) AS transaction_unnest,
    UNNEST (transaction_unnest.operations) AS operations_unnest,
    UNNEST (operations_unnest.value.json_metadata_dict.tags_list_str) AS t
WHERE 
    timestamp > TIMESTAMP("2020-03-20 14:00:00")
    AND operations_unnest.value.title != ""
    AND t IS NOT NULL
```

### Upvote/downvote count

``` sql
SELECT COUNTIF(o.value.weight > 0) AS upvotes, COUNTIF(o.value.weight < 0) AS downvotes
FROM `steemit-307308.hive_zurich.block_data_*`
CROSS JOIN UNNEST(transactions) as t
CROSS JOIN UNNEST(t.operations) as o
WHERE o.type = "vote_operation"
    AND timestamp > TIMESTAMP("2020-03-20 14:00:00")
```

### Communities created per month

``` sql
SELECT DATE_TRUNC(timestamp, MONTH) AS signup_month, COUNT(o) AS amount
FROM `steemit-307308.hive_zurich.block_data_*`
CROSS JOIN UNNEST(transactions) as t
CROSS JOIN UNNEST(t.operations) as o
WHERE o.type = "account_create_operation" AND REGEXP_CONTAINS(o.value.new_account_name, "hive-")
GROUP BY signup_month
ORDER BY signup_month ASC
```

## Rewards claimed per month

``` sql
WITH
  claimed_over_month AS (
  SELECT
    DATE_TRUNC(timestamp, MONTH) AS reward_month,
    SUM(CAST(o.value.reward_hbd.amount AS INT64) / POW(10, o.value.reward_hbd.precision)) AS claimed_hbd,
    SUM(CAST(o.value.reward_hive.amount AS INT64) / POW(10, o.value.reward_hive.precision)) AS claimed_hive,
    SUM(CAST(o.value.reward_vests.amount AS INT64) / POW(10, o.value.reward_vests.precision)) AS claimed_vests
  FROM
    `steemit-307308.hive_zurich.block_data_*`
  CROSS JOIN
    UNNEST(transactions) AS t
  CROSS JOIN
    UNNEST(t.operations) AS o
  WHERE
    o.type = "claim_reward_balance_operation"
    AND timestamp > TIMESTAMP("2020-03-20 14:00:00")
  GROUP BY
    reward_month)
SELECT
  reward_month,
  SUM(claimed_hbd) OVER (ORDER BY reward_month) AS claimed_hbd,
  SUM(claimed_hive) OVER (ORDER BY reward_month) AS claimed_hive,
  SUM(claimed_vests) OVER (ORDER BY reward_month) AS claimed_vests
FROM
  claimed_over_month
ORDER BY
  reward_month
```

## NFTShowroom

### Amount of tokens minted and amount of arts

``` sql
SELECT SUM(CAST(JSON_VALUE(o.value.json_dict.contractpayload_dict.memo_str, "$.tokens") AS INT64)) AS tokens_minted, COUNT(o.value.json_dict.contractpayload_dict.memo_str) AS arts_amount
FROM
  `steemit-307308.hive_zurich.block_data_*`
CROSS JOIN
  UNNEST(transactions) AS t
CROSS JOIN
  UNNEST(t.operations) AS o
WHERE
  o.value.id = "ssc-mainnet-hive"
  AND o.value.json_dict.contractaction_str = "transfer"
  AND o.value.json_dict.contractname_str = "tokens"
  AND o.value.json_dict.contractpayload_dict.to_str = "nftshowroom"
  # o.value.json_dict.contractpayload_dict.memo_str AS memo
```

### Amount of art bought

``` sql
WITH nft_list AS (SELECT o.value.json_dict.contractpayload_dict.nfts_list_str AS ls
FROM
  `steemit-307308.hive_zurich.block_data_*`
CROSS JOIN
  UNNEST(transactions) AS t
CROSS JOIN
  UNNEST(t.operations) AS o
WHERE
  o.value.id = "ssc-mainnet-hive"
  AND o.value.json_dict.contractaction_str = "buy"
  AND o.value.json_dict.contractname_str = "nftmarket"
  AND o.value.json_dict.contractpayload_dict.marketaccount_str = "nftshowroom")
SELECT COUNT(sn) AS nn
FROM nft_list AS n,
UNNEST(n.ls) AS sn
  # COUNT(o.value.json_dict.contractpayload_dict.nfts_list_str)
```
