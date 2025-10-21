/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
    
    /**
     * Override barcode scanning on product screen
     */
    async _barcodeProductAction(code) {
        const product = this.pos.db.get_product_by_barcode(code.base_code);
        
        if (product && !this.pos.isProductCategoryAllowed(product)) {
            // Show error message for restricted products
            this.popup.add("ErrorPopup", {
                title: "Product Not Available",
                body: `The product "${product.display_name}" cannot be added to this POS due to category restrictions.`,
            });
            return;
        }
        
        return await super._barcodeProductAction(code);
    },

    /**
     * Enhanced product filtering for search
     */
    _getSearchFields() {
        const fields = super._getSearchFields();
        
        // Ensure category restrictions are applied during search
        const originalMethod = this._searchProduct.bind(this);
        this._searchProduct = (searchDetails) => {
            const results = originalMethod(searchDetails);
            
            // Filter results based on category restrictions
            if (this.pos.config.limit_categories && this.pos.config.iface_available_categ_ids) {
                return results.filter(product => this.pos.isProductCategoryAllowed(product));
            }
            
            return results;
        };
        
        return fields;
    }
});