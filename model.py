def get_issue_id(data):
  return int(data['object_attributes']['title'])

def get_action(data):
  return data['object_attributes']['action']

def get_labels(data):
  res = []
  if 'labels' in data:
    for lbl in data['labels']:
      res.append(lbl['title'])
  return res

# все метки из настроек должны быть в MR
# labels - метки из MR
# sts['labels'] - метки из настроек
def check_labels(labels, sts):
  if 'labels' not in sts:
    return True
  return set(sts['labels']).issubset(set(labels))

def get_new_status(curr_sts, action, labels, sts_settings):
  new_sts = -1
  for sts in sts_settings:
    if sts['curr'] == curr_sts \
      and action in sts['actions'] \
      and check_labels(labels, sts):
          new_sts = sts['next']
          break
  return new_sts
              
def on_event(data, redmine, sts_settings):
  try:
      # номер таски 
      issue_id = get_issue_id(data)
      # текущий статус
      curr_sts = redmine.issue.get(issue_id).status.id
    
      # событие - open/reopen/close/merge
      action = get_action(data)
      # метки, если есть ("списано")
      labels = get_labels(data)
    
      # ищем новый статус
      new_sts = get_new_status(curr_sts, action, labels, sts_settings)
    
      if new_sts != -1:
          # если нашли, обновляем таску
          redmine.issue.update(issue_id, status_id = new_sts)
      
  except Exception as e:
    print(e)
