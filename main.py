from keys import keys
import todoist
import re

todoist_api = todoist.TodoistAPI(keys["todoist"])
todoist_api.sync()

wishlists = []
regex = r'\[.*?\]\(.*?\)'
for project in todoist_api.state['projects']:
    if str(project['parent_id']) == "1799452428":
        wishlists.append(str(project["id"]))

for list in wishlists:
    for item in todoist_api.state['items']:
        if str(item['project_id']) == list:
            content = item['content']
            if re.search(regex, content) != None:
                print("Matched: " + content)
            else: 
                print(content)