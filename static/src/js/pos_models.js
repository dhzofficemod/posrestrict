/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    
    /**
     * Override the scan_product method to add category restriction validation
     */
    async scan_product(parsed_code) {
        const product = this.db.get_product_by_barcode(parsed_code.base_code);

        if (!product) {
            return false;
        }

        // Check category restrictions
        if (!this.isProductCategoryAllowed(product)) {
            // Get the product's category name
            let categoryName = "another POS";
            if (product.pos_categ_id) {
                const category = this.db.get_category_by_id(product.pos_categ_id[0]);
                if (category) {
                    categoryName = category.name;
                }
            }

            // Show error notification
            this.env.services.notification.add(
                `Produsul "${product.display_name}" este de la ${categoryName} și nu poate fi scanat în acest POS.`,
                {
                    type: "danger",
                    sticky: false,
                }
            );
            return false;
        }

        return await super.scan_product(parsed_code);
    },

    /**
     * Check if product category is allowed in current POS
     */
    isProductCategoryAllowed(product) {
        const config = this.config;
        
        // If no category restrictions, allow all products
        if (!config.limit_categories || !config.iface_available_categ_ids) {
            return true;
        }

        const allowedCategoryIds = config.iface_available_categ_ids.map(cat => cat.id);
        
        // Check if product has a POS category and if it's allowed
        if (product.pos_categ_id) {
            return allowedCategoryIds.includes(product.pos_categ_id[0]);
        }
        
        // Handle products without categories (adjust based on your requirements)
        return false;
    },

    /**
     * Override product search to ensure consistency with barcode scanning
     */
    _search_product_in_category(category_id, query) {
        const products = super._search_product_in_category(category_id, query);
        
        // Filter products based on category restrictions
        if (this.config.limit_categories && this.config.iface_available_categ_ids) {
            return products.filter(product => this.isProductCategoryAllowed(product));
        }
        
        return products;
    }
});