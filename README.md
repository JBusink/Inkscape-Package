# Science symbols

Editable 2D SVG components and experiment examples for scientific drawings in Inkscape.

[Open the visual catalogue](https://jbusink.github.io/Inkscape-Package/) or [browse examples](https://jbusink.github.io/Inkscape-Package/#mode=examples).

## Download and install

[Download the complete package with Windows installer (ZIP)](https://jbusink.github.io/Inkscape-Package/downloads/Science-symbols.zip).

Extract the entire ZIP first. On Windows, double-click `Install.cmd` in the extracted folder. Then restart Inkscape and open the Symbols panel. No Python or administrator access is needed to install.

The ZIP includes all components, examples, symbol libraries, overviews and the offline catalogue. Open `index.html` in the extracted folder to browse offline.

## Use

- Open `Modular packages/Science-symbols/index.html` in a browser. Search, preview and download SVGs offline.
- Open a component or example directly in Inkscape to edit it.
- On Windows, use the ZIP and installer described above. The installer backs up existing managed libraries before replacing or removing them.
- On other systems, copy the SVGs from the extracted `Modular packages/Science-symbols/Libraries/` folder into the symbols folder of your Inkscape user profile, then restart Inkscape.

## Edit and rebuild

Edit the source SVGs in [Components](https://github.com/JBusink/Inkscape-Package/tree/main/Modular%20packages/Science-symbols/Components). Keep lettering outside component artwork; put symbol names in the catalogue. Edit standalone experiment drawings in [Examples](https://github.com/JBusink/Inkscape-Package/tree/main/Modular%20packages/Science-symbols/Examples).

When adding, renaming or removing an item, update [catalog.json](https://github.com/JBusink/Inkscape-Package/blob/main/Modular%20packages/Science-symbols/Maintenance/catalog.json). Run `Modular packages/Science-symbols/Build.cmd`, or run this from the repository root with Python 3:

```sh
python "Modular packages/Science-symbols/Maintenance/build.py"
```

The build regenerates Libraries, Overviews, index.html and `downloads/Science-symbols.zip`. It preserves authored examples. Commit and push the generated files, including the ZIP, to update GitHub Pages and the download together. Reinstall the libraries after rebuilding if you use the Inkscape Symbols panel.

## Files

- `Components/`: editable source artwork.
- `Examples/`: complete experiment drawings.
- `Libraries/`: generated Inkscape symbol collections.
- `Overviews/`: generated labelled sheets.
- `Maintenance/`: catalogue, builder and installer.
- `Archive/` at the repository root: historical snapshots, not part of the current catalogue or installation.

## README and catalogue

This README is the single documentation source. The build embeds it in the catalogue's README window, so it remains readable offline without a Markdown plugin or server. Edit this file and rebuild to update both views. Keep index.html for image previews, search and downloads.

## License

See [LICENSE](https://github.com/JBusink/Inkscape-Package/blob/main/LICENSE). Examples are editable schematic illustrations, not construction drawings or operating procedures.
