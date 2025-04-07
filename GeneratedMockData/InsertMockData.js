use DB_PlayerData


db.sprites.insertMany([
  { "sprite_id": "sprite_001", "filename": "hero_walk.png", "file_id": "gridfs1" },
  { "sprite_id": "sprite_002", "filename": "enemy_fly.png", "file_id": "gridfs2" },
  { "sprite_id": "sprite_003", "filename": "platform_tile.png", "file_id": "gridfs3" },
  { "sprite_id": "sprite_004", "filename": "boss_roar.png", "file_id": "gridfs4" },
  { "sprite_id": "sprite_005", "filename": "coin_spin.png", "file_id": "gridfs5" },
  { "sprite_id": "sprite_006", "filename": "door_open.png", "file_id": "gridfs6" },
  { "sprite_id": "sprite_007", "filename": "trap_spike.png", "file_id": "gridfs7" },
  { "sprite_id": "sprite_008", "filename": "fireball_cast.png", "file_id": "gridfs8" },
  { "sprite_id": "sprite_009", "filename": "shield_block.png", "file_id": "gridfs9" },
  { "sprite_id": "sprite_010", "filename": "npc_villager.png", "file_id": "gridfs10" }
])

db.audio.insertMany([
  { "audio_id": "audio_001", "filename": "main_theme.mp3", "file_id": "gridfs11" },
  { "audio_id": "audio_002", "filename": "battle_theme.mp3", "file_id": "gridfs12" },
  { "audio_id": "audio_003", "filename": "victory_jingle.mp3", "file_id": "gridfs13" },
  { "audio_id": "audio_004", "filename": "loss_theme.mp3", "file_id": "gridfs14" },
  { "audio_id": "audio_005", "filename": "menu_click.wav", "file_id": "gridfs15" },
  { "audio_id": "audio_006", "filename": "jump.wav", "file_id": "gridfs16" },
  { "audio_id": "audio_007", "filename": "coin_collect.wav", "file_id": "gridfs17" },
  { "audio_id": "audio_008", "filename": "door_open.wav", "file_id": "gridfs18" },
  { "audio_id": "audio_009", "filename": "explosion.wav", "file_id": "gridfs19" },
  { "audio_id": "audio_010", "filename": "ambient_forest.mp3", "file_id": "gridfs20" }
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


db.sprites.find().pretty()
db.audio.find().pretty()
db.scores.find().pretty()


//db.sprites.drop()
//db.audio.drop()
//db.scores.drop()
