"""Launch a headed Edge browser bound to a persistent user-data-dir.

This is the companion to ``export_dining_storage_state.py``. Before you can
snapshot a Microsoft Dining session into a Playwright ``storage_state`` file you
need to sign in once through a real browser whose profile lives in the same
``user-data-dir`` the exporter reads. This script opens that browser for you via
Playwright so you don't have to locate the ``msedge`` binary by hand.

Workflow:

1. Launch the browser against the user-data-dir and sign in interactively::

       python3 launch_dining_browser.py

   Complete the Microsoft SSO flow in the window that opens, then leave it open.

2. With the session now stored in the user-data-dir, snapshot it::

       python3 export_dining_storage_state.py --out ~/webarena/.auth/dining_state.json

The browser stays open until you close the window or press Ctrl-C in the
terminal, so any deferred auth cookies / tokens have time to materialize on
disk inside the profile.
"""
import argparse
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# Default dining URL, read the same way browser_env.env_config does so this
# script stays in sync without importing WebArena's heavy dependencies.
DINING = os.environ.get("DINING", "https://dining.microsoft.com")

# Edge profile that holds (or will hold) the signed-in dining.microsoft.com
# session. Must match what export_dining_storage_state.py uses.
DEFAULT_USER_DATA_DIR = Path.home() / ".dining_context"


def launch_browser(user_data_dir: Path, url: str, headless: bool) -> None:
    # Create the profile directory if it does not exist yet so a first-time
    # sign-in has somewhere to persist its cookies / local-storage.
    user_data_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        # Use the Edge channel + the persistent profile so an interactive SSO
        # session is written back to the on-disk user-data-dir. A persistent
        # context is required to read / write an on-disk profile rather than a
        # fresh, empty one.
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            channel="msedge",
            headless=headless,
        )
        try:
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(url, wait_until="domcontentloaded")

            print(
                f"Edge launched against {user_data_dir}\n"
                f"Navigated to {url}\n"
                "Sign in if prompted, then close the window (or press Ctrl-C "
                "here) when done."
            )

            # Block until the browser window is closed or the user interrupts.
            context.wait_for_event("close", timeout=0)
        except KeyboardInterrupt:
            print("\nInterrupted - closing browser.")
        finally:
            try:
                context.close()
            except Exception:
                pass


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--user-data-dir",
        type=Path,
        default=DEFAULT_USER_DATA_DIR,
        help=(
            "Edge user-data-dir to launch with "
            f"(default: {DEFAULT_USER_DATA_DIR})"
        ),
    )
    parser.add_argument(
        "--url",
        default=DINING,
        help=f"URL to open on launch (default: {DINING})",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the browser headless (default: headed, recommended).",
    )
    args = parser.parse_args()

    launch_browser(
        user_data_dir=args.user_data_dir,
        url=args.url,
        headless=args.headless,
    )


if __name__ == "__main__":
    main()
