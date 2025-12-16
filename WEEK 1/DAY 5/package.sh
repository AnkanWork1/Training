#!/bin/bash

echo "🚀 Starting packaging process..."

# Step 1: Generate SHA1 checksums
echo "🔧 Generating checksums..."
find src logs docs -type f -exec sha1sum {} \; > checksums.sha1
echo "✔ checksums.sha1 created."

# Step 2: Create timestamp
timestamp=$(date +%Y%m%d-%H%M%S)
bundle_name="bundle-$timestamp.zip"

# Step 3: Create bundle zip
echo "📦 Creating $bundle_name..."
zip -r "$bundle_name" src logs docs checksums.sha1 > /dev/null

echo "✅ Packaging complete!"
echo "Created file: $bundle_name"
echo "Included:"
echo "- src/"
echo "- logs/"
echo "- docs/"
echo "- checksums.sha1"
