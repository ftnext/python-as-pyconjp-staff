#!/usr/bin/env bash
set -eu

LAYER_FACTORY_DOCKER_IMAGE="aws-lambda-python38:1.0"
CONTAINER_NAME="layer_factory"

DEST_DIR="build"
mkdir -p ${DEST_DIR}

while getopts l:p: OPT
do
  case $OPT in
    "l" ) LAYER_ZIP_FILE=$OPTARG
      ;;
    "p" ) PACKAGE=$OPTARG
      ;;
  esac
done

shift `expr $OPTIND - 1`

if [ "${LAYER_ZIP_FILE}" = "" -o "${PACKAGE}" = "" ]; then
  exit 1
fi

docker run --name ${CONTAINER_NAME} ${LAYER_FACTORY_DOCKER_IMAGE} ${PACKAGE} 
docker cp ${CONTAINER_NAME}:/var/task/python_layer.zip ${DEST_DIR}/${LAYER_ZIP_FILE}
docker rm ${CONTAINER_NAME}
