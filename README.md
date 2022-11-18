<div align="center">

  <h1 id="-----">

<p align="center">
  <img src="./Assets/title.png" height="300px">
</p>

  </h1>

<h1 id="-----">
<a href="https://github.com/ra101/PokeShelf" target="_blank"><img src="https://img.shields.io/badge/Source%20code-404040?style=for-the-badge&logo=github" alt="source_code"></a> <a href="https://github.com/ra101/PokeShelf/releases/latest/download/PokeShelf.zip"><img src="https://img.shields.io/badge/download-639?style=for-the-badge&logo=windows" alt="download"></a> <a href="https://github.com/ra101/PokeShelf/releases/download/v1.2.4/PokeShelf.zip"><img src="https://img.shields.io/badge/sponser-dd6633?style=for-the-badge&logo=buymeacoffee&logoColor=white" alt="download"></a>


</h1>

<a href="https://github.com/ra101/PokeShelf/stargazers"><img src="https://img.shields.io/github/stars/ra101/PokeShelf?style=for-the-badge&color=goldenrod&label=⭐ Stars" alt="Stars"></a> <a href="https://github.com/ra101/PokeShelf/network/members"><img src="https://img.shields.io/github/forks/ra101/PokeShelf?style=for-the-badge&color=aaa&label=⛓️ Forks" alt="Forks"></a> <a href="https://github.com/ra101/PokeShelf/blob/core/LICENSE" target="_blank"><img src="https://img.shields.io/github/license/ra101/POkeShelf?style=for-the-badge&label=%F0%9F%93%9C%20License&color=critical" alt="License"></a> <a href="https://github.com/ra101/PokeShelf/issues"><img src="https://img.shields.io/github/issues/ra101/PokeShelf?style=for-the-badge&label=⚠️ Issuues&color=39e" alt="Open Issues"></a> <a href="https://github.com/ra101/PokeShelf/graphs/contributors" target="_blank"><img src="https://img.shields.io/github/contributors/ra101/PokeShelf?style=for-the-badge&label=%F0%9F%98%8E%20Devs&color=goldenrod" alt="Contributors"></a>

</div>

<br/>

## 📄 Prerequisite

There various methods to make a Pokémon fangames. The most notable ones are:

- Using [Pokémon Essentials](https://pokemon-fan-game.fandom.com/wiki/Pok%C3%A9mon_Essentials), A base [RPG Maker XP](https://www.rpgmakerweb.com/products/rpg-maker-xp) project that comes with its own debugger, map connector and alot of free tools, It is community driven project, and is always up-to-date! RPG-Maker-XP only compiles games to Windows, so these are essentially Windows only games!
- By [ROM Hacking](https://en.wikipedia.org/wiki/ROM_hacking), These are created by editing the base ROM of _legally owned_ Pokémon game, We will be taking only [GameBoy Series](https://en.wikipedia.org/wiki/Game_Boy_Advance) and [Nintendo DS](https://en.wikipedia.org/wiki/Nintendo_DS) in account, since they have the most used games as base Image. These Fangames are made for their respective console, but can be played on any device using [Emulator](https://en.wikipedia.org/wiki/Emulator)!

<br/>

## 💼 About

<p align="center">
<i><b>"</b>Those who play Pokémon Games, typically have alot of them<b>"</b></i>  ~ My Experience
</p>

**PokéShelf** is a living gallery that hosts all games downloaded/installed by the User, May it be _Essentials_ game or GBx/NDS ROM!

- PokéShelf itself is themed like a Pokémon game menu, with almost no mouse input and key bindings similar to _Emulators_ and _Essentials_ game, all this to maintain the Immersion.
- Once Configured, Play Games Directly from PokeShelf, even the ones that require Emulator!
- You can Add Custom Background Image/Video and Custom Music for each fangame.
- Auto Add functionality for BG and Music for most of the _Essentials_ Games, To enable this functionality with ROMs or with your incompatible _Essentials_ Game, Check the [Auto-Add Guide](#-auto-add-functionality).
- Lastly, A Quit-to-Tray Option, if required, _I personally never used It._

<br/>

## 💥Get Started



You are First Encountered with the **Splash** Screen, Add a game in order to get in the **Shelf**.

<br/>


( **θ** ) **Controls**:

| Action       | Key                                   |
| ------------ | ------------------------------------- |
| Escape       | `<Esc>` │ `<X>`|
| Navigation   | ⬆️ │ `<Shift-Tab>`  ; ⬇️ │ `<Tab>`|
| Adjust Value | ⬅️ ; ➡️|
| Enter        | `<Enter>` │ `<C>` │`<Z>` │`<Space>` |

<br/>
<br/>


**( I )**  Open **Options** by Press `Alt + S` *(S as in Settings)* or Click on `Options` in Menu Bar.

- Adjust Music Volume
- Adjust Screen Size, >= L recommended
- You can't update Game Order within Shelf, Edit it in `config.json`.
- Add GBx Emulator if you intend to add GameBoy ROMs, [VisualBoy Advance](https://visualboyadvance.org/) is tested and recommended, It can emulate all GameBoy Series consoles (`.gb`, `.gbc`, `.gba`)
- Add NDS Emulator if you intend to add Nintendo DS ROMs, [DeSmuME](https://desmume.org) is tested and recommended.
- Activate Quit-to-Tray Option, if required
- `Save` to remember this for next time, `Cancel` to revert back or Press `Esc` to simply use these settings as a one time thing.

<br/><br/>


**( II )**  Open **Add Game** by Press `Ctrl + A` *(A as in Add)* or Click on `Game > Add Game` in Menu Bar.

- Add Essentials Game (`.exe`) **or** GBx ROM (`.gb`, `.gbc`, `.gba`)  **or** NDS ROM (`.nds`). *(While Adding ROMs make sure to have already added respective Emulator or else Save Button won't work)*
-  As soon as you add Game, Auto Add functionality would kick in for `BG Image/Video` and `BG Music`, But incase it doesn't, You have ability to Manualy Select Both of Them
   - File type for `BG Image/Video`: `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.mp4`, `.mkv`, `.webm`, `.avi`, `.mov`
   - File type for `BG Music`: `.wav`, `.ogg`, `.flac` (unfortunately `.mid` is not yet supported)
   - If it doesn't kick in, To enable this functionality with ROMs or with your incompatible _Essentials_ Game, Check the [Auto-Add Guide](#-auto-add-functionality), and go to edit menu and readd the game.
- Press `Save`, It will send into the `Shelf` Screen, with your game displayed on front, `Cancel` will send you back to `Spash` Screen.

<br/><br/>



**( III )**  Once A Game is Added, You can go to **Shelf** Screen by `Ctrl + S` *(A as in Shelf)* or Click on `Game > PokeShelf` in Menu Bar.

- You can use `<Left>`-`<Right>` to navigate b/w Games; Press `<Enter>` to Exit Shelf and **Start** the selected Game!
- To **Remove Game**, Simpily naviagte to the game you want to remove and Press `Ctrl + R` *(R as in Remove)* or Click on `Game > Remove Game` in Menu Bar.
- To **Edit Game**, Simpily naviagte to the game you want to edit and Press `Ctrl + E` *(E as in Edit)* or Click on `Game > Edit Game` in Menu Bar.

<br/><br/>



**( IV )**  To get Details about the app, Press `Alt + A` *(A as in About)* or Click on `About` in Menu Bar.

<br/><br/>



<br/>

## 🤙Contact Me

[![Protonmail](https://img.shields.io/badge/Protonmail-📧%20Email-558?style=for-the-badge&logo=protonmail)](mailto://ping@ra101.dev) [![Telegram](https://img.shields.io/badge/Telegram-💬%20Chat-informational?style=for-the-badge&logo=telegram)](https://telegram.me/ra_101)

<br/>

<div align="center">

  <h3> Made with <b>❤️</b> by<b>〈 RA 〉</b></h3>
</div>
