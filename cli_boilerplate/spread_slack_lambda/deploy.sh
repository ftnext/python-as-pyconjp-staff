#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_DIR=$(dirname $(dirname ${SCRIPT_DIR}))

usage() {
  echo "Usage: $0 -n <lambda_function_name> -r <role_arn> -e <env_var_pair> [-e <env_var_pair>] [-- --profile foo]" 1>&2
  echo "" 1>&2
  echo "Deploy AWS Lambda function which can read/write Google spreadsheet and post to Slack." 1>&2
  echo "" 1>&2
  echo "-n: Specify name of the Lambda function. Required" 1>&2
  echo "-r: Specify ARN of role for the Lambda function. Required" 1>&2
  echo "-e: Specify environment variable as key=value format. Required at least one" 1>&2
  echo "-x: Be verbose." 1>&2
  echo "-h: Show this help message." 1>&2
  echo "" 1>&2
  echo "Use -- to pass other parameters (profile, region, ...) to aws-cli." 1>&2
  exit 1
}

if [ "$1" = "--help" -o "$1" = "-help" ]; then
  usage
fi

ENVIRONMENT_VARIABLES=()

while getopts n:r:e:xh OPT
do
  case $OPT in
    "n" ) FUNCTION_NAME=$OPTARG
      ;;
    "r" ) ROLE_ARN=$OPTARG
      ;;
    "e" ) ENVIRONMENT_VARIABLES+=($OPTARG)
      ;;
    "x" ) set -x
      ;;
    "h" ) usage
      ;;
    *   ) usage
      ;;
  esac
done

shift `expr $OPTIND - 1`

if [ "${FUNCTION_NAME}" = "" -o "${ROLE_ARN}" = "" ]; then
  usage
fi

if [ ${#ENVIRONMENT_VARIABLES[@]} -eq 0 ]; then
  usage
fi

grep_from_json() {
  json_string=$1
  keyword=$2
  echo ${json_string} | python3 -m json.tool | grep ${keyword}
}

strip_trailing_comma() {
  echo $1 | sed -E 's/,$//'
}

strip_double_quotes() {
  echo $1 | sed -E 's/^"//' | sed -E 's/"$//'
}

publish_lambda_layer() {
  layer_zip=$1
  layer_package=$2
  layer_name=$3
  layer_description=$4
  shift 4
  echo $@

  cd ${PROJECT_DIR}/layer_factory
  rm build/${layer_zip}
  ./create_layer_zip.sh -p ${layer_package} -l ${layer_zip}
  cd build/
  aws lambda publish-layer-version \
    --layer-name ${layer_name} \
    --compatible-runtimes python3.8 \
    --description python38_${layer_description} \
    --zip-file fileb://${layer_zip} \
    $@
}

# set -eだとgrepで見つからないときstatusは0以外が返るが、スクリプトがエラー終了しないように緩める
set +e

LIST_LAYER_ARNS=$(aws lambda list-layers --query 'Layers[*].LatestMatchingVersion.LayerVersionArn' $@)

POSTSLACK_LAYER_ARN=$(grep_from_json "${LIST_LAYER_ARNS}" postslack)
if [ "${POSTSLACK_LAYER_ARN}" = "" ]; then
  echo "postslack layer does not exist yet. Publish postslack layer ..."
  publish_lambda_layer "python38_diypostslack01_layer.zip" \
    git+https://github.com/ftnext/diy-slack-post@master#egg=postslack \
    diy-postslack diypostslack01 $@
fi

GSPREAD_LAYER_ARN=$(grep_from_json "${LIST_LAYER_ARNS}" gspread)
if [ "${GSPREAD_LAYER_ARN}" = "" ]; then
  echo "gspread layer does not exist yet. Publish gspread layer ..."
  publish_lambda_layer "python38_gspread36_layer.zip " \
    gspread==3.6.0 gspread36 gspread36 $@
fi

set -e

LAYER_ARNS=()
LIST_LAYER_ARNS=$(aws lambda list-layers --query 'Layers[*].LatestMatchingVersion.LayerVersionArn' $@)

POSTSLACK_LAYER_ARN=$(grep_from_json "${LIST_LAYER_ARNS}" postslack)
POSTSLACK_LAYER_ARN=$(strip_trailing_comma ${POSTSLACK_LAYER_ARN})
POSTSLACK_LAYER_ARN=$(strip_double_quotes ${POSTSLACK_LAYER_ARN})
LAYER_ARNS+=(${POSTSLACK_LAYER_ARN})

GSPREAD_LAYER_ARN=$(grep_from_json "${LIST_LAYER_ARNS}" gspread)
GSPREAD_LAYER_ARN=$(strip_trailing_comma ${GSPREAD_LAYER_ARN})
GSPREAD_LAYER_ARN=$(strip_double_quotes ${GSPREAD_LAYER_ARN})
LAYER_ARNS+=(${GSPREAD_LAYER_ARN})

ENVIRONMENT_VARIABLES_STRING=""
for env_var in ${ENVIRONMENT_VARIABLES[@]}
do
  ENVIRONMENT_VARIABLES_STRING="${env_var},${ENVIRONMENT_VARIABLES_STRING}"
done
ENVIRONMENT_VARIABLES_STRING=$(strip_trailing_comma ${ENVIRONMENT_VARIABLES_STRING})

# zipにフルパス分のディレクトリができないようにcdすることにした
cd ${SCRIPT_DIR}

# zipはアーカイブに追加する挙動なので、アップロードするコードが増えないように前回デプロイしたファイルを消す
rm function.zip
zip function.zip lambda_function.py

aws lambda create-function \
  --function-name ${FUNCTION_NAME} \
  --runtime python3.8 \
  --role ${ROLE_ARN} \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 10 \
  --environment Variables="{${ENVIRONMENT_VARIABLES_STRING}}" \
  --layers ${LAYER_ARNS[@]} \
  $@
