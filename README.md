[Markovsecrets](http://secrets.oychang.com)
===========================================

Generate one-off anecdotes à la [UMiami Secrets](https://facebook.com/UMiamiSecrets) with Markov Chains.


Sources
=======

* Up to Secrets #4265
* 20 lyrics each from Jay-Z, Kendrick Lamar, & Psy
* The soundtrack to Disney's Frozen
* Saga of King Olaf, The Road Not Taken
* TODO: The Odyssey

NB: the raw data files are not stored in this repository.
Rather, to keep repo size down, only `mapping.json` is made available.
The true structure of `data/` is so:

```bash
$ tree data
data
├── condensed.json
├── mapping.json
├── books
│   └── odyssey.txt
├── facebook
│   ├── [1-44].json
├── poetry
│   ├── saga-of-king-olaf.txt
│   └── the-road-not-taken.txt
└── rapgenius
    ├── frozen.json
    └── lyrics.json
```


License
=======

MIT License
