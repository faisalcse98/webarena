"""Export a Microsoft Dining session into a Playwright storage_state file.

The dining.microsoft.com site is gated behind Microsoft SSO, so WebArena tasks
authenticate via a Playwright ``storage_state`` JSON instead of a username /
password pair. That JSON is produced by replaying the cookies / local-storage
from a persistent Edge profile (``user-data-dir``) where you have already signed
in to dining.microsoft.com through the regular browser.

Workflow:

1. Sign in once with a normal Edge browser pointed at the user-data-dir, e.g.::

       msedge --user-data-dir="$HOME/.dining_context" https://dining.microsoft.com

2. Run this script to snapshot that session into a storage_state file::

       python3 export_dining_storage_state.py --out ~/webarena/.auth/dining_state.json

   Re-run whenever the export is older than the MSAL refresh-token TTL.

The script launches a *headed* persistent context against the same
user-data-dir, navigates to the dining homepage so any deferred auth cookies are
materialized, then writes ``context.storage_state(path=...)``.
"""
import argparse
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

# Default dining URL, read the same way browser_env.env_config does so this
# script stays in sync without importing WebArena's heavy dependencies.
DINING = os.environ.get("DINING", "https://dining.microsoft.com")

# Edge profile that holds the signed-in dining.microsoft.com session.
DEFAULT_USER_DATA_DIR = Path.home() / ".dining_context"
DEFAULT_OUT = Path.home() / "webarena" / ".auth" / "dining_state.json"


def export_storage_state(
    user_data_dir: Path,
    out: Path,
    url: str,
    headless: bool,
    wait: float,
) -> None:
    if not user_data_dir.exists():
        sys.exit(
            f"Edge user-data-dir not found: {user_data_dir}\n"
            "Sign in to dining.microsoft.com once with an Edge browser pointed "
            "at this directory before exporting."
        )

    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        # Use the Edge channel + the existing profile so the live SSO session is
        # available. A persistent context is required to read an on-disk
        # user-data-dir rather than a fresh, empty profile.
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            channel="msedge",
            headless=headless,
        )
        try:
            page = context.pages[0] if context.pages else context.new_page()
            page.goto(url, wait_until="networkidle")
            # Give any deferred MSAL redirects / token refreshes time to settle.
            time.sleep(wait)

            if "login.microsoftonline.com" in page.url:
                sys.exit(
                    "Landed on the Microsoft login page instead of dining. The "
                    f"session in {user_data_dir} is not signed in (or expired). "
                    "Sign in again with a regular Edge browser, then re-run."
                )

            context.storage_state(path=str(out))
        finally:
            context.close()

    print(f"Wrote dining storage_state to {out}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output storage_state path (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--user-data-dir",
        type=Path,
        default=DEFAULT_USER_DATA_DIR,
        help=(
            "Edge user-data-dir with a signed-in dining session "
            f"(default: {DEFAULT_USER_DATA_DIR})"
        ),
    )
    parser.add_argument(
        "--url",
        default=f"{DINING}/buildings",
        help=f"URL to visit before snapshotting (default: {DINING}/buildings)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the browser headless (default: headed, recommended).",
    )
    parser.add_argument(
        "--wait",
        type=float,
        default=3.0,
        help="Seconds to wait after navigation for auth to settle (default: 3).",
    )
    args = parser.parse_args()

    export_storage_state(
        user_data_dir=args.user_data_dir,
        out=args.out,
        url=args.url,
        headless=args.headless,
        wait=args.wait,
    )


if __name__ == "__main__":
    main()
