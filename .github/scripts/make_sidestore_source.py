#!/usr/bin/env python3
"""Write a SideStore / AltStore source (source.json) for the IPA in a release.

Usage: make_sidestore_source.py <ipa> <download-url> <release-date> <out>
Version fields come from the IPA's Info.plist so SideStore sees them match.
"""
import json
import os
import plistlib
import sys
import zipfile

REPO = "Cat-in-a-Box-0115/PiliNara-BTR"


def read_info_plist(ipa):
    with zipfile.ZipFile(ipa) as z:
        name = next(
            n for n in z.namelist()
            if n.count("/") == 2 and n.endswith(".app/Info.plist")
        )
        return plistlib.loads(z.read(name))


def main():
    ipa, download_url, date, out = sys.argv[1:5]
    info = read_info_plist(ipa)
    source = {
        "name": "PiliNara-BTR",
        "identifier": "io.github.cat-in-a-box-0115.pilinara-btr",
        "sourceURL": f"https://github.com/{REPO}/releases/latest/download/source.json",
        "subtitle": "PiliNara with multi-thread loading on iPad",
        "website": f"https://github.com/{REPO}",
        "apps": [
            {
                "name": info.get("CFBundleDisplayName") or info["CFBundleName"],
                "bundleIdentifier": info["CFBundleIdentifier"],
                "developerName": "Cat-in-a-Box-0115",
                "subtitle": "Third-party Bilibili client",
                "localizedDescription": (
                    "PiliNara (tyechan fork) with the BTR multi-thread "
                    "proxy enabled on iOS / iPadOS."
                ),
                "iconURL": f"https://raw.githubusercontent.com/{REPO}/main/assets/images/logo/logo.png",
                "tintColor": "#FB7299",
                "versions": [
                    {
                        "version": info["CFBundleShortVersionString"],
                        "buildVersion": info["CFBundleVersion"],
                        "date": date,
                        "downloadURL": download_url,
                        "size": os.path.getsize(ipa),
                        "minOSVersion": info.get("MinimumOSVersion", "15.0"),
                    }
                ],
                "appPermissions": {"entitlements": [], "privacy": {}},
            }
        ],
        "news": [],
    }
    with open(out, "w") as f:
        json.dump(source, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
