{
    'name': 'POS Product Category Restriction Fix',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Fix POS barcode scanning to respect product category restrictions',
    'description': '''
        This module fixes an issue where barcode scanning in POS bypasses product category restrictions.
        
        Features:
        - Ensures barcode scanning respects POS product category limitations
        - Maintains existing manual search restrictions
        - Shows appropriate error messages for restricted products
        
        Issue Fixed:
        - Products with categories not assigned to a POS can no longer be scanned via barcode
        - Aligns barcode scanning behavior with manual product search behavior
    ''',
    'author': 'Custom Development',
    'website': '',
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_category_restriction/static/src/js/pos_models.js',
            'pos_category_restriction/static/src/js/product_screen.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}