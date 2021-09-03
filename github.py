import requests as request

# Global Vars
RMT_GIT_URL = 'https://api.github.com/repos'

def get_pulls_by_status(reqObj):
  proj      = reqObj['proj']
  repo      = reqObj['repo']
  queryPars = {'state': reqObj['state']}
  url       = f'{RMT_GIT_URL}/{proj}/{repo}/pulls'
  try:
    response  = request.get(
      url, 
      params   = queryPars,
      headers  = {
      'accept' : 'application/vnd.github.v3+json',
      })
  except Exception as e:
    response = e
  finally:
      return response


# Git does not have pull by date as query param so need to pull all pulls then check for  pulls were created in the past week
# def get_pulls_by_date(reqObj):
#   proj      = reqObj['proj']
#   repo      = reqObj['repo']
#   queryPars = {'state': reqObj['state']}
#   url       = f'{RMT_GIT_URL}/{proj}/{repo}/pulls'
#   response  = request.get(
#     url, 
#     params   = queryPars,
#     headers  = {
#     'accept' : 'application/vnd.github.v3+json',
#     })
#   return response