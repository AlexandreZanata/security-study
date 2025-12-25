#!/bin/bash
# Example run script for reconner
# This demonstrates how to use reconner with various options

set -e

echo "=========================================="
echo "Reconner Example Run Script"
echo "=========================================="
echo ""

# Configuration
OUTPUT_DIR="./example-results"
TARGET="example.com"  # WARNING: Only use authorized targets!

# Clean previous results (optional)
if [ -d "$OUTPUT_DIR" ]; then
    echo "Cleaning previous results..."
    rm -rf "$OUTPUT_DIR"
fi

echo "Starting reconner scan..."
echo "Target: $TARGET"
echo "Output: $OUTPUT_DIR"
echo ""

# Example 1: Basic scan
echo "=== Example 1: Basic Scan ==="
python -m reconner \
    --target "$TARGET" \
    --output-dir "$OUTPUT_DIR" \
    --threads 20 \
    || echo "Note: This will fail if tools are not installed or target is not authorized"

echo ""
echo "=========================================="
echo "Scan completed!"
echo "=========================================="
echo ""
echo "Check results in: $OUTPUT_DIR"
echo "  - summary.json: Complete scan data"
echo "  - report.md: Markdown report"
echo "  - report.pdf: PDF report (if conversion succeeded)"
echo "  - highlights.txt: Quick summary"
echo "  - raw/: Raw tool outputs"
echo ""

# Example 2: Fast mode (commented out - uncomment to use)
# echo "=== Example 2: Fast Mode ==="
# python -m reconner \
#     --target "$TARGET" \
#     --output-dir "${OUTPUT_DIR}-fast" \
#     --fast \
#     --threads 10

# Example 3: Stealth mode (commented out - uncomment to use)
# echo "=== Example 3: Stealth Mode ==="
# python -m reconner \
#     --target "$TARGET" \
#     --output-dir "${OUTPUT_DIR}-stealth" \
#     --stealth \
#     --threads 5

# Example 4: With proxy (commented out - uncomment to use)
# echo "=== Example 4: With Proxy ==="
# python -m reconner \
#     --target "$TARGET" \
#     --output-dir "${OUTPUT_DIR}-proxy" \
#     --proxy "http://127.0.0.1:8080" \
#     --threads 20

# Example 5: Multiple targets from file (commented out - uncomment to use)
# echo "=== Example 5: Multiple Targets ==="
# echo "example.com" > targets.txt
# echo "test.example.com" >> targets.txt
# python -m reconner \
#     --input-file targets.txt \
#     --output-dir "${OUTPUT_DIR}-multi" \
#     --threads 20

echo ""
echo "For more examples, see README.md"
echo ""

