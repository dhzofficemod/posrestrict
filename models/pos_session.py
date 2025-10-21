from odoo import models, api
from odoo.exceptions import UserError


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def find_product_by_barcode(self, barcode):
        """
        Override barcode search to respect category restrictions
        """
        # First, find the product using the standard method
        product = super().find_product_by_barcode(barcode)
        
        if not product:
            return False
            
        # Check if the current POS config has category restrictions
        pos_config = self.config_id
        
        if pos_config.limit_categories and pos_config.iface_available_categ_ids:
            # Check if the product's category is allowed
            if not pos_config._is_product_category_allowed(product):
                # Return False to indicate product not found (respecting restrictions)
                return False
                
        return product

    def _get_pos_ui_product_product(self, params):
        """
        Override product loading to ensure category restrictions are applied
        """
        products = super()._get_pos_ui_product_product(params)
        
        # Apply category filtering if restrictions are enabled
        if self.config_id.limit_categories and self.config_id.iface_available_categ_ids:
            allowed_category_ids = self.config_id.iface_available_categ_ids.ids
            filtered_products = []
            
            for product in products:
                if product.get('pos_categ_id') and product['pos_categ_id'][0] in allowed_category_ids:
                    filtered_products.append(product)
                elif not product.get('pos_categ_id') and self.config_id.allow_uncategorized_products:
                    # Include uncategorized products if allowed (you may want to add this field)
                    filtered_products.append(product)
                    
            return filtered_products
            
        return products