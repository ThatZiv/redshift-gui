# Redshift GUI

![logo](/.github/logo.png)

Just a simple non-configurable (at the moment) GUI for redshift via its cli with python. Created this because I hated using the command line to control screen temp.

## CLI mode

This project now supports a CLI mode that stores the last used temperature/brightness in `main.db` (same as the GUI), so you can increment values reliably.

Examples:

- Increment temperature by +200K:

  `python3 main.py inc --temp-delta 200`

- Decrement brightness by 0.05:

  `python3 main.py inc --brightness-delta -0.05`

- Increment both at once:

  `python3 main.py inc --temp-delta -300 --brightness-delta 0.05`

- Print current stored values:

  `python3 main.py status`

- Set absolute values:

  `python3 main.py set --temp 4200 --brightness 0.80`

GUI is still available via:

- `python3 main.py gui`

## TODO:

- More configuration
- Build and release
