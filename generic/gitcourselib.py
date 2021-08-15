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


def get_title_tag(commit):
  lines = commit.message.splitlines()
  title = lines[0]
  match_obj = re.search(r'\[(\w+)\].*', title)
  try:
    tag = match_obj[1]
    return tag
  except IndexError:
    # Check if Merge commit with default message
    if "Merge" in title:
      return "Merge"
    raise ValueError("Commit does not follow the '[Component] Title...' convention")


def check_code(commit, code_snippets_to_add = {}, conflict_leftover_check=True):
  '''
  commit = pygit2 commit object
  code_snippets_to_add = {'changed_filename': ["snippet_to_exist_1", "snippet_to_exist_2"]}
  '''
  tree = commit.tree
  # Check against previous from the splitted commit
  diff = tree.diff_to_tree(commit.parents[0].tree)
  patches = [p for p in diff]

  # Check the files changed in the commit
  patch_files = {}
  for p in patches:
    if p.delta.new_file.path not in code_snippets_to_add:
      return False, f"[{commit.id}] [{get_title_tag(commit)}] commit changes irrelevant file: '{p.delta.new_file.path}'"

    patch_files[p.delta.new_file.path] = p

  # Number of files changed different of files supposed to change
  if len(patch_files.keys()) != len(code_snippets_to_add.keys()):
    different_files = set(code_snippets_to_add.keys()) - set(patch_files.keys())
    # Files that had to change but didn't
    if different_files:
      return False, f"[{commit.id}] [{get_title_tag(commit)}] commit did not change files '{different_files}'."

    # Files that changed while they were not supposed to (also caught in the `patches` for-loop
    different_files = set(patch_files.keys()) - set(code_snippets_to_add.keys())
    if different_files:
      return False, f"[{commit.id}] [{get_title_tag(commit)}] commit changes irrelevant files '{different_files}'."

  # Iterate through all file changes
  for patch_file, checked_patch in patch_files.items():
    # Examine all commited hunks for lines
    code = ""
    for hunk in checked_patch.hunks:
      for l in hunk.lines:
        # print(l.origin, l.content, hunk)
        if l.new_lineno == -1:

          # print(l.origin, l.content, hunk)
          code += l.content

    # `code` contains all added code in the commit

    # Check if all snippets are present in the code changes
    for snippet in code_snippets_to_add[patch_file]:
      if snippet not in code:
        return False, f"[{commit.id}] [{get_title_tag(commit)}] commit does not seem to contain all the appropriate code."

    if conflict_leftover_check:
      for snippet in ["<<<<<<<", "=======", ">>>>>>>"]:
        if snippet in code:
          return False, f"[{commit.id}] [{get_title_tag(commit)}] commit seems to contain Git Conflict leftovers."

  return True, f"[{commit.id}] [{get_title_tag(commit)}] commit passes!"
