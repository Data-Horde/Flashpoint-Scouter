# Flashpoint-Game-Scouter
A Tool for Scouting game sites full of Flash Games for [Bluemaxima's Flashpoint Project](http://bluemaxima.org/flashpoint/)


#### Adobe is [~~killing~~ ending the life of Flash](https://www.adobe.com/products/flashplayer/end-of-life.html) at the end of this year.

and people are understably not too happy about this decision. There are several projects out there dedicated to preserving flash media post-2020. One in particular is [Bluemaxima's Flashpoint](http://bluemaxima.org/flashpoint/) dedicated to preserving games and animations.

As of my writing this, Flashpoint sports a whopping **60,000 games**. But there is still more to be found. So in hopes of making the hunting process easier the _FlashPoint Scouter (FPS)_ is a tool designed to scour game sites, to see if there are any games currently not included in Flashpoint. This is done by comparing game titles on the website, to those in the Flashpoint database; to determine how much of this website's content is _unrecognized_.

# How it works

![](/FPS.png)

1. First a local copy of the [Flashpoint Master list](https://docs.google.com/spreadsheets/d/1JfxEL5PxoOz9r-cz-2ivdvooscQrX6uuhbV_Na2xGss/edit#gid=0) is made/updated to get a list of all currently curated games.
2. The current scope of this project is to target game sites which have *ID-based* URLs, either as a field:
  - Ex. a game on http://www.oyunlar1.com is located at http://www.oyunlar1.com/games.php?flash=11637
  or game sites which have an *ID sorting* system even if URLs are unpredictable:
  - Ex. a game on http://www.flash-game.net is located at http://www.flash-game.net/game/7519/quadrato.html and while `quadrato` in the URL might not be predictable, there is a page which allows for all games to be sorted (and thus crawled) by ID.
3. Next, a CSS-selector is specified to tell _FPS_ where to look for the game's title on the page.
4. And finally, to ensure correct localization (ensuring the page is in English) or layout (ensuring a game's title is in its usual location) additional cookies might be specified.
5. Once all of this information has been provided, the Scouter will crawl through the given game site and build a list of available games.
6. The game site's titles are queried against the local Flashpoint Master list, while accounting for typos, name differences etc., to search for `likely` matches.
7. After comparing the lists, the Scouter reports what percentage of games from this game site are:
  - In the Flashpoint Master list
  - Very similar to games in the Flashpoint Master list
  - Kind of similar to games in the Flashpoint Master list
  - Unrecognizd
  
This gives game hunters and curators a quick-look to determine if it's worth gathering games from one game site or another.
  

