#!/usr/bin/env bash

set -e

SCRIPT_DIR=$(cd $(dirname $0); pwd)

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

strip_trailing_comma() {
  echo $1 | sed -E 's/,$//'
}

strip_double_quotes() {
  echo $1 | sed -E 's/^"//' | sed -E 's/"$//'
}

LAYER_ARNS=()
LIST_LAYER_ARNS=$(aws lambda list-layers --query 'Layers[*].LatestMatchingVersion.LayerVersionArn' $@)

POSTSLACK_LAYER_ARN=$(echo ${LIST_LAYER_ARNS} | python3 -m json.tool | grep postslack)
POSTSLACK_LAYER_ARN=$(strip_trailing_comma ${POSTSLACK_LAYER_ARN})
POSTSLACK_LAYER_ARN=$(strip_double_quotes ${POSTSLACK_LAYER_ARN})
LAYER_ARNS+=(${POSTSLACK_LAYER_ARN})

GSPREAD_LAYER_ARN=$(echo ${LIST_LAYER_ARNS} | python3 -m json.tool | grep gspread)
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
