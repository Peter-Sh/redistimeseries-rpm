#!/bin/bash

if [ -z "$NAME" ]; then
	NAME=$(basename $PWD)
fi
OWNER=$(sed   -n '/^%global gh_vend/{s/.* //;p}'   $NAME.spec)
PROJECT=$(sed -n '/^%global gh_proj/{s/.* //;p}'   $NAME.spec)
VERSION=$(sed -n '/^Version:/{s/.* //;p}'          $NAME.spec)

echo -e "\nCreate git snapshot\nName=$NAME, Owner=$OWNER, Project=$PROJECT, Version=$VERSION\n"

echo "Cloning..."
rm -rf $PROJECT-$VERSION
git clone --branch v$VERSION --recursive https://github.com/$OWNER/$PROJECT.git $PROJECT-$VERSION

echo "Archiving..."
tar czf $NAME-$VERSION.tgz --exclude-vcs $PROJECT-$VERSION

echo "Cleaning..."
rm -rf $PROJECT-$VERSION

echo "Done."
