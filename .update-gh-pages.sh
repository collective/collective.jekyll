if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  echo -e "Starting to update gh-pages\n"

  cd $HOME
  mkdir $TRAVIS_BUILD_NUMBER
  cp -R parts/test $HOME/$TRAVIS_BUILD_NUMBER
  
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis"
  git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com/gotcha/collective.jekyll.git  gh-pages > /dev/null

  cd gh-pages
  cp -Rf $HOME/$TRAVIS_BUILD_NUMBER .

  git add -f .
  git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to gh-pages"
  git push -fq origin gh-pages > /dev/null

  echo -e "Done magic with robot_reports\n"
fi
