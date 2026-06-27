# Follow-up — S3-like Object Store

**Mirrors:** Problem 17 (hierarchical/prefix structure, path resolution, Composite-ish) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design an in-memory object store like Amazon S3: objects live in **buckets** under flat string **keys**; support prefix listing, metadata, and object **versioning**.

## Functional requirements
1. **Buckets**: `create_bucket(name)`, `delete_bucket(name)` (empty only, unless force), `list_buckets()`.
2. **Objects**: `put(bucket, key, data, metadata)`, `get(bucket, key) -> (data, metadata)`, `delete(bucket, key)`. Keys are flat strings but may contain `/` (virtual folders).
3. **Prefix listing**: `list(bucket, prefix, delimiter='/')` — returns matching keys, and when a delimiter is given, **rolls up** common prefixes into "folders" (S3 `CommonPrefixes` behavior).
4. **Versioning** (toggle per bucket): each `put` to an existing key creates a new **version**; `get` returns the latest; `get(bucket, key, version_id)` returns a specific version; `delete` adds a delete-marker (and can be undone).
5. Metadata: size, content-type, last-modified (injectable clock), etag/version id.
6. (Bonus) simple object-key **copy** and a `list` pagination (continuation token).

## Non-functional / constraints
- Prefix queries should not scan all objects across all buckets — index per bucket (e.g. sorted keys + range scan).
- Versioning storage is layered cleanly; non-versioned buckets behave like simple overwrite.
- Clear errors: no-such-bucket/key, bucket-not-empty, version-not-found.
- (Bonus) thread-safety for concurrent puts/gets.

## Driver scenario
1. Create bucket "photos" (versioning on).
2. `put("photos","2024/jan/a.jpg",...)`, `put("photos","2024/feb/b.jpg",...)`, `put("photos","2024/jan/a.jpg",...)` (new version).
3. `list("photos","2024/", delimiter="/")` → CommonPrefixes `["2024/jan/","2024/feb/"]`.
4. `get("photos","2024/jan/a.jpg")` → latest; then get an older version id.
5. `delete` the key → delete-marker; `get` → not found; show version history still has both versions.

## Edge cases
- Delete a non-empty bucket. · Get a missing key/version. · Prefix with no matches. · Delimiter rollup with nested "folders". · Overwrite in a non-versioned bucket. · Delete-marker then get specific version.
