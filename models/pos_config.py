from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    @api.model
    def _get_available_product_categories(self):
        """
        Get available product categories for this POS configuration
        """
        if self.limit_categories and self.iface_available_categ_ids:
            return self.iface_available_categ_ids.ids
        return []

    def _is_product_category_allowed(self, product):
        """
        Check if a product's category is allowed in this POS
        """
        if not self.limit_categories or not self.iface_available_categ_ids:
            return True
            
        allowed_category_ids = self.iface_available_categ_ids.ids
        
        # Check if product's POS category is in allowed categories
        if product.pos_categ_id:
            return product.pos_categ_id.id in allowed_category_ids
            
        # If no POS category is set, check if uncategorized products are allowed
        # You might want to adjust this logic based on your requirements
        return False