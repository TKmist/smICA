# smICA analytical add-on template

This directory is a working skeleton for a directory-based analytical mode.
Copy the complete directory to `src/smICA/Modes`, rename the copied directory,
and then replace the `Template` and `template` identifiers with names unique to
the new mode.

The directory must contain exactly one file ending in `_config.json`. The
configuration names the layout, initialization, and Analysis-menu files, plus
the global menu-controller object used while switching modes. All referenced
files and `__init__.py` are required; incomplete directories are ignored by
smICA and by the updater.

Files in this template:

- `Template_config.json` declares the mode entry points.
- `Template_menu_item.py` adds the mode to the Analysis menu and controls its
  mount/unmount lifecycle.
- `Template_layout.py` creates the visible Dear PyGui items.
- `Template_INIT.py` contains layout state, callbacks, and analytical logic.
- `__init__.py` marks the directory as an importable Python package.

Before committing a new mode, update every import path, mode path, class name,
callback name, Dear PyGui tag, and visible label. Tags must remain unique across
the entire application. Keep third-party dependencies in the main project
dependency definition so a normal installation and update can provide them.

The full development procedure is documented in `docs/For_developers.ipynb`.
