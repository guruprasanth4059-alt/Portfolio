#!/usr/bin/env python3
"""
Integration verification script for Guru Prasanth Resume & Download Feature
"""
import os
import urllib.request

def run_tests():
    print("=== RUNNING QA VERIFICATION TESTS ===")
    
    # 1. Check local file existence and sizes
    paths = [
        "assets/Guruprasanth_Resume.pdf",
        "guruprasanth-portfolio/assets/Guruprasanth_Resume.pdf",
        "Guruprasanth_Resume.pdf"
    ]

    for p in paths:
        assert os.path.exists(p), f"Missing: {p}"
        size = os.path.getsize(p)
        assert size > 5000, f"File too small: {p} ({size} bytes)"
        with open(p, "rb") as f:
            header = f.read(5)
        assert header == b"%PDF-", f"Invalid PDF header in {p}"
        print(f"[PASS] File exists and is valid PDF: {p} ({size:,} bytes)")

    # 2. Test HTTP download from running web server
    url = "http://localhost:5173/assets/Guruprasanth_Resume.pdf"
    req = urllib.request.urlopen(url)
    assert req.status == 200, f"Bad HTTP status: {req.status}"
    content = req.read()
    assert content.startswith(b"%PDF-"), "Downloaded content is not a PDF"
    print(f"[PASS] HTTP Download verified from {url} ({len(content):,} bytes, HTTP {req.status})")

    # 3. Verify HTML download buttons and attributes
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert 'download="Guruprasanth_Resume.pdf"' in html, "Missing download attribute"
    assert 'href="assets/Guruprasanth_Resume.pdf"' in html, "Missing href attribute"
    assert "guruking2537@gmail.com" in html, "Missing updated email in HTML"
    assert "Download Resume" in html, "Missing Download Resume text"
    print("[PASS] HTML download buttons and attributes verified")

    print("\nALL QA TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
