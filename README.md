# Science symbols

Editable 2D SVG components and experiment examples for scientific drawings in Inkscape.

[Open the visual catalogue](https://jbusink.github.io/Inkscape-Package/) or [browse examples](https://jbusink.github.io/Inkscape-Package/#mode=examples).

## Use

- Open `Modular packages/Science-symbols/index.html` in a browser. Search, preview and download SVGs offline.
- Open a component or example directly in Inkscape to edit it.
- On Windows, run [Install.cmd](Modular%20packages/Science-symbols/Install.cmd), then restart Inkscape and open the Symbols panel. The installer backs up existing managed libraries before replacing or removing them.
- On other systems, copy the SVGs from [Libraries](Modular%20packages/Science-symbols/Libraries/) into the symbols folder of your Inkscape user profile, then restart Inkscape.

## Edit and rebuild

Edit the source SVGs in [Components](Modular%20packages/Science-symbols/Components/). Keep lettering outside component artwork; put symbol names in the catalogue. Edit standalone experiment drawings in [Examples](Modular%20packages/Science-symbols/Examples/).

When adding, renaming or removing an item, update [catalog.json](Modular%20packages/Science-symbols/Maintenance/catalog.json). Run [Build.cmd](Modular%20packages/Science-symbols/Build.cmd), or run this from the repository root with Python 3:

```sh
python "Modular packages/Science-symbols/Maintenance/build.py"
```

The build regenerates Libraries, Overviews and index.html. It preserves authored examples. Reinstall the libraries after rebuilding if you use the Inkscape Symbols panel.

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

See [LICENSE](LICENSE). Examples are editable schematic illustrations, not construction drawings or operating procedures.
