import argparse
import sys

from src.db import DB
from src.redshift import Redshift


DEFAULT_TEMP = 6500
DEFAULT_BRIGHTNESS = 1.0
TEMP_MIN = 1000
TEMP_MAX = 10000
BRIGHTNESS_MIN = 0.0
BRIGHTNESS_MAX = 1.0


def _clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def _load_settings(db: DB) -> tuple[int, float]:
    temp = db.get("temp")
    brightness = db.get("brightness")
    temp = int(temp) if temp is not None else DEFAULT_TEMP
    brightness = float(brightness) if brightness is not None else DEFAULT_BRIGHTNESS
    return temp, brightness


def _save_settings(db: DB, temp: int, brightness: float) -> None:
    db.set("temp", int(temp))
    db.set("brightness", float(brightness))


def cmd_status(args: argparse.Namespace) -> int:
    db = DB(args.db)
    temp, brightness = _load_settings(db)
    print(f"temp={temp}K brightness={brightness:.3f}")
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    db = DB(args.db)
    rs = Redshift()
    current_temp, current_brightness = _load_settings(db)

    new_temp = current_temp if args.temp is None else int(args.temp)
    new_brightness = current_brightness if args.brightness is None else float(args.brightness)

    new_temp = _clamp(new_temp, TEMP_MIN, TEMP_MAX)
    new_brightness = _clamp(new_brightness, BRIGHTNESS_MIN, BRIGHTNESS_MAX)

    rs.change_color(new_temp, new_brightness)
    _save_settings(db, new_temp, new_brightness)
    print(f"Applied: temp={new_temp}K brightness={new_brightness:.3f}")
    return 0


def cmd_inc(args: argparse.Namespace) -> int:
    db = DB(args.db)
    rs = Redshift()
    current_temp, current_brightness = _load_settings(db)

    new_temp = current_temp + int(args.temp_delta)
    new_brightness = current_brightness + float(args.brightness_delta)

    new_temp = _clamp(new_temp, TEMP_MIN, TEMP_MAX)
    new_brightness = _clamp(new_brightness, BRIGHTNESS_MIN, BRIGHTNESS_MAX)

    rs.change_color(new_temp, new_brightness)
    _save_settings(db, new_temp, new_brightness)
    print(
        f"Applied: temp={new_temp}K (delta {int(args.temp_delta):+d}), "
        f"brightness={new_brightness:.3f} (delta {float(args.brightness_delta):+.3f})"
    )
    return 0


def cmd_reset(args: argparse.Namespace) -> int:
    rs = Redshift()
    rs.reset()
    if not args.no_store:
        db = DB(args.db)
        _save_settings(db, DEFAULT_TEMP, DEFAULT_BRIGHTNESS)
    print("Reset redshift")
    return 0


def cmd_gui(_: argparse.Namespace) -> int:
    try:
        from tkinter import Tk
    except ImportError:
        print(
            "tkinter is not available. Install your OS package (e.g. python3-tk) or use the CLI mode.",
            file=sys.stderr,
        )
        return 1

    import src.gui as gui

    root = Tk()
    app = gui.RedshiftGUI(root)
    app.run()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="redshift-gui", add_help=True)
    parser.add_argument(
        "--db",
        default="main.db",
        help="SQLite DB file for storing temp/brightness (default: main.db)",
    )
    sub = parser.add_subparsers(dest="command")

    p_gui = sub.add_parser("gui", help="Launch the Tk GUI")
    p_gui.set_defaults(func=cmd_gui)

    p_status = sub.add_parser("status", help="Print stored temp/brightness")
    p_status.set_defaults(func=cmd_status)

    p_set = sub.add_parser("set", help="Set absolute temperature/brightness")
    p_set.add_argument("--temp", type=int, help="Temperature in Kelvin (1000-10000)")
    p_set.add_argument("--brightness", type=float, help="Brightness (0.0-1.0)")
    p_set.set_defaults(func=cmd_set)

    p_inc = sub.add_parser("inc", help="Increment temperature/brightness")
    p_inc.add_argument(
        "--temp-delta",
        type=int,
        default=0,
        help="Delta in Kelvin (can be negative)",
    )
    p_inc.add_argument(
        "--brightness-delta",
        type=float,
        default=0.0,
        help="Delta in brightness (can be negative)",
    )
    p_inc.set_defaults(func=cmd_inc)

    p_reset = sub.add_parser("reset", help="Reset redshift to default")
    p_reset.add_argument(
        "--no-store",
        action="store_true",
        help="Do not overwrite stored values in the DB",
    )
    p_reset.set_defaults(func=cmd_reset)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Backwards compatible: no command launches GUI.
    if not getattr(args, "command", None):
        return cmd_gui(args)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
