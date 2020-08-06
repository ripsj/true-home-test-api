#!/bin/bash


setup () {
  echo ------- SETUP -------
  apt-get update
  apt-get install -y zip
  pip install virtualenv
  virtualenv --python=python3 env
  source env/bin/activate
  pip install -r requeriments.txt
  return $?
}

tests () {
  echo ------- TEST -------
  pip install -r requeriments-tests.txt
  tox
  return $?
}

deploy () {
  echo ------- DEPLOY -------
  echo $1
  pip install awscli
  # aws s3 cp s3://$S3BUCKET/zappa_settings.json .
  zappa deploy $1 || zappa update $1
  # zappa certify $1 --yes
  zappa manage $1 "migrate"
  # zappa manage $1 "collectstatic --noinput"
  return $?
}

setup && deploy $1
