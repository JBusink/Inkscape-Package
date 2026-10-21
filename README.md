# Science symbols

SVG symbol libraries and editable scientific drawings for Inkscape.

[Open index.html: the catalogue](https://jbusink.github.io/Inkscape-Package/index.html) | [Browse examples](https://jbusink.github.io/Inkscape-Package/index.html#mode=examples)

## Download the Inkscape libraries

[Download Inkscape libraries with Windows installer (ZIP)](https://jbusink.github.io/Inkscape-Package/downloads/Science-symbols.zip)

The ZIP contains the 13 SVG symbol libraries and a Windows installer. Website files, standalone components and examples are available separately through the catalogue.

## Install on Windows

- Download the ZIP and choose Extract All in Windows Explorer.
- Open the extracted folder and double-click `Install.cmd`.
- Wait for the installation message, then restart Inkscape.
- Open the Symbols panel and select a Science library.

The installer runs for your Windows user and needs no Python or administrator access. It backs up previously installed Science libraries before updating them.

## Manual installation (all systems)

- In Inkscape, open Preferences, then System, and find the User symbols folder.
- Open that folder in your file manager. Create the folder if it does not exist.
- Copy the SVG files from the extracted `Libraries` folder into that folder. Replace older versions with the same names when updating.
- Restart Inkscape and open the Symbols panel. Select a Science library to use its symbols.

On a standard Windows installation, the folder is `%APPDATA%\inkscape\symbols`.

## Use the catalogue

Search or select a category to browse components. Use the SVG download beside an item to save an editable drawing. In a category, use the library download to save that category's Inkscape symbol library, or the overview download to save its labelled reference sheet.

Use Examples to browse complete experiment drawings. Download an example as an SVG and open it directly in Inkscape. Examples are separate drawings and are not included in the libraries ZIP.

## Edit and rebuild (maintainers)

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

To browse offline from a local clone, open `index.html` in the repository root. This is also the website start page. The older `Modular packages/Science-symbols/index.html` entry remains available. This README is also embedded in the catalogue; rebuild after editing it.

## License

MIT license; see `LICENSE` in the repository. Examples are schematic illustrations, not construction drawings or operating procedures.
