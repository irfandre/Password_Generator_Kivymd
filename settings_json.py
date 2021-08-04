import json

setting_json = json.dumps([

            {
                'type': 'title',
                'title': 'example title'
            },
            {
                'type' : 'bool',
                'title': 'Save Settings',
                'desc': 'Save the selection of characters',
                'section': 'Example',
                'key': 'bool'

            },
            {
                'type' : 'bool',
                'title': 'Dark Mode',
                'desc': 'Enable/Disable Dark Mode',
                'section': 'Example',
                'key': 'darkmode'

            },
            # {
            #     'type': 'title',
            #     'title': 'title2'
            # },
            # {
            #     'type' : 'bool',
            #     'title': 'boolean setting2',
            #     'desc': 'bollena description2',
            #     'section': 'Example2',
            #     'key': 'bool'
            #
            # }

       ])