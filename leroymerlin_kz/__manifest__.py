# -*- coding: utf-8 -*-
{
    'name': "Leroymerlin",

    'summary': """
        Whole Catalogue Of Leroymerlin.kz""",

    'description': """
        Tables with catalog information, all products information and all products details
    """,
    
    'category': 'Uncategorized',
    'version': '13.0.2.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/leroymerlinkz_groups.xml',
        'security/ir.model.access.csv',
        'views/leroymerlin.xml',
    ],
    
}
