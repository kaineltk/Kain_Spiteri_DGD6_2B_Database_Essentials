use DB_PlayerData

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

//INSERT AUDIO AND SCORES MANUALY FROM JSON FILES

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