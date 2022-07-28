'''
Run some script.
'''

import time
import yaml
import daytona

variables = {
    'var1': 'oneVar',
    'var2': 2
    }

start = time.process_time()

# TODO: multiple documents
with open('script.yml', 'r', encoding='utf-8') as f:
    body_dict = yaml.safe_load(f)

daytona.register_keywords(body_dict)
daytona.register_variables(variables)
daytona.execute_script('main')
end = time.process_time()

print(f'=== TEST RUN TIME: {end - start} microseconds')
