import json

setting_json = json.dumps([

            {
                'type': 'title',
                'title': 'example title'
            },
            {
                'type' : 'bool',
                'title': 'Goto Intro',
                'desc': 'Go back to intro screen',
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
            {
                'type': 'bool',
                'title': 'Save Options',
                'desc': 'Save Selected Character options',
                'section': 'Example',
                'key': 'saveoptions'

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