require 'json'
require 'rapgenius'

SAVE_DIRECTORY = '../../data/rapgenius'
# ARTISTS = [
#   'Jay-Z',
#   'Kendrick Lamar',
#   'Psy'
# ]
FROZEN_SONG_IDS = [
  378398,
  355884,
  353400,
  345497,
  352918,
  378424,
  358333,
  360588,
  378449,
  243465,
  378400,
  378904
]

def get_lyrics(id)
  lyrics = Array.new

  track = RapGenius::Song.find id
  lines = track.lines
  lines.each do |line|
    lyrics.push line.lyric
  end

  lyrics
end


lyrics = Hash.new

FROZEN_SONG_IDS.each do |id|
  lyrics[id] = get_lyrics id
end

puts lyrics
Dir.mkdir(SAVE_DIRECTORY) unless Dir.exist?(SAVE_DIRECTORY)
File.open("#{SAVE_DIRECTORY}/frozen.json", 'w') do |f|
  f.write(lyrics.to_json)
end
