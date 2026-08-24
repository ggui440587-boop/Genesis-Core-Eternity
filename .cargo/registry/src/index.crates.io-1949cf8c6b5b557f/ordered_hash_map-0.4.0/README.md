# OrderedHashMap

A HashMap (and Set) which preserves insertion order.

This crate provides a no\_std implementation of a Ordered Hash Map (and it's corresponding Set) using as little unsafe as possible. [MIRI](https://github.com/rust-lang/miri) is used to audit the unsafe which does exist.

The API aims to match the standard library HashMap/Set with additional LinkedList style methods and ordered-itertors.

## [Changelog](CHANGELOG.md)

## Details

This crate is powered by [hashbrown](https://github.com/rust-lang/hashbrown), leveraging the already well vetted HashMap implementation and added the bits required to implement a LinkedList within the map. The additional memory footprint of the OrderedHashMap over the hashbrown HashMap is 2 pointers upon making a collection + 3 pointers per element. The pointers arise from the LinkedList where the collection itself has a pointer to the head and the tail, each node has a pointer to the next and previous node, and the Key in the map is a pointer into the Value where it lives.

## Features
`serde` - Enable serde Serialization and Deserialization

## Usage
```rust
use ordered_hash_map::OrderedHashMap;

let mut map: OrderedHashMap<_, _> = [(1, "one"), (2, "two")].into_iter().collect();
map.insert(3, "three");
assert_eq!(map.iter().next(), Some((&1, &"one")));
```
