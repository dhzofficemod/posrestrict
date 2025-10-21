from odoo import models, api


class PosSession(models.Model):
    _inherit = 'pos.session'

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
