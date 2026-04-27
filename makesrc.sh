#!/bin/bash

SPECFILE=$(find . -name '*.spec' -print -quit)
if [ -z "$SPECFILE" ]; then
	echo "spec file not found"
	exit 1
fi
NAME=$(basename "$SPECFILE" | cut -d. -f1)
OWNER=$(sed   -n '/^%global gh_vend/{s/.* //;p}'   "$SPECFILE")
PROJECT=$(sed -n '/^%global gh_proj/{s/.* //;p}'   "$SPECFILE")
VERSION=$(sed -n '/^Version:/{s/.* //;p}'          "$SPECFILE")

echo -e "\nCreate git snapshot\nName=$NAME, Owner=$OWNER, Project=$PROJECT, Version=$VERSION\n"

echo "Cloning..."
rm -rf "$PROJECT-$VERSION"
git clone --branch "v$VERSION" --recursive "https://github.com/$OWNER/$PROJECT.git" "$PROJECT-$VERSION"

echo "Archiving..."
tar czf "$NAME-$VERSION.tar.gz" --exclude-vcs "$PROJECT-$VERSION"

echo "Cleaning..."
rm -rf "$PROJECT-$VERSION"

echo "Done."
