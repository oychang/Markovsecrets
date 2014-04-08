require 'json'
require 'rapgenius'

SAVE_DIRECTORY = '../../data/rapgenius'
ARTISTS = [
  'Jay-Z',
  'Kendrick Lamar',
  'Psy'
]

def get_lyrics(artist)
  lyrics = Array.new
  tracks = RapGenius.search_by_artist artist

  tracks.each do |track|
    lines = track.lines
    lines.each do |line|
      lyrics.push line.lyric
    end
  end

  lyrics
end


lyrics = {
  'count' => ARTISTS.length
}

ARTISTS.each do |artist|
  lyrics[artist] = get_lyrics artist
end

Dir.mkdir(SAVE_DIRECTORY) unless Dir.exist?(SAVE_DIRECTORY)
File.open("#{SAVE_DIRECTORY}/lyrics.json", 'w') do |f|
  f.write(lyrics.to_json)
end
