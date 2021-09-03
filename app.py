from tabulate import tabulate
import datetime as dt
import github as git
from mail import SendMail
import logging

# Configure logging
logging.root.setLevel(logging.NOTSET)
logging.getLogger("urllib3").setLevel(logging.WARNING)

def get_pull_req():
  TodaysDate       = dt.datetime.strptime(dt.datetime.utcnow().strftime('%Y-%m-%d'), "%Y-%m-%d").date()
  LastWeekDate     = TodaysDate - dt.timedelta(days=7)

  resultSet = []
  resp = git.get_pulls_by_status(reqObj)
  if resp and resp.status_code == 200: # 200 Resp is too stric to use. better way
    for item in resp.json():
      creationTimestamp = dt.datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%SZ")
      creationTimestamp = dt.datetime.strptime(creationTimestamp.strftime('%Y-%m-%d'), "%Y-%m-%d").date()
      if creationTimestamp >= LastWeekDate:
        resultSet.append([item['id'], item['title'], item['state'], creationTimestamp, item['url']])

  if len(resultSet) > 0:
    resultSetTable = tabulate(resultSet, headers=["ID", "TITLE", "STATE", "DATE", "URL"], tablefmt='html')
    
    emailStatus = SendMail('GitPullSummary', reqObj['team'], resultSetTable)
    if emailStatus['success'] == False:
      logging.error(emailStatus)
    if emailStatus['success'] == True:
      logging.info(emailStatus)


# Triggered Event
reqObj = {
  'proj'   : 'netbox-community',
  'repo'   : 'netbox',
  'state'  : 'all',
  'team'   : 'email@sailpoint.com' # The team receiving the email/report
}
get_pull_req()