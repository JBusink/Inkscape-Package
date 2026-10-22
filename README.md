# Science symbols

SVG symbol libraries and editable scientific drawings for Inkscape.

Use the libraries in Object > Symbols (`Ctrl+Shift+Y`). They do not appear in the Extensions menu.

[Open index.html: the catalogue](https://jbusink.github.io/Inkscape-Package/index.html) | [Browse examples](https://jbusink.github.io/Inkscape-Package/index.html#mode=examples)

## Download the Inkscape libraries

[Download Inkscape libraries with Windows installer (ZIP)](https://jbusink.github.io/Inkscape-Package/downloads/Science-symbols.zip)

The ZIP contains the 13 SVG symbol libraries and a Windows installer. Website files, standalone components and examples are available separately through the catalogue.

## Install on Windows

- Download the ZIP and choose Extract All in Windows Explorer.
- Save your work and close all Inkscape windows.
- Open the extracted folder and double-click `Install.cmd`.
- Wait for the installation message, then start Inkscape.
- Open Object > Symbols (`Ctrl+Shift+Y`). In the symbol-set selector, choose a category such as `Optics`, `Circuits` or `Acoustics`.
- Drag a symbol from the panel onto your drawing. An empty `Current document` set is normal for a new drawing; choose a library first.

The installer runs for your Windows user and needs no Python or administrator access. It backs up previously installed Science libraries before updating them.

## Manual installation (all systems)

- In Inkscape, open Preferences, then System, and find the User symbols folder.
- Open that folder in your file manager. Create the folder if it does not exist.
- Copy the SVG files from the extracted `Libraries` folder into that folder. Replace older versions with the same names when updating.
- Restart Inkscape and open Object > Symbols (`Ctrl+Shift+Y`). Choose a category such as `Optics` in the symbol-set selector.

On a standard Windows installation, the folder is `%APPDATA%\inkscape\symbols`.

## Load a library directly in Inkscape (without installation)

- Extract the ZIP. In Inkscape, choose File > Open (`Ctrl+O`).
- Open a file from the extracted `Libraries` folder, for example `Science-optics.svg`.
- Open Object > Symbols (`Ctrl+Shift+Y`) and select `Current document`. The symbols in that SVG are now available in the panel.
- To use one in another drawing, select the wanted object on the library's overview sheet, copy it (`Ctrl+C`), switch to your drawing and paste (`Ctrl+V`). Keep the downloaded library as your reusable source.

To bring an entire library sheet into an existing drawing, use File > Import (`Ctrl+I`) and select the library SVG. If Inkscape asks how to import the SVG, choose editable objects rather than an image link. This imports the whole sheet into that document; it does not install a library for all documents. For permanent availability in the symbol-set selector, use the installer or the manual installation steps above.

For a single component or example, download its SVG from the catalogue and use File > Open or File > Import in the same way.

## If the Symbols panel closes Inkscape

Earlier downloads used compact SVG files that could crash the Symbols panel in Inkscape 1.4.x on Windows. Close Inkscape, download the current ZIP, extract it into a new folder and run the updated `Install.cmd`. It replaces the old libraries after backing them up. For manual installation, replace all 13 old `Science-*.svg` files in your User symbols folder with the current versions, then restart Inkscape.

## Use the catalogue

Search or select a category to browse components. Use the SVG download beside an item to save an editable drawing. In a category, use the library download to save that category's Inkscape symbol library, or the overview download to save its labelled reference sheet.

Use Examples to browse complete experiment drawings. Download an example as an SVG and open it directly in Inkscape. Examples are separate drawings and are not included in the libraries ZIP.

## Edit and rebuild (maintainers)

### Preview locally

Open `index.html` in the repository root directly in your browser. To use VS Code Live Server, set `"liveServer.settings.useWebExt": true` in your local workspace settings first. This disables script injection, which can truncate SVG files containing nested SVGs. Stop and restart Live Server after changing the setting, then refresh the browser with `Ctrl+F5`. During editing, refresh manually with `F5`; no browser extension is needed to view the site. Local `.vscode` settings are excluded from Git.

Alternatively, run `python -m http.server 8000` from the repository root and open `http://localhost:8000/index.html`.

### Update artwork

Work in a local clone of this repository. All paths below are relative to the repository root.

- Edit component artwork in `Modular packages/Science-symbols/Components/`.
- Edit experiment drawings in `Modular packages/Science-symbols/Examples/`.
- When adding, renaming or removing an item, update `Modular packages/Science-symbols/Maintenance/catalog.json`.
- Run `Modular packages/Science-symbols/Build.cmd`, or use Python 3:

```sh
python "Modular packages/Science-symbols/Maintenance/build.py"
```

The build updates the symbol libraries, overview sheets, catalogue and `downloads/Science-symbols.zip`. It preserves edited examples. The ZIP includes the libraries listed in the catalogue and the files needed by the Windows installer.

Commit and push the updated files, including the ZIP, to publish them through GitHub Pages. After updating libraries, install them again and restart Inkscape.

The repository has one website entry point, `index.html`, and one installer entry point, `Install.cmd`, both in the root folder. The installer also works in the extracted download ZIP. `Modular packages/Science-symbols/` contains the artwork, generated libraries, overview sheets and maintenance tools. This README is embedded in the root catalogue; rebuild after editing it.

## License

MIT license; see `LICENSE` in the repository. Examples are schematic illustrations, not construction drawings or operating procedures.
