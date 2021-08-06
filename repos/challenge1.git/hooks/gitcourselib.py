def _logprint(m, ref):
  print(m)
  # Repository description
  with open("./description") as d:
    DESC = d.read().strip()
  with open(f"/tmp/{DESC}.log",'a') as l:
    l.write(f"[{DESC}] - {ref} - {m}\n")


import re
def check_commit(commit):

  lines = commit.message.splitlines()
  title = lines[0]
  body = ""

  if len(title) >= 50:
    return False, f"[{commit.id}] - Title has more than 49 characters"

  if lines[0][-1] == '.':
    return False, f"[{commit.id}] - Title ends with a period"
 
  if len(lines) < 2:
    return False, f"[{commit.id}] - Commit does not have a Message Body"
 
  if len(lines) < 3:
    if len(lines[1]) > 0:
      return False, f"[{commit.id}] - Title and message are not split by a newline"

  for line in lines[2:]:
    body += line + "\n"
    if len(line) > 72:
      return False, f"[{commit.id}] - Message Body line has more than 72 characters"

  if len(body) < 15:
    return False, f"[{commit.id}] - Message Body seems too short"

  if not re.match("\[\w+\] .+", title):
    return False, f"[{commit.id}] - Commit does not follow convention of: '[Component] Title'"

  return True, f"[{commit.id}] Convention passes!"

