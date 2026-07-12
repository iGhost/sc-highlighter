# Highlight My Items

**Highlight My Items** is a utility for **Star Citizen** that changes the color of in-game item names based on custom lists.

![Main application window](https://cp.expanseunion.com/media/highlighter_main_window_thin.png)

The utility modifies `global.ini` to make selected items, ores, and objects easier to find and identify visually.

---

## Project page

[Highlight My Items](https://www.expanseunion.com/sc/expanseutility) | Expanse Utility by people in slippers.

Small utilities for a vast universe.

---

## Features

- Highlight items using custom lists
- Use multiple lists at once
- Select a highlight color
- Back up `global.ini`
- Restore a backed-up `global.ini`
- Simple visual indication of successful and failed operations

---

## Requirements

- A `global.ini` file for the selected language in `data\Localization\[language]`
- If `g_language` is set in `user.cfg`, the utility uses that localization; otherwise it uses `english`

The English version of `global.ini` is available in [Data.zip](https://github.com/iGhost/global-ini/releases/latest/download/Data.zip).
Download the archive and extract it directly into the Star Citizen game root folder, such as `StarCitizen\LIVE`.

---

## Installation

1. Copy `highlighter.exe` to the Star Citizen game root folder, such as `StarCitizen\LIVE`.
2. Run `highlighter.exe` from that folder.

On first launch, the utility creates the `highlights` directory for custom item lists.

The `_backup` directory is created after you click **[ Backup global.ini ]**.

---

## First launch (required)

1. Run `highlighter.exe` **from the `StarCitizen\LIVE` folder**.
2. Click **[ Backup global.ini ]** to save the current version of `global.ini`.
3. Select the required list using its checkbox.
4. Click **[ Highlight ]** to apply the changes.

### Button indicators

- 🟢 **Green** — the operation completed successfully
- 🔴 **Red** — an error occurred

---

## Checking the result in game

Highlights are visible:

- when grabbing items with an FPS tractor beam,
- when viewing ore with the **ATLS GEO**,
- when scanning (pinging) objects from a ship.

---

## Item lists

### List format

- Custom lists are stored in the `highlights` folder.
- Lists are `*.txt` files.
- Use **one key per line**.
- Keys are taken from `global.ini`.

Example:

```
items_commodities_bexalite
items_commodities_carbon
items_commodities_copper
```

### Creating a custom list

1. Create a text file, for example `iloveburrito.txt`.
2. Put it in `StarCitizen\LIVE\highlights`.
3. Add the keys for the required items, for example:

   ```
   item_NameFood_burrito_01_a
   item_NameFood_burrito_01_beef_a
   item_NameFood_burrito_01_chile_a
   ```

4. Save `iloveburrito.txt`.
5. Run the utility and select the list in the interface.
6. Start the game.

---

## Restoring global.ini

1. Run `highlighter.exe` **from the `StarCitizen\LIVE` folder**.
2. Click **[ Restore global.ini ]** to restore your latest backup of `global.ini` for the current language.

To apply highlighting again after restoring the file:

1. Select the required item lists.
2. Select a color from the drop-down list.
3. Click **[ Highlight ]**.

---

## Uninstallation

First, click **[ Restore global.ini ]** to restore your latest backup of `global.ini`.

Then:

1. Delete `highlighter.exe`.
2. Delete the `highlights` and `_backup` folders if you no longer need their contents.

---

## Troubleshooting

If **[ Restore global.ini ]** cannot restore the backup, or items are highlighted incorrectly in the game,
download [Data.zip](https://github.com/iGhost/global-ini/releases/latest/download/Data.zip) and extract it directly into the Star Citizen game root folder.
Before using Highlight My Items again, click **[ Backup global.ini ]** to create a new backup.

---

## Important

- Use this utility **at your own risk**.
- The author is not responsible for:
  - incorrect use,
  - damage to game files,
  - any resulting consequences.

---

## Community

You can:

- create item lists yourself,
- request lists from the community on [Discord](https://discord.gg/69X4YZPjht).
