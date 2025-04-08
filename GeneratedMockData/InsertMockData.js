use DB_PlayerData

// Mock GridFS files for sprites
db.sprites.files.insertMany([
  { _id: ObjectId("661000000000000000000001"), filename: "hero_walk.png", length: 20, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000002"), filename: "enemy_fly.png", length: 18, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000003"), filename: "platform_tile.png", length: 22, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000004"), filename: "boss_roar.png", length: 25, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000005"), filename: "coin_spin.png", length: 19, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000006"), filename: "door_open.png", length: 21, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000007"), filename: "trap_spike.png", length: 23, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000008"), filename: "fireball_cast.png", length: 26, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000009"), filename: "shield_block.png", length: 24, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("66100000000000000000000a"), filename: "npc_villager.png", length: 22, chunkSize: 261120, uploadDate: new Date() }
])

// Corresponding chunks for each sprite (1 chunk per file for simplicity)
db.sprites.chunks.insertMany([
  { files_id: ObjectId("661000000000000000000001"), n: 0, data: BinData(0, "aGVybyB3YWxrIGRhdGE=") },
  { files_id: ObjectId("661000000000000000000002"), n: 0, data: BinData(0, "ZW5lbXkgZmx5IGRhdGE=") },
  { files_id: ObjectId("661000000000000000000003"), n: 0, data: BinData(0, "cGxhdGZvcm0gdGlsZSBkYXRh") },
  { files_id: ObjectId("661000000000000000000004"), n: 0, data: BinData(0, "Ym9zcyByb2FyIGRhdGE=") },
  { files_id: ObjectId("661000000000000000000005"), n: 0, data: BinData(0, "Y29pbiBzcGluIGRhdGE=") },
  { files_id: ObjectId("661000000000000000000006"), n: 0, data: BinData(0, "ZG9vciBvcGVuIGRhdGE=") },
  { files_id: ObjectId("661000000000000000000007"), n: 0, data: BinData(0, "dHJhcCBzcGlrZSBkYXRh") },
  { files_id: ObjectId("661000000000000000000008"), n: 0, data: BinData(0, "ZmlyZWJhbGwgY2FzdCBkYXRh") },
  { files_id: ObjectId("661000000000000000000009"), n: 0, data: BinData(0, "c2hpZWxkIGJsb2NrIGRhdGE=") },
  { files_id: ObjectId("66100000000000000000000a"), n: 0, data: BinData(0, "bnBjIHZpbGxhZ2VyIGRhdGE=") }
])

// Mock GridFS files for audio
db.audio.files.insertMany([
  { _id: ObjectId("66100000000000000000000b"), filename: "main_theme.mp3", length: 1234, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("66100000000000000000000c"), filename: "battle_theme.mp3", length: 1150, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("66100000000000000000000d"), filename: "victory_jingle.mp3", length: 980, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("66100000000000000000000e"), filename: "loss_theme.mp3", length: 1020, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("66100000000000000000000f"), filename: "menu_click.wav", length: 880, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000010"), filename: "jump.wav", length: 640, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000011"), filename: "coin_collect.wav", length: 740, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000012"), filename: "door_open.wav", length: 710, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000013"), filename: "explosion.wav", length: 910, chunkSize: 261120, uploadDate: new Date() },
  { _id: ObjectId("661000000000000000000014"), filename: "ambient_forest.mp3", length: 1100, chunkSize: 261120, uploadDate: new Date() }
])

// Corresponding chunks for audio (1 chunk each for simplicity)
db.audio.chunks.insertMany([
  { files_id: ObjectId("66100000000000000000000b"), n: 0, data: BinData(0, "bWFpbiB0aGVtZSBhdWRpbyBkYXRh") },
  { files_id: ObjectId("66100000000000000000000c"), n: 0, data: BinData(0, "YmF0dGxlIHRoZW1lIGF1ZGlvIGRhdGE=") },
  { files_id: ObjectId("66100000000000000000000d"), n: 0, data: BinData(0, "dmljdG9yeSBqdW5nbGUgZGF0YQ==") },
  { files_id: ObjectId("66100000000000000000000e"), n: 0, data: BinData(0, "bG9zcyB0aGVtZSBhdWRpbyBkYXRh") },
  { files_id: ObjectId("66100000000000000000000f"), n: 0, data: BinData(0, "bWVudSBjbGljayBzb3VuZCBiZWVw") },
  { files_id: ObjectId("661000000000000000000010"), n: 0, data: BinData(0, "anVtcCBzb3VuZCBhdWRpbw==") },
  { files_id: ObjectId("661000000000000000000011"), n: 0, data: BinData(0, "Y29pbiBjb2xsZWN0IHNvdW5kIGJpcA==") },
  { files_id: ObjectId("661000000000000000000012"), n: 0, data: BinData(0, "ZG9vciBvcGVuIGF1ZGlvIGRhdGE=") },
  { files_id: ObjectId("661000000000000000000013"), n: 0, data: BinData(0, "ZXhwbG9zaW9uIHNvdW5kIGVmZmVjdA==") },
  { files_id: ObjectId("661000000000000000000014"), n: 0, data: BinData(0, "Zm9yZXN0IGFtYmllbnQgdHJhY2s=") }
])


db.scores.insertMany([
  { "player_name": "player_001", "score": 1500 },
  { "player_name": "player_002", "score": 2450 },
  { "player_name": "player_003", "score": 3200 },
  { "player_name": "player_004", "score": 2100 },
  { "player_name": "player_005", "score": 1200 },
  { "player_name": "player_006", "score": 4000 },
  { "player_name": "player_007", "score": 900 },
  { "player_name": "player_008", "score": 1980 },
  { "player_name": "player_009", "score": 3700 },
  { "player_name": "player_010", "score": 1600 }
])

db.sprites.files.find().pretty()
db.sprites.chunks.find().pretty()
db.audio.files.find().pretty()
db.audio.chunks.find().pretty()
db.scores.find().pretty()

//db.audio.chunks.drop()
//db.audio.files.drop()
//db.sprites.chunks.drop()
//db.sprites.files.drop()
//db.scores.drop()