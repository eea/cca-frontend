#!/bin/sh
env \
  DEBUG=esmiddleware \
  #RAZZLE_PROXY_ES_DSN_datahub=http://10.120.10.86:60168/data_searchui_datahub \
  #RAZZLE_PROXY_QA_DSN_datahub=http://10.120.10.204:60022/api \
  RAZZLE_PROXY_ES_DSN_globalsearch=http://10.120.10.131:60168/data_searchui_new \
  RAZZLE_PROXY_QA_DSN_globalsearch=http://10.120.10.204:60022/api \
  yarn start

# RAZZLE_PROXY_ES_DSN_datahub=http://10.120.10.131:57664/data_searchui_datahub \
# RAZZLE_PROXY_QA_DSN_globalsearch=http://localhost:8000/api \
